from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

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

    author: "User" = Relationship(back_populates="posts")
    comments: list["Comment"] = Relationship(back_populates="post")


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    id: int


class PostReadWithComments(PostRead):
    comments: list["CommentRead"] = Field()


class PostReadWithCommentsAndAuthor(PostRead):
    author: "User"
