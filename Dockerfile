FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (leverage Docker layer cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY greeter/ greeter/
COPY main.py .

# ENTRYPOINT keeps the binary fixed; CMD provides default args that
# users can override at `docker run` time.
ENTRYPOINT ["python", "main.py"]
CMD []
