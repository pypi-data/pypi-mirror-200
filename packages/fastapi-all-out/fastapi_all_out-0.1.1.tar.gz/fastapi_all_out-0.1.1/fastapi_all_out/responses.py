import json
from typing import Any, Optional

from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.exceptions import HTTPException, RequestValidationError
from starlette.responses import JSONResponse

from fastapi_all_out.pydantic import CamelModel


class DefaultJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        for data_type, encoder in CamelModel.Config.json_encoders.items():
            if isinstance(o, data_type):
                return encoder(o)
        return super().default(o)


_default_encoder = DefaultJSONEncoder(
    ensure_ascii=False,
    allow_nan=False,
    indent=None,
    separators=(",", ":"),
)


class DefaultJSONResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        return _default_encoder.encode(content).encode("utf-8")


class BgHTTPException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[dict[str, Any]] = None,
        background: BackgroundTasks = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.background = background


# HTTPException
async def http_exception_handler(request: Request, exc: HTTPException) -> DefaultJSONResponse:
    headers = getattr(exc, "headers", None)
    if headers:
        return DefaultJSONResponse(exc.detail, status_code=exc.status_code, headers=headers)
    else:
        return DefaultJSONResponse(exc.detail, status_code=exc.status_code)


# BgHTTPException
async def bg_http_exception_handler(request: Request, exc: BgHTTPException) -> DefaultJSONResponse:
    headers = getattr(exc, "headers", None)
    if headers:
        response = DefaultJSONResponse(exc.detail, status_code=exc.status_code, headers=headers)
    else:
        response = DefaultJSONResponse(exc.detail, status_code=exc.status_code)
    response.background = exc.background
    return response


# RequestValidationError
async def validation_error_handler(request: Request, exc: RequestValidationError) -> DefaultJSONResponse:
    messages = {}
    for error in exc.errors():
        loc = error['loc']
        place = messages
        for item in loc[:-1]:
            if not (new_place := place.get(item)):
                new_place = place[
                    item] = {}  # type: ignore # int and str are possible, but linter also see dict
            place = new_place
        place[loc[-1]] = error.get('msg')
    return DefaultJSONResponse(messages, status_code=422)


default_exception_handlers = {
    HTTPException: http_exception_handler,
    BgHTTPException: bg_http_exception_handler,
    RequestValidationError: validation_error_handler,
}


def change_openapi_validation_error_schema(app: FastAPI):
    obj = dict[str, dict[str, dict[str, str] | str] | str]

    class ValidationErr(CamelModel):
        body: Optional[obj]
        query: Optional[obj]
        file: Optional[obj]
        form: Optional[obj]
        path: Optional[obj]

    del app.openapi()['components']['schemas']['ValidationError']
    app.openapi()['components']['schemas']['HTTPValidationError']['properties'] = ValidationErr.schema()['properties']
