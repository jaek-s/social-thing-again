from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, SQLModel, select

from app import models
from app.auth import create_access_token, verify_password
from app.dependencies import get_db_session

router = APIRouter()


class TokenResponse(SQLModel):
    access_token: str | int
    token_type: str = "bearer"


@router.post("/token", response_model=TokenResponse)
def get_auth_jwt(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[Session, Depends(get_db_session)],
):
    db_user = session.exec(
        select(models.User).where(models.User.username == form_data.username)
    ).first()

    if (
        not db_user
        or not db_user.id
        or not verify_password(form_data.password, db_user.hashed_password)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    return TokenResponse(access_token=create_access_token(db_user.id))
