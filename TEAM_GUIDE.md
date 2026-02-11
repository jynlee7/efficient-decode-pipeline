# Next Steps & Suggestions for the Team

This document outlines the roadmap for turning this boilerplate into a production-ready competition platform.

## 1. Immediate Next Steps (The "Must Haves")

*   **[ ] Replace Simulation with Reality**: The `worker` currently sleeps for 5 seconds. This needs to be replaced with actual `docker run` calls.
*   **[ ] Database Migration**: SQLite is fine for development, but switch to PostgreSQL for production to handle concurrent writes better.
*   **[ ] Authentication**: Implement GitHub/Google OAuth. We cannot rely on users typing in a username without verification.

## 2. Methodology Suggestions

### 🟢 For the Data Processing Team (Worker & Sandbox)

Your goal is to ensure fair, reproducible, and secure evaluation of code.

1.  **Containerization Strategy**:
    *   **Base Images**: Create a set of "official" base images (e.g., `efficient-decode/torch-2.1:v1`) that participants *must* use. This reduces submission size and ensures compatible drivers.
    *   **Security**: Use `gvisor` or strictly limited capabilities (`--cap-drop ALL`) when running user containers. **Never** run user code as `root`.
    *   **Network**: Disable network access during the benchmark phase (`--network none`) to prevent data leaks.

2.  **Metric Collection (The "Secret Sauce")**:
    *   **Sidecar Pattern**: Instead of asking users to print metrics, run a *sidecar* process that monitors the container using `docker stats` or `nvidia-smi dmon`.
    *   **Memory Bandwidth**: Use `dcgm-exporter` or direct CUPTI calls to measure actual memory throughput, not just allocation.
    *   **Standardized Output**: Enforce a JSON schema for the results.
        ```json
        {
          "metrics": {
            "tokens_per_second": 12.5,
            "peak_memory_bw_GBs": 850.2,
            "latency_p99_ms": 45
          },
          "status": "success"
        }
        ```

3.  **Job Queue Optimization**:
    *   Use **Priority Queues** in Redis. e.g., `high_priority` for quick validation checks, `low_priority` for full training runs that take hours.

### 🔵 For the API/Portal Team (Web & Backend)

Your goal is to creating a frictionless submission experience.

1.  **API-First Design**:
    *   Move away from form-based submissions (`application/x-www-form-urlencoded`) to a proper REST API (`POST /api/v1/submissions`).
    *   This allows the CLI client (`sdk/client.py`) to be a first-class citizen, which engineers prefer over web forms.

2.  **Validation Layer**:
    *   Validate the zip file *before* enqueueing. Check for:
        *   `Dockerfile` existence.
        *   `requirements.txt` presence.
        *   Malicious patterns (e.g., rigid paths).
    *   Rejecting invalid submissions early saves expensive GPU worker time.

3.  **Real-time Feedback**:
    *   Users hate refreshing the page. Implement a **WebSocket** connection for the logs.
    *   Stream the build logs from the worker back to the portal so the user can see if `pip install` fails immediately.

4.  **Admin Dashboard**:
        *   View cluster health (GPU utilization).

## 3. Learning Resources

### 📦 For Data Processing & Sandbox
*   **Docker SDK for Python**: [Documentation](https://docker-py.readthedocs.io/en/stable/) - Learn how to run containers programmatically.
*   **NVIDIA Container Toolkit**: [User Guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/index.html) - Essential for enabling GPU access in containers.
*   **GVisor**: [One-minute Quickstart](https://gvisor.dev/docs/) - Learn about sandboxing to prevent container escapes.
*   **Redis Queue (RQ)**: [Docs](https://python-rq.org/) - Simple job queues for Python.
*   **Prometheus**: [Getting Started](https://prometheus.io/docs/prometheus/latest/getting_started/) - For scraping metrics.

### 🌐 For API & Portal
*   **FastAPI**: [Tutorial - User Guide](https://fastapi.tiangolo.com/tutorial/) - The best way to learn modern Python APIs.
*   **OAuth2 with FastAPI**: [Security Guide](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/) - How to implement login correctly.
*   **WebSockets**: [FastAPI WebSockets](https://fastapi.tiangolo.com/advanced/websockets/) - For streaming logs to the frontend.
*   **PostgreSQL**: [SQLAlchemy with Postgres](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html) - Moving away from SQLite.

### 📚 General Architecture
*   **The Twelve-Factor App**: [12factor.net](https://12factor.net/) - Best practices for building cloud-native apps.
*   **System Design Primer**: [GitHub Repo](https://github.com/donnemartin/system-design-primer) - Great for understanding scalability concepts.
