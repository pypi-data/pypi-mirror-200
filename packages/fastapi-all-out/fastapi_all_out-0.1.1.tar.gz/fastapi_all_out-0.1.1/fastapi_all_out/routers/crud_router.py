from collections.abc import Sequence
from enum import Enum
from typing import Callable, Any, Generic, TypeVar, Optional, Type

from fastapi import Response, Request, APIRouter, Body, Path, Query, params, Depends, BackgroundTasks
from fastapi.exceptions import RequestValidationError
from pydantic.error_wrappers import ErrorWrapper

from fastapi_all_out.code_responses import BaseCodes
from fastapi_all_out.pydantic import CommaSeparatedOf, lower_camel, CamelModel
from fastapi_all_out.lazy import get_codes
from fastapi_all_out.responses import BgHTTPException
from fastapi_all_out.routers import BaseRepository
from .exceptions import ItemNotFound, ObjectErrors
from .filters import BaseFilter
from .utils import pagination_factory, PAGINATION, get_filters, sort_factory


DISPLAY_FIELDS = tuple[str, ...]
REPO = TypeVar('REPO', bound=BaseRepository)
DEPENDENCIES = Optional[Sequence[params.Depends]]
ROUTES_KWARGS = dict[str, bool | dict[str, Any]]


Codes = get_codes()


class CRUDRouter(Generic[REPO], APIRouter):
    repo: Type[BaseRepository]
    max_items_get_many_routes: Optional[int]
    max_items_delete_many_routes: Optional[int]
    filters: list[Type[BaseFilter]]
    available_sort: set[str]
    max_page_size: int | None
    auto_routes_dependencies: DEPENDENCIES

    read_schema: Optional[Type[CamelModel]]
    read_many_schema: Optional[Type[CamelModel]]
    read_list_item_schema: Optional[Type[CamelModel]]
    create_schema: Optional[Type[CamelModel]]
    edit_schema: Optional[Type[CamelModel]]

    def __init__(
            self,
            repo: Type[REPO],
            *,
            read_schema: Optional[Type[CamelModel]] = None,
            read_many_schema: Optional[Type[CamelModel]] = None,
            read_list_item_schema: Optional[Type[CamelModel]] = None,
            create_schema: Optional[Type[CamelModel]] = None,
            edit_schema: Optional[Type[CamelModel]] = None,
            max_items_get_many: int = 100,
            max_items_delete_many: int = 100,
            prefix: str = None,
            tags: Optional[list[str | Enum]] = None,
            filters: list[Type[BaseFilter]] = None,
            available_sort: set[str] = None,
            max_page_size: int | None = 100,
            auto_routes_dependencies: DEPENDENCIES = None,
            routes_kwargs: ROUTES_KWARGS = None,
            add_tree_routes: bool = False,
            read_only: bool = False,
            routes_only: set[str] = None,
            complete_auto_routes: bool = True,
            **kwargs,
    ) -> None:
        """
            :param max_items_get_many         отпределяет маскимальное количество записей, которые достаются по id
            :param max_items_delete_many      отпределяет маскимальное количество записей, которые удаляются по id
            :param prefix                     префикс из APIRouter
            :param tags                       tags из APIRouter
            :param filters                    фильтры для get_all
            :param available_sort             поля для сортировки для get_all
            :param auto_routes_dependencies   инъекции которые применяются для всех роутов, сгенерированных
                                              автоматически, если нужно для всех, не только автоматически
                                              сгенерированных, то нужно использовать dependencies
            :param routes_kwargs              словарь вида {route_name: add_api_route kwargs},
                                              значение может быть равно False, если этот роут не нужен ({create: False})
            :param add_tree_routes            добавляет методы для деревьев
            :param read_only                  создаёт только get методы
            :param routes_only                set из роутов, которые нужно создать
            :param complete_auto_routes       если нужно создать какие-то роуты, без Path параметров, которые просто так
                                              перекрываются
            :param kwargs                     всё что передаётся в APIRouter
        """

        self.repo = repo
        prefix = prefix.strip('/') if prefix else self.repo.model.__name__.lower() + 's'
        tags = tags or [prefix]
        prefix = '/' + prefix
        super().__init__(prefix=prefix, tags=tags, **kwargs)

        self.read_schema = read_schema
        self.read_many_schema = read_many_schema or self.read_schema
        self.read_list_item_schema = read_list_item_schema or self.read_many_schema
        self.create_schema = create_schema
        self.edit_schema = edit_schema

        self.max_items_get_many_routes = max_items_get_many
        self.max_items_delete_many_routes = max_items_delete_many
        self.read_only = read_only

        self.auto_routes_dependencies = auto_routes_dependencies or []
        self.routes_kwargs = routes_kwargs or {}

        if routes_only:
            routes_names = routes_only
        else:
            routes_names = self.default_routes_names()
            if add_tree_routes:
                routes_names = *routes_names, *self.tree_route_names()
        self.routes_names = routes_names

        if filters is None:
            filters = []
        self.filters = filters
        self.available_sort = available_sort or self.repo.get_default_sort_fields()
        self.max_page_size = max_page_size

        if complete_auto_routes:
            self.complete_auto_routes()

    def complete_auto_routes(self) -> None:
        for route_name in self.routes_names:
            route_data = self.routes_kwargs.get(route_name, True)
            if route_data is False:
                continue
            self._register_route(route_name, (route_data if isinstance(route_data, dict) else {}))

    def _get_all_route(self) -> Callable[..., Any]:
        list_item_schema = self.get_read_list_item_schema()

        async def route(
                background_tasks: BackgroundTasks,
                request: Request,
                response: Response,
                pagination: PAGINATION = pagination_factory(self.max_page_size),
                sort: set[str] = Depends(sort_factory(self.available_sort)),
                applied_filters: list[BaseFilter] = Depends(get_filters(self.filters))
        ):
            raise_if_error_in_filters(applied_filters)
            skip, limit = pagination
            repository = self.repo(request=request, background_tasks=background_tasks)
            result, total = await repository.get_all(
                skip=skip,
                limit=limit,
                sort=sort,
                filters=applied_filters,
            )
            response.headers.append('X-Total-Count', str(total))
            return [list_item_schema.from_orm(r) for r in result]

        return route

    def _get_many_route(self) -> Callable[..., Any]:
        pk_field_type = self.repo.pk_field_type
        max_items = self.max_items_get_many_routes
        read_many_schema = self.get_read_many_schema()

        async def route(
                request: Request,
                background_tasks: BackgroundTasks,
                item_ids: CommaSeparatedOf(pk_field_type, max_items=max_items, in_query=True) = Query(..., alias='ids')
        ):
            repository = self.repo(request=request, background_tasks=background_tasks)
            results = await repository.get_many(item_ids)
            return [read_many_schema.from_orm(r) for r in results]

        return route

    def _get_one_route(self) -> Callable[..., Any]:
        pk_field_type = self.repo.pk_field_type
        read_schema = self.get_read_schema()

        async def route(
                request: Request,
                background_tasks: BackgroundTasks,
                item_id: pk_field_type = Path(...),
        ):
            try:
                repository = self.repo(request=request, background_tasks=background_tasks)
                item = await repository.get_one(item_id)
            except ItemNotFound:
                raise self.not_found_error()
            return read_schema.from_orm(item)

        return route

    def _get_tree_node_route(self) -> Callable[..., Any]:
        pk_field_type = self.repo.pk_field_type
        get_list_item_schema = self.get_read_list_item_schema()
        alias = lower_camel(self.repo.node_key)

        async def route(
                request: Request,
                background_tasks: BackgroundTasks,
                node_id: Optional[pk_field_type] = Query(None, alias=alias)
        ):
            repository = self.repo(request=request, background_tasks=background_tasks)
            return [get_list_item_schema.from_orm(item) for item in await repository.get_tree_node(node_id)]

        return route

    def _create_route(self) -> Callable[..., Any]:
        create_schema = self.get_create_schema()
        read_schema = self.get_read_schema()

        async def route(
                request: Request,
                background_tasks: BackgroundTasks,
                data: create_schema = Body(...)
        ):
            try:
                repository = self.repo(request=request, background_tasks=background_tasks)
                instance = await repository.create(data)
            except ObjectErrors as e:
                raise self.field_errors(e)
            return read_schema.from_orm(instance)

        return route

    def _edit_route(self) -> Callable[..., Any]:
        pk_field_type = self.repo.pk_field_type
        read_schema = self.get_read_schema()
        edit_schema = self.get_edit_schema()

        async def route(
                request: Request,
                background_tasks: BackgroundTasks,
                item_id: pk_field_type = Path(...),
                data: edit_schema = Body(...)
        ):
            repository = self.repo(request=request, background_tasks=background_tasks)
            try:
                instance = await repository.get_one(item_id)
            except ItemNotFound:
                raise self.not_found_error()
            try:
                instance = await repository.edit(instance, data)
            except ObjectErrors as e:
                raise self.field_errors(e)
            return read_schema.from_orm(instance)

        return route

    def _delete_many_route(self) -> Callable[..., Any]:
        pk_field_type = self.repo.pk_field_type
        max_items = self.max_items_get_many_routes

        async def route(
                request: Request,
                background_tasks: BackgroundTasks,
                item_ids: CommaSeparatedOf(pk_field_type, max_items=max_items, in_query=True) = Query(..., alias='ids')
        ):
            repository = self.repo(request=request, background_tasks=background_tasks)
            deleted_items_count = await repository.delete_many(item_ids)
            return self.ok_response(count=deleted_items_count)

        return route

    def _delete_one_route(self) -> Callable[..., Any]:
        pk_field_type = self.repo.pk_field_type

        async def route(
                request: Request,
                background_tasks: BackgroundTasks,
                item_id: pk_field_type = Path(...)
        ):
            try:
                repository = self.repo(request=request, background_tasks=background_tasks)
                await repository.delete_one(item_id)
            except ItemNotFound:
                raise self.not_found_error()
            return self.ok_response(item=item_id)

        return route

    @classmethod
    def _ok_response_instance(cls) -> BaseCodes:
        return Codes.OK

    def ok_response(self, **kwargs) -> dict[str, Any]:
        if kwargs:
            return self._ok_response_instance().resp_detail(**kwargs)
        return self._ok_response_instance().resp

    @classmethod
    def not_found_error_instance(cls) -> BaseCodes:
        return Codes.not_found

    def not_found_error(self) -> BgHTTPException:
        return self.not_found_error_instance().err()

    @classmethod
    def field_errors_instance(cls) -> BaseCodes:
        return Codes.fields_error

    def field_errors_response_example(self) -> tuple[BaseCodes, dict[str, str]]:
        return (self.field_errors_instance(), {
            'errors': 'Объект, который соответствует заполняемой модели, но вместо значений - ошибки'
        })

    def field_errors(self, object_errors: ObjectErrors) -> BgHTTPException:
        return self.field_errors_instance().err({'errors': object_errors.to_error()})

    def default_routes_names(self) -> tuple[str, ...]:
        if self.read_only:
            return 'get_all', 'get_many', 'get_one'
        return 'get_all', 'get_many', 'get_one', 'create', 'edit', 'delete_many', 'delete_one'

    @staticmethod
    def tree_route_names() -> tuple[str, ...]:
        return 'get_tree_node',

    def all_route_names(self) -> tuple[str, ...]:
        return *self.default_routes_names(), *self.tree_route_names()

    def _register_route(
            self,
            route_name: str,
            route_kwargs: dict[str, Any],
    ) -> None:
        responses = {}
        response_model = None
        status = 200
        openapi_extra = None
        route_kwargs = {**self.routes_kwargs.get('all', {}), ** route_kwargs}
        match route_name:
            case 'get_all':
                path = '/all'
                method = ["GET"]
                response_model = list[self.get_read_list_item_schema()]
                check_perms_dependency = Depends(self.repo.with_get_permissions())
                openapi_extra = {'parameters': [f.query_openapi_desc() for f in self.filters]}
            case 'get_many':
                path = '/many'
                method = ["GET"]
                response_model = list[self.get_read_many_schema()]
                check_perms_dependency = Depends(self.repo.with_get_permissions())
            case 'get_one':
                path = '/one/{item_id}'
                method = ["GET"]
                response_model = self.get_read_schema()
                responses = Codes.responses(self.not_found_error_instance())
                check_perms_dependency = Depends(self.repo.with_get_permissions())
            case 'get_tree_node':
                path = '/tree'
                method = ["GET"]
                response_model = list[self.get_read_list_item_schema()]
                check_perms_dependency = Depends(self.repo.with_get_permissions())
            case 'create':
                path = '/create'
                method = ["POST"]
                response_model = self.get_read_schema()
                responses = Codes.responses(self.field_errors_response_example())
                status = 201
                check_perms_dependency = Depends(self.repo.with_create_permissions())
            case 'edit':
                path = '/{item_id}'
                method = ["PATCH"]
                response_model = self.get_read_schema()
                responses = Codes.responses(
                    self.not_found_error_instance(),
                    self.field_errors_response_example()
                )
                check_perms_dependency = Depends(self.repo.with_edit_permissions())
            case 'delete_many':
                path = '/many'
                method = ["DELETE"]
                # don`t need response model, responses has one with status 200
                responses = Codes.responses((self._ok_response_instance(), {'count': 30}), )
                check_perms_dependency = Depends(self.repo.with_delete_permissions())
            case 'delete_one':
                path = '/{item_id}'
                method = ["DELETE"]
                # don`t need response model, responses has one with status 200
                responses = Codes.responses((self._ok_response_instance(), {'item': 77}), )
                check_perms_dependency = Depends(self.repo.with_delete_permissions())
            case _:
                raise Exception(f'Unknown name of route: {route_name}.\n'
                                f'Available are {", ".join(self.default_routes_names())}')
        summary = f"{route_name.title().replace('_', ' ')} {self.repo.model.__name__}"

        if route_kwargs.get('check_perms', True):
            dependencies = [*self.auto_routes_dependencies, check_perms_dependency]
        elif route_kwargs.get('check_auth', True):
            dependencies = [*self.auto_routes_dependencies, Depends(self.repo.check_auth())]
        else:
            dependencies = [*self.auto_routes_dependencies]
        route_kwargs = get_route_kwargs(route_kwargs, dependencies, responses)

        self.add_api_route(
            path=path,
            endpoint=getattr(self, f'_{route_name}_route')(),
            methods=method,
            response_model=response_model,
            summary=summary,
            status_code=status,
            openapi_extra=openapi_extra,
            **route_kwargs,
        )

    def get_read_schema(self):
        return self.read_schema

    def get_read_many_schema(self):
        return self.read_many_schema

    def get_read_list_item_schema(self):
        return self.read_list_item_schema

    def get_create_schema(self):
        return self.create_schema

    def get_edit_schema(self):
        return self.edit_schema


def get_route_kwargs(
        route_data: dict[str, Any],
        dependencies: DEPENDENCIES,
        responses: dict[str, Any],
) -> dict[str, Any]:
    if isinstance(route_data, bool):
        route_data = {}
    else:
        route_data = {**route_data}
    route_data['dependencies'] = [*dependencies, *route_data.get('dependencies', [])] or None
    route_data['responses'] = {**responses, **route_data.get('responses', {})} or None
    for kwarg in tuple(route_data.keys()):
        if kwarg not in available_api_route_kwargs:
            del route_data[kwarg]
    return route_data


def raise_if_error_in_filters(filters: list[BaseFilter]) -> None:
    errors = [ErrorWrapper(f.error, loc=("filters", f.camel_source)) for f in filters if f.error is not None]
    if errors:
        raise RequestValidationError(errors)


available_api_route_kwargs = [
    'dependencies',
    'responses',
    'tags',
    'description',
    'response_description',
    'deprecated',
    'operation_id',
    'response_model_include',
    'response_model_exclude',
    'response_model_by_alias',
    'response_model_exclude_unset',
    'response_model_exclude_defaults',
    'response_model_exclude_none',
    'include_in_schema',
    'response_class',
    'name',
    'route_class_override',
    'callbacks',
    'openapi_extra',
    'generate_unique_id_function',
]
