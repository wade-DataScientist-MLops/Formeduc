FROM python:3.10-slim

# Installer dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copier requirements et installer d'abord pour profiter du cache Docker
COPY requirements.txt .

# Installer pip et dépendances
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copier le reste du code
COPY . .

# Variable d'environnement
ENV PYTHONPATH=/app

# Exposer le port
EXPOSE 8000

# Commande de démarrage
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
