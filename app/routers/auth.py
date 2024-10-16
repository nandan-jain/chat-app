# add routes for register, login, logout, reset password, change password, forgot password
from datetime import timedelta
from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db_sesion
from app.core.security import get_password_hash, verify_password, create_access_token

from app.models.user import User
from app.schemas.auth import RegisterSchema, LoginSchema, Token
from app.core.config import settings

from sqlalchemy import or_

auth_router = APIRouter()

@auth_router.post("/register", status_code=status.HTTP_201_CREATED, tags=["Auth"])
def register(user_details: RegisterSchema, session: Session = Depends(get_db_sesion)):
    existing_user = session.query(User).filter(
        or_(
            User.email == user_details.email,
            User.phone_number == user_details.phone_number
        )).first()

    if existing_user:
        # Return a generic error message for either email or phone number conflict
        raise HTTPException(status_code=400, detail="Email or phone number already exists.")

    db_obj = User(
        email = user_details.email,
        phone_number = user_details.phone_number,
        hashed_password = get_password_hash(user_details.password),
        role = "customer"
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return {"message": "User created successfully"}


@auth_router.post("/login", tags=["Auth"])
def login(user_details: LoginSchema, session: Session = Depends(get_db_sesion))->Token:
    user = session.query(User).filter(
        or_(
            User.email == user_details.identifier,
            User.phone_number == user_details.identifier
        )).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not verify_password(user_details.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(access_token=create_access_token(user.id, expires_delta=access_token_expires))

