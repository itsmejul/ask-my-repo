FROM python:3.11-slim

WORKDIR /app   

# Copy and install dependencies
COPY requirements.txt .
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy app code
COPY . .

# Expose port and run Flask
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000
ENV PYTHONUNBUFFERED=1

CMD ["./venv/bin/flask", "--app", "main", "run", "--host=0.0.0.0"]
