from functools import wraps
from z8ter.responses import RedirectResponse
from z8ter.requests import Request


def login_required(handler):
    @wraps(handler)
    async def wrapper(self, request: Request, *args, **kwargs):
        config = request.app.state.services["config"]
        login_path = config('LOGIN_PATH')
        user = getattr(request.state, "user", None)
        if not user:
            next_url = request.url.path
            if request.url.query:
                next_url = f"{next_url}?{request.url.query}"
            return RedirectResponse(
                f"{login_path}?next={request.url.path}",
                status_code=303
            )
        return await handler(self, request, *args, **kwargs)
    return wrapper


def skip_if_authenticated(handler):
    @wraps(handler)
    async def wrapper(self, request: Request, *args, **kwargs):
        config = request.app.state.services["config"]
        app_path = config('APP_PATH')
        user = getattr(request.state, "user", None)
        if user:
            return RedirectResponse(f"{app_path}", status_code=303)
        return await handler(self, request, *args, **kwargs)
    return wrapper
