from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app import models
from app.dependencies import get_db_session, get_post_from_param

router = APIRouter()


@router.post("/posts/{post_id}/comments", response_model=models.CommentRead)
def create_comment(
    comment: models.CommentCreate,
    post: Annotated[models.Post, Depends(get_post_from_param)],
    session: Annotated[Session, Depends(get_db_session)],
):
    db_comment = models.Comment.model_validate({ **comment.model_dump(), "post_id": post.id})
    session.add(db_comment)
    session.commit()
    session.refresh(db_comment)
    return db_comment


@router.get("/posts/{post_id}/comments", response_model=list[models.CommentRead])
def get_comment_list(
    post: Annotated[models.Post, Depends(get_post_from_param)],
    session: Annotated[Session, Depends(get_db_session)],
):
    return session.exec(select(models.Comment).where(models.Comment.post == post)).all()
