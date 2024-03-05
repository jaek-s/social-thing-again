from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from app import models
from app.db import engine


def get_db_session():
    with Session(engine) as session:
        yield session


def get_post_from_param(
    post_id: int, db_session: Annotated[Session, Depends(get_db_session)]
):
    post = db_session.get(models.Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return post
