from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, col, select

from app import models
from app.config import config
from app.dependencies import (
    get_active_post_from_param,
    get_current_user,
    get_db_session,
)

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
    limit: int = Query(default=config.max_posts_per_page, le=config.max_posts_per_page),
):
    return session.exec(
        select(models.Post)
        .where(col(models.Post.deleted).is_(None))
        .order_by(col(models.Post.created).desc())
        .offset(offset)
        .limit(limit)
    ).all()


@router.get("/posts/{post_id}", response_model=models.PostReadWithComments)
def get_single_post(
    post: Annotated[models.Post, Depends(get_active_post_from_param)],
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


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post: Annotated[models.Post, Depends(get_active_post_from_param)],
    current_user: Annotated[models.User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_db_session)],
):
    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot delete posts you did not create.",
        )

    post.deleted = datetime.now(timezone.utc)
    session.add(post)
    session.commit()
