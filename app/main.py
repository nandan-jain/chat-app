from fastapi import FastAPI
from .database import get_db, test_db_connection

test_db_connection()
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
