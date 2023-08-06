from abc import ABC, abstractmethod
from typing import Callable, Coroutine, Any, TYPE_CHECKING

from fastapi import APIRouter

if TYPE_CHECKING:
    from fastapi_all_out.auth.user_service import BaseUserService


class AuthStrategy(ABC):
    authorize_response_model: Any

    def authorize(self, user) -> Any: ...


class AuthBackend(ABC):

    strategy: "AuthStrategy"

    @abstractmethod
    def check_auth(self) -> Callable[[], Coroutine[Any, Any, bool]]: ...

    @abstractmethod
    def get_auth(self) -> Callable[[], Coroutine[Any, Any, "BaseUserService"]]: ...

    @abstractmethod
    def get_auth_with_permissions(
            self, *permissions: tuple[str, str]
    ) -> Callable[[], Coroutine[Any, Any, "BaseUserService"]]: ...

    def create_router(self, **kwargs) -> APIRouter: ...
