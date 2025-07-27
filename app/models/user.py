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


