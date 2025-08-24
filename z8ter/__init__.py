__all__ = ["API", "Page"]
__version__ = "0.1.0"
from .api import API
from .page import Page
from starlette.templating import Jinja2Templates
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FAVICON_PATH = BASE_DIR / "static" / "favicon" / "favicon.ico"
TEMPLATES_DIR = BASE_DIR / "templates"
VIEWS_DIR = BASE_DIR / "views"
TS_DIR = BASE_DIR / "src" / "ts"
API_DIR = BASE_DIR / "api"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
