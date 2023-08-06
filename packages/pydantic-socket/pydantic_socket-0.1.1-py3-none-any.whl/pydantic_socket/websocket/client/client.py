import asyncio
from enum import Enum
from typing import (
    Any,
    Callable,
    Coroutine,
)

import pydantic
import ujson
from aiohttp import (
    ClientConnectorError,
    ClientSession,
    WSCloseCode,
)

from ..base_client import BaseClient
from ..constants import CLIENT_ID_HEADER_NAME
from ...types import (
    Action,
    ActionResponse,
    ActionResponsePayload,
    ActionType,
    BearerSecret,
    ClientId,
)

ClientActionHandler = Callable[
    ['Client', Action],
    Coroutine[Any, Any, ActionResponsePayload | None]
]


class Client(BaseClient):
    DEFAULT_RECONNECT_TIMEOUT = 5
    closed: bool = False
    session: ClientSession | None = None
    handlers: dict[ActionType, ClientActionHandler] = {}

    def __init__(
            self,
            url: str,
            *,
            auto_reconnect: bool = True,
            reconnect_timeout: int = DEFAULT_RECONNECT_TIMEOUT,
            bearer_secret: BearerSecret | None = None,
            client_id: ClientId | None = None
    ):
        super().__init__(client_id=client_id)
        self.url = url
        self.auto_reconnect = auto_reconnect
        self.reconnect_timeout = reconnect_timeout
        self.bearer_secret = (
            bearer_secret.get_secret_value()
            if isinstance(bearer_secret, pydantic.SecretStr)
            else bearer_secret
        )

    async def run(self, *, headers: dict = None, **kwargs):
        self.closed = False

        if not bool(headers):
            headers = {}

        if bool(self.bearer_secret) and 'Authorization' not in headers:
            headers['Authorization'] = f"Bearer {self.bearer_secret}"

        if bool(self.client_id) and CLIENT_ID_HEADER_NAME not in headers:
            headers[CLIENT_ID_HEADER_NAME] = str(self.client_id)

        while True:
            if self.closed:
                break

            try:
                self.logger.info(f'Trying to connect to server {self.url}...')
                self.session = ClientSession(json_serialize=ujson.dumps)

                async with self.session.ws_connect(self.url, headers=headers, **kwargs) as ws_connection:
                    self.connection = ws_connection
                    self.logger.info(f'Connection to server {self.url} established')

                    async for action in self.listen():
                        asyncio.create_task(self._handle_action(action))
            except (ClientConnectorError, RuntimeError, OSError) as e:
                self.logger.error(f'Unable to connect to server {self.url}: {e.__class__.__name__}: {e}')

                if self.auto_reconnect:
                    self.logger.info(f'Reconnecting after {self.reconnect_timeout} seconds')
                    await asyncio.sleep(self.reconnect_timeout)
                    continue

                return
            finally:
                if bool(self.session) and not self.session.closed:
                    await self.session.close()

    async def close(self, *, code: int = WSCloseCode.OK, message: bytes = b'') -> bool:
        self.closed = True

        await super().close(code=code, message=message)

        if bool(self.session):
            await self.session.close()
            self.session = None

        self.logger.error(f'Connection to server closed')
        return True

    def set_action_handler(self, action_type: ActionType, handler: ClientActionHandler):
        action_type = str(action_type.value) if isinstance(action_type, Enum) else str(action_type)
        self.handlers[action_type] = handler

    def action_handler(self, action_type: ActionType):
        def decorator(func: ClientActionHandler) -> ClientActionHandler:
            self.set_action_handler(action_type, func)
            return func

        return decorator

    async def _handle_action(self, action: Action):
        handler = self.handlers.get(action.type, None)

        if not bool(handler):
            self.logger.warning(f'No registered handlers for action of type {action.type}')
            return

        # noinspection PyBroadException
        try:
            response = await handler(self, action)
        except (asyncio.CancelledError, KeyboardInterrupt, SystemExit):
            raise
        except BaseException:
            self.logger.error(
                f"Unhandled exception for action {action.type}",
                exc_info=True
            )
        else:
            if action.need_response and bool(action.id):
                try:
                    await self.send(ActionResponse(action_id=action.id, payload=response))
                except (asyncio.CancelledError, KeyboardInterrupt, SystemExit):
                    raise
                except BaseException as e:
                    self.logger.error(
                        f'Unable to send response for action {action.id} of type {action.type}: {e}',
                        exc_info=True
                    )
