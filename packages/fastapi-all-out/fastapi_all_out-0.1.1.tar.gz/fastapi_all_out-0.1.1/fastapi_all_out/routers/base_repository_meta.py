from typing import Type


class BaseRepositoryMeta(type):
    def __new__(mcs, name: str, bases: tuple[Type, ...], attrs: dict):
        attrs.setdefault('create_handlers', {})
        attrs.setdefault('edit_handlers', {})
        attrs.setdefault('fk_get_instance_map', {})
        attrs.setdefault('defaults', {})

        return super().__new__(mcs, name, bases, attrs)

