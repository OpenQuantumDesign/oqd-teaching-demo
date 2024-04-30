from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/pynq", tags=["PYNQ"])
