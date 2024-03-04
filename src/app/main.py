from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select

# ---------------------------------- models ---------------------------------- #


class Post(SQLModel, table=True):
    id: int = Field(primary_key=True)
    title: str
    content: str


# --------------------------------- DB setup --------------------------------- #


sqlite_url = "sqlite:///database.db"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # NOTE: When this file is broken up, all models must be imported before this is run.
    SQLModel.metadata.create_all(engine)
    yield


# --------------------------------- app setup -------------------------------- #


app = FastAPI(
    lifespan=lifespan,
)


# ------------------------------- Dependencies ------------------------------- #


def get_db_session():
    with Session(engine) as session:
        yield session


# ---------------------------------- Routes ---------------------------------- #


@app.post("/posts")
def create_post(session: Annotated[Session, Depends(get_db_session)], post: Post):
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


@app.get("/posts")
def get_post_list(session: Annotated[Session, Depends(get_db_session)]):
    return session.exec(select(Post)).all()
