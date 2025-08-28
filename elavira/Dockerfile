# --- Étape 1 : Base Ollama ---
FROM ollama/ollama:latest   # Remplace 'latest' par la version souhaitée si nécessaire

# --- Étape 2 : Créer le répertoire de travail ---
WORKDIR /app

# --- Étape 3 : Copier tout le projet ---
COPY . /app

# --- Étape 4 : Variables d'environnement ---
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV OLLAMA_URL=http://localhost:11434   # URL de l'API Ollama (locale dans le container)

# --- Étape 5 : Installer les dépendances Python ---
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r backend/requirements.txt

# --- Étape 6 : Créer le dossier pour ChromaDB ---
RUN mkdir -p /app/backend/chroma_data

# --- Étape 7 : Exposer le port pour FastAPI ---
EXPOSE 8000

# --- Étape 8 : Commande pour lancer le serveur FastAPI ---
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
