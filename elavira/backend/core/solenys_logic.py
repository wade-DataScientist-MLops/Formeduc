# Fichier: backend/core/solenys_logic.py

import os
import requests
import json
from datetime import datetime
import uuid
from .conversation_memory import get_conversation_context, add_message

def ask_solenys(question: str, user_id: str = "default") -> dict:
    """
    Fonction principale pour interagir avec Solenys, le professeur québécois.
    Spécialisé dans l'enseignement secondaire selon le programme PFEQ.
    """
    print(f"[Solenys] Question reçue: {question}")
    
    # Récupération du contexte de conversation
    conversation_context = get_conversation_context(user_id, "solenys", max_messages=3)
    
    # Construction du prompt optimisé avec mémoire de conversation
    full_prompt = f"""
Tu es Solenys, professeur québécois spécialisé dans l'enseignement secondaire selon le programme PFEQ du Québec.

Contexte de conversation:
{conversation_context}

Ton rôle est de :
- Accompagner les élèves du secondaire (12-17 ans) dans leur apprentissage
- Enseigner selon le programme PFEQ (Programme de formation de l'école québécoise)
- Adapter ton approche pédagogique au niveau de l'élève
- Encourager et motiver dans l'apprentissage
- Proposer des exercices pratiques et concrets

Instructions pédagogiques :
- Utilise un ton bienveillant, professionnel et motivant
- Adapte ton langage au niveau secondaire
- Propose des exemples concrets et pratiques
- Encourage la participation et la réflexion
- Reste dans le cadre du programme PFEQ
- Sois clair et structuré dans tes explications

Réponse:
"""
    # Détecter les calculs mathématiques simples
    import re
    math_pattern = r'(\d+)\s*[+\-*/]\s*(\d+)|(\d+)\s*(fois|×|x)\s*(\d+)|(\d+)\s*(plus|moins|divisé|divisé par)\s*(\d+)'
    if re.search(math_pattern, question.lower()):
        # Utiliser Ollama pour les calculs mathématiques
        try:
            math_prompt = f"""Tu es Solenys, professeur de mathématiques québécois. 

Question de l'élève: {question}

Réponds de manière pédagogique et encourageante. Explique le calcul étape par étape selon le programme PFEQ.

Exemple de réponse:
"Excellente question ! Calculons ensemble : 2 × 2 = 4

Voici comment procéder :
1. 2 × 2 = (2 + 2) = 4
2. Ou directement : 2 × 2 = 4

En mathématiques, la multiplication est une addition répétée. 2 × 2 signifie '2 répété 2 fois', ce qui donne 4.

As-tu d'autres calculs à faire ensemble ?"

Réponse:"""
            
            response_text = ollama_generate_simple(math_prompt, "Tu es Solenys, professeur de mathématiques québécois spécialisé dans le programme PFEQ.")
        except Exception as e:
            print(f"[Solenys] Erreur calcul: {e}")
            response_text = f"Bonjour ! Je suis Solenys, votre professeur de mathématiques ! 📐\n\nJe vois que vous me demandez : '{question}'\n\nMalheureusement, je rencontre des difficultés techniques pour effectuer ce calcul. Pouvez-vous reformuler votre question ?\n\nJe peux vous aider avec :\n• **Calculs de base** - Addition, soustraction, multiplication, division\n• **Algèbre** - Équations, fonctions\n• **Géométrie** - Formes, angles, aires\n• **Statistiques** - Moyennes, probabilités"
    elif "math" in question.lower() or "mathématiques" in question.lower() or "algèbre" in question.lower() or "en mathematiques" in question.lower():
        response_text = f"Bonjour ! Je suis Solenys, votre professeur de mathématiques ! 📐\n\nJe vois que vous vous intéressez aux mathématiques. Selon le programme PFEQ, je peux vous accompagner dans plusieurs domaines :\n\n• **Algèbre et équations** - Résolution d'équations, fonctions\n• **Géométrie** - Formes, angles, calculs d'aires\n• **Statistiques et probabilités** - Analyse de données\n• **Fonctions** - Représentation graphique et analyse\n• **Calcul différentiel et intégral** - Pour les niveaux avancés\n\nQuel niveau êtes-vous et sur quel aspect aimeriez-vous travailler ? Je peux adapter mes explications à votre niveau !"
    elif "science" in question.lower() or "physique" in question.lower() or "chimie" in question.lower() or "biologie" in question.lower():
        response_text = f"Bonjour ! Je suis Solenys, votre professeur de sciences ! 🔬\n\nExcellent choix ! Les sciences sont fascinantes. Selon le programme PFEQ, je peux vous accompagner dans :\n\n• **Physique** - Mécanique, électricité, ondes, énergie\n• **Chimie** - Réactions chimiques, liaisons, équilibres\n• **Biologie** - Cellules, génétique, évolution, écosystèmes\n\nLes sciences permettent de comprendre le monde qui nous entoure. Quel domaine vous passionne le plus ? Et à quel niveau scolaire êtes-vous ?"
    elif "français" in question.lower() or "littérature" in question.lower() or "grammaire" in question.lower():
        response_text = f"Bonjour ! Je suis Solenys, votre professeur de français ! 📚\n\nLe français est une langue magnifique ! Selon le programme PFEQ, je peux vous aider avec :\n\n• **Grammaire et syntaxe** - Structure de la langue française\n• **Littérature québécoise** - Auteurs et œuvres du Québec\n• **Analyse de textes** - Compréhension et interprétation\n• **Rédaction et composition** - Techniques d'écriture\n• **Communication orale** - Expression et présentation\n\nLa maîtrise du français est essentielle pour réussir. Sur quel aspect aimeriez-vous vous concentrer ?"
    elif "probabilité" in question.lower() or "probabilite" in question.lower() or "probabilités" in question.lower() or "en probabilite" in question.lower() or "en probabilité" in question.lower():
        response_text = f"Excellent ! Les probabilités sont fascinantes ! 🎲\n\nSelon le programme PFEQ, je peux vous accompagner dans :\n\n• **Probabilités simples** - Lancer de dés, pièces de monnaie\n• **Probabilités composées** - Événements indépendants et dépendants\n• **Arbres de probabilités** - Visualisation des résultats possibles\n• **Espérance mathématique** - Valeur attendue d'un événement\n• **Applications pratiques** - Jeux, statistiques, prise de décision\n\nLes probabilités nous aident à comprendre le hasard et à prendre de meilleures décisions ! Quel niveau êtes-vous et quel aspect vous intéresse le plus ?"
    elif "histoire" in question.lower() or "géographie" in question.lower():
        response_text = f"Bonjour ! Je suis Solenys, votre professeur d'histoire et géographie ! 🗺️\n\nL'histoire et la géographie nous aident à comprendre notre monde ! Selon le programme PFEQ :\n\n• **Histoire du Québec** - De la Nouvelle-France à aujourd'hui\n• **Histoire mondiale** - Civilisations et événements marquants\n• **Géographie du Québec** - Territoire, ressources, population\n• **Géographie mondiale** - Pays, cultures, enjeux contemporains\n\nCes matières nous connectent à notre héritage et à notre place dans le monde. Quel aspect vous intéresse ?"
    elif "bonjour" in question.lower() or "salut" in question.lower() or "bonsoir" in question.lower():
        response_text = "Bonjour et bienvenue ! 👋\n\nJe suis Solenys, votre professeur québécois spécialisé dans l'enseignement secondaire selon le programme PFEQ du Québec.\n\nJe suis là pour vous accompagner dans votre apprentissage et vous aider à réussir ! Je peux vous assister en :\n\n• **Mathématiques** - Algèbre, géométrie, statistiques\n• **Sciences** - Physique, chimie, biologie\n• **Français** - Littérature, grammaire, rédaction\n• **Histoire et géographie** - Québec et monde\n\nQuelle matière aimeriez-vous explorer ensemble aujourd'hui ?"
    else:
        response_text = f"Bonjour ! Je suis Solenys, votre professeur québécois ! 🎓\n\nJe vois que vous me demandez : '{question}'\n\nSelon le programme PFEQ, je peux vous accompagner dans plusieurs matières du secondaire :\n\n• **Mathématiques** - Tous niveaux, du calcul de base au calcul avancé\n• **Sciences** - Physique, chimie, biologie avec expériences pratiques\n• **Français** - Littérature québécoise, grammaire, communication\n• **Histoire et géographie** - Du Québec et du monde\n\nJe m'adapte à votre niveau et votre style d'apprentissage. Sur quelle matière aimeriez-vous vous concentrer ?"

    # Ajouter le message utilisateur et la réponse à la mémoire
    add_message(user_id, "solenys", "user", question)
    add_message(user_id, "solenys", "assistant", response_text)

    return {
        "id": f"{datetime.now().isoformat()}_assistant_response_{str(uuid.uuid4())[:8]}",
        "text": response_text,
        "user_id": "Solenys Assistant",
        "timestamp": datetime.now().isoformat()
    }

def ollama_generate_simple(prompt: str, system_persona: str) -> str:
    """Génère une réponse via Ollama sans ChromaDB"""
    print(f"[Solenys] Envoi du prompt : {prompt[:100]}...")
    try:
        url = "http://ollama:11434/api/generate"
        data = {
            "model": "llama3.2:1b",
            "prompt": f"{system_persona}\n\nQuestion: {prompt}\n\nRéponse:",
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 200,
                "repeat_penalty": 1.1
            }
        }
        
        response = requests.post(url, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        generated_text = result.get("response", "").strip()
        
        print(f"[Solenys] Réponse Ollama reçue : {generated_text[:100]}...")
        return generated_text
        
    except requests.exceptions.RequestException as e:
        print(f"[Solenys] Erreur de connexion Ollama : {e}")
        return "Désolé, je ne peux pas répondre pour le moment."
    except Exception as e:
        print(f"[Solenys] Erreur inattendue : {e}")
        return "Désolé, je ne peux pas répondre pour le moment."
