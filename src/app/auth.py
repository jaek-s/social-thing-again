from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext
from sqlmodel import SQLModel

from app.config import config

ACCESS_JWT_EXPIRATION_MINUTES = 30
JWT_ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


class DecodedToken(SQLModel):
    sub: str
    exp: datetime


def create_access_token(subject: int | str):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_JWT_EXPIRATION_MINUTES
    )
    claims = DecodedToken(sub=str(subject), exp=expire)
    return jwt.encode(
        claims=claims.model_dump(), key=config.jwt_secret_key, algorithm=JWT_ALGORITHM
    )


def decode_access_token(token: str):
    decoded_token = jwt.decode(
        token, key=config.jwt_secret_key, algorithms=[JWT_ALGORITHM]
    )
    return DecodedToken(**decoded_token)
