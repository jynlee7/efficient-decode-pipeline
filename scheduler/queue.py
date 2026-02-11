import os
from redis import Redis
from rq import Queue

REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

redis_conn = Redis.from_url(REDIS_URL)
submission_queue = Queue('submissions', connection=redis_conn)

def enqueue_submission(submission_id: int):
    """Enqueues a submission ID for processing."""
    submission_queue.enqueue('worker.executor.process_submission', submission_id)
