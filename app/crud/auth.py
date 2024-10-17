from typing import Optional
from sqlalchemy.orm import Session
from app.core.security import get_password_hash, verify_password

from app.models.user import User
from app.schemas.auth import RegisterSchema, LoginSchema

from sqlalchemy import or_


def get_user_by_email_or_phone(*, session: Session, user_details: RegisterSchema) -> User | None:
    """
    Retrieve a user either by email or phone number.
    """
    user = session.query(User).filter(
        or_(
            User.email == user_details.email,
            User.phone_number == user_details.phone_number
        )).first()
    return user


def get_user_by_identifier(*, session: Session, identifier: str) -> User | None:
    user = session.query(User).filter(
        or_(
            User.email == identifier,
            User.phone_number == identifier
        )).first()
    return user


def create_user(*, session: Session, user_details: dict) -> User:
    """
    Create a new user in the system with hashed password.
    """
    hashed_password = get_password_hash(user_details.password)
    new_user = User(
        email=user_details.email,
        phone_number=user_details.phone_number,
        hashed_password=hashed_password,
        role="merchant"
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


def authenticate(*, session: Session, user_details: LoginSchema) -> User | None:
    """
    Authenticate a user based on identifier (email or phone number) and password.
    """
    user = get_user_by_identifier(session=session, identifier=user_details.identifier)
    if not user or not verify_password(user_details.password, user.hashed_password):
        return None
    return user


def verify_user_token(session: Session, token: str) -> Optional[User]:
    user = session.query(User).filter(User.verification_token == token).first()
    if user and not user.is_verified:
        user.is_verified = True
        user.verification_token = None
        session.commit()
    return user