from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models import Comment, Post


class UserBase(SQLModel):
    username: str = Field(unique=True, index=True)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field()

    posts: list["Post"] = Relationship(back_populates="author")
    comments: list["Comment"] = Relationship(back_populates="author")


class UserRead(UserBase):
    id: int


class UserCreate(UserBase):
    password: str
