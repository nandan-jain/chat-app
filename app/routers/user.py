from typing import List, Optional
from fastapi import APIRouter, Depends, status, HTTPException, Query
from app.core.database import get_db_sesion
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserSchema, UserCreateSchema

user_router = APIRouter()


@user_router.get("/users", response_model=List[UserSchema])
def list_users(
    username: Optional[str] = Query(None),
    session: Session = Depends(get_db_sesion)
):
    if username:
        # If username is provided, filter by username
        users = session.query(User).filter(User.username.ilike(f"%{username}%")).all()
    else:
        # If no username is provided, return all users
        users = session.query(User).all()
    
    return users


@user_router.post("/user", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreateSchema, session: Session = Depends(get_db_sesion)):
    user_obj = User(username=user.username)

    session.add(user_obj)
    session.commit()
    session.refresh(user_obj)

    return user_obj


@user_router.get("/user/{id}", response_model=UserSchema)
def retrieve_users(id: int, session: Session = Depends(get_db_sesion)):
    user_obj = session.query(User).get(id)  # Get given id

    # Check if id exists. If not, return 404 not found response
    if not user_obj:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")

    return user_obj


@user_router.put("/user/{id}", response_model=UserSchema)
def update_user(id: int, username: str, session: Session = Depends(get_db_sesion)):
    user_obj = session.query(User).get(id)  # Get given id

    if user_obj:
        user_obj.username = username
        session.commit()

    # Check if id exists. If not, return 404 not found response
    if not user_obj:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")

    return user_obj


@user_router.delete("/user/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, session: Session = Depends(get_db_sesion)):
    # Get given id
    user_obj = session.query(User).get(id)

    # If user with given id exists, delete it from the database. Otherwise, raise 404 error
    if user_obj:
        session.delete(user_obj)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")

    return None


