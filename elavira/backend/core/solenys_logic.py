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
    
    # Recherche dans les documents PFEQ pour les questions éducatives (collection Solenys uniquement)
    from .chroma_client import query_documents
    pfeq_context = ""
    try:
        # Rechercher dans les documents PFEQ (collection solenys)
        pfeq_docs = query_documents(question, n_results=3, collection_name="solenys")
        if pfeq_docs:
            pfeq_context = "\n\nDocuments PFEQ pertinents:\n" + "\n".join(pfeq_docs)
            print(f"[Solenys] Contexte PFEQ trouvé: {len(pfeq_docs)} documents")
    except Exception as e:
        print(f"[Solenys] Erreur recherche PFEQ: {e}")
        pfeq_context = ""
    
    # Construction du prompt optimisé avec mémoire de conversation et documents PFEQ
    full_prompt = f"""
Tu es Solenys, professeur québécois spécialisé dans l'enseignement secondaire selon le programme PFEQ du Québec.

Contexte de conversation:
{conversation_context}

{pfeq_context}

Ton rôle est de :
- Accompagner les élèves du secondaire (12-17 ans) dans leur apprentissage
- Enseigner selon le programme PFEQ (Programme de formation de l'école québécoise)
- Adapter ton approche pédagogique au niveau de l'élève
- Encourager et motiver dans l'apprentissage
- Proposer des exercices pratiques et concrets
- Utiliser les documents PFEQ pour donner des réponses précises et conformes

Instructions pédagogiques :
- Utilise un ton bienveillant, professionnel et motivant
- Adapte ton langage au niveau secondaire
- Propose des exemples concrets et pratiques
- Encourage la participation et la réflexion
- Reste dans le cadre du programme PFEQ
- Sois clair et structuré dans tes explications
- Référence les documents PFEQ quand c'est pertinent
- Donne des réponses basées sur le programme officiel

Question de l'élève: {question}

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

Réponds de manière concise et pédagogique. Donne la réponse directe puis une explication courte.

Format de réponse:
"**Résultat :** [réponse]

**Explication :** [explication courte]

**Autre calcul ?**"

Réponse:"""
            
            response_text = ollama_generate_simple(math_prompt, "Tu es Solenys, professeur de mathématiques québécois spécialisé dans le programme PFEQ.")
        except Exception as e:
            print(f"[Solenys] Erreur calcul: {e}")
            response_text = f"📐 **Erreur de calcul**\n\n**Question :** {question}\n\n**Problème technique** - Reformulez votre question.\n\n**Calculs disponibles :**\n• **Addition, soustraction, multiplication, division**\n• **Algèbre, géométrie, statistiques**\n\n**Autre calcul ?**"
    elif "math" in question.lower() or "mathématiques" in question.lower() or "algèbre" in question.lower() or "en mathematiques" in question.lower():
        response_text = f"📐 **Mathématiques - Programme PFEQ**\n\n**Domaines disponibles :**\n• **Algèbre** - Équations, fonctions, polynômes\n• **Géométrie** - Formes, angles, aires, volumes\n• **Statistiques** - Moyennes, probabilités, graphiques\n• **Calcul** - Dérivées, intégrales (niveaux avancés)\n\n**Quel est votre niveau ?** (Secondaire 1-5)\n**Sur quoi voulez-vous travailler ?**"
    elif "science" in question.lower() or "physique" in question.lower() or "chimie" in question.lower() or "biologie" in question.lower() or "eau" in question.lower() or "composition" in question.lower():
        # Utiliser Ollama avec les documents PFEQ pour les questions scientifiques
        try:
            print(f"[Solenys] Question scientifique détectée, utilisation d'Ollama avec PFEQ")
            response_text = ollama_generate_simple(full_prompt, "Tu es Solenys, professeur de sciences québécois spécialisé dans le programme PFEQ.")
        except Exception as e:
            print(f"[Solenys] Erreur sciences: {e}")
            response_text = f"🔬 **Sciences - Programme PFEQ**\n\n**Matières disponibles :**\n• **Physique** - Mécanique, électricité, ondes\n• **Chimie** - Réactions, liaisons, équilibres\n• **Biologie** - Cellules, génétique, écosystèmes\n\n**Quel domaine vous intéresse ?**\n**Quel est votre niveau ?** (Secondaire 1-5)"
    elif "français" in question.lower() or "littérature" in question.lower() or "grammaire" in question.lower():
        response_text = f"📚 **Français - Programme PFEQ**\n\n**Domaines disponibles :**\n• **Grammaire** - Syntaxe, conjugaisons, orthographe\n• **Littérature** - Auteurs québécois, analyse de textes\n• **Rédaction** - Composition, techniques d'écriture\n• **Communication** - Expression orale, présentation\n\n**Quel aspect vous intéresse ?**\n**Quel est votre niveau ?** (Secondaire 1-5)"
    elif "probabilité" in question.lower() or "probabilite" in question.lower() or "probabilités" in question.lower() or "en probabilite" in question.lower() or "en probabilité" in question.lower():
        response_text = f"🎲 **Probabilités - Programme PFEQ**\n\n**Concepts disponibles :**\n• **Probabilités simples** - Dés, pièces, cartes\n• **Probabilités composées** - Événements multiples\n• **Arbres de probabilités** - Visualisation\n• **Espérance mathématique** - Valeur attendue\n\n**Quel niveau ?** (Secondaire 1-5)\n**Quel concept vous intéresse ?**"
    elif "histoire" in question.lower() or "géographie" in question.lower():
        response_text = f"🗺️ **Histoire & Géographie - Programme PFEQ**\n\n**Domaines disponibles :**\n• **Histoire du Québec** - Nouvelle-France à aujourd'hui\n• **Histoire mondiale** - Civilisations, événements\n• **Géographie du Québec** - Territoire, ressources\n• **Géographie mondiale** - Pays, cultures\n\n**Quel domaine vous intéresse ?**\n**Quel est votre niveau ?** (Secondaire 1-5)"
    elif "bonjour" in question.lower() or "salut" in question.lower() or "bonsoir" in question.lower():
        response_text = "👋 **Bonjour ! Je suis Solenys**\n\n**Professeur québécois - Programme PFEQ**\n\n**Matières disponibles :**\n• **Mathématiques** - Algèbre, géométrie, statistiques\n• **Sciences** - Physique, chimie, biologie\n• **Français** - Littérature, grammaire, rédaction\n• **Histoire & Géographie** - Québec et monde\n\n**Quelle matière vous intéresse ?**"
    else:
        # Utiliser Ollama avec les documents PFEQ pour les questions éducatives
        try:
            print(f"[Solenys] Utilisation d'Ollama avec contexte PFEQ")
            response_text = ollama_generate_simple(full_prompt, "Tu es Solenys, professeur québécois spécialisé dans le programme PFEQ.")
        except Exception as e:
            print(f"[Solenys] Erreur Ollama: {e}")
            response_text = f"🎓 **Solenys - Professeur PFEQ**\n\n**Question :** {question}\n\n**Matières disponibles :**\n• **Mathématiques** - Calcul, algèbre, géométrie\n• **Sciences** - Physique, chimie, biologie\n• **Français** - Littérature, grammaire\n• **Histoire & Géographie** - Québec et monde\n\n**Quelle matière vous intéresse ?**"

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
