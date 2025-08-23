from __future__ import annotations
from starlette.routing import Route, Mount


class API():
    """
    Class which supports endpoint decorators to provide a list of endpoints
    for a particular app
    """
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        mod = cls.__module__
        if mod.startswith("api."):
            id = mod.removeprefix("api.")
        else:
            id = mod
        cls._api_id = id.replace('.', '/')
        cls._endpoints = []
        cls._endpoints = []
        for name, obj in cls.__dict__.items():
            meta = getattr(obj, "_z8_endpoint", None)
            if meta:
                http_method, subpath = meta
                cls._endpoints.append((http_method, subpath, name))

    @classmethod
    def build_mount(cls) -> Mount:
        prefix = f"/api/{getattr(cls, "_api_id")}"
        inst = cls()
        routes = [
            Route(subpath, endpoint=getattr(inst, func_name), methods=[method])
            for (method, subpath, func_name) in getattr(cls, "_endpoints", [])
        ]
        return Mount(prefix, routes=routes)

    @staticmethod
    def endpoint(method: str, path: str):
        def deco(fn):
            setattr(fn, "_z8_endpoint", (method.upper(), path))
            return fn
        return deco
