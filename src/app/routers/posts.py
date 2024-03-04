from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.dependencies import get_db_session
from app.models import Post, PostCreate

router = APIRouter()


@router.post("/posts")
def create_post(
    session: Annotated[Session, Depends(get_db_session)], post: PostCreate
) -> Post:
    db_post = Post.model_validate(post)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


@router.get("/posts", response_model=list[Post])
def get_post_list(session: Annotated[Session, Depends(get_db_session)]):
    return session.exec(select(Post)).all()


@router.get("/posts/{post_id}")
def get_single_post(
    session: Annotated[Session, Depends(get_db_session)], post_id: int
) -> Post:
    post = session.exec(select(Post).where(Post.id == post_id)).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    return post
