FROM python:3.12-slim

WORKDIR /app

# Install dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .

# ENTRYPOINT allows args to be passed through: docker run <image> --name Alice
ENTRYPOINT ["python", "main.py"]
