from z8ter.responses import JSONResponse
from starlette.exceptions import HTTPException


def register_exception_handlers(app):
    target = getattr(app, "app", app)

    async def http_exc(request, exc: HTTPException):
        return JSONResponse(
            {
                "ok": False,
                "error": {"message": exc.detail}
            },
            status_code=exc.status_code)

    async def any_exc(request, exc: Exception):
        return JSONResponse(
            {
                "ok": False,
                "error": {"message": "Internal server error"}
            },
            status_code=500)

    target.add_exception_handler(HTTPException, http_exc)
    target.add_exception_handler(Exception, any_exc)
