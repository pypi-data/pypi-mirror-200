from typing import Type

from fastapi_all_out.routers.base_repository_meta import BaseRepositoryMeta


class TortoiseRepositoryMeta(BaseRepositoryMeta):
    def __new__(mcs, name: str, bases: tuple[Type, ...], attrs: dict):
        if 'model' in attrs:
            model = attrs['model']
            attrs['opts'] = opts = model._meta
            attrs['pk_field_type'] = opts.pk.field_type
            attrs['pk_attr'] = opts.pk_attr

        return super().__new__(mcs, name, bases, attrs)
