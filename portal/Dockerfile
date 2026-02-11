FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY portal/requirements.txt /app/portal/requirements.txt
RUN pip install --no-cache-dir -r /app/portal/requirements.txt

# Copy logic
COPY portal /app/portal
COPY common /app/common
COPY scheduler /app/scheduler

# Set PYTHONPATH
ENV PYTHONPATH=/app

CMD ["uvicorn", "portal.app:app", "--host", "0.0.0.0", "--port", "8000"]
