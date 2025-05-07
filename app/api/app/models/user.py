from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from enum import Enum


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True
    role: UserRole = UserRole.USER
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str

    @validator("password")
    def password_min_length(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v


class UserInDB(UserBase):
    id: str
    hashed_password: str


class User(UserBase):
    id: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None
