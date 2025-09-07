import uvicorn
import socket
import logging
import z8ter
from z8ter.logging_utils import uvicorn_log_config
logger = logging.getLogger("z8ter.cli")


def run_server(
        mode: str = "prod",
        host: str = "127.0.0.1",
        port: int = 8080,
        reload: bool | None = None,
) -> None:
    def lan_ip() -> str:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
        finally:
            s.close()
    isProd = mode == "prod"
    isDev = not isProd
    reload = isDev if reload is None else reload
    if mode == "WAN":
        host = "0.0.0.0"
        logger.warning(
            f"🌐 WAN: The host has been set to {host} and reload: {reload}"
        )
    elif mode == "LAN":
        host = lan_ip()
        logger.warning(
            f"🌐 LAN: The host has been set to {host} and reload: {reload}"
        )
    if mode == "prod":
        host = "0.0.0.0"
        reload = False
        logger.warning(
            f"🚀 PROD: The host has been set to {host} and reload: {reload}"
        )
    uvicorn.run(
        "main:app_builder.build",
        factory=True,
        host=host,
        port=port,
        reload=reload,
        app_dir=str(z8ter.BASE_DIR),
        reload_dirs=[str(z8ter.BASE_DIR)],
        log_level="info",
        log_config=uvicorn_log_config(isDev),
    )
