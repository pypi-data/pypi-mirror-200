from fastapi import APIRouter

from fastapi_all_out.routers import CRUDRouter
from fastapi_all_out.lazy import get_schema, get_repository
from fastapi_all_out.models import Permission, PermissionGroup
from fastapi_all_out.schemas import PermissionRead, PermissionGroupRead, PermissionGroupCreate, PermissionGroupEdit


Repository = get_repository()


def get_roles_router(prefix: str = '/roles', **kwargs) -> APIRouter:
    router = APIRouter(prefix=prefix, **kwargs)

    router.include_router(CRUDRouter(
        repo=type('PermissionRepository', (Repository, ), {'model': Permission}),  # type: ignore
        read_schema=get_schema(PermissionRead),
        read_only=True,
    ))

    router.include_router(CRUDRouter(
        repo=type('PermissionGroupRepository', (Repository, ), {'model': PermissionGroup}),  # type: ignore
        read_schema=get_schema(PermissionGroupRead),
        edit_schema=get_schema(PermissionGroupEdit),
        create_schema=get_schema(PermissionGroupCreate),
    ))

    return router
