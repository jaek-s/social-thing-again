from sqlmodel import SQLModel, create_engine

# NOTE: This import is necessary for the create_all() function to work
from app import models as models
from app.config import config

connect_args = {"check_same_thread": False}
engine = create_engine(config.db_url, connect_args=connect_args, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)
