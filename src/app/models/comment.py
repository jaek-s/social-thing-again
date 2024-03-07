from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models import Post, User


class CommentBase(SQLModel):
    content: str


class Comment(CommentBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    post_id: int = Field(foreign_key="post.id")
    author_id: int = Field(foreign_key="user.id")

    author: "User" = Relationship(back_populates="comments")
    post: "Post" = Relationship(back_populates="comments")


class CommentCreate(CommentBase):
    pass


class CommentRead(CommentBase):
    id: int
    post_id: int
