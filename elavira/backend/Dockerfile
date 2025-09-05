FROM python:3.10-slim

WORKDIR /app

# The COPY command is still useful for the build process, even with volumes
COPY . .

ENV PYTHONPATH=/app

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]