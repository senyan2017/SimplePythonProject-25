# Match the local interpreter (3.12) so behaviour is identical in and out of Docker.
FROM python:3.12-slim

# Deterministic, UTF-8 output regardless of the host locale.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONIOENCODING=UTF-8

WORKDIR /app

# Install runtime dependencies first for better layer caching. The app is
# stdlib-only today, so this stays a no-op while keeping the contract explicit.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the application code (tests/dev tooling stay out of the image).
COPY main.py .

# Same invocation as running locally (`python main.py`). Arguments passed to
# `docker run <image> --name World` are forwarded straight through to main.py,
# so the container accepts the exact same flags as the local command.
ENTRYPOINT ["python", "main.py"]
