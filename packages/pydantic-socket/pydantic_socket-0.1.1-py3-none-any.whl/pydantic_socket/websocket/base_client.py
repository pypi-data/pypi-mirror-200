import abc
import asyncio
import logging
from typing import (
    AsyncGenerator,
)

import aiohttp
import pydantic
from aiohttp import (
    ClientWebSocketResponse,
    WSCloseCode,
)
from aiohttp import (
    WSMessage,
    WSMsgType,
)
from aiohttp.web import WebSocketResponse

from ..types import (
    Action,
    ActionResponse,
    ClientId,
    Packet,
)


class BaseClient(abc.ABC):
    MAX_REQUEST_TIMEOUT = 10
    connection: WebSocketResponse | ClientWebSocketResponse = None
    _responses: dict[str, ActionResponse] = {}
    _responses_events: dict[str, asyncio.Event] = {}

    def __init__(self, *, client_id: ClientId):
        self.logger = logging.getLogger(f"{self.__class__.__name__} {client_id}")
        self.client_id = client_id

    async def send(
            self,
            packet: Packet,
            *,
            wait_response: bool = False,
            request_timeout: int = MAX_REQUEST_TIMEOUT
    ) -> ActionResponse | None:
        if isinstance(packet, ActionResponse):
            await self.connection.send_str(packet.json())
            return None

        packet.need_response = packet.need_response or wait_response
        packet_id = str(packet.id)

        if packet.need_response:
            self._responses_events[packet_id] = asyncio.Event()

        try:
            await self.connection.send_str(packet.json())
        except BaseException:
            self._responses_events.pop(packet_id, None)
            raise

        if packet.need_response:
            try:
                await asyncio.wait_for(
                    self._responses_events[packet_id].wait(),
                    request_timeout
                )
                return self._responses.pop(packet_id, None)
            except asyncio.TimeoutError:
                self.logger.warning(f'{packet.type} request cancelled due to timeout error')
                self._responses_events.pop(packet_id, None)

    async def request(
            self,
            action: Action,
            *,
            request_timeout: int = MAX_REQUEST_TIMEOUT
    ) -> ActionResponse:
        return await self.send(action, wait_response=True, request_timeout=request_timeout)

    async def close(self, *, code: int = WSCloseCode.OK, message: bytes = b'') -> bool:
        if bool(self.connection) and not self.connection.closed:
            return await self.connection.close(code=code, message=message)

        return True

    async def listen(self) -> AsyncGenerator[Action, None]:
        async for msg in self.connection:  # type: WSMessage
            if msg.type in (WSMsgType.TEXT, WSMsgType.BINARY):
                try:
                    try:
                        packet = pydantic.parse_raw_as(Packet, msg.data)
                    except BaseException as e:
                        self.logger.error(f'Unable to parse Action in message: {e}. Raw message: {msg.data}')
                        continue

                    if isinstance(packet, Action):
                        yield packet
                    elif isinstance(packet, ActionResponse):
                        asyncio.create_task(self._handle_action_response(packet))
                    else:
                        self.logger.warning(f"Unsupported packet: {packet.__class__.__name__}: {packet}")
                except BaseException as e:
                    self.logger.error(f'Unable to parse action in message: {e}. Raw data: {msg.data}')
            elif msg.type == WSMsgType.ERROR:
                self.logger.error(f'Error message received. {msg.data}.')
                break
            elif msg.type == WSMsgType.CLOSE:
                self.logger.error(f'Close message received. {msg.data}.')
                try:
                    await self.close()
                except aiohttp.WebSocketError:
                    pass
            else:
                self.logger.warning(f"Unhandled message type: {msg.type}")

    async def _handle_action_response(self, action_response: ActionResponse):
        action_id = str(action_response.action_id)
        event = self._responses_events.pop(action_id, None)

        if bool(event):
            self._responses[action_id] = action_response
            event.set()
