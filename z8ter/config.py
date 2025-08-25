from __future__ import annotations
from starlette.config import Config
from z8ter import BASE_DIR


def build_config(env_file: str) -> Config:
    cf: Config = Config(env_file)
    cf.file_values["BASE_DIR"] = str(BASE_DIR)
    return cf
