from datetime import datetime
from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    username: str
    is_active: bool
    created_at: datetime

class UserCreateSchema(BaseModel):
    username: str
