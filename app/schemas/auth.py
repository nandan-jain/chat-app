from pydantic import BaseModel


class RegisterSchema(BaseModel):
    email: str
    phone_number: str
    password: str
    role: str = "customer"


class LoginSchema(BaseModel):
    identifier: str
    password: str


class Token(BaseModel):
    access_token: str

