from fastapi import FastAPI
from .core.database import test_db_connection

from app.routers.user import user_router
from app.routers.auth import auth_router

test_db_connection()
app = FastAPI()
app.include_router(user_router)
app.include_router(auth_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


