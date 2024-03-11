from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel, text

# TODO: There seems to be a bug related to moving this into the `TYPE_CHECKING` block. Investigate and report
# ALSO: I'm not able to remove the `.user` from the import, and UserRead is the last thing in __init__.py
from app.models.user import UserRead

if TYPE_CHECKING:
    from app.models import Post, User


class CommentBase(SQLModel):
    content: str


class Comment(CommentBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    post_id: int = Field(foreign_key="post.id")
    author_id: int = Field(foreign_key="user.id")
    created: datetime | None = Field(
        default=None,
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
        },
    )
    deleted: datetime | None = None

    author: "User" = Relationship(back_populates="comments")
    post: "Post" = Relationship(back_populates="comments")


class CommentCreate(CommentBase):
    pass


class CommentRead(CommentBase):
    id: int
    post_id: int


class CommentReadWithAuthor(CommentRead):
    author: UserRead
