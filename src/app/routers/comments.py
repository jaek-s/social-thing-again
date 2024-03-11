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


@router.post("/posts/{post_id}/comments", response_model=models.CommentRead)
def create_comment(
    comment: models.CommentCreate,
    current_user: Annotated[models.User, Depends(get_current_user)],
    post: Annotated[models.Post, Depends(get_active_post_from_param)],
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
    post: Annotated[models.Post, Depends(get_active_post_from_param)],
    session: Annotated[Session, Depends(get_db_session)],
    offset: int = Query(default=0),
    limit: int = Query(default=1, le=config.max_comments_per_page),
):
    return session.exec(
        select(models.Comment)
        .where(models.Comment.post == post)
        .where(col(models.Comment.deleted).is_(None))
        .order_by(col(models.Comment.created).desc())
        .offset(offset)
        .limit(limit)
    ).all()


@router.delete(
    "/posts/{post_id}/comments/{comment_id}",
    dependencies=[Depends(get_current_user)],
)
def delete_comment(
    user: Annotated[models.User, Depends(get_current_user)],
    comment_id: int,
    session: Annotated[Session, Depends(get_db_session)],
):
    comment = session.exec(
        select(models.Comment)
        .where(models.Comment.id == comment_id)
        .where(models.Comment.author_id == user.id)
        .where(col(models.Comment.deleted).is_(None))
    ).first()

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )

    comment.deleted = datetime.now(timezone.utc)
    session.add(comment)
    session.commit()
