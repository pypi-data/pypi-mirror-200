from enum import Enum
from typing import Type, Optional, Any

from tortoise.fields.data import CharEnumFieldInstance, CharEnumType


class NameCharEnumFieldInstance(CharEnumFieldInstance):

    def to_python_value(self, value: str | None) -> Enum | None:
        self.validate(value)
        if value is None or isinstance(value, self.enum_type):
            return value
        return getattr(self.enum_type, value)

    def to_db_value(
        self, value: Enum | None | str, instance: "Type[Model] | Model"
    ) -> str | None:
        self.validate(value)
        if isinstance(value, Enum):
            return str(value.name)
        if isinstance(value, str):
            return str(getattr(self.enum_type, value).name)
        return value


def NameCharEnumField(
    enum_type: Type[CharEnumType],
    description: Optional[str] = None,
    max_length: int = 0,
    **kwargs: Any,
) -> CharEnumType:
    """
    Char Enum Field

    A field representing a character enumeration.

    **Warning**: If ``max_length`` is not specified or equals to zero, the size of represented
    char fields is automatically detected. So if later you update the enum, you need to update your
    table schema as well.

    **Note**: Valid str value of ``enum_type`` is acceptable.

    ``enum_type``:
        The enum class
    ``description``:
        The description of the field. It is set automatically if not specified to a multiline list
        of "name: value" pairs.
    ``max_length``:
        The length of the created CharField. If it is zero it is automatically detected from
        enum_type.

    """

    return NameCharEnumFieldInstance(enum_type, description, max_length, **kwargs)  # type: ignore
