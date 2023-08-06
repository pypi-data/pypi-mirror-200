from typing import Type, Any, TypeVar, Generic, Optional, Protocol, Callable, Coroutine
from uuid import UUID

from fastapi import Request, BackgroundTasks

from fastapi_all_out.pydantic import CamelModel
from fastapi_all_out.lazy import get_auth_backend
from .base_repository_meta import BaseRepositoryMeta
from .filters import BaseFilter


SERVICE = TypeVar('SERVICE', bound="BaseCRUDService")
PK = TypeVar('PK', int, UUID)
DB_MODEL = TypeVar('DB_MODEL')


class CreateHandler(Protocol[DB_MODEL]):
    async def __call__(
            self,
            data: CamelModel,
            exclude: set[str],
            defaults: dict[str, Any] = None
    ) -> DB_MODEL: ...


class EditHandler(Protocol[DB_MODEL]):
    async def __call__(
            self,
            instance: DB_MODEL,
            data: CamelModel,
            exclude: set[str],
            defaults: dict[str, Any] = None
    ) -> DB_MODEL: ...


class FKGetInstance(Protocol[PK, DB_MODEL]):
    async def __call__(self, repository: "BaseRepository", pk: PK) -> Optional[DB_MODEL]: ...


class ModelPrefix(str):
    def plus(self, field_name: str):
        if self == '':
            return self.__class__(field_name)
        else:
            return self.__class__(f'{self}__{field_name}')


class BaseRepository(Generic[DB_MODEL], metaclass=BaseRepositoryMeta):
    model: Type[DB_MODEL]
    pk_attr: str
    node_key: str
    pk_field_type: Type[PK]

    create_handlers: dict[str, CreateHandler[DB_MODEL]]
    edit_handlers: dict[str, EditHandler[DB_MODEL]]
    fk_get_instance_map: dict[str, FKGetInstance[PK, DB_MODEL]]
    defaults: dict[str, dict[str, Any]]

    request: Optional[Request]
    background_tasks: Optional[BackgroundTasks]

    def __init__(self, *, request: Request = None, background_tasks: BackgroundTasks = None):
        self.request = request
        self.background_tasks = background_tasks

    def get_queryset(self):
        raise NotImplementedError()

    async def get_all(
            self,
            skip: Optional[int],
            limit: Optional[int],
            sort: set[str],
            filters: list[BaseFilter],
    ) -> tuple[list[DB_MODEL], int]:
        raise NotImplementedError()

    async def get_many(self, item_ids: list[PK]) -> list[DB_MODEL]:
        raise NotImplementedError()

    async def get_one(self, item_id: PK, *, field_name: str = 'pk') -> DB_MODEL:
        raise NotImplementedError()

    async def get_tree_node(self, node_id: Optional[PK]) -> list[DB_MODEL]:
        raise NotImplementedError()

    async def create(
            self,
            data: CamelModel,
            *,
            model: Type[DB_MODEL] = None,
            exclude: set[str] = None,
            defaults: dict[str, Any] = None,
            inside_transaction: bool = False,
            prefix: ModelPrefix = ModelPrefix(),
    ) -> DB_MODEL:
        raise NotImplementedError()

    async def edit(
            self,
            instance: DB_MODEL,
            data: CamelModel,
            *,
            exclude: set[str] = None,
            defaults: dict[str, Any] = None,
            inside_transaction: bool = False,
            prefix: ModelPrefix = ModelPrefix(),
    ) -> DB_MODEL:
        raise NotImplementedError()

    async def delete_many(self, item_ids: list[PK]) -> int:
        raise NotImplementedError()

    async def delete_one(self, item_id: PK) -> None:
        raise NotImplementedError()

    @classmethod
    def with_model_permissions(cls, name: str) -> Callable[[...], Coroutine]:
        return get_auth_backend().get_auth_with_permissions((cls.model.__name__, name))

    @classmethod
    def check_auth(cls) -> Callable[[...], Coroutine]:
        return get_auth_backend().check_auth()

    @classmethod
    def with_create_permissions(cls) -> Callable[[...], Coroutine]:
        return cls.with_model_permissions('create')

    @classmethod
    def with_get_permissions(cls) -> Callable[[...], Coroutine]:
        return cls.with_model_permissions('get')

    @classmethod
    def with_edit_permissions(cls) -> Callable[[...], Coroutine]:
        return cls.with_model_permissions('edit')

    @classmethod
    def with_delete_permissions(cls) -> Callable[[...], Coroutine]:
        return cls.with_model_permissions('delete')

    @classmethod
    def get_default_sort_fields(cls) -> set[str]:
        raise NotImplementedError
