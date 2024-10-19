from uuid import UUID
from pydantic import BaseModel, field_validator, ValidationError
import re
from app.schemas.validators import validate_password


class UserSchema(BaseModel):
    id: UUID
    email: str
    phone_number: str
    is_active: bool

class RegisterSchema(BaseModel):
    email: str
    phone_number: str
    password: str

    _validate_password = field_validator('password')(validate_password)

    @field_validator('phone_number')
    def validate_phone_number(cls, value):
        # Check if the phone number is in a valid format
        if not re.match(r'^\+?[1-9]\d{1,14}$', value):
            raise ValueError('Phone number must be in a valid international format (e.g., +1234567890)')

        return value


class LoginSchema(BaseModel):
    identifier: str
    password: str


class Token(BaseModel):
    access_token: str


class ForgotPasswordSchema(BaseModel):
    identifier: str


class ResetPasswordSchema(BaseModel):
    password: str

    _validate_password = field_validator('password')(validate_password)
