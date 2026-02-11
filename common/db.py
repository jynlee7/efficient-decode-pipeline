from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Enum as SAEnum, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
import enum

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./competition.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class SubmissionStatus(str, enum.Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)

class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True) # Foreign key logic omitted for brevity
    file_path = Column(String)
    status = Column(SAEnum(SubmissionStatus), default=SubmissionStatus.QUEUED)
    result_metrics = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)
