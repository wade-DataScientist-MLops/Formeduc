# Fichier: backend/core/llm_loader.py

import os
import requests
import json
from typing import List
import chromadb
from sentence_transformers import SentenceTransformer
from .conversation_memory import get_conversation_context, add_message

# --- Pour éviter le warning parallelism Huggingface (optionnel) ---
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# --- Configuration Ollama API ---
OLLAMA_API_URL = "http://ollama:11434/api/generate"
MODEL_NAME = "llama3.2:1b"  # Modèle utilisé (plus rapide)

# --- Import des composants ChromaDB depuis chroma_client ---
from .chroma_client import elavira_collection, embedder, query_documents

# --- Fonctions pour indexer et requêter les documents ---
def index_documents(texts: List[str], ids: List[str] = None):
    if not texts:
        return []
    embeddings = embedder.encode(texts).tolist()
    metadatas = [{"source": f"doc_{i}"} for i in range(len(texts))]
    if ids is None:
        current_count = elavira_collection.count()
        ids = [f"doc_{current_count + i}" for i in range(len(texts))]
    elavira_collection.add(documents=texts, embeddings=embeddings, metadatas=metadatas, ids=ids)
    print(f"✅ {len(texts)} documents indexés dans ChromaDB.")
    return ids

# --- Fonction pour générer la réponse avec Ollama via CLI ---
def ollama_generate(prompt: str) -> str:
    print(f"[Ollama API] Envoi du prompt : {prompt[:100]}...")
    try:
        # Utiliser l'API HTTP d'Ollama
        data = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.8,
                "top_p": 0.9,
                "max_tokens": 100,
                "repeat_penalty": 1.1
            }
        }
        
        response = requests.post(OLLAMA_API_URL, json=data, timeout=300)
        response.raise_for_status()
        
        result = response.json()
        generated_text = result.get("response", "").strip()
        
        print(f"[Ollama API] Réponse reçue : {generated_text[:200]}...")
        return generated_text
        
    except requests.exceptions.RequestException as e:
        print(f"[Ollama API] Erreur de connexion : {e}")
        return f"Erreur de connexion Ollama : {e}"
    except Exception as e:
        print(f"[Ollama API] Erreur inattendue : {e}")
        return f"Erreur inattendue : {e}"

# --- Fonction principale pour générer la réponse RAG ---
def rag_generate(query: str, system_persona: str = None, user_id: str = "default", agent_id: str = "elavira") -> str:
    """
    Génère une réponse en combinant le contexte ChromaDB Formeduc et le modèle Ollama.
    Spécialement conçu pour Elavira avec les données de Formeduc.
    """
    # Persona optimisée pour Elavira selon le cahier des charges FormEduc
    if system_persona is None:
        system_persona = """Tu es Elavira, l'assistante virtuelle intelligente de FormEduc, spécialisée dans l'accompagnement des professionnels de la petite enfance et du milieu scolaire.

🎯 MISSION PRINCIPALE :
Accueillir, guider et accompagner les visiteurs du site FormEduc dans leur parcours de formation professionnelle avec une approche personnalisée et bienveillante.

👋 ACCUEIL PERSONNALISÉ :
- Message d'introduction chaleureux et professionnel dès l'arrivée
- Invitation à poser une question ou indiquer leur besoin spécifique
- Ton : Professionnel, chaleureux, bienveillant, motivant
- Langue : Français (prioritaire)

🔍 FONCTIONNALITÉS CLÉS :
1. **Réponses aux FAQ** : Tarifs, durées, certifications, exigences, processus d'inscription
2. **Guidage contextuel** : Accompagnement dans la navigation et recherche de formations
3. **Recommandations personnalisées** : Suggestions basées sur le profil utilisateur
4. **Questions de qualification** : "Travaillez-vous en milieu de garde ?", "Quel est votre profil professionnel ?"
5. **Support processus d'achat** : Inscription, paiement, téléchargement, certifications
6. **Double modalité** : Interaction textuelle et vocale

👥 PROFILS UTILISATEURS :
- Éducateurs en petite enfance
- Responsables de service de garde (RSG/RSGE)
- Parents et familles d'accueil
- Professionnels de la santé
- Animateurs de camp et gardiens futés

📚 FORMATIONS FORMEDUC :
- **Secourisme** : Service de garde, petite enfance, milieu scolaire
- **Formations 45h** : Programme obligatoire pour RSG et RSGE
- **Perfectionnements** : Développement de l'enfant, allergies, maltraitance
- **Familles d'accueil** : Formations hybrides spécialisées
- **Programme jeunesse** : Gardien futé, animateur de camp
- **Formations 100% en ligne** : Accès 24h/24, certifications reconnues

⚖️ RÉGLEMENTATIONS :
Conformes au Règlement sur les services de garde éducatifs et à la Loi sur l'instruction publique (chapitre l-13.3, a. 454.1).

🎯 STYLE DE COMMUNICATION :
- Toujours professionnel, chaleureux, bienveillant et motivant
- Pose des questions de qualification pour personnaliser l'accompagnement
- Réponses claires, concises et contextualisées
- Capacité à rediriger vers les bonnes sections du site
- Support immédiat pendant la navigation"""
    
    # Récupération du contexte de conversation
    conversation_context = get_conversation_context(user_id, agent_id, max_messages=3)
    
    # Récupération des documents les plus pertinents de Formeduc (collection Elavira uniquement)
    context_docs = query_documents(query, n_results=3)
    context = "\n\n".join(context_docs) if context_docs else "Aucun contexte Formeduc disponible."

    # Construction du prompt avec mémoire de conversation
    prompt = f"""
{system_persona}

Contexte de conversation:
{conversation_context}

Données Formeduc:
{context}

Question: {query}

Instructions importantes:
- Si la question n'est pas claire ou contient des fautes de frappe, demande des clarifications
- Reste toujours professionnel et serviable
- Propose des alternatives si tu ne comprends pas

Réponse:
"""
    
    # Vérifier si c'est le premier message ou une conversation continue
    is_first_message = len(conversation_context.split('\n')) <= 2
    
    # Logique de réponse intelligente et précise
    query_lower = query.lower()
    
    # Salutations simples - réponse directe et chaleureuse
    if any(greeting in query_lower for greeting in ["salut", "bonjour", "bonsoir", "coucou", "hello"]):
        if is_first_message:
            response = """Bonjour ! 👋 Je suis Elavira, votre assistante FormEduc !

Je suis là pour vous accompagner dans vos besoins de formation professionnelle. Comment puis-je vous aider aujourd'hui ?

**Je peux vous aider avec :**
• Informations sur nos formations
• Processus d'inscription
• Tarifs et certifications
• Support technique

Que souhaitez-vous savoir ?"""
        else:
            response = "Salut ! 😊 Comment puis-je vous aider aujourd'hui ?"
    
    # Questions spécifiques - utiliser la base de connaissances
    elif context_docs and len(context_docs) > 0:
        # Analyser le contexte pour donner une réponse précise
        if "prix" in query_lower or "tarif" in query_lower or "coût" in query_lower:
            response = f"""💰 **Tarifs FormEduc :**

Basé sur nos informations actuelles, nos formations offrent :
• **Prix compétitifs** - Tarifs abordables pour tous les budgets
• **Meilleur rapport qualité-prix** du marché
• **Formations 100% en ligne** - Économies sur les déplacements

**Pour obtenir un devis précis :**
📞 **418 842-7523**
📧 **info@formeduc.ca**

Quelle formation vous intéresse ? Je peux vous orienter vers la meilleure option !"""
        
        elif "certification" in query_lower or "certificat" in query_lower:
            response = f"""🏆 **Certifications FormEduc :**

Toutes nos formations délivrent des **certifications reconnues** :
• Conformes au **Règlement sur les services de garde éducatifs**
• Conformes à la **Loi sur l'instruction publique** (chapitre l-13.3, a. 454.1)
• **Certifications numériques** - Accessibles en ligne 24h/24
• **Reconnaissance par les employeurs**

Nos certifications valorisent vos compétences professionnelles !"""
        
        elif "formation" in query_lower or "cours" in query_lower:
            response = f"""📚 **Formations FormEduc disponibles :**

{context[:500]}...

**Contactez-nous pour plus d'informations :**
📞 **418 842-7523** | 📧 **info@formeduc.ca**"""
        
        else:
            # Réponse générale basée sur le contexte
            response = f"""Basé sur les informations FormEduc :

{context[:300]}...

**Besoin d'aide ?** 📞 418 842-7523 | 📧 info@formeduc.ca"""
    
    else:
        # Fallback pour questions non reconnues
        response = f"""Bonjour ! Je suis Elavira, votre assistante FormEduc ! 🎓

Je ne trouve pas d'informations spécifiques sur votre question. 

**Comment puis-je vous aider ?**
• Informations sur nos formations
• Processus d'inscription  
• Tarifs et certifications
• Support technique

**Contact direct :** 📞 418 842-7523 | 📧 info@formeduc.ca"""
    
    # Ajouter le message utilisateur et la réponse à la mémoire
    add_message(user_id, agent_id, "user", query)
    add_message(user_id, agent_id, "assistant", response)
    
    return response

# --- Test rapide (optionnel) ---
if __name__ == "__main__":
    try:
        result = subprocess.run([OLLAMA_BIN, "list"], capture_output=True, text=True, check=True)
        print("✅ Ollama accessible depuis Python :\n", result.stdout)
    except Exception as e:
        print("❌ Ollama introuvable depuis Python :", e)

    test_query = "Quels sont les programmes disponibles pour le secondaire ?"
    print(rag_generate(test_query, "Tu es un assistant professionnel spécialisé pour les élèves du secondaire."))
