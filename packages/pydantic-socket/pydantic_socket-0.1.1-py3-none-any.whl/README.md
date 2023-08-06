# pydantic_socket - Simple socket client and server with [Pydantic](https://github.com/samuelcolvin/pydantic) models

[![PyPI version shields.io](https://img.shields.io/pypi/v/pydantic_socket.svg)](https://pypi.python.org/pypi/pydantic_socket/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/pydantic_socket.svg)](https://pypi.python.org/pypi/pydantic_socket/)
[![PyPI license](https://img.shields.io/pypi/l/pydantic_socket.svg)](https://pypi.python.org/pypi/pydantic_socket/)

## Examples

> Output examples are provided for simultaneous run of Server and Client examples

### Server

```python
import asyncio
import logging

import pydantic_socket
from pydantic_socket.types import Action
from pydantic_socket.websocket import (
    Server,
    ServerClient,
)

server = Server()


class TestResponse(pydantic_socket.types.BaseModel):
    foo: int = 1
    bar: str = "bar"
    input: str | None = None


# Register handler for certain action type    
@server.action_handler("hello")
async def hello_handler(s: Server, client: ServerClient, action: Action):
    logging.info(f"Hello, {action.payload.get('name', 'World')}!")
    # Will print:
    # INFO:root:Hello, pydantic_socket!


async def test_handler(s: Server, client: ServerClient, action: Action):
    return TestResponse(foo=1, bar="bar", input=action.payload.get('input'))


# Another way to register handler for certain action type
server.set_action_handler("test", test_handler)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(server.run())

```

### Client

```python
import asyncio
import logging

import pydantic

from pydantic_socket.types import Action
from pydantic_socket.websocket import Client

client = Client("http://127.0.0.1:8080", auto_reconnect=False, client_id=1)


class SomeActionInputPayload(pydantic.BaseModel):
    input: str


async def main():
    # Establishing connection to server
    asyncio.create_task(client.run())
    # Wait some time until connection is done
    await asyncio.sleep(2)
    # Send action
    await client.send(Action(type='hello', payload={"name": "pydantic_socket"}))
    # Send and wait for response
    response = await client.request(Action(type='test', payload={"input": "Some Input"}))

    logging.info(f"Payload is: {response.payload}")
    # Will print: 
    # INFO:root:Payload is: {'foo': 1, 'bar': 'bar', 'input': 'Some Input'}

    await client.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

```

## LICENSE

This project is licensed under the terms of the MIT license.
