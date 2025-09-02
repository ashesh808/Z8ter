from __future__ import annotations
from typing import Any, Callable, ClassVar, List, Tuple, Type
from starlette.routing import Route, Mount


class API:
    """
    Class which supports endpoint decorators to provide a list of endpoints
    for a particular app
    """

    _api_id: ClassVar[str]
    _endpoints: ClassVar[List[Tuple[str, str, str]]]

    def __init_subclass__(cls: Type[API], **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        mod: str = cls.__module__
        if mod.startswith("api."):
            id = mod.removeprefix("api.")
        else:
            id = mod
        cls._api_id = id.replace(".", "/")
        cls._endpoints = []
        for name, obj in cls.__dict__.items():
            meta: Tuple[str, str] | None = getattr(obj, "_z8_endpoint", None)
            if meta:
                http_method, subpath = meta
                cls._endpoints.append((http_method, subpath, name))

    @classmethod
    def build_mount(cls: Type[API]) -> Mount:
        prefix: str = f"{getattr(cls, '_api_id')}".removeprefix('endpoints')
        inst: API = cls()
        routes: List[Route] = [
            Route(subpath, endpoint=getattr(inst, func_name), methods=[method])
            for (method, subpath, func_name) in getattr(cls, "_endpoints", [])
        ]
        return Mount(prefix, routes=routes)

    @staticmethod
    def endpoint(
            method: str, path: str
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
            setattr(fn, "_z8_endpoint", (method.upper(), path))
            return fn
        return deco
