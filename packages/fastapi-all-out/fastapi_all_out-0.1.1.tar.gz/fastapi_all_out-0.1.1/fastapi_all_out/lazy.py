from importlib import import_module
from typing import Any, TYPE_CHECKING, Type, TypeVar

from pydantic.utils import import_string

from fastapi_all_out.settings import MainDB, BaseSettings,\
    MAIN_DB, USER_MODEL, REPOSITORY, USER_REPOSITORY, USER_SERVICE, MAIL_SENDER, CODES, AUTH

if TYPE_CHECKING:
    from fastapi_all_out.code_responses import DefaultCodes
    from fastapi_all_out.routers.base_repository import BaseRepository
    from fastapi_all_out.mailing import MailSender
    from fastapi_all_out.auth.base import AuthBackend
    from fastapi_all_out.auth.user_service import BaseUserService


_T = TypeVar('_T')


def get_settings(var: str, default: Any = '__undefined__') -> Any:
    settings = import_module('settings')
    if default == '__undefined__':
        return getattr(settings, var)
    return getattr(settings, var, default)


def get_settings_obj() -> BaseSettings:
    return get_settings('settings')


def get_schema(default: Type[_T], field: bool = False) -> Type[_T]:
    prefix = 'fields' if field else 'schemas'
    try:
        return import_string(f'{prefix}.{default.__name__}')
    except ImportError as e:
        try:
            if not get_settings('PROD'):
                print(e)
        except AttributeError:
            pass
        return default


def get_main_db() -> MainDB:
    main_db = get_settings('MAIN_DB', MAIN_DB)
    assert isinstance(main_db, MainDB)
    return main_db


def import_settings(name: str, default: str) -> Any:
    return import_string(get_settings(name, default))


def get_codes() -> Type["DefaultCodes"]:
    return import_settings('CODES', CODES)


def get_user_model_path() -> str:
    return get_settings('USER_MODEL', USER_MODEL)


def get_user_model():
    return import_settings('USER_MODEL', USER_MODEL)


def get_repository() -> Type["BaseRepository"]:
    main_db = get_main_db().value
    return import_settings('REPOSITORY', REPOSITORY.format(main_db.lower(), main_db.title()))


def get_user_repository() -> Type["BaseRepository"]:
    main_db = get_main_db().value
    return import_settings('USER_REPOSITORY', USER_REPOSITORY.format(main_db.lower(), main_db.title()))


def get_user_service() -> Type["BaseUserService"]:
    main_db = get_main_db().value
    return import_settings('USER_SERVICE', USER_SERVICE.format(main_db.lower(), main_db.title()))


def get_mail_sender() -> "MailSender":
    return import_settings('MAIL_SENDER', MAIL_SENDER)


AUTH_BACKEND = None


def get_auth_backend() -> "AuthBackend":
    global AUTH_BACKEND
    if AUTH_BACKEND is None:
        auth_config = get_settings('AUTH', AUTH)
        strategy = import_string(auth_config['strategy'][0])(**auth_config['strategy'][1])
        AUTH_BACKEND = import_string(auth_config['backend'][0])(strategy, **auth_config['backend'][1])
    return AUTH_BACKEND
