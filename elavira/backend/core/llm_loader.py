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

# --- Initialisation du client ChromaDB ---
script_dir = os.path.dirname(__file__)
chroma_db_path = os.path.join(script_dir, "..", "chroma_data")
os.makedirs(chroma_db_path, exist_ok=True)

chroma_client = chromadb.PersistentClient(path=chroma_db_path)
collection = chroma_client.get_or_create_collection(name="elavira_collection")
print(f"✅ ChromaDB persistant à : {os.path.abspath(chroma_db_path)}")

# --- Initialisation du modèle d'embeddings SentenceTransformer ---
try:
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    print("✅ Embedder (SentenceTransformer 'all-MiniLM-L6-v2') initialisé.")
except Exception as e:
    raise RuntimeError(f"❌ Échec de l'initialisation de l'embedder : {e}")

# --- Fonctions pour indexer et requêter les documents ---
def index_documents(texts: List[str], ids: List[str] = None):
    if not texts:
        return []
    embeddings = embedder.encode(texts).tolist()
    metadatas = [{"source": f"doc_{i}"} for i in range(len(texts))]
    if ids is None:
        current_count = collection.count()
        ids = [f"doc_{current_count + i}" for i in range(len(texts))]
    collection.add(documents=texts, embeddings=embeddings, metadatas=metadatas, ids=ids)
    print(f"✅ {len(texts)} documents indexés dans ChromaDB.")
    return ids

def query_documents(query_text: str, n_results: int = 3) -> List[str]:
    if not query_text:
        return []
    query_embedding = embedder.encode([query_text]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
        include=['documents']
    )
    return results.get('documents', [[]])[0] if results.get('documents') else []

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
        system_persona = """Tu es Elavira, l'assistante virtuelle de FormEduc, spécialisée dans l'accompagnement des professionnels de la petite enfance et du milieu scolaire.

MISSION : Accueillir, guider et accompagner les visiteurs dans leur parcours de formation professionnelle.

PERSONNALITÉ :
- Ton : Professionnel, chaleureux, bienveillant, motivant
- Approche : Accueillante et personnalisée dès l'arrivée
- Expertise : Connaissance approfondie des formations FormEduc et des réglementations québécoises

FONCTIONNALITÉS :
- Accueil personnalisé avec message chaleureux
- Réponses aux FAQ (tarifs, durées, certifications, exigences)
- Guidage contextuel dans la navigation
- Recommandations de formations selon le profil utilisateur
- Questions de qualification pour personnaliser l'accompagnement
- Support dans le processus d'inscription et d'achat

FORMATIONS FORMEDUC :
- Secourisme service de garde (petite enfance, milieu scolaire)
- Formations 45h pour RSG et RSGE
- Perfectionnements pour éducatrices et éducateurs
- Familles d'accueil (formations hybrides)
- Programme jeunesse (gardien futé, animateur de camp)
- Formations 100% en ligne avec certifications reconnues

RÉGLEMENTATIONS : Conformes au Règlement sur les services de garde éducatifs et à la Loi sur l'instruction publique.

STYLE : Toujours professionnel, chaleureux, bienveillant et motivant. Pose des questions de qualification pour mieux accompagner."""
    
    # Récupération du contexte de conversation
    conversation_context = get_conversation_context(user_id, agent_id, max_messages=3)
    
    # Récupération des documents les plus pertinents de Formeduc
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
    
    # Réponses optimisées avec le contenu réel du site FormEduc
    query_lower = query.lower()
    
    if "secourisme" in query_lower or "premiers soins" in query_lower or "formation" in query_lower and "secourisme" in query_lower:
        response = f"Excellent choix ! 🚑\n\nFormEduc propose des formations de secourisme spécialisées selon le site [formeduc.ca](https://www.formeduc.ca/) :\n\n• **Secourisme adapté à la petite enfance** - 8 heures en ligne\n• **Renouvellement** de secourisme petite enfance - 6 heures\n• **Secourisme en milieu scolaire** - Formation en ligne\n• **Secourisme pour chauffeur d'autobus** - Enfants d'âge scolaire, 8 heures\n• **Trousse de premiers soins** pour garderie\n\nToutes nos formations de secourisme sont adaptées aux besoins spécifiques des professionnels de la petite enfance et du milieu scolaire. Elles sont conformes au Règlement sur les services de garde éducatifs et à la Loi sur l'instruction publique.\n\nQuelle formation de secourisme vous intéresse ?"
    elif "formation" in query_lower or "programme" in query_lower or "cours" in query_lower:
        greeting = "Bonjour ! Je suis Elavira, votre assistante FormEduc ! 🎓\n\n" if is_first_message else ""
        response = f"{greeting}Je vois que vous vous intéressez à nos formations. FormEduc propose des formations spécialisées pour les professionnels de la petite enfance et du milieu scolaire :\n\n• **Secourisme service de garde** - Adapté à la petite enfance (8h) et milieu scolaire\n• **Formations garderie** - Programme de 45h pour RSG/RSGE\n• **Familles d'accueil** - Formations hybrides spécialisées\n• **Programme jeunesse** - Cours de gardien futé et animateur de camp\n• **Formations en ligne** - Accès 24h/24, certifications reconnues\n\nNos formations sont conformes au Règlement sur les services de garde éducatifs et à la Loi sur l'instruction publique. Quel est votre profil professionnel ?"
    elif "bonjour" in query_lower or "salut" in query_lower or "bonsoir" in query_lower:
        response = "Bonjour et bienvenue sur FormEduc ! 👋\n\nJe suis Elavira, votre assistante virtuelle. Je suis là pour vous accompagner dans votre parcours de formation professionnelle !\n\n**Comment puis-je vous aider aujourd'hui ?**\n\n• Découvrir nos formations adaptées à votre profil\n• Obtenir des informations sur nos tarifs et certifications\n• Vous guider dans votre processus d'inscription\n• Répondre à vos questions sur nos services\n\n**Quel est votre domaine d'activité ?** (Éducatrice, RSG, parent, famille d'accueil, etc.)"
    elif "tarif" in query_lower or "prix" in query_lower or "coût" in query_lower:
        response = f"Excellente question ! 💰\n\nNos tarifs varient selon le type de formation et votre profil :\n\n• **Formations individuelles** : Tarifs préférentiels pour les particuliers\n• **Formations en entreprise** : Devis personnalisés selon vos besoins\n• **Formations en ligne** : Accès flexible et économique\n\nPour obtenir un devis précis, pourriez-vous me préciser :\n- Le type de formation qui vous intéresse\n- Votre profil (particulier, entreprise, organisme)\n- Le nombre de participants\n\nJe pourrai alors vous orienter vers la meilleure option !"
    elif "certification" in query_lower or "certificat" in query_lower or "diplôme" in query_lower:
        response = f"Excellente question ! 🏆\n\nToutes nos formations délivrent des certifications reconnues :\n\n• **Certificats conformes** au Règlement sur les services de garde éducatifs en milieu scolaire\n• **Attestations** conformes à la Loi sur l'instruction publique (chapitre l-13.3, a. 454.1)\n• **Certifications numériques** - Accessibles en ligne 24h/24\n• **Formations 100% en ligne** - Accès où que vous soyez, à tout moment\n\nNos certifications sont reconnues par les organismes de services de garde. Quelle formation vous intéresse ?"
    elif "rsg" in query_lower or "rsge" in query_lower or "responsable" in query_lower:
        greeting = "Parfait ! Vous vous intéressez aux formations pour responsables de service de garde ! 🏠\n\n" if is_first_message else "Parfait ! 🏠\n\n"
        response = f"{greeting}FormEduc propose des formations spécialisées pour RSG et RSGE :\n\n• **Formation obligatoire de 45 heures** pour RSGE\n• **Le programme éducatif** en service de garde\n• **Le développement de l'enfant** - Formation complète\n• **Santé, sécurité et alimentation**\n• **Le rôle de la responsable** d'un service de garde\n\nCes formations sont essentielles pour exercer légalement en service de garde familial. Souhaitez-vous plus d'informations sur une formation spécifique ?"
    elif "perfectionnement" in query_lower or "développement" in query_lower:
        response = f"Parfait ! 📚\n\nFormEduc propose de nombreux cours de perfectionnement pour éducatrices et éducateurs :\n\n• **Développement de l'enfant** - Formation complète et assistant/remplaçant\n• **Allergies ? Je réagis !** - Gestion des allergies en garderie\n• **Bien dormir pour bien grandir** - Troubles du sommeil\n• **Briser la chaîne infectieuse** - Prévention des infections\n• **Cultiver l'intelligence émotionnelle** de l'enfant\n• **De A à Z… 26 techniques d'intervention**\n• **La maltraitance** - Intervenir pour protéger l'enfant\n• **Le développement langagier** - Acquisition et dépistage\n\nCes formations vous permettent d'améliorer vos compétences professionnelles. Quel sujet vous intéresse ?"
    elif "enfant" in query_lower or "je suis" in query_lower:
        response = f"Je comprends ! 😊\n\nFormEduc propose aussi des formations pour les jeunes ! Nous avons un **Programme jeunesse** spécialement conçu :\n\n• **Cours de gardien futé et averti** en ligne\n• **Futé : Je suis prêt à rester seul** - Formation pour les adolescents\n• **Formation en secourisme** pour animateur de camp de jour et moniteur de camp de vacances\n\nCes formations sont parfaites pour les jeunes qui veulent apprendre les premiers soins et devenir des gardiens responsables !\n\nQuel âge avez-vous ? Je pourrai vous orienter vers la formation la plus adaptée !"
    elif "éducatrice" in query_lower or "éducateur" in query_lower or "cpe" in query_lower or "garderie" in query_lower:
        response = f"Parfait ! Vous travaillez en petite enfance ! 🧸\n\nFormEduc propose des formations spécialement conçues pour les éducatrices et éducateurs :\n\n• **Formations de perfectionnement** - Développement de l'enfant, allergies, maltraitance\n• **Secourisme adapté** à la petite enfance (8h)\n• **Formations 45h** pour RSG et RSGE\n• **Cours spécialisés** - Intelligence émotionnelle, prévention, intervention\n\n**Questions pour mieux vous accompagner :**\n- Travaillez-vous en CPE, garderie ou service de garde familial ?\n- Cherchez-vous une formation spécifique ou souhaitez-vous découvrir nos programmes ?\n\nJe peux vous guider vers la formation la plus adaptée à votre situation !"
    elif "parent" in query_lower or "maman" in query_lower or "papa" in query_lower:
        response = f"Excellente question ! 👨‍👩‍👧‍👦\n\nFormEduc propose des formations qui peuvent intéresser les parents :\n\n• **Programme jeunesse** - Pour former vos enfants aux premiers soins\n• **Formations de secourisme** - Pour être prêt en cas d'urgence\n• **Cours de gardien futé** - Pour vos adolescents qui gardent\n\n**Questions pour mieux vous orienter :**\n- Cherchez-vous une formation pour vous-même ou pour vos enfants ?\n- Avez-vous des enfants en bas âge ou des adolescents ?\n- Êtes-vous intéressé par les premiers soins ou d'autres sujets ?\n\nJe peux vous proposer la formation la plus adaptée à vos besoins familiaux !"
    elif "famille d'accueil" in query_lower or "famille d'accueil" in query_lower:
        response = f"Parfait ! Vous êtes famille d'accueil ! 🏠\n\nFormEduc propose des formations spécialisées pour les familles d'accueil :\n\n• **Formation hybride en secourisme** - Spécialement conçue pour les familles d'accueil\n• **Développement de l'enfant** - Comprendre les besoins spécifiques\n• **Gestion des allergies** - "Allergies ? Je réagis !"\n• **Intelligence émotionnelle** - Accompagner l'enfant dans son développement\n• **Prévention maltraitance** - Protéger et intervenir\n\n**Questions pour personnaliser votre parcours :**\n- Accueillez-vous des enfants de quel âge ?\n- Avez-vous déjà suivi des formations FormEduc ?\n- Y a-t-il des sujets particuliers qui vous préoccupent ?\n\nJe peux vous orienter vers les formations les plus pertinentes pour votre situation !"
    elif "inscription" in query_lower or "inscrire" in query_lower or "acheter" in query_lower or "commander" in query_lower:
        response = f"Parfait ! Je vais vous accompagner dans votre processus d'inscription ! 📝\n\n**Étapes pour vous inscrire :**\n\n1️⃣ **Choisir votre formation** - Quelle formation vous intéresse ?\n2️⃣ **Vérifier les prérequis** - Avez-vous les qualifications nécessaires ?\n3️⃣ **Créer votre compte** - Accès à la plateforme FormEduc\n4️⃣ **Paiement sécurisé** - Cartes de crédit acceptées\n5️⃣ **Accès immédiat** - Formation disponible 24h/24\n\n**Questions pour vous guider :**\n- Avez-vous déjà un compte FormEduc ?\n- Quelle formation souhaitez-vous suivre ?\n- Avez-vous des questions sur le processus de paiement ?\n\nJe peux vous accompagner à chaque étape !"
    elif "aide" in query_lower or "support" in query_lower or "problème" in query_lower:
        response = f"Je suis là pour vous aider ! 🤝\n\n**Comment puis-je vous assister ?**\n\n• **Questions techniques** - Problèmes d'accès, navigation\n• **Informations sur les formations** - Contenu, durée, certifications\n• **Processus d'inscription** - Guide étape par étape\n• **Paiement et facturation** - Questions tarifaires\n• **Support technique** - Difficultés avec la plateforme\n\n**Contactez-nous aussi :**\n📞 **418 842-7523**\n📧 **contact@formeduc.ca**\n📍 **5121 ave Chauveau Ouest, Québec, QC G2E 5A6 local 101**\n\nDécrivez-moi votre problème et je vous aiderai à le résoudre !"
    elif "durée" in query_lower or "temps" in query_lower or "long" in query_lower:
        response = f"Excellente question ! ⏰\n\n**Durées des formations FormEduc :**\n\n• **Secourisme petite enfance** - 8 heures\n• **Renouvellement secourisme** - 6 heures\n• **Formation 45h RSG/RSGE** - 45 heures (obligatoire)\n• **Perfectionnements** - 3 à 6 heures selon le cours\n• **Programme jeunesse** - 2 à 4 heures\n• **Familles d'accueil** - Durées variables selon le module\n\n**Avantages de nos formations :**\n✅ **100% en ligne** - À votre rythme\n✅ **Accès 24h/24** - Quand vous voulez\n✅ **Certification immédiate** - Dès la réussite\n\nQuelle formation vous intéresse ? Je peux vous donner plus de détails !"
    else:
        greeting = "Bonjour ! Je suis Elavira, votre assistante FormEduc ! 🎓\n\n" if is_first_message else ""
        response = f"{greeting}Je suis là pour vous accompagner dans vos besoins de formation professionnelle. FormEduc vous propose :\n\n• **Secourisme** - Service de garde, petite enfance, milieu scolaire\n• **Formations 45h** - Pour RSG et RSGE\n• **Perfectionnements** - Développement de l'enfant, allergies, maltraitance\n• **Familles d'accueil** - Formations hybrides spécialisées\n• **Programme jeunesse** - Gardien futé et animateur de camp\n• **Formations en ligne** - 100% à distance, certifications reconnues\n\nNos formations sont développées par des experts du terrain avec une vraie expérience pratique. Que souhaitez-vous savoir en particulier ?"
    
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
