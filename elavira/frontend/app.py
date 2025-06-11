# app.py (Votre script Streamlit complet et corrigé - Version 3)

import streamlit as st
import base64
import os
import requests # Assurez-vous que requests est importé

# --- Configuration du chemin de l'image de fond ---
current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, "images", "4 - Elavira (1).png")

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
    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        st.session_state.messages.append(response.json())
        st.success("Message envoyé à l'API !")
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
        st.success("Historique des messages récupéré de l'API.")
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la récupération de l'historique : {e}")

# --- Section Authentification ---
st.header("Authentification Utilisateur")

tab_register, tab_login = st.tabs(["S'inscrire", "Se connecter"])

with tab_register:
    st.subheader("Créer un nouveau compte")
    new_username = st.text_input("Nom d'utilisateur", key="new_username_input")
    new_password = st.text_input("Mot de passe", type="password", key="new_password_input")

    if st.button("S'inscrire", key="register_button"):
        if new_username and new_password:
            register_endpoint = f"{FASTAPI_BASE_URL}/users/register/"
            payload = {"username": new_username, "password": new_password}
            try:
                response = requests.post(register_endpoint, json=payload)
                response.raise_for_status()
                st.success(f"Compte '{new_username}' créé avec succès !")
                st.session_state.new_username_input = ""
                st.session_state.new_password_input = ""
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 400:
                    # CORRECTION APPLIQUÉE ICI : Utilisation de triples guillemets pour la chaîne interne
                    st.error(f"Erreur d'inscription : {e.response.json().get('detail', '''Nom d'utilisateur déjà pris ou autre erreur.''')}")
                else:
                    st.error(f"Erreur lors de l'inscription : {e}")
            except requests.exceptions.RequestException as e:
                st.error(f"Erreur de connexion à l'API lors de l'inscription : {e}")
        else:
            st.warning("Veuillez saisir un nom d'utilisateur et un mot de passe.")

with tab_login:
    st.subheader("Se connecter")
    login_username = st.text_input("Nom d'utilisateur", key="login_username_input")
    login_password = st.text_input("Mot de passe", type="password", key="login_password_input")

    if st.button("Se connecter", key="login_button"):
        if login_username and login_password:
            login_endpoint = f"{FASTAPI_BASE_URL}/users/login/"
            payload = {"username": login_username, "password": login_password}
            try:
                response = requests.post(login_endpoint, json=payload)
                response.raise_for_status()
                token_data = response.json()
                st.success(f"Connexion réussie ! Token : {token_data.get('access_token')}")
                st.session_state.access_token = token_data.get('access_token')
                st.session_state.logged_in_user = login_username
                st.session_state.login_username_input = ""
                st.session_state.login_password_input = ""
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
    st.info(f"Vous êtes connecté en tant que : {st.session_state.logged_in_user}")
    if st.button("Se déconnecter", key="logout_button"):
        st.session_state.access_token = None
        st.session_state.logged_in_user = None
        st.success("Vous êtes déconnecté.")
        st.rerun() # Rafraîchit l'application pour mettre à jour l'interface

st.write("---")

# --- Interface utilisateur du chat ---
st.header("Interface de Chat avec Elavira")

if st.button("Obtenir le statut du chat de l'API"):
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

message_input = st.text_input("Tapez votre message ici :", key="chat_message_input")

if st.button("Envoyer le message", key="send_chat_button"):
    if message_input:
        send_message_to_api(message_input, user_id=1)
        st.session_state.chat_message_input = ""
    else:
        st.warning("Veuillez taper un message.")

if st.button("Actualiser l'historique du chat", key="refresh_chat_button"):
    fetch_chat_history_from_api()

st.write("---")

st.subheader("Historique des conversations")

if not st.session_state.messages:
    st.info("Aucun message dans l'historique. Envoyez un message ou actualisez.")
else:
    for msg in st.session_state.messages:
        st.text(f"Utilisateur {msg.get('user_id', 'Inconnu')} [{msg.get('timestamp', 'N/A')}]: {msg.get('text', '')}")