from datetime import timedelta
import uuid
from fastapi import APIRouter, Body, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db_sesion
from app.core.security import create_access_token, get_password_hash

from app.schemas.auth import RegisterSchema, LoginSchema, ResetPasswordSchema, Token, ForgotPasswordSchema
from app.core.config import settings
from app.crud.auth import get_user_by_email_or_phone, create_user, authenticate, get_user_by_identifier, verify_reset_password_token, verify_user_token, generate_reset_password_token


auth_router = APIRouter()


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_details: RegisterSchema, session: Session = Depends(get_db_sesion)):
    existing_user = get_user_by_email_or_phone(session=session, user_details=user_details)

    if existing_user:
        # Return a generic error message for either email or phone number conflict
        raise HTTPException(status_code=400, detail="Email or phone number already exists.")

    user = create_user(session=session, user_details=user_details)
    return {"message": "User created successfully", "verification_link": f"{settings.APP_URL}/verify?token={user.verification_token}"}


@auth_router.post("/login")
def login(user_details: LoginSchema, session: Session = Depends(get_db_sesion))->Token:
    user = authenticate(session=session, user_details=user_details)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid Credentials")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    elif not user.is_verified:
        raise HTTPException(status_code=400, detail="User not verified")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(access_token=create_access_token(user.id, expires_delta=access_token_expires))


@auth_router.get("/verify")
def verify_user(token: str = Query(...), session: Session = Depends(get_db_sesion)):
    user = verify_user_token(session=session, token=token)
    
    if not user:
        raise HTTPException(status_code=400, detail="Invalid verification token")
    
    return {"message": "User verified successfully"}


@auth_router.post("/forgot-password")
def forgot_password(user_details: ForgotPasswordSchema, session: Session = Depends(get_db_sesion)):
    user = get_user_by_identifier(session=session, identifier=user_details.identifier)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or phone number")
    
    reset_password_token = generate_reset_password_token(session=session, user=user)
    return {"message": "Password reset email sent successfully", "reset_link": f"{settings.FRONTEND_HOST}/reset-password?token={reset_password_token}"}


@auth_router.post("/reset-password")
def reset_password(
    token: str = Query(...),
    session: Session = Depends(get_db_sesion),
    password: ResetPasswordSchema = Body(...)
):
    user = verify_reset_password_token(session=session, token=token)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid reset password token")
    user.hashed_password = get_password_hash(password.password)
    session.commit()
    return {"message": "Password reset successfully"}

