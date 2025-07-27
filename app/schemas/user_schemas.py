from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    id: Optional[int] = None
    phone_number: str
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    phone_number: str
    name: str
    email: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    phone_number: str = Field(..., example="+91551234567")
    name: str         = Field(..., example="Alice")
    email: EmailStr   = Field(..., example="alice@example.com")