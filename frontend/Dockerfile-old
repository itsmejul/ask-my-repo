FROM python:3.11-slim

WORKDIR /app

COPY index.html .
EXPOSE 8010
CMD ["python", "-m", "http.server", "8010"]  
# 8010 ist der port im container