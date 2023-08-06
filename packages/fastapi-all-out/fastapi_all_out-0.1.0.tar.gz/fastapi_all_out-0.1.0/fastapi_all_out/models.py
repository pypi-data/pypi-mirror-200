from fastapi_all_out.settings import MainDB
from fastapi_all_out.lazy import get_main_db


match get_main_db():
    case MainDB.tortoise:
        from fastapi_all_out.contrib.tortoise.models import \
            BaseModel, default_of, max_len_of, \
            Permission, PermissionGroup
    case _:
        BaseModel = None
        default_of = None
        max_len_of = None
        Permission = None
        PermissionGroup = None


__all__ = [
    BaseModel, default_of, max_len_of,
    Permission, PermissionGroup
]
