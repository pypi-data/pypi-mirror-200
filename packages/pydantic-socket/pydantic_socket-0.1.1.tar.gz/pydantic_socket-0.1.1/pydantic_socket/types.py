from __future__ import annotations

import uuid
from enum import Enum
from typing import (
    Annotated,
    Literal,
)

import pydantic
import ujson
from pydantic.generics import GenericModel

ActionId = str | uuid.UUID
ActionType = str | Enum
# TODO: Support Generic pydantic model as ActionPayload
ActionPayload = dict | pydantic.BaseModel
ActionResponsePayload = dict | pydantic.BaseModel
ClientId = int | str | uuid.UUID
BearerSecret = str | pydantic.SecretStr


class BaseModel(pydantic.BaseModel):
    class Config:
        use_enum_values = True
        allow_population_by_field_name = True
        json_dumps = ujson.dumps
        json_loads = ujson.loads


class BaseGenericModel(GenericModel):
    class Config:
        use_enum_values = True
        allow_population_by_field_name = True
        json_dumps = ujson.dumps
        json_loads = ujson.loads


class Action(BaseModel):
    packet_type: Literal['action'] = 'action'
    id: ActionId | None = pydantic.Field(default_factory=uuid.uuid4)
    type: str | None = None
    payload: ActionPayload | None = None
    need_response: bool = False


class ActionResponse(BaseModel):
    packet_type: Literal['action_response'] = 'action_response'
    action_id: ActionId
    payload: ActionResponsePayload


Packet = Annotated[
    Action | ActionResponse,
    pydantic.Field(discriminator='packet_type')
]
