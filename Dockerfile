FROM python:3.8-slim

WORKDIR /app

# Install dependencies first so this layer stays cached unless requirements change.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source.
COPY . .

# The entry point forwards container arguments to the CLI, so the image can be
# run with flags and/or environment variables, e.g.:
#   docker run --rm greeter
#   docker run --rm greeter --name Bob --language ko --scene morning
#   docker run --rm -e GREETER_NAME=Bob greeter
ENTRYPOINT [ "python", "main.py" ]
