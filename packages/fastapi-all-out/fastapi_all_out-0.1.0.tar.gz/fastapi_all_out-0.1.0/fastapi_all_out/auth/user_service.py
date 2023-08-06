from datetime import datetime
from typing import Protocol, Optional, TypeVar, Any, Generic, Literal
from abc import ABC, abstractmethod
from uuid import UUID

from passlib.context import CryptContext
from fastapi import Request, BackgroundTasks

from fastapi_all_out.enums import TempCodeTriggers
from fastapi_all_out.schemas import PasswordsPair


class UserInterface(Protocol):
    id: int
    uuid: UUID
    username: Optional[str]
    email: Optional[str]
    password_hash: str
    password_change_dt: datetime
    password_salt: str
    is_superuser: bool
    is_active: bool
    created_at: datetime
    EMAIL_FIELD: str
    AUTH_FIELDS: tuple[str, ...]


USER_MODEL = TypeVar("USER_MODEL", bound=UserInterface)


class BaseUserService(Generic[USER_MODEL], ABC):

    user: USER_MODEL
    pwd_context = CryptContext(schemes=["md5_crypt"])

    def __init__(self, user: USER_MODEL):
        self.user = user

    @classmethod
    @abstractmethod
    async def create_user(
            cls,
            data: PasswordsPair,
            should_exclude: set[str] = None,
            defaults: dict[str, Any] = None
    ) -> USER_MODEL: ...

    @abstractmethod
    async def post_registration(self, request: Request, background_tasks: BackgroundTasks) -> None: ...

    @property
    @abstractmethod
    def pk(self) -> int | UUID: ...

    @property
    @abstractmethod
    def is_user_active(self) -> bool: ...

    def can_login(self) -> bool:
        return self.is_user_active

    @property
    @abstractmethod
    def is_superuser(self) -> bool: ...

    @property
    @abstractmethod
    def uuid(self) -> UUID: ...

    @abstractmethod
    def token_expired(self, iat: int) -> bool: ...

    @abstractmethod
    def set_password(self, password: str) -> None: ...

    @abstractmethod
    def get_fake_password(self, password: str) -> str: ...

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(self.get_fake_password(password))

    @abstractmethod
    def verify_password(self, password: str) -> bool: ...

    @abstractmethod
    def get_permissions(self) -> tuple[tuple[int, str], ...]: ...

    @abstractmethod
    def has_permissions(self, *permissions: tuple[str, str]) -> bool: ...

    @abstractmethod
    async def get_or_create_temp_code(self, trigger: TempCodeTriggers) -> Any: ...

    @abstractmethod
    async def update_or_create_temp_code(self, trigger: TempCodeTriggers) -> None: ...

    @abstractmethod
    async def send_activation_email(self) -> None: ...

    @abstractmethod
    async def send_password_reset_email(self) -> None: ...

    def add_send_activation_email_task(self, background_tasks: BackgroundTasks) -> None:
        background_tasks.add_task(self.send_activation_email)

    @abstractmethod
    def check_temp_code_error(self, code: str, trigger: TempCodeTriggers) -> Literal['expired', 'incorrect'] | None: ...

    @abstractmethod
    async def activate(self) -> None: ...
