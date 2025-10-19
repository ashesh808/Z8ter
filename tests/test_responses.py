from __future__ import annotations

from starlette.responses import (
    JSONResponse as StarletteJSONResponse,
)
from starlette.responses import (
    RedirectResponse as StarletteRedirectResponse,
)
from starlette.responses import (
    Response as StarletteResponse,
)

from z8ter.responses import JSONResponse, RedirectResponse, Response


def test_responses_reexport_starlette_classes() -> None:
    assert Response is StarletteResponse
    assert JSONResponse is StarletteJSONResponse
    assert RedirectResponse is StarletteRedirectResponse
