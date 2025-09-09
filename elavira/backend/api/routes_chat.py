from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import base64
import io
import asyncio
import requests
from gtts import gTTS
from concurrent.futures import ThreadPoolExecutor
import random

# Import des fonctions de ChromaDB et Ollama
# Assurez-vous que ces imports sont corrects pour votre structure de projet
from backend.core.chroma_client import collection, embedder, ollama_generate, query_documents

router = APIRouter(prefix="/chat", tags=["Chat"])

class MessageDisplay(BaseModel):
    id: int
    text: str
    user_id: str
    timestamp: str
    agent_id: Optional[str] = None
    audio_base64: Optional[str] = None
    suggested_prompts: Optional[List[str]] = None

class MessageCreate(BaseModel):
    text: str
    user_id: str = "Guest"
    agent_id: Optional[str] = None

fake_db_messages: List[Dict] = []
message_id_counter = 0
executor = ThreadPoolExecutor()

def _synthesize_speech_blocking(text: str) -> str:
    try:
        mp3_fp = io.BytesIO()
        tts = gTTS(text, lang="fr")
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        return base64.b64encode(mp3_fp.read()).decode("utf-8")
    except Exception as e:
        print(f"[TTS] Erreur synthèse vocale : {e}")
        return None

async def synthesize_speech_async(text: str) -> str:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, _synthesize_speech_blocking, text)

# NOUVEAU : Catalogue des formations détaillé et structuré
# REMPLACER L'ANCIENNE LISTE PAR CELLE-CI
catalogue_formations_data = [
    {
        "category": "Formations en secourisme (en ligne)",
        "name": "Secourisme adapté à la petite enfance – en ligne",
        "duration": "8 heures",
        "price": "47,83 $CAD",
        "link": "https://www.formeduc.ca/panier?add-to-cart=9999", # Exemple, à remplacer par le vrai lien produit du panier si disponible
        "keywords": ["secourisme", "petite enfance", "en ligne"]
    },
    {
        "category": "Formations en secourisme (en ligne)",
        "name": "Renouvellement – Secourisme adapté à la petite enfance – en ligne",
        "duration": "6 heures",
        "price": "47,83 $CAD",
        "link": None, # À vérifier si un lien direct existe pour le renouvellement
        "keywords": ["renouvellement", "secourisme", "petite enfance", "en ligne"]
    },
    {
        "category": "Formations en secourisme (en ligne)",
        "name": "Secourisme en milieu scolaire – en ligne",
        "duration": "8 heures",
        "price": "47,83 $CAD",
        "link": "https://www.formeduc.ca/secourisme-service-de-garde/secourisme-en-milieu-scolaire-en-ligne/", # Lien plus précis
        "keywords": ["secourisme", "scolaire", "en ligne"]
    },
    {
        "category": "Formations en secourisme (en ligne)",
        "name": "Renouvellement – Secourisme en milieu scolaire – en ligne",
        "duration": "6 heures",
        "price": "47,83 $CAD",
        "link": None, # À vérifier si un lien direct existe pour le renouvellement
        "keywords": ["renouvellement", "secourisme", "scolaire", "en ligne"]
    },
    {
        "category": "Formations en secourisme (en ligne)",
        "name": "Secourisme adapté aux enfants d’âge scolaire – en ligne (chauffeur d’autobus)",
        "duration": "8 heures",
        "price": "47,83 $CAD",
        "link": None, # À vérifier
        "keywords": ["secourisme", "enfants", "scolaire", "chauffeur", "autobus", "en ligne"]
    },
    {
        "category": "Formations en secourisme (en ligne)",
        "name": "Trousse premiers soins pour service de garde",
        "duration": None,
        "price": "69,36 $CAD",
        "link": None, # À vérifier
        "keywords": ["trousse", "premiers soins", "service de garde"]
    },
    {
        "category": "Formations en secourisme (en ligne)",
        "name": "Trousse premiers soins (de main à main)",
        "duration": None,
        "price": "47,83 $CAD",
        "link": "https://www.formeduc.ca/trousse-premiers-soins-de-main-a-main/", # Lien plus précis
        "keywords": ["trousse", "premiers soins", "main à main"]
    },
    {
        "category": "Formations en secourisme (en ligne)",
        "name": "Protéger nos Enfants : prévention de la maltraitance",
        "duration": None,
        "price": "gratuit (0,00 $CAD)",
        "link": "https://www.formeduc.ca/proteger-nos-enfants-prevention-de-la-maltraitance/", # Lien plus précis
        "keywords": ["maltraitance", "gratuit", "enfants", "prévention"]
    },
    {
        "category": "Formation à distance – Programme 45 heures (RSGE)",
        "name": "Formation en ligne obligatoire de 45 heures (RSGE) - Version en ligne seulement",
        "duration": "45 heures",
        "price": "100 $CAD",
        "link": "https://www.formeduc.ca/formation-obligatoire-pour-rsge/", # Lien principal RSGE
        "keywords": ["RSGE", "obligatoire", "45 heures", "en ligne"]
    },
    {
        "category": "Formation à distance – Programme 45 heures (RSGE)",
        "name": "Formation en ligne obligatoire de 45 heures (RSGE) - Avec matériel imprimé par la poste",
        "duration": "45 heures",
        "price": "175 $CAD",
        "link": "https://www.formeduc.ca/formation-obligatoire-pour-rsge/", # Lien principal RSGE
        "keywords": ["RSGE", "obligatoire", "45 heures", "matériel imprimé"]
    },
    # Sub-modules du programme 45h (si vous voulez qu'ils soient individuellement citables)
    {
        "category": "Module Programme 45h RSGE",
        "name": "Programme éducatif en service de garde",
        "duration": None,
        "price": "Inclus dans 45h RSGE",
        "link": None,
        "keywords": ["programme éducatif", "service de garde"]
    },
    {
        "category": "Module Programme 45h RSGE",
        "name": "Développement de l’enfant",
        "duration": None,
        "price": "Inclus dans 45h RSGE",
        "link": None,
        "keywords": ["développement", "enfant"]
    },
    {
        "category": "Module Programme 45h RSGE",
        "name": "Rôle de la responsable d’un service de garde",
        "duration": None,
        "price": "Inclus dans 45h RSGE",
        "link": None,
        "keywords": ["responsable", "service de garde", "rôle"]
    },
    {
        "category": "Module Programme 45h RSGE",
        "name": "Santé, sécurité et alimentation",
        "duration": None,
        "price": "Inclus dans 45h RSGE",
        "link": None,
        "keywords": ["santé", "sécurité", "alimentation"]
    },
    {
        "category": "Formation hybride – Familles d’accueil",
        "name": "Formation hybride en secourisme pour familles d’accueil",
        "duration": None,
        "price": "Tarif non précisé (Contacter Formeduc)",
        "link": "https://www.formeduc.ca/formations/", # Lien général Formeduc, à affiner si page spécifique
        "contact_info": "info@formeduc.ca ou (418) 842‑7523",
        "keywords": ["familles d'accueil", "hybride", "secourisme"]
    },
    {
        "category": "Programme jeunesse (9–14 ans)",
        "name": "Futé : Je suis prêt à rester seul",
        "duration": None,
        "price": "47,83 $CAD",
        "link": "https://dev.formeduc.ca/product/fute-je-suis-pret-a-rester-seul/", # Exemple, à ajuster si le vrai lien diffère
        "keywords": ["jeunesse", "rester seul"]
    },
    {
        "category": "Programme jeunesse (9–14 ans)",
        "name": "Gardien futé et averti",
        "duration": None,
        "price": "47,83 $CAD",
        "link": "https://dev.formeduc.ca/product/gardien-fute-et-averti/", # Exemple, à ajuster si le vrai lien diffère
        "keywords": ["jeunesse", "gardien"]
    },
    {
        "category": "Programme jeunesse (9–14 ans)",
        "name": "Secourisme pour animateur de camp de jour / camp de vacances",
        "duration": None,
        "price": "47,83 $CAD",
        "link": "https://dev.formeduc.ca/product/secourisme-pour-animateur-de-camp-de-jour-camp-de-vacances/", # Exemple, à ajuster si le vrai lien diffère
        "keywords": ["jeunesse", "secourisme", "animateur", "camp"]
    }
]

# Fonction pour formater le catalogue en texte
def format_catalogue_text(formations: List[Dict]) -> str:
    # Utilisation d'un set pour garder trace des catégories déjà ajoutées
    added_categories = set()
    formatted_lines = ["Voici un aperçu complet des formations offertes par Formeduc (Québec) :"]

    for f in formations:
        if f.get("category") and f["category"] not in added_categories:
            formatted_lines.append(f"\n**{f['category']}**") # Ajoute la catégorie comme un titre
            added_categories.add(f["category"])
        
        # Formatage de l'information de la formation
        name = f['name']
        duration = f" ({f['duration']})" if f['duration'] else ""
        price = f" - Prix: {f['price']}" if f['price'] else ""
        
        link_text = ""
        if f['link']:
            link_text = f" [Lien direct]"
            # On ajoute le lien entre parenthèses ou de manière plus discrète pour le texte direct
            # car le LLM pourrait avoir du mal avec des URLs complexes en milieu de phrase.
            # Le prompt système doit être optimisé pour gérer l'URL.
            # Pour l'affichage direct, nous pouvons toujours l'inclure.
            # Pour le LLM, il est souvent mieux d'avoir le lien séparé.
            # Pour l'affichage final, nous mettrons un lien cliquable si possible.
            # Ici, nous mettons le lien complet pour le LLM.
            link_for_ollama = f" (Lien: {f['link']})"
        else:
            link_for_ollama = ""

        formatted_lines.append(f"- {name}{duration}{price}{link_for_ollama}") # Inclure le lien complet ici pour Ollama

    formatted_lines.append("\nPour toute question sur les tarifs non précisés ou des détails supplémentaires, n'hésitez pas à nous contacter.")
    formatted_lines.append("Visitez notre site principal pour plus d'informations: https://www.formeduc.ca/formations/")
    
    return "\n".join(formatted_lines)

# Fonction pour générer des prompts suggérés
def generate_suggested_prompts(user_message_text: str, assistant_response_text: str) -> List[str]:
    prompts = []
    
    # Logique basée sur la réponse de l'assistant (peut être affinée avec les nouvelles catégories)
    if "formation" in assistant_response_text.lower() or "formations" in assistant_response_text.lower():
        prompts.append("Quelles sont les formations en ligne ?")
        prompts.append("Parlez-moi de la formation RSGE")
        prompts.append("Y a-t-il des formations gratuites ?")
        prompts.append("Comment m'inscrire à une formation ?")
    elif "secourisme" in assistant_response_text.lower():
        prompts.append("Combien coûte le secourisme en milieu scolaire ?")
        prompts.append("Comment renouveler ma certification de secourisme ?")
        prompts.append("Détails sur le secourisme adapté petite enfance")
    elif "trousse" in assistant_response_text.lower():
        prompts.append("Prix de la trousse de premiers soins (main à main)")
        prompts.append("Détails sur la trousse pour service de garde")
    elif "maltraitance" in assistant_response_text.lower() or "protéger nos enfants" in assistant_response_text.lower():
        prompts.append("Parlez-moi de la prévention de la maltraitance.")
        prompts.append("Est-ce que cette formation est certifiante ?")
    elif "famille d'accueil" in assistant_response_text.lower() or "hybride" in assistant_response_text.lower():
        prompts.append("Quel est le prix de la formation hybride ?")
        prompts.append("Comment s'inscrire à la formation pour familles d'accueil ?")
    elif "jeunesse" in assistant_response_text.lower() or "futé" in assistant_response_text.lower():
        prompts.append("Dites-m'en plus sur le programme 'Futé : Je suis prêt à rester seul'.")
        prompts.append("Quel est le prix du programme Gardien futé et averti ?")

    # Suggestions génériques si aucune correspondance spécifique
    if not prompts:
        if "aide" in user_message_text.lower() or "bonjour" in user_message_text.lower():
            prompts.extend([
                "Quelles formations proposez-vous ?",
                "Parlez-moi de Formeduc",
                "Comment fonctionne le secourisme en ligne ?"
            ])
        else:
            prompts.extend([
                "Pouvez-vous me lister toutes les formations ?",
                "Quel est le prix de la formation X?", 
                "Où puis-je trouver plus d'informations ?"
            ])

    # Supprime les doublons et limite le nombre pour ne pas submerger l'utilisateur.
    return list(set(prompts))[:4] 

@router.get("/")
async def read_chat_status():
    return {"message": "Chat routes are working!", "status": "active"}

@router.post("/send_message/", response_model=MessageDisplay)
async def send_message(message: MessageCreate):
    global message_id_counter

    # Sauvegarde message utilisateur
    message_id_counter += 1
    user_msg = {
        "id": message_id_counter,
        "text": message.text,
        "user_id": message.user_id,
        "timestamp": datetime.utcnow().isoformat(),
        "agent_id": message.agent_id or "agent-001",
    }
    fake_db_messages.append(user_msg)

    text_lower = message.text.lower().strip()
    greetings = ["salut", "bonjour", "coucou", "hello", "hey"]

    response_text = ""
    generated_suggested_prompts = [] 

    if any(greet in text_lower for greet in greetings):
        salutations = [
            "Salut ! Je suis Elavira, votre éducatrice en secourisme chez Formeduc. Comment puis-je vous aider aujourd’hui ?",
            "Bonjour, c’est Elavira, ravie de vous aider. Que puis-je faire pour vous ?",
            "Coucou, ici Elavira, prête à répondre à vos questions sur nos formations."
        ]
        response_text = random.choice(salutations)
        generated_suggested_prompts = [
            "Quelles formations proposez-vous ?",
            "Parlez-moi de Formeduc",
            "Comment fonctionne le secourisme en ligne ?"
        ]

    elif any(keyword in text_lower for keyword in ["formation", "formations", "proposez", "cours", "offrez", "liste des formations", "catalogue", "tarifs"]): # Ajout de "tarifs"
        response_text = format_catalogue_text(catalogue_formations_data) 
        generated_suggested_prompts = [
            "Détails sur la formation RSGE",
            "Quelles sont les formations en ligne ?",
            "Y a-t-il des formations gratuites ?",
            "Comment m'inscrire à une formation ?",
            "Quel est le prix du secourisme en milieu scolaire ?" 
        ]
        
    else:
        try:
            # Recherche contextuelle avec ChromaDB
            context_docs = query_documents(message.text, n_results=5)
            context = "\n\n".join(context_docs) if context_docs else ""
            print(f"[DEBUG] Contexte extrait : {context[:200]}...")
        except Exception as e:
            print(f"[ChromaDB] Erreur lors de la recherche contextuelle : {e}")
            context = ""

        text_catalogue_for_ollama = format_catalogue_text(catalogue_formations_data)

        base_system_prompt = (
            "Tu es Elavira, une assistante IA bienveillante, chaleureuse et experte en secourisme. "
            "Ton objectif principal est d'aider les utilisateurs à trouver les informations spécifiques "
            "dont ils ont besoin sur les formations Formeduc en ligne, en te basant **uniquement** sur "
            "le catalogue de formations et le contexte fourni. "
            "Si la réponse n'est pas dans le contexte ou le catalogue, dis que tu ne sais pas mais propose "
            "des alternatives ou de reformuler la question. "
            "Tu réponds de manière concise, claire et naturelle, comme dans une vraie conversation. "
            "Tu ne rédiges jamais de documents administratifs ou rapports. "
            "Tu poses des questions ouvertes pour comprendre les besoins si ce n’est pas clair. "
            "Utilise ce catalogue de formations pour guider tes réponses :\n"
            f"{text_catalogue_for_ollama}\n" 
            "Sois polie, engageante et simple. Réponds **spécifiquement** à la question posée, sans digresser."
        )

        full_prompt = (
            f"{base_system_prompt}\n\n"
            f"Contexte pertinent (si disponible) : {context}\n"
            f"Question de l'utilisateur : {message.text}\n"
            "Réponse d'Elavira :"
        )

        loop = asyncio.get_running_loop()
        response_text = await loop.run_in_executor(executor, ollama_generate, full_prompt)
        print(f"[AI Response] Réponse générée : {response_text[:100]}...")
        
        generated_suggested_prompts = generate_suggested_prompts(message.text, response_text)

    audio_base64 = await synthesize_speech_async(response_text)
    print(f"[TTS] Audio généré : {'Oui' if audio_base64 else 'Non'}")

    message_id_counter += 1
    bot_msg = {
        "id": message_id_counter,
        "text": response_text,
        "user_id": "Elavira Assistant",
        "timestamp": datetime.utcnow().isoformat(),
        "agent_id": message.agent_id or "agent-001",
        "audio_base64": audio_base64,
        "suggested_prompts": generated_suggested_prompts
    }
    fake_db_messages.append(bot_msg)

    return bot_msg

@router.get("/history/", response_model=List[MessageDisplay])
async def get_chat_history(agent_id: Optional[str] = None, user_id: Optional[str] = None):
    filtered = fake_db_messages
    if agent_id:
        filtered = [m for m in filtered if m.get("agent_id") == agent_id]
    if user_id:
        filtered = [m for m in filtered if m.get("user_id") in [user_id, "Elavira Assistant", "Solenys Assistant"]]
    return filtered

@router.post("/transcribe_audio/")
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        if not file:
            raise HTTPException(status_code=400, detail="Aucun fichier n’a été fourni.")
        audio_bytes = await file.read()
        response = requests.post(
            "http://localhost:11434/api/transcribe",
            files={"audio": ("audio.wav", audio_bytes, "audio/wav")}
        )
        response.raise_for_status()
        data = response.json()
        return {"transcribed_text": data.get("text", "")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de transcription : {e}")