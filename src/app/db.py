from sqlmodel import SQLModel, create_engine

# NOTE: This import is necessary for the create_all() function to work
from app import models  # noqa: F401

sqlite_url = "sqlite:///database.db"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def init_db():
    SQLModel.metadata.create_all(engine)
