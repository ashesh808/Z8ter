from typing import cast
from starlette.types import HTTPExceptionHandler, ExceptionHandler
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from z8ter.core import Z8ter
from z8ter.responses import JSONResponse
from z8ter.requests import Request


async def http_exc(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        {"ok": False, "error": {"message": exc.detail}},
        status_code=exc.status_code,
    )


async def any_exc(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        {"ok": False, "error": {"message": "Internal server error"}},
        status_code=500,
    )


def register_exception_handlers(app: Z8ter) -> None:
    target = cast(Starlette, getattr(app, "starlette_app", app))
    target.add_exception_handler(
        HTTPException, cast(HTTPExceptionHandler, http_exc)
    )
    target.add_exception_handler(Exception, cast(ExceptionHandler, any_exc))
