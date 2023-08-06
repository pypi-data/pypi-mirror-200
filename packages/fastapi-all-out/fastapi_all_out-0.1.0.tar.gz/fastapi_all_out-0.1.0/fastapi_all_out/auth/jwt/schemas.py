from typing import Any

from pydantic import root_validator

from fastapi_all_out.lazy import get_schema
from fastapi_all_out.enums import JWTTokenTypes
from fastapi_all_out.pydantic import CamelModel, CamelModelORM


class JWTTokenUser(CamelModelORM):
    id: int
    is_superuser: bool


class JWTToken(CamelModel):
    type: JWTTokenTypes
    user: get_schema(JWTTokenUser)
    iat: int  # timestamp


class JWTTokenIssue(JWTToken):
    exp: int  # timestamp

    @root_validator(pre=True)
    def calc_ext(cls, values: dict[str, Any]) -> dict[str, Any]:
        if 'exp' not in values:
            values["exp"] = values["iat"] + values['seconds']
        return values
