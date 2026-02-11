from fastapi import FastAPI, Request, Form, File, UploadFile, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pathlib import Path
import shutil
import os
import uuid

# Import common modules
# Note: In docker, we mount common into /app/common, so this works.
# Locally we need to make sure python path is set correctly or install common as package.
try:
    from common.db import SessionLocal, engine, Base, Submission, User
    from common.models import SubmissionStatus
    from scheduler.queue import enqueue_submission
except ImportError:
    # Fallback for local dev without proper path setup, though docker-compose handles this
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from common.db import SessionLocal, engine, Base, Submission, User
    from common.models import SubmissionStatus
    from scheduler.queue import enqueue_submission

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Mount static/templates
app.mount("/static", StaticFiles(directory="portal/static"), name="static")
templates = Jinja2Templates(directory="portal/templates")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root(request: Request, db: Session = Depends(get_db)):
    submissions = db.query(Submission).order_by(Submission.created_at.desc()).all()
    return templates.TemplateResponse("index.html", {"request": request, "submissions": submissions})

@app.post("/submit")
async def submit_job(
    request: Request,
    username: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 1. Create User if not exists (Simplified for boilerplate)
    user = db.query(User).filter(User.username == username).first()
    if not user:
        user = User(username=username)
        db.add(user)
        db.commit()
        db.refresh(user)

    # 2. Save File
    upload_dir = Path("data/uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    file_id = str(uuid.uuid4())
    file_extension = Path(file.filename).suffix
    file_path = upload_dir / f"{file_id}{file_extension}"
    
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 3. Create Submission Record
    submission = Submission(
        user_id=user.id,
        file_path=str(file_path),
        status=SubmissionStatus.QUEUED
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)

    # 4. Enqueue Job
    enqueue_submission(submission.id)

    # Redirect home
    submissions = db.query(Submission).order_by(Submission.created_at.desc()).all()
    return templates.TemplateResponse("index.html", {"request": request, "submissions": submissions})
