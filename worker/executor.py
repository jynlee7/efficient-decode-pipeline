import time
import os
import json
import logging
import zipfile
from pathlib import Path

# Common imports (assuming /app is in PYTHONPATH)
try:
    from common.db import SessionLocal, Submission, SubmissionStatus, engine, Base
except ImportError:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from common.db import SessionLocal, Submission, SubmissionStatus, engine, Base

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure tables exist (worker might start before portal)
Base.metadata.create_all(bind=engine)

def process_submission(submission_id: int):
    """
    Main worker function called by RQ.
    """
    logger.info(f"Starting processing for submission {submission_id}")
    db = SessionLocal()
    submission = db.query(Submission).filter(Submission.id == submission_id).first()

    if not submission:
        logger.error(f"Submission {submission_id} not found!")
        return

    try:
        # Update status to PROCESSING
        submission.status = SubmissionStatus.PROCESSING
        db.commit()

        # Simulate work:
        # 1. Provide Sandbox (Docker)
        # 2. Run Training/Inference
        # 3. Collect Metrics
        
        # Real implementation would be:
        # run_docker_container(submission.file_path)
        
        logger.info(f"Simulating execution for submission {submission_id}...")
        time.sleep(5) # Simulate 5s job

        # Dummy result
        result = {
            "accuracy": 0.85,
            "memory_bandwidth_utilization": "78%",
            "latency_ms": 120
        }

        # Update status to COMPLETED
        submission.status = SubmissionStatus.COMPLETED
        submission.result_metrics = result
        db.commit()
        logger.info(f"Finished processing submission {submission_id}")

    except Exception as e:
        logger.error(f"Error processing submission {submission_id}: {e}")
        submission.status = SubmissionStatus.FAILED
        db.commit()
    finally:
        db.close()
