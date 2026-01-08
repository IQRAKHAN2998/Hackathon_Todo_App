from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid
from models import User  # Import the main User model

class Token(SQLModel):
    """Token response model for JWT authentication"""
    access_token: str
    token_type: str


class TokenData(SQLModel):
    """Token data model for storing user information in JWT"""
    email: Optional[str] = None


class UserCreate(SQLModel):
    """Schema for user creation (signup)"""
    email: str
    password: str


class UserLogin(SQLModel):
    """Schema for user login"""
    email: str
    password: str