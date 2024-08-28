from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from httpx import AsyncClient

########################################################################################

from routes import router

########################################################################################


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.async_client = AsyncClient()
    yield
    await app.state.async_client.aclose()


app = FastAPI(lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")
