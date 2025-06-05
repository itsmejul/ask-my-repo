FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
# Install system dependencies
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*
    
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .



ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5020

ENV PATH="/app/venv/bin:$PATH" 
# Because we create the venv already inside path
# Set path to inside venv folder, otherwise we have to call like ./venv/bin/flask run
ENV PYTHONUNBUFFERED=1

CMD ["flask", "--app", "main", "run", "--host=0.0.0.0"]