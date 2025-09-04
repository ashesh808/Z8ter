from z8ter.core import Z8ter
from z8ter.config import build_config
from z8ter.errors import register_exception_handlers
from z8ter.db import init_db

init_db()
config = build_config(".env")


def create_app() -> Z8ter:
    app = Z8ter(
        debug=False,
        mode=config('Z8_MODE')
        )
    register_exception_handlers(app)
    return app


if __name__ == "__main__":
    app = create_app()
