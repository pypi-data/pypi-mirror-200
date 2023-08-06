from typing import Optional

from pydantic import Field

from fastapi_all_out.pydantic import CamelModel, CamelModelORM, RelatedList, FieldInRelatedModel
from fastapi_all_out.models import Permission, PermissionGroup, max_len_of


__all__ = [
    "PermissionRead", "PermissionIDS",
    "PermissionGroupRead", "PermissionGroupCreate", "PermissionGroupEdit"
]


max_len_pg = max_len_of(PermissionGroup)
PermissionIDS = RelatedList[FieldInRelatedModel(Permission, 'id', int)]


class PermissionRead(CamelModelORM):
    id: int
    name: str
    content_type_name: str


class PermissionGroupRead(CamelModelORM):
    id: int
    name: str
    permissions: PermissionIDS


class PermissionGroupCreate(CamelModel):
    name: str = Field(max_length=max_len_pg('name'))
    permissions: list[int]


class PermissionGroupEdit(CamelModel):
    name: Optional[str] = Field(max_length=max_len_pg('name'))
    permissions: Optional[list[int]]
