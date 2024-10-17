from datetime import timedelta
from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db_sesion
from app.core.security import create_access_token

from app.schemas.auth import RegisterSchema, LoginSchema, Token
from app.core.config import settings
from app.crud.auth import get_user_by_email_or_phone, create_user, authenticate

from sqlalchemy import or_

auth_router = APIRouter()

@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_details: RegisterSchema, session: Session = Depends(get_db_sesion)):
    existing_user = get_user_by_email_or_phone(session=session, user_details=user_details)

    if existing_user:
        # Return a generic error message for either email or phone number conflict
        raise HTTPException(status_code=400, detail="Email or phone number already exists.")

    user = create_user(session=session, user_details=user_details)
    return {"message": "User created successfully"}


@auth_router.post("/login")
def login(user_details: LoginSchema, session: Session = Depends(get_db_sesion))->Token:
    user = authenticate(session=session, user_details=user_details)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid Credentials")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(access_token=create_access_token(user.id, expires_delta=access_token_expires))

