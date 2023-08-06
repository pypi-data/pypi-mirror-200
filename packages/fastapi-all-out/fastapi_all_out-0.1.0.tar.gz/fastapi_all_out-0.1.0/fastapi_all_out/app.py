from typing import Literal

from fastapi import FastAPI, APIRouter

from fastapi_all_out.responses import \
    default_exception_handlers, \
    change_openapi_validation_error_schema
from fastapi_all_out.settings import MainDB


class ExFastAPI(FastAPI):
    router: APIRouter

    def __init__(
            self,
            *,
            db_provider: MainDB = None,
            db_config: dict = None,
            **kwargs
    ) -> None:
        kwargs.setdefault('swagger_ui_parameters', {"operationsSorter": "method", "docExpansion": "none"})
        exception_handlers = kwargs.get('exception_handlers', {})
        kwargs['exception_handlers'] = {**default_exception_handlers, **exception_handlers}
        super().__init__(**kwargs)

        if db_config:
            match db_provider:
                case MainDB.tortoise:
                    from fastapi_all_out.contrib.tortoise import conntection
                    db_on_start = conntection.on_start(config=db_config)
                    db_on_shutdown = conntection.on_shutdown
                case None:
                    db_on_start = None
                    db_on_shutdown = None
                case _:
                    raise Exception(f'Unknown {db_provider=}')
            if db_on_start:
                self.router.on_startup.append(db_on_start)
            if db_on_shutdown:
                self.router.on_shutdown.append(db_on_shutdown)

        async def default_on_start():
            try:
                change_openapi_validation_error_schema(self)
            except KeyError:
                pass

        self.router.on_startup.append(default_on_start)
