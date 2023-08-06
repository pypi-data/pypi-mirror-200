from aiohttp.web import WebSocketResponse

from ..base_client import BaseClient
from ...types import ClientId


class ServerClient(BaseClient):
    def __init__(self, client_id: ClientId, connection: WebSocketResponse):
        super().__init__(client_id=client_id)
        self.connection = connection
