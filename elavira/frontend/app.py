# app.py (Votre script Streamlit complet avec améliorations esthétiques)

import streamlit as st
import base64
import os
import requests
import datetime
from streamlit_mic_recorder import mic_recorder

# --- Configuration du chemin de l'image de fond ---
current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, "images", "4 - Elavira (1).png") # Assurez-vous que ce chemin est correct

# --- Configuration de la page Streamlit (pour l'esthétique) ---
st.set_page_config(layout="wide") # Utilise toute la largeur de l'écran

# CSS pour masquer le menu Streamlit et le footer "Made with Streamlit"
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    /* Attention: masquer le header peut aussi masquer le menu hamburger qui contient l'option de thème clair/sombre */
    /* header {visibility: hidden;} */
    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Fonction pour ajouter une image de fond
def add_bg_from_local(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: 47% auto;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# --- Titre et fond de l'application Streamlit ---
st.title("Bienvenue sur Elavira 🤖")
add_bg_from_local(image_path)
st.write("---")

# --- Configuration de l'API FastAPI ---
FASTAPI_BASE_URL = "http://127.0.0.1:8000"

# --- Initialisation de l'état de la session Streamlit ---
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'access_token' not in st.session_state:
    st.session_state.access_token = None
if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None

# --- Fonctions pour interagir avec l'API de chat ---
def send_message_to_api(message_text, user_id=1):
    endpoint = f"{FASTAPI_BASE_URL}/chat/send_message/"
    payload = {"text": message_text, "user_id": user_id}

    # Utilise le nom d'utilisateur connecté comme user_id pour le message
    if st.session_state.logged_in_user:
        payload["user_id"] = st.session_state.logged_in_user
    else:
        payload["user_id"] = "Guest" # Utilisateur invité si non connecté

    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        st.session_state.messages.append(response.json())
        st.success("Message envoyé à l'API ! 🎉")
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de l'envoi du message à l'API : {e}")
        return False

def fetch_chat_history_from_api():
    endpoint = f"{FASTAPI_BASE_URL}/chat/history/"
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        history = response.json()
        st.session_state.messages = history
        st.success("Historique des messages récupéré de l'API. 📚")
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la récupération de l'historique : {e}")

# --- Section Authentification (Améliorée avec st.columns) ---
st.header("Authentification Utilisateur 🔐")

# Utilisation de colonnes pour un alignement horizontal des inputs
col_register, col_login = st.columns(2)

with col_register:
    st.subheader("Créer un nouveau compte ✨")
    new_username = st.text_input("Nom d'utilisateur", key="new_username_input_col")
    new_password = st.text_input("Mot de passe", type="password", key="new_password_input_col")

    if st.button("S'inscrire", key="register_button_col"):
        if new_username and new_password:
            register_endpoint = f"{FASTAPI_BASE_URL}/users/register/"
            payload = {"username": new_username, "password": new_password}
            try:
                response = requests.post(register_endpoint, json=payload)
                response.raise_for_status()
                st.success(f"Compte '{new_username}' créé avec succès ! Bienvenue !")
                st.session_state.new_username_input_col = "" # Vide le champ
                st.session_state.new_password_input_col = "" # Vide le champ
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 400:
                    st.error(f"Erreur d'inscription : {e.response.json().get('detail', '''Nom d'utilisateur déjà pris ou autre erreur.''')}")
                else:
                    st.error(f"Erreur lors de l'inscription : {e}")
            except requests.exceptions.RequestException as e:
                st.error(f"Erreur de connexion à l'API lors de l'inscription : {e}")
        else:
            st.warning("Veuillez saisir un nom d'utilisateur et un mot de passe.")

with col_login:
    st.subheader("Se connecter 👋")
    login_username = st.text_input("Nom d'utilisateur", key="login_username_input_col")
    login_password = st.text_input("Mot de passe", type="password", key="login_password_col")

    if st.button("Se connecter", key="login_button_col"):
        if login_username and login_password:
            login_endpoint = f"{FASTAPI_BASE_URL}/users/login/"
            payload = {"username": login_username, "password": login_password}
            try:
                response = requests.post(login_endpoint, json=payload)
                response.raise_for_status()
                token_data = response.json()
                st.success(f"Connexion réussie ! Vous êtes maintenant connecté en tant que {login_username}.")
                st.session_state.access_token = token_data.get('access_token')
                st.session_state.logged_in_user = login_username
                st.session_state.login_username_input_col = "" # Vide le champ
                st.session_state.login_password_col = "" # Vide le champ
                st.rerun() # Rafraîchit pour afficher l'état de connexion
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 401:
                    st.error("Échec de la connexion : Nom d'utilisateur ou mot de passe incorrect.")
                else:
                    st.error(f"Erreur de connexion : {e}")
            except requests.exceptions.RequestException as e:
                st.error(f"Erreur de connexion à l'API lors de la connexion : {e}")
        else:
            st.warning("Veuillez saisir un nom d'utilisateur et un mot de passe.")

if st.session_state.logged_in_user:
    st.info(f"Vous êtes connecté en tant que : **{st.session_state.logged_in_user}** 🎉")
    if st.button("Se déconnecter", key="logout_button"):
        st.session_state.access_token = None
        st.session_state.logged_in_user = None
        st.success("Vous êtes déconnecté. À bientôt !")
        st.rerun()

st.write("---")

# --- Interface utilisateur du chat ---
st.header("Interface de Chat avec Elavira 💬")

if st.button("Obtenir le statut du chat de l'API 📡"):
    try:
        response = requests.get(f"{FASTAPI_BASE_URL}/chat/")
        response.raise_for_status()
        data = response.json()
        st.success(f"Statut de l'API (Chat) : {data['message']}")
        st.json(data)
    except requests.exceptions.ConnectionError:
        st.error(f"Erreur de connexion : Assurez-vous que votre API FastAPI est lancée sur {FASTAPI_BASE_URL}")
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la requête API : {e}")

# Section pour la reconnaissance vocale
st.subheader("Parlez à Elavira 🎤 ou Écrivez ✍️")
recorded_audio_data = mic_recorder(
    start_prompt="Commencer à parler",
    stop_prompt="Arrêter l'enregistrement",
    key='mic_recorder_chat'
)

# Champ de message textuel (peut être pré-rempli par la transcription vocale)
chat_input_key = "chat_message_input"
if chat_input_key not in st.session_state:
    st.session_state[chat_input_key] = ""

# Si de nouvelles données vocales sont enregistrées, mettez à jour le champ de texte
if recorded_audio_data:
    if isinstance(recorded_audio_data, dict) and 'text' in recorded_audio_data and recorded_audio_data['text']:
        st.session_state[chat_input_key] = recorded_audio_data['text']
        st.success("Transcription vocale : " + recorded_audio_data['text'])
    elif isinstance(recorded_audio_data, str) and recorded_audio_data:
        st.session_state[chat_input_key] = recorded_audio_data
        st.success("Transcription vocale : " + recorded_audio_data)
    else:
        st.warning("Aucune transcription vocale détectée ou l'audio seul a été renvoyé. 🔇")

# Le champ de texte interactif (sa valeur est contrôlée par session_state)
message_input_from_text_or_voice = st.text_input(
    "Votre message :",
    value=st.session_state[chat_input_key],
    key=chat_input_key,
    placeholder="Tapez votre message ou utilisez le micro...",
)

# Bouton pour envoyer le message (qu'il vienne du texte ou de la voix)
if st.button("Envoyer le message 🚀", key="send_chat_button"):
    if message_input_from_text_or_voice:
        # user_id est ajusté dans la fonction send_message_to_api
        success = send_message_to_api(message_input_from_text_or_voice)
        if success:
            st.session_state[chat_input_key] = "" # Vide le champ de saisie
            fetch_chat_history_from_api() # Actualise l'historique
            st.rerun() # Pour rafraîchir l'interface et afficher les changements
    else:
        st.warning("Veuillez saisir ou dicter un message. 🤔")

st.write("---")

# Historique des messages (Amélioré avec st.chat_message)
st.subheader("Historique des conversations 📜")

# Charger l'historique initial si ce n'est pas déjà fait
if not st.session_state.messages:
    fetch_chat_history_from_api()

if not st.session_state.messages:
    st.info("Aucun message dans l'historique. Envoyez un message ou parlez. 🗣️")
else:
    for msg in st.session_state.messages:
        timestamp = msg.get('timestamp', 'N/A')
        try:
            dt_object = datetime.datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            formatted_timestamp = dt_object.strftime("%H:%M:%S") # Heure, Minute, Seconde
        except ValueError:
            formatted_timestamp = timestamp # Garde l'original si le format n'est pas bon

        sender_id = msg.get('user_id', 'Inconnu')
        message_text = msg.get('text', '')

        # Déterminer le rôle pour st.chat_message
        if st.session_state.logged_in_user and sender_id == st.session_state.logged_in_user:
            with st.chat_message("user"): # Avatar par défaut de l'utilisateur
                st.write(f"**Vous** à {formatted_timestamp}:")
                st.write(message_text)
        elif sender_id == "Elavira Assistant": # Supposons que l'agent Ollama envoie des messages avec cet ID
            with st.chat_message("assistant"): # Avatar par défaut de l'assistant
                st.write(f"**Elavira** à {formatted_timestamp}:")
                st.write(message_text)
        else: # Pour les autres utilisateurs (ex: "Guest" ou user_id 1 si non connecté)
            with st.chat_message("user"): # On utilise "user" par défaut pour les messages des utilisateurs
                st.write(f"**{sender_id}** à {formatted_timestamp}:")
                st.write(message_text)

st.write("---")

# --- Section Agents ---
st.header("Gestion et Interaction avec les Agents 🤖")

# Bouton pour lister tous les agents
if st.button("Lister tous les agents disponibles 🔍"):
    agents_endpoint = f"{FASTAPI_BASE_URL}/agents/"
    try:
        response = requests.get(agents_endpoint)
        response.raise_for_status()
        agents_list = response.json()
        st.subheader("Agents disponibles :")
        if agents_list:
            for agent in agents_list:
                st.json(agent)
        else:
            st.info("Aucun agent trouvé. 😔")
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la récupération des agents : {e}")

st.subheader("Interagir avec un Agent Spécifique 🗣️")
st.info("L'agent 'Elavira Assistant' (agent-001) est configuré pour utiliser Ollama. 🧠")

selected_agent_id = st.selectbox(
    "Choisissez un agent avec lequel interagir :",
    options=["agent-001", "agent-002", "agent-003"], # Listez vos IDs d'agents ici
    key="selected_agent_id"
)

agent_message_input = st.text_input(
    f"Message pour l'agent {selected_agent_id}:",
    key="agent_message_input",
    placeholder="Demandez quelque chose à l'agent..."
)

if st.button(f"Envoyer à {selected_agent_id} ➡️", key="send_to_agent_button"):
    if agent_message_input and selected_agent_id:
        interact_endpoint = f"{FASTAPI_BASE_URL}/agents/interact/{selected_agent_id}"
        payload = {"text": agent_message_input}
        try:
            response = requests.post(interact_endpoint, json=payload)
            response.raise_for_status()
            agent_response_data = response.json()

            response_text = agent_response_data.get("response", "Aucune réponse valide de l'agent.")
            st.write(f"**Réponse de l'agent {agent_response_data.get('agent_name', selected_agent_id)} :**")
            st.info(response_text)

            # Ajoute la réponse de l'agent à l'historique global du chat pour un affichage continu
            st.session_state.messages.append({
                "user_id": agent_response_data.get('agent_name', selected_agent_id),
                "text": response_text,
                "timestamp": datetime.datetime.now().isoformat() + "Z" # Horodatage actuel
            })
            st.rerun() # Pour rafraîchir l'historique du chat

            st.session_state.agent_message_input = "" # Vide le champ après envoi
        except requests.exceptions.HTTPError as e:
            error_detail = e.response.json().get('detail', 'Erreur inconnue de l\'agent. ❌')
            st.error(f"Erreur lors de l'interaction avec l'agent : {error_detail}")
        except requests.exceptions.RequestException as e:
            st.error(f"Erreur de connexion à l'API lors de l'interaction avec l'agent : {e} 🔌")
    else:
        st.warning("Veuillez saisir un message pour l'agent. 📝")