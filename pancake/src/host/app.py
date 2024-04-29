from fastapi import FastAPI

from pynq.overlays.logictools import LogicToolsOverlay

from contextlib import asynccontextmanager

########################################################################################

from routes import router

########################################################################################


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.overlay = LogicToolsOverlay("logictools.bit")
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router, prefix="/api/pynq", tags=["PYNQ"])
