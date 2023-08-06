from collections import defaultdict
from typing import Any, Optional, TypeVar, TYPE_CHECKING, Type, Callable, Coroutine

from tortoise.models import MetaInfo
from tortoise.fields import ManyToManyRelation
from tortoise.queryset import QuerySet
from tortoise.transactions import in_transaction

from fastapi_all_out.pydantic import CamelModel
from fastapi_all_out.routers.base_repository import BaseRepository, PK, ModelPrefix, CreateHandler, EditHandler, \
    FKGetInstance
from fastapi_all_out.routers.exceptions import ItemNotFound, ObjectErrors, NotUnique, ListFieldError, NotFoundFK, \
    FieldRequired
from .repository_meta import TortoiseRepositoryMeta
from .models import BaseModel

if TYPE_CHECKING:
    from fastapi_all_out.routers.filters import BaseFilter


DB_MODEL = TypeVar('DB_MODEL', bound=BaseModel)


class TortoiseRepository(BaseRepository[DB_MODEL], metaclass=TortoiseRepositoryMeta):
    opts: MetaInfo
    node_key = 'parent_id'

    select_related: tuple[str]
    prefetch_related: tuple[str]

    def __init__(self, *args, select_related: tuple[str] = (), prefetch_related: tuple[str] = (), **kwargs):
        super().__init__(*args, **kwargs)
        self.select_related = select_related
        self.prefetch_related = prefetch_related

    def get_queryset(self):
        if self.request is None:
            path, method = '', ''
        else:
            path, method = self.request.scope['route'].path, self.request.method

        query = self.model.all()
        if default_filters := self.qs_default_filters(path, method):
            query = query.filter(**default_filters)
        if annotate_fields := self.qs_annotate_fields(path, method):
            query = query.annotate(**annotate_fields)
        if final_select_related := {*self.qs_select_related(path, method), *self.select_related}:
            query = query.select_related(*final_select_related)
        if final_prefetch_related := {*self.qs_prefetch_related(path, method), *self.prefetch_related}:
            query = query.prefetch_related(*final_prefetch_related)
        return query

    @classmethod
    def qs_default_filters(cls, path: str, method: str) -> dict[str, Any]:
        return {}

    @classmethod
    def qs_annotate_fields(cls, path: str, method: str) -> dict[str, Any]:
        return {}

    @classmethod
    def qs_select_related(cls, path: str, method: str) -> set[str]:
        return set()

    @classmethod
    def qs_prefetch_related(cls, path: str, method: str) -> set[str]:
        return set()

    async def get_all(
            self,
            skip: Optional[int],
            limit: Optional[int],
            sort: set[str],
            filters: list["BaseFilter"],
    ) -> tuple[list[DB_MODEL], int]:
        query = self.get_queryset()
        for f in filters:
            query = f.filter(query)
        base_query = query
        if sort:
            query = query.order_by(*sort)
        if skip:
            query = query.offset(skip)
        if limit:
            query = query.limit(limit)
        async with in_transaction():
            result = await query
            count = await base_query.count()
        return result, count

    def _get_many_queryset(self, item_ids: list[PK]) -> QuerySet[DB_MODEL]:
        return self.get_queryset().filter(pk__in=item_ids)

    async def get_many(self, item_ids: list[PK]) -> list[DB_MODEL]:
        return await self._get_many_queryset(item_ids)

    async def get_one(self, item_id: PK, *, field_name: str = 'pk') -> Optional[DB_MODEL]:
        instance = await self.get_queryset()\
            .get_or_none(**{field_name: item_id})
        if instance is None:
            raise ItemNotFound()
        return instance

    async def get_tree_node(self, node_id: Optional[PK]) -> list[DB_MODEL]:
        return await self.get_queryset().filter(**{self.node_key: node_id})

    async def create(
            self,
            data: CamelModel,
            *,
            model: Type[BaseModel] = None,
            exclude: set[str] = None,
            defaults: dict[str, Any] = None,
            inside_transaction: bool = False,
            prefix: ModelPrefix = ModelPrefix(),
    ) -> DB_MODEL:
        model: Type[BaseModel] = model or self.model
        fk_fields, bfk_fields, o2o_fields, bo2o_fields, m2m_fields = exclude_fk_bfk_o2o_bo2o_m2m(model, data)
        exclude_dict = get_exclude_dict(exclude or set())
        errors = ObjectErrors()
        defaults = defaults or {}

        async def get_new_instance() -> DB_MODEL:
            not_unique = await model.check_unique(data.dict(include=model._meta.db_fields))
            for field_name in not_unique:
                errors.add(field_name, NotUnique)

            # Сначала создаём o2o и fk, потому что они могут быть not null, из-за этого вылетает ошибка.
            created_o2o, picked_fks = {}, {}

            for o2o_field_name in o2o_fields:
                try:
                    o2o_instance = await self.create_o2o(
                        model=model,
                        field_name=o2o_field_name,
                        data=data,
                        exclude=exclude_dict[o2o_field_name],
                        prefix=prefix
                    )
                    created_o2o[o2o_field_name] = o2o_instance
                except ObjectErrors as e:
                    errors.add(o2o_field_name, e)

            try:
                picked_fks = await self.pick_fks(model=model, fk_fields=fk_fields, data=data, prefix=prefix)
            except ObjectErrors as e:
                errors.merge(e)

            if errors:
                raise errors
            try:
                instance: DB_MODEL = await self.handle_create(prefix, model=model)(
                    data=data,
                    exclude={*exclude_dict['__root__'], *fk_fields},
                    defaults={**self.defaults.get(prefix, {}), **defaults, **created_o2o, **picked_fks}
                )
            except ObjectErrors as e:
                raise errors.merge(e)

            for bo2o_field_name in bo2o_fields:
                try:
                    await self.create_backward_o2o(
                        instance=instance,
                        field_name=bo2o_field_name,
                        data=data,
                        exclude=exclude_dict[bo2o_field_name],
                        prefix=prefix
                    )
                except ObjectErrors as e:
                    errors.add(bo2o_field_name, e)

            for bfk_field_name in bfk_fields:
                try:
                    await self.create_backward_fk(
                        instance=instance,
                        field_name=bfk_field_name,
                        data=data,
                        exclude=exclude_dict[bfk_field_name],
                        prefix=prefix,
                    )
                except ListFieldError as e:
                    errors.add(bfk_field_name, e)

            for m2m_field_name in m2m_fields:
                await self.save_m2m(
                    instance=instance,
                    data=data,
                    field_name=m2m_field_name,
                    prefix=prefix,
                )

            if errors:
                raise errors
            return instance

        if inside_transaction:
            return await get_new_instance()
        else:
            async with in_transaction():
                new_instance = await get_new_instance()
            return await self.get_one(new_instance.pk)

    async def create_o2o(
            self,
            model: Type[DB_MODEL],
            field_name: str,
            data: CamelModel,
            exclude: set[str],
            prefix: ModelPrefix,
    ) -> Optional[DB_MODEL]:
        o2o_data = getattr(data, field_name)
        if o2o_data is None:
            return None
        o2o_model: Type[BaseModel] = model._meta.fields_map[field_name].related_model
        return await self.create(
            data=o2o_data,
            model=o2o_model,
            exclude=exclude,
            inside_transaction=True,
            prefix=prefix.plus(field_name)
        )

    async def create_backward_o2o(
            self,
            instance: BaseModel,
            field_name: str,
            data: CamelModel,
            exclude: set[str],
            prefix: ModelPrefix,
    ) -> None:
        back_o2o_data = getattr(data, field_name)
        if back_o2o_data is None:
            return
        back_o2o_field = instance._meta.fields_map[field_name]
        back_o2o_model: Type[BaseModel] = back_o2o_field.related_model
        back_o2o_source_field = back_o2o_model._meta\
            .fields_map[back_o2o_field.relation_source_field]\
            .reference.model_field_name
        await self.create(
            data=back_o2o_data,
            model=back_o2o_model,
            exclude=exclude,
            defaults={back_o2o_source_field: instance},
            inside_transaction=True,
            prefix=prefix.plus(field_name)
        )

    async def create_backward_fk(
            self,
            instance: BaseModel,
            field_name: str,
            data: CamelModel,
            exclude: set[str],
            prefix: ModelPrefix,
    ) -> None:
        list_errors = ListFieldError()
        back_fk_field = instance._meta.fields_map[field_name]
        back_fk_model: Type[BaseModel] = back_fk_field.related_model
        back_fk_source_field = back_fk_model._meta \
            .fields_map[back_fk_field.relation_source_field] \
            .reference.model_field_name
        next_prefix = prefix.plus(field_name)
        for index, back_fk_data in enumerate(getattr(data, field_name)):
            try:
                await self.create(
                    data=back_fk_data,
                    model=back_fk_model,
                    exclude=exclude,
                    defaults={back_fk_source_field: instance},
                    inside_transaction=True,
                    prefix=next_prefix,
                )
            except ObjectErrors as e:
                list_errors.append(index, e)
        if list_errors:
            raise list_errors

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
        model: Type[BaseModel] = instance.__class__
        fk_fields, bfk_fields, o2o_fields, bo2o_fields, m2m_fields = exclude_fk_bfk_o2o_bo2o_m2m(model, data)
        exclude_dict = get_exclude_dict(exclude or set())
        errors = ObjectErrors()
        defaults = defaults or {}

        async def get_changed_instance() -> DB_MODEL:
            not_unique = await model.check_unique(data.dict(include=model._meta.db_fields, exclude_unset=True))
            for field_name in not_unique:
                errors.add(field_name, NotUnique)

            created_o2o, picked_fks = {}, {}
            for o2o_field_name in o2o_fields:
                try:
                    o2o_instance = await self.edit_o2o(
                        instance=instance,
                        field_name=o2o_field_name,
                        data=data,
                        exclude=exclude_dict[o2o_field_name],
                        prefix=prefix,
                    )
                    if o2o_instance:
                        created_o2o[o2o_field_name] = o2o_instance
                except ObjectErrors as e:
                    errors.add(o2o_field_name, e)

            try:
                picked_fks = await self.pick_fks(model=model, fk_fields=fk_fields, data=data, prefix=prefix)
            except ObjectErrors as e:
                errors.merge(e)

            if errors:
                raise errors

            await self.handle_edit(prefix, model=model)(
                instance=instance,
                data=data,
                exclude={*exclude_dict['__root__'], *fk_fields},
                defaults={**defaults, **created_o2o, **picked_fks}
            )

            for bo2o_field_name in bo2o_fields:
                try:
                    await self.edit_backward_o2o(
                        instance=instance,
                        field_name=bo2o_field_name,
                        data=data,
                        exclude=exclude_dict[bo2o_field_name],
                        prefix=prefix
                    )
                except ObjectErrors as e:
                    errors.add(bo2o_field_name, e)

            for bfk_source_field_name in bfk_fields:
                try:
                    await self.edit_backward_fk(
                        instance=instance,
                        field_name=bfk_source_field_name,
                        data=data,
                        exclude=exclude_dict[bfk_source_field_name],
                        prefix=prefix
                    )
                except ListFieldError as e:
                    errors.add(bfk_source_field_name, e)

            for m2m_field_name in m2m_fields:
                await self.save_m2m(
                    instance=instance,
                    data=data,
                    field_name=m2m_field_name,
                    prefix=prefix,
                    clear=True,
                )

            if errors:
                raise errors
            return instance

        if inside_transaction:
            return await get_changed_instance()
        else:
            async with in_transaction():
                changed_instance = await get_changed_instance()
            return await self.get_one(changed_instance.pk)

    async def edit_o2o(
            self,
            instance: DB_MODEL,
            field_name: str,
            data: CamelModel,
            exclude: set[str],
            prefix: ModelPrefix,
    ) -> Optional[BaseModel]:
        o2o_instance: Optional[BaseModel] = getattr(instance, field_name)
        o2o_data = getattr(data, field_name)
        if o2o_data is None:
            if o2o_instance is not None:
                await o2o_instance.delete()
            return None
        if o2o_instance is not None:
            await self.edit(
                instance=o2o_instance,
                data=o2o_data,
                exclude=exclude,
                inside_transaction=True,
                prefix=prefix.plus(field_name),
            )
        else:
            return await self.create(
                data=o2o_data,
                exclude=exclude,
                model=instance._meta.fields_map[field_name].related_model,
                inside_transaction=True,
                prefix=prefix.plus(field_name),
            )

    async def edit_backward_o2o(
            self,
            instance: DB_MODEL,
            field_name: str,
            data: CamelModel,
            exclude: set[str],
            prefix: ModelPrefix,
    ) -> None:
        back_o2o_instance = getattr(instance, field_name)
        back_o2o_data = getattr(data, field_name)
        back_o2o_field = instance._meta.fields_map[field_name]
        back_o2o_model: Type[BaseModel] = back_o2o_field.related_model
        back_o2o_source_field = back_o2o_model._meta \
            .fields_map[back_o2o_field.relation_source_field] \
            .reference.model_field_name
        if back_o2o_instance is not None:
            await self.edit(
                instance=back_o2o_instance,
                data=back_o2o_data,
                exclude=exclude,
                inside_transaction=True,
                prefix=prefix.plus(field_name),
            )
        else:
            await self.create(
                data=back_o2o_data,
                model=back_o2o_model,
                exclude=exclude,
                defaults={back_o2o_source_field: instance},
                inside_transaction=True,
                prefix=prefix.plus(field_name),
            )

    async def edit_backward_fk(
            self,
            instance: DB_MODEL,
            field_name: str,
            data: CamelModel,
            exclude: set[str],
            prefix: ModelPrefix,
    ) -> None:
        def get_fk_instance(instances: list[BaseModel], pk_value) -> BaseModel | None:
            for i in instances:
                if i.pk == pk_value:
                    return i

        list_errors = ListFieldError()
        back_fk_instances: list[BaseModel] = getattr(instance, field_name)
        back_fk_field = instance._meta.fields_map[field_name]
        back_fk_model: Type[BaseModel] = back_fk_field.related_model
        back_fk_source_field = back_fk_model._meta \
            .fields_map[back_fk_field.relation_source_field] \
            .reference.model_field_name
        back_pk_attr = back_fk_model._meta.pk_attr
        for index, back_fk_data in enumerate(getattr(data, field_name)):
            if pk := getattr(back_fk_data, back_pk_attr, None):
                fk_instance = get_fk_instance(back_fk_instances, pk)
                if fk_instance:
                    coro = self.edit(
                        instance=fk_instance,
                        data=back_fk_data,
                        exclude=exclude,
                        inside_transaction=True,
                        prefix=prefix.plus(field_name),
                    )
                else:
                    list_errors.append(index, NotFoundFK)
                    continue
            else:
                coro = self.create(
                    data=back_fk_data,
                    model=back_fk_model,
                    exclude=exclude,
                    defaults={back_fk_source_field: instance},
                    inside_transaction=True,
                    prefix=prefix.plus(field_name),
                )
            try:
                await coro
            except ObjectErrors as e:
                list_errors.append(index, e)

        if list_errors:
            raise list_errors

    async def pick_fk(
            self,
            model: Type[DB_MODEL],
            fk_source_field_name: str,
            data: CamelModel,
            prefix: ModelPrefix,
    ) -> tuple[str, Optional[DB_MODEL]]:
        opts = model._meta
        rel_model, field_name = None, None
        for field in opts.fk_fields:
            if (f_opts := opts.fields_map[field]).source_field == fk_source_field_name:
                rel_model = f_opts.related_model
                field_name = field

        value = getattr(data, fk_source_field_name, None)
        if value is None:
            return field_name, None

        get_rel_instance_func = self.fk_get_instance_map.get(prefix.plus(fk_source_field_name), None)
        if get_rel_instance_func is None:
            get_rel_instance_func = \
                self.fk_get_instance_map[prefix.plus(fk_source_field_name)] = get_fk_instance(rel_model)
        rel_instance = await get_rel_instance_func(self, pk=value)
        if rel_instance is None:
            raise NotFoundFK
        return field_name, rel_instance

    async def pick_fks(
            self,
            model: Type[DB_MODEL],
            fk_fields: set[str],
            data: CamelModel,
            prefix: ModelPrefix,
    ) -> dict[str, Optional[DB_MODEL]]:
        picked_fks = {}
        errors = ObjectErrors()
        for fk_source_field_name in fk_fields:
            try:
                fk_field_name, fk_instance = await self.pick_fk(
                    model=model,
                    fk_source_field_name=fk_source_field_name,
                    data=data,
                    prefix=prefix
                )
                picked_fks[fk_field_name] = fk_instance
            except NotFoundFK:
                errors.add(fk_source_field_name, NotFoundFK)
        if errors:
            raise errors
        return picked_fks

    async def delete_many(self, item_ids: list[PK]) -> int:
        return await self._get_many_queryset(item_ids).delete()

    async def delete_one(self, item_id: PK) -> None:
        item = await self.get_one(item_id)
        await item.delete()

    def handle_create(self, prefix: ModelPrefix, model: Type[DB_MODEL]) -> CreateHandler[DB_MODEL]:
        if handler := self.create_handlers.get(prefix):
            return handler

        async def base_handler(
                data: CamelModel,
                exclude: set[str],
                defaults: dict[str, Any] = None,
        ) -> DB_MODEL:
            errors = ObjectErrors()
            include_fields = model._meta.db_fields.difference(exclude)
            data_dict = data.dict(include=include_fields, exclude_unset=True)
            if defaults is not None:
                data_dict.update(defaults)
            instance = model(**data_dict)
            opts = model._meta
            for field_name in (*opts.db_fields, *opts.fk_fields, *opts.o2o_fields):
                f_opts = opts.fields_map[field_name]
                if (
                        f_opts.null is False
                        and f_opts.pk is False
                        and getattr(instance, field_name) is None
                ):
                    errors.add(field_name, FieldRequired)
            if errors:
                raise errors
            await instance.save(force_create=True)
            return instance

        self.create_handlers[prefix] = base_handler
        return base_handler

    def handle_edit(self, prefix: ModelPrefix, model: Type[DB_MODEL]) -> EditHandler[DB_MODEL]:
        if handler := self.edit_handlers.get(prefix):
            return handler

        async def base_handler(
                instance: DB_MODEL,
                data: CamelModel,
                exclude: set[str],
                defaults: dict[str, Any] = None,
        ) -> DB_MODEL:
            include_fields = model._meta.db_fields.difference(exclude)
            data_dict = data.dict(include=include_fields, exclude_unset=True)
            if defaults is not None:
                data_dict.update(defaults)
            instance.update_from_dict(data_dict)
            await instance.save(force_update=True)
            return instance

        self.edit_handlers[prefix] = base_handler
        return base_handler

    async def save_m2m(
            self,
            instance: DB_MODEL,
            data: CamelModel,
            field_name: str,
            prefix: ModelPrefix,
            clear=False,
    ) -> None:
        rel: ManyToManyRelation = getattr(instance, field_name)
        ids: list[PK] = getattr(data, field_name)
        if clear:
            await rel.clear()
        await rel.add(*(await rel.remote_model.filter(pk__in=ids)))

    @classmethod
    def get_default_sort_fields(cls) -> set[str]:
        return {*cls.opts.db_fields}


def get_exclude_dict(fields: set[str]) -> dict[str, set[str]]:
    """
    Из {a, b, c.d, c.e, f.g.h, f.g.i} делает
    {
        '__root__': {'a', 'b'},
        'c': {'d', 'e'},
        'f': {'g.h', 'g.i'}
    }
    """
    exclude_dict = defaultdict(set)
    for field in fields:
        if '.' not in field:
            exclude_dict['__root__'].add(field)
        else:
            base, _, field_in_related = field.partition('.')
            exclude_dict[base].add(field_in_related)
    return exclude_dict


def exclude_fk_bfk_o2o_bo2o_m2m(
        model: Type[BaseModel], data: CamelModel
) -> tuple[set[str], set[str], set[str], set[str], set[str]]:
    opts = model._meta
    return (
        exclude_fields_from_data(data, *(opts.fields_map[f].source_field for f in opts.fk_fields)),
        exclude_fields_from_data(data, *opts.backward_fk_fields),
        exclude_fields_from_data(data, *opts.o2o_fields),
        exclude_fields_from_data(data, *opts.backward_o2o_fields),
        exclude_fields_from_data(data, *opts.m2m_fields)
    )


def exclude_fields_from_data(data: CamelModel, *fields: str) -> set[str]:
    return_fields: set[str] = set()
    for field_name in fields:
        if field_name in data.__fields_set__:
            return_fields.add(field_name)
    return return_fields


def get_fk_instance(model: Type[DB_MODEL]) -> FKGetInstance[PK, DB_MODEL]:
    async def func(repository: "BaseRepository", pk: PK) -> Optional[DB_MODEL]:
        return await model.get_or_none(pk=pk)
    return func
