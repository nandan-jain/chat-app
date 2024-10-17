from pydantic import BaseModel, field_validator, ValidationError
import re


class RegisterSchema(BaseModel):
    email: str
    phone_number: str
    password: str

    @field_validator('password')
    def validate_password(cls, value):
        # Check for minimum length
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')

        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', value):
            raise ValueError('Password must contain at least one uppercase letter')

        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', value):
            raise ValueError('Password must contain at least one lowercase letter')

        # Check for at least one digit
        if not re.search(r'[0-9]', value):
            raise ValueError('Password must contain at least one digit')

        # Check for at least one special character
        if not re.search(r'[\W_]', value):
            raise ValueError('Password must contain at least one special character')

        return value

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

