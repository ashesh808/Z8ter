from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException


def register_exception_handlers(app):
    @app.exception_handler(HTTPException)
    async def http_exc(request, exc):
        return JSONResponse(
            {
                "ok": False,
                "error": {"message": exc.detail}
            },
            status_code=exc.status_code
        )

    @app.exception_handler(Exception)
    async def any_exc(request, exc):
        return JSONResponse(
            {
                "ok": False,
                "error": {"message": "Internal server error"}
            },
            status_code=500
        )
