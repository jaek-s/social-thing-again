from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app import models
from app.auth import hash_password
from app.dependencies import get_current_user, get_db_session

router = APIRouter()


@router.post("/account", response_model=models.UserRead)
def create_account(
    user: models.UserCreate, session: Annotated[Session, Depends(get_db_session)]
):
    db_user = models.User.model_validate(
        user, update={"hashed_password": hash_password(user.password)}
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/account", response_model=models.UserRead)
def get_account(current_user: Annotated[models.User, Depends(get_current_user)]):
    return current_user
