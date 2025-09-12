#!/bin/bash

echo "🚀 Test de vitesse des modèles Ollama"
echo "======================================"

# Test du modèle actuel
echo "🔄 Test du modèle actuel: qwen2:1.5b"
time curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2:1.5b",
    "prompt": "Quelles formations en secourisme proposez-vous?",
    "stream": false,
    "options": {
      "temperature": 0.7,
      "max_tokens": 100
    }
  }' 2>/dev/null | jq -r '.response' | head -c 200

echo -e "\n\n🔄 Test avec un modèle plus rapide: llama3.2:1b"
echo "Téléchargement du modèle llama3.2:1b..."
docker-compose exec ollama ollama pull llama3.2:1b

echo "Test de vitesse..."
time curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2:1b",
    "prompt": "Quelles formations en secourisme proposez-vous?",
    "stream": false,
    "options": {
      "temperature": 0.7,
      "max_tokens": 100
    }
  }' 2>/dev/null | jq -r '.response' | head -c 200

echo -e "\n\n✅ Test terminé!"
echo "Si llama3.2:1b est plus rapide, vous pouvez l'utiliser en modifiant MODEL_NAME dans les fichiers de configuration."
