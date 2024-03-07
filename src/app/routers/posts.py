from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select

from app import models
from app.config import config
from app.dependencies import get_current_user, get_db_session, get_post_from_param

router = APIRouter()


@router.post("/posts", response_model=models.PostRead)
def create_post(
    post: models.PostCreate,
    current_user: Annotated[models.User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_db_session)],
):
    db_post = models.Post.model_validate(post, update={"author_id": current_user.id})
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


@router.get("/posts", response_model=list[models.PostRead])
def get_post_list(
    session: Annotated[Session, Depends(get_db_session)],
    offset: int = Query(default=0),
    limit: int = Query(default=1, le=config.max_posts_per_page),
):
    return session.exec(select(models.Post).offset(offset).limit(limit)).all()


@router.get("/posts/{post_id}", response_model=models.PostReadWithComments)
def get_single_post(
    post: Annotated[models.Post, Depends(get_post_from_param)],
    session: Annotated[Session, Depends(get_db_session)],
):
    comments = session.exec(
        select(models.Comment)
        .where(models.Comment.post_id == post.id)
        .limit(config.max_comments_per_page)
    ).all()

    response_post = models.PostReadWithComments.model_validate(
        post, update={"comments": comments}
    )
    return response_post
