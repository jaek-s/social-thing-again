from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    username: str = Field(unique=True)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field()


class UserRead(UserBase):
    id: int


class UserCreate(UserBase):
    password: str
