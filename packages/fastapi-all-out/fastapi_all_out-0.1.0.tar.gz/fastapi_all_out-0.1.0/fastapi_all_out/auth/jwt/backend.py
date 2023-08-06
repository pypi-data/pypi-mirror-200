from typing import Callable, Coroutine, Any

from fastapi import APIRouter, Request, BackgroundTasks, Body, Header, Depends

from fastapi_all_out.lazy import get_schema, get_user_model, get_user_repository, get_user_service, get_codes
from fastapi_all_out.routers.exceptions import ItemNotFound
from fastapi_all_out.schemas import LoginPasswordSchema, UserMeRead
from ..base import AuthBackend
from .schemas import JWTTokenUser
from .strategy import JWTAuthStrategy


LoginPasswordSchema = get_schema(LoginPasswordSchema)
UserMeRead = get_schema(UserMeRead)
JWTTokenUser = get_schema(JWTTokenUser)
UserModel = get_user_model()
UserRepository = get_user_repository()
UserService = get_user_service()
Codes = get_codes()


class JWTAuthBackend(AuthBackend):

    strategy: "JWTAuthStrategy"

    def __init__(self, strategy: "JWTAuthStrategy"):
        assert isinstance(strategy, JWTAuthStrategy)
        self.strategy = strategy

    def check_auth(self) -> Callable[[], Coroutine[Any, Any, bool]]:
        async def wrapper(token: str = Header(default=None, alias='Token')) -> bool:
            return self.strategy.get_auth(token) is not None

        return wrapper

    def get_auth(self) -> Callable[[], Coroutine[Any, Any, UserService]]:
        async def wrapper(
                request: Request,
                background_tasks: BackgroundTasks,
                token: str = Header(default=None, alias='Token')
        ) -> UserService:
            token = self.strategy.get_auth(token)
            try:
                user = await UserRepository(request=request, background_tasks=background_tasks)\
                    .get_one(token.user.id)
            except ItemNotFound:
                raise Codes.not_authenticated.err()
            user_service = UserService(user)
            if user_service.token_expired(token.iat):
                raise Codes.not_authenticated.err()
            return user_service

        return wrapper

    def get_auth_with_permissions(
            self, *permissions: tuple[str, str]
    ) -> Callable[[], Coroutine[Any, Any, UserService]]:
        async def wrapper(user_service: UserService = Depends(self.get_auth())) -> UserService:
            if not (user_service.is_superuser or user_service.has_permissions(*permissions)):
                raise Codes.permission_denied.err()
            return user_service

        return wrapper

    def create_router(self, **kwargs) -> APIRouter:
        kwargs.setdefault('prefix', '/auth/jwt')
        kwargs.setdefault('tags', ['auth'])
        router = APIRouter(**kwargs)

        self.add_login_route(router)
        self.add_logout_route(router)
        self.add_refresh_route(router)

        return router

    def add_login_route(self, router: APIRouter) -> None:
        @router.post('/login', response_model=self.strategy.authorize_response_model, responses=Codes.responses(
            Codes.not_authenticated
        ))
        async def wrapper(
                request: Request,
                background_tasks: BackgroundTasks,
                login_password: LoginPasswordSchema = Body(...)
        ):
            field, value = login_password.get_auth_field_and_value()
            try:
                user = await UserRepository(request=request, background_tasks=background_tasks)\
                    .get_one(value, field_name=field)
            except ItemNotFound:
                raise Codes.not_authenticated.err()

            user_service = UserService(user)
            if not user_service.verify_password(password=login_password.password):
                raise Codes.not_authenticated.err()

            if not user_service.can_login():
                raise Codes.not_authenticated.err()
            return self.strategy.authorize(user)

    def add_logout_route(self, router: APIRouter) -> None:
        pass

    def add_refresh_route(self, router: APIRouter) -> None:
        @router.post('/refresh', response_model=self.strategy.authorize_response_model, responses=Codes.responses(
            Codes.not_authenticated
        ))
        async def wrapper(
                request: Request,
                background_tasks: BackgroundTasks,
                token: str = Body(..., alias='refreshToken')
        ):
            token = self.strategy.get_refresh_token(token)
            try:
                user = await UserRepository(request=request, background_tasks=background_tasks).get_one(token.user.id)
            except ItemNotFound:
                raise Codes.not_authenticated.err()
            if UserService(user).token_expired(token.iat):
                raise Codes.not_authenticated.err()
            return self.strategy.authorize(user)
