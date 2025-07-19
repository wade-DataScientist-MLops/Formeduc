FROM python:3.10-slim

WORKDIR /app

COPY . .

# 👇 Ajouter le dossier courant au PYTHONPATH
ENV PYTHONPATH=/app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
