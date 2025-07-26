from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel, EmailStr
from typing import Optional

class Base(DeclarativeBase):
    pass

class UserORM(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)

# Pydantic Models for API validation and data handling
class User(BaseModel):
    id: Optional[int] = None
    phone_number: str  
    name: str
    email: EmailStr
    
    class Config:
        from_attributes = True  # For Pydantic v2

class UserCreate(BaseModel):
    phone_number: str  
    name: str
    email: EmailStr

class UserResponse(BaseModel):
    id: int
    phone_number: str
    name: str
    email: str
    
    class Config:
        from_attributes = True
