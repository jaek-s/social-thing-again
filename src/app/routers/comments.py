from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select

from app import models
from app.config import config
from app.dependencies import get_current_user, get_db_session, get_post_from_param

router = APIRouter()


@router.post("/posts/{post_id}/comments", response_model=models.CommentRead)
def create_comment(
    comment: models.CommentCreate,
    current_user: Annotated[models.User, Depends(get_current_user)],
    post: Annotated[models.Post, Depends(get_post_from_param)],
    session: Annotated[Session, Depends(get_db_session)],
):
    db_comment = models.Comment.model_validate(
        comment, update={"post_id": post.id, "author_id": current_user.id}
    )
    session.add(db_comment)
    session.commit()
    session.refresh(db_comment)
    return db_comment


@router.get(
    "/posts/{post_id}/comments", response_model=list[models.CommentReadWithAuthor]
)
def get_comment_list(
    post: Annotated[models.Post, Depends(get_post_from_param)],
    session: Annotated[Session, Depends(get_db_session)],
    offset: int = Query(default=0),
    limit: int = Query(default=1, le=config.max_comments_per_page),
):
    return session.exec(
        select(models.Comment)
        .where(models.Comment.post == post)
        .offset(offset)
        .limit(limit)
    ).all()
