# --- Étape 1 : Image de base ---
FROM python:3.10-slim

# --- Étape 2 : Répertoire de travail ---
WORKDIR /app

# --- Étape 3 : Copier le code source ---
COPY . .

# --- Étape 4 : Variables d'environnement ---
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV OLLAMA_URL=http://localhost:11434  # URL de l'API Ollama dans le container

# --- Étape 5 : Installer les dépendances Python ---
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r backend/requirements.txt

# --- Étape 6 : Exposer le port de l'application ---
EXPOSE 8000

# --- Étape 7 : Commande de lancement ---
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
