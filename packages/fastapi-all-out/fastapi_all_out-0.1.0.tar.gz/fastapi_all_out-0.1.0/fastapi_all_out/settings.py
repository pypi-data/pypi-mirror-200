import os
from enum import Enum
from pathlib import Path

from pydantic import BaseSettings as PydanticBaseSettings, DirectoryPath, AnyHttpUrl


MODE = os.environ.get('MODE') or 'DEBUG'
DEBUG = MODE == 'DEBUG'
DEV = MODE == 'DEV'
PROD = MODE == 'PROD'


class MainDB(Enum):
    tortoise = 'tortoise'


class SettingsConfig(PydanticBaseSettings.Config):
    env_file = '.env' if DEBUG else None


class BaseSettings(PydanticBaseSettings):

    API_PREFIX: str = '/api'
    HOST: AnyHttpUrl = 'http://localhost:8000'

    class Config(SettingsConfig):
        pass


lib = 'fastapi_all_out'
MAIN_DB = MainDB.tortoise
USER_MODEL = 'models.User'
REPOSITORY = f'{lib}.contrib.{{}}.repository.{{}}Repository'
USER_REPOSITORY = f'{lib}.contrib.{{}}.user_repository.{{}}UserRepository'
USER_SERVICE = f'{lib}.contrib.{{}}.user_service.{{}}UserService'
AUTH = {
    'strategy': (f'{lib}.auth.jwt.strategy.RS256JWTAuthStrategy', {'private_key': None, 'public_key': None}),
    'backend': (f'{lib}.auth.jwt.backend.JWTAuthBackend', {}),
}
MAIL_SENDER = f'{lib}.mailing.mail_sender'
CODES = f'{lib}.code_responses.DefaultCodes'


try:
    from fastapi_mail import ConnectionConfig

    class MailingConfig(ConnectionConfig):
        TEMPLATE_FOLDER: DirectoryPath = Path(__file__).parent / 'templates'

        class Config(SettingsConfig):
            pass
except ImportError:
    MailingConfig, ConnectionConfig = None, None
