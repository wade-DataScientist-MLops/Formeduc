#!/bin/bash

echo "🚀 Test simple de vitesse Ollama"
echo "================================"

echo "🔄 Test du modèle actuel: qwen2:1.5b"
echo "Début du test..."
start_time=$(date +%s.%N)

curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2:1.5b",
    "prompt": "Bonjour, comment allez-vous?",
    "stream": false,
    "options": {
      "temperature": 0.7,
      "max_tokens": 50
    }
  }' > /tmp/ollama_test.json 2>/dev/null

end_time=$(date +%s.%N)
duration=$(echo "$end_time - $start_time" | bc -l)

echo "Temps de réponse: ${duration}s"
echo "Réponse:"
grep -o '"response":"[^"]*"' /tmp/ollama_test.json | head -c 100
echo ""

echo "🔄 Téléchargement du modèle plus rapide: llama3.2:1b"
sudo docker-compose exec ollama ollama pull llama3.2:1b

echo "🔄 Test du modèle plus rapide: llama3.2:1b"
echo "Début du test..."
start_time=$(date +%s.%N)

curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2:1b",
    "prompt": "Bonjour, comment allez-vous?",
    "stream": false,
    "options": {
      "temperature": 0.7,
      "max_tokens": 50
    }
  }' > /tmp/ollama_test2.json 2>/dev/null

end_time=$(date +%s.%N)
duration=$(echo "$end_time - $start_time" | bc -l)

echo "Temps de réponse: ${duration}s"
echo "Réponse:"
grep -o '"response":"[^"]*"' /tmp/ollama_test2.json | head -c 100
echo ""

echo "✅ Test terminé!"
echo "Comparez les temps de réponse pour choisir le meilleur modèle."
