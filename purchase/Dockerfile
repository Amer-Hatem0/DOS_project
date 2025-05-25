FROM ubuntu:latest


RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /app


COPY .. /app

RUN python3 -m venv /app/venv

ENV PATH="/app/venv/bin:$PATH"
RUN pip install --upgrade pip
 
RUN pip install flask requests


 EXPOSE 5000

CMD ["python3", "purchase.py"]
