from pydantic_settings import BaseSettings


class Config(BaseSettings):
    jwt_secret_key: str
    db_url: str


config = Config()  # type: ignore # NOTE: pyright doesn't like that props like jwt_scheme are not being set
