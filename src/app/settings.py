from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    jwt_secret: str


settings = Settings()  # type: ignore
