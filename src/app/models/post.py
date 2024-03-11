from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel, text

# TODO: There seems to be a bug related to moving this into the `TYPE_CHECKING` block. Investigate and report
from app.models import CommentRead

if TYPE_CHECKING:
    from app.models import Comment, User


class PostBase(SQLModel):
    title: str
    content: str


class Post(PostBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    author_id: int = Field(foreign_key="user.id")
    created: datetime | None = Field(
        default=None,
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
        },
    )
    deleted: datetime | None = None

    author: "User" = Relationship(back_populates="posts")
    comments: list["Comment"] = Relationship(back_populates="post")


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    id: int
    created: datetime
    deleted: datetime | None = Field(
        default=None,
        description="Time that this record was soft-deleted. Null if not deleted.",
    )


class PostReadWithComments(PostRead):
    comments: list["CommentRead"] = Field()


class PostReadWithCommentsAndAuthor(PostRead):
    author: "User"
