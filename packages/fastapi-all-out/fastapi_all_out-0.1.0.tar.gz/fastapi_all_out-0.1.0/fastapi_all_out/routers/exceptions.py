from typing import Union, Type, Self


class ItemNotFound(Exception):
    pass


class FieldError(Exception):
    key: str

    @classmethod
    def to_error(cls):
        return cls.key


class NotUnique(FieldError):
    key = 'notUnique'


class NotFoundFK(FieldError):
    key = 'notFoundFK'


class FieldRequired(FieldError):
    key = 'requiredField'


class ListFieldError(FieldError):
    objects_map: dict[int, Union["ObjectErrors", "FieldError"]]

    def __init__(self,  *args):
        super().__init__(*args)
        self.objects_map = {}

    def append(self, index: int, err: Union[Type["FieldError"], "FieldError", "ObjectErrors"]):
        self.objects_map[index] = err

    def to_error(self):
        return {key: error.to_error() for key, error in self.objects_map.items()}

    def __bool__(self):
        return not not self.objects_map


class ObjectErrors(Exception):
    errors: dict[str, Union[Type["FieldError"], "FieldError", "ObjectErrors"]]

    def __init__(self, *args):
        super().__init__(*args)
        self.errors = {}

    def to_error(self):
        return {key: error.to_error() for key, error in self.errors.items()}

    def add(self, field: str, error: Union[Type["FieldError"], "FieldError", "ObjectErrors"]):
        self.errors[field] = error

    def merge(self, obj_error: "ObjectErrors") -> Self:
        self.errors.update(obj_error.errors)
        return self

    def __bool__(self):
        return not not self.errors
