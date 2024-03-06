from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db import init_db
from app.routers import account, comments, posts, token


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    lifespan=lifespan,
)

app.include_router(account.router, tags=["Account"])
app.include_router(comments.router, tags=["Comments"])
app.include_router(posts.router, tags=["Posts"])
app.include_router(token.router, tags=["Authentication"])
