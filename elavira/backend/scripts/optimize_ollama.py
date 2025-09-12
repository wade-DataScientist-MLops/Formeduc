#!/usr/bin/env python3
"""
Script pour optimiser Ollama avec un modèle plus rapide
"""

import requests
import json
import time

def test_model_speed(model_name: str, test_prompt: str = "Bonjour, comment allez-vous?"):
    """Teste la vitesse d'un modèle"""
    print(f"🔄 Test de vitesse pour le modèle: {model_name}")
    
    start_time = time.time()
    
    try:
        url = "http://ollama:11434/api/generate"
        data = {
            "model": model_name,
            "prompt": test_prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "max_tokens": 100
            }
        }
        
        response = requests.post(url, json=data, timeout=60)
        response.raise_for_status()
        
        end_time = time.time()
        duration = end_time - start_time
        
        result = response.json()
        response_text = result.get("response", "").strip()
        
        print(f"✅ Modèle {model_name}:")
        print(f"   Temps de réponse: {duration:.2f} secondes")
        print(f"   Réponse: {response_text[:100]}...")
        print(f"   Longueur: {len(response_text)} caractères")
        
        return duration, response_text
        
    except Exception as e:
        print(f"❌ Erreur avec le modèle {model_name}: {e}")
        return None, None

def main():
    """Fonction principale pour optimiser Ollama"""
    print("🚀 Optimisation d'Ollama pour des réponses plus rapides")
    
    # Modèles à tester (du plus rapide au plus lent)
    models_to_test = [
        "llama3.2:1b",      # Très rapide, léger
        "llama3.2:3b",      # Rapide, bon équilibre
        "qwen2:1.5b",       # Modèle actuel
        "llama3.2:8b"       # Plus lent mais plus intelligent
    ]
    
    test_prompt = "Quelles formations en secourisme proposez-vous?"
    
    print(f"📝 Prompt de test: {test_prompt}")
    print("=" * 60)
    
    results = []
    
    for model in models_to_test:
        print(f"\n🔄 Test du modèle: {model}")
        duration, response = test_model_speed(model, test_prompt)
        
        if duration is not None:
            results.append({
                'model': model,
                'duration': duration,
                'response_length': len(response) if response else 0
            })
    
    print("\n" + "=" * 60)
    print("📊 RÉSULTATS DES TESTS:")
    print("=" * 60)
    
    # Trier par vitesse (plus rapide en premier)
    results.sort(key=lambda x: x['duration'])
    
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['model']}")
        print(f"   ⏱️  Temps: {result['duration']:.2f}s")
        print(f"   📝 Longueur: {result['response_length']} caractères")
        print()
    
    # Recommandation
    if results:
        fastest = results[0]
        print(f"🏆 RECOMMANDATION: {fastest['model']}")
        print(f"   Temps de réponse: {fastest['duration']:.2f} secondes")
        print(f"   C'est le modèle le plus rapide testé!")
        
        # Instructions pour changer de modèle
        print("\n🔧 POUR CHANGER DE MODÈLE:")
        print(f"1. Télécharger le modèle recommandé:")
        print(f"   docker-compose exec ollama ollama pull {fastest['model']}")
        print(f"2. Modifier la configuration dans les fichiers:")
        print(f"   - core/llm_loader.py")
        print(f"   - core/chroma_client.py") 
        print(f"   - core/solenys_logic.py")
        print(f"3. Changer MODEL_NAME vers: {fastest['model']}")
        print(f"4. Redémarrer le backend:")
        print(f"   docker-compose restart backend")

if __name__ == "__main__":
    main()
