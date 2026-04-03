# ABOUTME: Pydantic schemas for user signup/login and JWT token responses.
# ABOUTME: Validates authentication payloads exchanged with API clients.
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
