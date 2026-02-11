FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY worker/requirements.txt /app/worker/requirements.txt
RUN pip install --no-cache-dir -r /app/worker/requirements.txt

# Copy logic
COPY worker /app/worker
COPY common /app/common
COPY scheduler /app/scheduler

# Set PYTHONPATH
ENV PYTHONPATH=/app

# Default command starts RQ worker
CMD ["rq", "worker", "-u", "redis://redis:6379/0", "submissions"]
