from starlette.config import Config
from z8ter import BASE_DIR, FAVICON_PATH, VIEWS_DIR


def build_config(env_file: str) -> Config:
    cf = Config(env_file)
    cf.file_values["ROOT"] = str(BASE_DIR)
    cf.file_values["FAVICON_PATH"] = str(FAVICON_PATH)
    cf.file_values["VIEW_PATH"] = str(VIEWS_DIR)
    return cf
