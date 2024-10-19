from fastapi import FastAPI, Depends

from app.core.security import get_current_user
from app.models.user import User
from app.schemas.auth import UserSchema

from .core.database import test_db_connection

from app.routers.user import user_router
from app.routers.auth import auth_router

test_db_connection()
app = FastAPI()
app.include_router(user_router)
app.include_router(auth_router, tags=["auth"])


# adding token in the view makes sure that Bearer token needs to be sent in the header if not it will return 401
# called as dependency injection system
@app.get("/", response_model=UserSchema,)
def getme(user: User = Depends(get_current_user)):
    return user


