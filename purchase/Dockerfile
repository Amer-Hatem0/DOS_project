FROM ubuntu:latest

# Install Python, pip, and the venv module
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy your application files into the container
COPY .. /app

# Create a virtual environment
RUN python3 -m venv /app/venv

# Activate the virtual environment by updating the PATH and upgrade pip
ENV PATH="/app/venv/bin:$PATH"
RUN pip install --upgrade pip

# Install your Python dependencies inside the virtual environment
RUN pip install flask requests

 EXPOSE 5000


CMD ["python3", "purchase.py"]
