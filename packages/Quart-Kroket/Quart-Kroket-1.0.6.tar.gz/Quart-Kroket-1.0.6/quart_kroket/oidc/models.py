import os
import json
import re
import inspect
from uuid import uuid4, UUID
from datetime import timedelta
from dataclasses import dataclass, field
from typing import Optional, Union, Tuple, List

from dataclasses_json import dataclass_json


@dataclass
class UserSession:
    user_name: str
    user_username: str
    user_uuid: Union[str, UUID]
    roles: Optional[List[str]]

    refresh_token: dict
    access_token: dict
    id_token: str
    user_info: dict


@dataclass_json
@dataclass
class KeycloakUser:
    id: uuid4
    username: str
    email: str
    enabled: bool
    attributes: Optional[dict[str, List]] = field(default_factory=lambda: {})
    groups: Optional[List['KeycloakGroup']] = field(default_factory=lambda: [])
    roles: Optional[List['KeycloakRole']] = field(default_factory=lambda: [])

    def has_role(self, name: str) -> bool:
        from quart import current_app
        current_app.logger.info(f"has_role? {name}")
        if not self.roles:
            return False

        for r in self.roles:
            if r.name == name:
                return True
        return False

    @classmethod
    def from_dict(cls, env):
        return cls(**{
            k: v for k, v in env.items()
            if k in inspect.signature(cls).parameters
        })


@dataclass_json
@dataclass
class KeycloakRole:
    id: uuid4
    name: str
    description: str
    composite: bool
    clientRole: bool
    containerId: uuid4

    @classmethod
    def from_dict(cls, env):
        return cls(**{
            k: v for k, v in env.items()
            if k in inspect.signature(cls).parameters
        })


@dataclass_json
@dataclass
class KeycloakGroup:
    id: uuid4
    name: str
    path: str

    @classmethod
    def from_dict(cls, env):
        return cls(**{
            k: v for k, v in env.items()
            if k in inspect.signature(cls).parameters
        })
