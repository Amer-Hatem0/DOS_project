FROM ubuntu:latest

# Install Python, pip, and the virtual environment module
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && apt-get clean

WORKDIR /app

# Copy your application code and requirements file into the container
COPY . /app

# Create a virtual environment
RUN python3 -m venv /app/venv

# Activate the virtual environment by updating PATH
ENV PATH="/app/venv/bin:$PATH"

# Upgrade pip and install dependencies from requirements.txt inside the virtual environment
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python3", "catalogservice.py"]
