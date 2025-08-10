from starlette.templating import Jinja2Templates
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
VIEWS_DIR = BASE_DIR / "views"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
