 
FROM ubuntu:latest

 
RUN apt-get update && \
    apt-get install -y python3 python3-venv python3-pip && \
    rm -rf /var/lib/apt/lists/*

 
WORKDIR /app

 
COPY requirements.txt .

 
RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install --upgrade pip && \
    /app/venv/bin/pip install --no-cache-dir -r requirements.txt

 
COPY . .

 
ENV PATH="/app/venv/bin:$PATH"

 
CMD ["python3", "front.py"]
