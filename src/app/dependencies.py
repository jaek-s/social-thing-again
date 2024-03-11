from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlmodel import Session, col, select

from app import models
from app.auth import decode_access_token
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


def get_active_post_from_param(
    post_id: int, db_session: Annotated[Session, Depends(get_db_session)]
):
    post = db_session.exec(
        select(models.Post)
        .where(models.Post.id == post_id)
        .where(col(models.Post.deleted).is_(None))
    ).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    return post


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db_session: Annotated[Session, Depends(get_db_session)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        decoded_token = decode_access_token(token)
    except JWTError:
        raise credentials_exception from None
    # TODO: catch pydantic.ValidationError too?

    user = db_session.get(models.User, decoded_token.sub)
    if user is None:
        raise credentials_exception

    return user
