from abc import abstractmethod
from datetime import timedelta, datetime
from typing import Any

from jwt import PyJWT, InvalidSignatureError, DecodeError, ExpiredSignatureError

from fastapi_all_out.pydantic import CamelModel
from fastapi_all_out.responses import DefaultJSONEncoder
from fastapi_all_out.lazy import get_schema, get_codes
from fastapi_all_out.enums import JWTTokenTypes
from fastapi_all_out.schemas import UserMeRead
from ..base import AuthStrategy
from .schemas import JWTToken, JWTTokenIssue


LIFETIME = dict[JWTTokenTypes, int]
DEFAULT_LIFETIME: LIFETIME = {
    JWTTokenTypes.access: int(timedelta(minutes=5).total_seconds()),
    JWTTokenTypes.refresh: int(timedelta(days=10).total_seconds()),
}

JWTToken = get_schema(JWTToken)
JWTTokenIssue = get_schema(JWTTokenIssue)
UserMeRead = get_schema(UserMeRead)
Codes = get_codes()


class TokenPair(CamelModel):
    access_token: str
    refresh_token: str
    user: UserMeRead


class JWTAuthStrategy(AuthStrategy):
    jwt = PyJWT()
    json_encoder = DefaultJSONEncoder

    authorize_response_model = TokenPair

    DECODE_SECRET: str
    ENCODE_SECRET: str
    SCHEMA: str

    def __init__(self, *, lifetime: LIFETIME = None, schema: str = "bearer"):
        self.lifetime = {**DEFAULT_LIFETIME, **(lifetime or {})}
        self.SCHEMA = schema.lower()

    @property
    @abstractmethod
    def ALGORITHM(self) -> str: ...

    def decode(self, token: str) -> dict[str, Any]:
        return self.jwt.decode(token, self.DECODE_SECRET, [self.ALGORITHM])

    def encode(self, payload: dict[str, Any]) -> str:
        return self.jwt.encode(payload, self.ENCODE_SECRET, self.ALGORITHM, json_encoder=self.json_encoder)

    @staticmethod
    def now() -> int:
        return int(datetime.now().timestamp())

    def create_token(self, user, token_type: JWTTokenTypes, iat: int = None) -> str:
        return self.encode(
            JWTTokenIssue(
                user=user,
                type=token_type,
                iat=iat or self.now(),
                seconds=self.lifetime[token_type]
            ).dict()
        )

    def create_access_token(self, user, iat: int = None) -> str:
        return self.create_token(user, JWTTokenTypes.access, iat=iat)

    def create_refresh_token(self, user, iat: int = None) -> str:
        return self.create_token(user, JWTTokenTypes.refresh, iat=iat)

    def authorize(self, user) -> TokenPair:
        now = self.now()
        return TokenPair(
            access_token=self.create_access_token(user, iat=now),
            refresh_token=self.create_refresh_token(user, iat=now),
            user=user,
        )

    def get_token_payload(self, token: str):
        try:
            payload = self.decode(token)
        except (InvalidSignatureError, DecodeError):
            raise Codes.invalid_token.err()
        except ExpiredSignatureError:
            raise Codes.expired_token.err()
        return JWTToken(**payload)

    def parse_token(self, token: str, token_type: JWTTokenTypes) -> JWTToken:
        payload = self.get_token_payload(token)
        if payload.type != token_type:
            raise Codes.not_authenticated.err()
        return payload

    def get_access_token(self, token: str) -> JWTToken:
        if token is None:
            raise Codes.not_authenticated.err()
        schema, _, token = token.partition(" ")
        if schema.lower() != self.SCHEMA:
            raise Codes.not_authenticated.err()
        return self.parse_token(token, token_type=JWTTokenTypes.access)

    get_auth = get_access_token

    def get_refresh_token(self, token: str) -> JWTToken:
        return self.parse_token(token, token_type=JWTTokenTypes.refresh)


class RS256JWTAuthStrategy(JWTAuthStrategy):
    ALGORITHM = 'RS256'

    def __init__(self, *args, public_key: str = None, private_key: str = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.ENCODE_SECRET = private_key.replace('|||n|||', '\n').strip("'").strip('"') if private_key else None
        self.DECODE_SECRET = public_key.strip("'").strip('"') if public_key else None
