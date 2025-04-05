# Use the official Ubuntu base image
FROM ubuntu:latest

# Install necessary packages including python3-venv
RUN apt-get update && \
    apt-get install -y python3 python3-venv python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file first (to leverage Docker caching)
COPY requirements.txt .

# Create a virtual environment and update PATH so pip and python use the venv
RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install --upgrade pip && \
    /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Set environment variable to use the virtual environment
ENV PATH="/app/venv/bin:$PATH"

# Specify the command to run your application (adjust as needed)
CMD ["python3", "front.py"]
