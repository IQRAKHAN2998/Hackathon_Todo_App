from sqlmodel import SQLModel
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TimestampMixin:
    """Mixin to add timestamp fields to models"""
    created_at: datetime
    updated_at: datetime


class BaseResponse(BaseModel):
    """Base response model"""
    success: bool
    message: Optional[str] = None