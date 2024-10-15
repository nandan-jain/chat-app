from fastapi import FastAPI
from .core.database import test_db_connection

from app.routers.user import user_router

test_db_connection()
app = FastAPI()
app.include_router(user_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


