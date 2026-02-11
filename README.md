# Efficient-Decode Competition Platform

A boilerplate platform for hosting the "Efficient-Decode Competition", managing submissions, and evaluating memory bandwidth efficiency.

## Architecture

*   **Portal (FastAPI)**: Web interface for submissions and leaderboards.
*   **Worker (Python/RQ)**: Processes submissions, runs containers, and evaluates performance.
*   **Scheduler (Redis)**: Manages the job queue.
*   **Database (SQLite)**: Stores user and submission data.

## Getting Started

1.  **Prerequisites**:
    *   Docker & Docker Compose
    *   Python 3.9+

2.  **Run with Docker Compose**:
    ```bash
    docker-compose up --build
    ```

3.  **Access the Portal**:
    *   Open [http://localhost:8000](http://localhost:8000)
    *   Enter a username to "login/signup".
    *   Upload a `.zip` file containing your code.

4.  **Worker Logs**:
    *   Watch the `worker` service logs to see it pick up the job.
    *   It will simulate processing (5s delay) and generate dummy metrics.

## Development

*   **Portal**: `portal/`
*   **Worker**: `worker/`
*   **Shared Models**: `common/`

## Extension for Production

*   **Databases**: Switch `sqlite` to `Postgres` in `docker-compose.yml`.
*   **Worker**: Implement actual `docker run` logic in `worker/executor.py`.
*   **Security**: Implement OAuth2 in `portal/app.py`.