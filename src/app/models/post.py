from sqlmodel import Field, SQLModel


class Post(SQLModel, table=True):
    id: int = Field(primary_key=True)
    title: str
    content: str
