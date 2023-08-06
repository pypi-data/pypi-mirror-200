import contextlib
from typing import TypeVar
from fastapi import FastAPI
from .context import ctx
from .config import BaseConfig
from .types import TConfigType

AppType = TypeVar("AppType", bound="FastAPI")


class BaseApp(FastAPI):

    _project_dir: str
    _cfg_class: TConfigType = BaseConfig
    _initialised: bool = False

    def __init__(self, project_dir: str, **kwargs):
        self._project_dir = project_dir
        # changing the lifespan API a little for convenience
        kwargs["lifespan"] = BaseApp._lifespan
        super().__init__(**kwargs)

    @contextlib.asynccontextmanager
    async def _lifespan(self: AppType):
        self.initialise()
        await self.on_startup()
        yield
        await self.on_shutdown()

    def initialise(self: AppType):
        if not self._initialised:
            ctx.setup(self._project_dir, self._cfg_class)
            self._initialised = True

    async def on_startup(self: AppType) -> None:
        pass

    async def on_shutdown(self: AppType) -> None:
        pass
