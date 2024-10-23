# Base image: Ubuntu
FROM ubuntu:22.04

# Set environment variables to avoid prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update and install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    curl \
    wget \
    git \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    python3-venv \
    ca-certificates \
    redis-server \
    rabbitmq-server \
    lsb-release \
    software-properties-common \
    sudo

# Install Foundry (for Solidity development)
RUN curl -L https://foundry.paradigm.xyz | bash && \
    ~/.foundry/bin/foundryup

# Install Solidity static analysis tools: Slither and Semgrep
RUN pip3 install --upgrade pip && \
    pip3 install slither-analyzer semgrep

# Install FastAPI and other Python dependencies
RUN pip3 install fastapi uvicorn

# Expose necessary ports (e.g., for FastAPI, Redis, RabbitMQ)
EXPOSE 8000 6379 5672

# Start Redis and RabbitMQ services
RUN service redis-server start && \
    service rabbitmq-server start

# Set up working directory


# Copy the FastAPI app and other files to the container
COPY . /app
WORKDIR /app/src

RUN pip3 install -r /app/requirements.txt

# Command to run FastAPI (adjust if necessary)
CMD ["tail", "-f", "/dev/null"]
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
