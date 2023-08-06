from __future__ import annotations

import asyncio
import logging
import uuid
from typing import (
    Any,
    Callable,
    Coroutine,
    Generic,
    Iterable,
    Type,
    TypeVar,
)

from aiohttp import WSCloseCode
# noinspection PyProtectedMember
from aiohttp import web
from aiohttp import web_request
# noinspection PyProtectedMember
from aiohttp.web_app import _Middleware
from pydantic import SecretStr

from .server_client import (
    ServerClient,
)
from ..constants import CLIENT_ID_HEADER_NAME
from ...types import (
    Action,
    ActionResponse,
    ActionResponsePayload,
    BearerSecret,
    ClientId,
)

ServerClientType = TypeVar('ServerClientType', bound=ServerClient)
ServerActionHandler = Callable[
    ['Server', ServerClientType, Action],
    Coroutine[Any, Any, ActionResponsePayload | None]
]


class Server(Generic[ServerClientType]):
    clients: dict[str, ServerClientType] = {}
    handlers: dict[str, ServerActionHandler] = {}

    def __init__(
            self,
            *,
            host: str = "127.0.0.1",
            port: int = 8080,
            middlewares: Iterable[_Middleware] = None,
            client_class: Type[ServerClientType] = ServerClient,
            bearer_secret: BearerSecret | None = None
    ):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.host = host
        self.port = port
        self.client_class = client_class
        self.bearer_secret = (
            bearer_secret.get_secret_value()
            if isinstance(bearer_secret, SecretStr)
            else bearer_secret
        )

        if not bool(middlewares):
            middlewares = []

        if self.bearer_secret:
            middlewares.append(self.bearer_secret_auth_middleware)

        middlewares.append(self.client_id_middleware)

        self.app = web.Application(logger=self.logger, middlewares=middlewares)
        self.app.on_startup.append(self._on_startup)
        self.app.on_shutdown.append(self._on_shutdown)
        self.app.on_cleanup.append(self._on_cleanup)
        self.app.router.add_get('/', self.connections_handler)

    @web.middleware
    async def bearer_secret_auth_middleware(self, request, handler):
        auth_header = request.headers.get('Authorization')

        if not bool(auth_header):
            return web.Response(status=401)

        if auth_header != f"Bearer {self.bearer_secret}":
            return web.Response(status=401)

        return await handler(request)

    @web.middleware
    async def client_id_middleware(self, request, handler):
        try:
            request['client_id'] = str(request.headers.get(CLIENT_ID_HEADER_NAME))
        except (ValueError, KeyError):
            pass

        if not bool(request['client_id']):
            request['client_id'] = str(uuid.uuid4())

        return await handler(request)

    async def run(self):
        # noinspection PyProtectedMember
        await web._run_app(self.app, host=self.host, port=self.port)

    async def _on_startup(self, app: web.Application):
        pass

    async def _on_shutdown(self, app: web.Application):
        pass

    async def _on_cleanup(self, app: web.Application):
        pass

    async def _handle_action(self, client: ServerClientType, action: Action):
        handler = self.handlers.get(action.type, None)

        if not bool(handler):
            self.logger.warning(f'No registered handlers for action of type {action.type}')
            return

        # noinspection PyBroadException
        try:
            response = await handler(self, client, action)
        except (asyncio.CancelledError, KeyboardInterrupt, SystemExit):
            raise
        except BaseException:
            self.logger.error(
                f"Unhandled exception for action {action.type} from client {client.client_id}",
                exc_info=True
            )
        else:
            if action.need_response and bool(action.id):
                # noinspection PyBroadException
                try:
                    await client.send(ActionResponse(action_id=action.id, payload=response))
                except (asyncio.CancelledError, KeyboardInterrupt, SystemExit):
                    raise
                except BaseException as e:
                    self.logger.error(
                        f"Unable to send response to client "
                        f"because of unhandled exception for action {action.id} of type {action.type} "
                        f"from client {client.client_id}: {e}",
                        exc_info=True
                    )

    def set_action_handler(self, action_type: str, handler: ServerActionHandler):
        self.handlers[action_type] = handler

    def action_handler(self, action_type: str):
        def decorator(func: ServerActionHandler) -> ServerActionHandler:
            self.set_action_handler(action_type, func)
            return func

        return decorator

    async def connections_handler(self, request: web_request.BaseRequest):
        client_id = request['client_id']
        worker_connection = web.WebSocketResponse()
        await worker_connection.prepare(request)

        client = self.client_class(client_id, worker_connection)
        self.clients[client_id] = client
        self.logger.info(
            f'Client {client_id} connected. '
            f'Total connections: {len(self.clients.keys())}'
        )

        try:
            async for packet in client.listen():
                asyncio.create_task(self._handle_action(client, packet))
        except BaseException as e:
            self.logger.error(e)
        finally:
            await self.disconnect_client(client_id)

        return worker_connection

    async def send(self, client_id: ClientId, action: Action, *, wait_response: bool = False) -> ActionResponse | None:
        client = self.get_client(client_id)

        if not bool(client):
            raise ValueError(f'No client to send message. Client {client_id} is not connected!')

        try:
            return await client.send(action, wait_response=wait_response)
        except BaseException as e:
            self.logger.error(f'Unable to send message to client {client.client_id}. {e.__class__.__name__}. {e}')
            await self.disconnect_client(client_id)

    async def request(self, client_id: ClientId, action: Action) -> ActionResponse:
        return await self.send(client_id, action, wait_response=True)

    async def broadcast(self, action: Action):
        tasks = [client.send(action) for client in self.clients.values()]
        await asyncio.gather(*tasks, return_exceptions=True)

    async def disconnect_client(self, client_id: ClientId):
        client_id = str(client_id)
        client = self.clients.pop(client_id, None)

        if not bool(client):
            return

        try:
            await client.close()
        except BaseException as e:
            self.logger.warning(f'Unable to close connection with client. {e}')
        else:
            self.logger.info(
                f'Client {client_id} disconnected. '
                f'Total connections: {len(self.clients.keys())}'
            )

    async def disconnect_all_clients(self):
        clients = self.clients.copy()

        for client in clients.values():
            try:
                await client.close(code=WSCloseCode.GOING_AWAY, message=b'Server shutdown')
            except BaseException as e:
                self.logger.debug(f'Unable to close client {client.client_id}. {e.__class__.__name__}. {e}')

    def get_client(self, client_id: ClientId) -> ServerClientType:
        return self.clients.get(str(client_id))
