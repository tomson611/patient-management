from pydantic import BaseModel, EmailStr, Field
from typing import Literal

class CreateUserRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, pattern=r'^[a-zA-Z0-9_-]+$')
    email: EmailStr
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    password: str = Field(..., min_length=8, max_length=128)
    role: Literal['admin', 'user']  

    class Config:
        str_min_length = 1
        str_strip_whitespace = True

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str