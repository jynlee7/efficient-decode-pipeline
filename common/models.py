from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from enum import Enum

class SubmissionStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_admin: bool = False

    class Config:
        orm_mode = True

class SubmissionBase(BaseModel):
    description: Optional[str] = None

class SubmissionCreate(SubmissionBase):
    pass

class Submission(SubmissionBase):
    id: int
    user_id: int
    status: SubmissionStatus
    result_metrics: Optional[dict] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
