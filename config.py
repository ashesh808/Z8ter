from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()
Z8_MODE = os.getenv("Z8_MODE")
ROOT = Path(__file__).resolve().parent
FAVICON_PATH = ROOT / "static" / "favicon" / "favicon.ico"
VIEW_PATH = ROOT / "views"
