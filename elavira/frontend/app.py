import streamlit as st
import base64
import os
import requests
import datetime
from streamlit_mic_recorder import mic_recorder

# --- Configuration de la page ---
st.set_page_config(layout="wide")

# --- Chemin image de fond ---
current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, "images", "4 - Elavira (1).png")

# --- Masquer éléments Streamlit ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- Ajout image de fond ---
def add_bg(image_file):
    if not os.path.exists(image_file):
        st.error(f"Image non trouvée : {image_file}")
        return
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
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

# --- URL API ---
FASTAPI_BASE_URL = "http://127.0.0.1:8000"

# --- Init session_state ---
defaults = {
    "messages": [],
    "access_token": None,
    "logged_in_user": None,
    "chat_input": "",
    "chat_message_input_final": "",
    "register_new_username": "",
    "register_new_password": "",
    "login_input_username": "",
    "login_input_password": "",
    "agent_message_input": "",
    "selected_agent_id": "agent-001"
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- UI ---
st.title("Bienvenue sur Elavira 🤖")
add_bg(image_path)
st.write("---")

# --- API functions ---
def send_message_to_api(text):
    endpoint = f"{FASTAPI_BASE_URL}/chat/send_message/"
    payload = {"text": text, "user_id": st.session_state.logged_in_user or "Guest"}
    try:
        r = requests.post(endpoint, json=payload)
        r.raise_for_status()
        st.success("Message envoyé ✅")
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur API : {e}")
        return False

def fetch_chat_history_from_api():
    try:
        r = requests.get(f"{FASTAPI_BASE_URL}/chat/history/")
        r.raise_for_status()
        st.session_state.messages = r.json()  # ✅ Correction ici
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur historique : {e}")

# --- Authentification ---
st.header("Authentification 🔐")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Créer un compte")
    st.text_input("Nom d'utilisateur", key="register_new_username")
    st.text_input("Mot de passe", type="password", key="register_new_password")
    if st.button("S'inscrire"):
        if st.session_state.register_new_username and st.session_state.register_new_password:
            payload = {
                "username": st.session_state.register_new_username,
                "password": st.session_state.register_new_password
            }
            try:
                res = requests.post(f"{FASTAPI_BASE_URL}/users/register/", json=payload)
                res.raise_for_status()
                st.success("Compte créé 🎉")
            except requests.exceptions.HTTPError as e:
                detail = e.response.json().get("detail", "Erreur")
                st.error(detail)
        else:
            st.warning("Champs vides")

with col2:
    st.subheader("Connexion")
    st.text_input("Nom d'utilisateur", key="login_input_username")
    st.text_input("Mot de passe", type="password", key="login_input_password")
    if st.button("Se connecter"):
        if st.session_state.login_input_username and st.session_state.login_input_password:
            payload = {
                "username": st.session_state.login_input_username,
                "password": st.session_state.login_input_password
            }
            try:
                res = requests.post(f"{FASTAPI_BASE_URL}/users/login/", json=payload)
                res.raise_for_status()
                data = res.json()
                st.session_state.access_token = data.get("access_token")
                st.session_state.logged_in_user = st.session_state.login_input_username
                st.success(f"Bienvenue {st.session_state.logged_in_user}")
                st.rerun()
            except requests.exceptions.HTTPError:
                st.error("Identifiants incorrects")
        else:
            st.warning("Champs vides")

if st.session_state.logged_in_user:
    st.info(f"Connecté : **{st.session_state.logged_in_user}**")
    if st.button("Se déconnecter"):
        st.session_state.logged_in_user = None
        st.session_state.access_token = None
        st.rerun()

st.write("---")

# --- Chat ---
st.header("Chat avec Elavira 💬")

if st.button("Tester l'API 📡"):
    try:
        res = requests.get(f"{FASTAPI_BASE_URL}/chat/")
        res.raise_for_status()
        st.success(res.json().get("message", "OK"))
    except:
        st.error("API non disponible")

# 🎙️ Micro + texte
st.subheader("Parlez ou écrivez")
audio_data = mic_recorder("🎙️ Démarrer", "🛑 Stop", key="mic_recorder_chat")

st.text_input(
    "Votre message",
    value=st.session_state.chat_input,
    key="chat_message_input_final",
    on_change=lambda: setattr(
        st.session_state, "chat_input", st.session_state.chat_message_input_final
    ),
    placeholder="Tapez un message ou utilisez le micro..."
)

if audio_data:
    text = audio_data.get("text", audio_data if isinstance(audio_data, str) else "")
    if text:
        st.session_state.chat_input = text
        st.success(f"🎤 Transcription : {text}")
        st.rerun()

# ➡️ Envoyer message
if st.button("Envoyer 🚀"):
    msg = st.session_state.chat_input.strip()
    if msg:
        if send_message_to_api(msg):
            st.session_state.chat_input = ""
            fetch_chat_history_from_api()
            st.rerun()
    else:
        st.warning("Message vide !")

st.write("---")

# --- Historique ---
st.subheader("Historique 📜")

if not st.session_state.messages:
    fetch_chat_history_from_api()

for msg in st.session_state.messages:
    user = msg.get("user_id", "inconnu")
    text = msg.get("text", "")
    ts = msg.get("timestamp", "???")
    try:
        time = datetime.datetime.fromisoformat(ts.replace("Z", "+00:00")).strftime("%H:%M:%S")
    except:
        time = ts
    role = "assistant" if user == "Elavira Assistant" else "user"
    with st.chat_message(role):
        st.write(f"**{user}** à {time} :")
        st.write(text)

st.write("---")

# --- Agents ---
st.header("Agents 🤖")

if st.button("Lister agents"):
    try:
        res = requests.get(f"{FASTAPI_BASE_URL}/agents/")
        res.raise_for_status()
        agents = res.json()
        st.subheader("Agents :")
        for a in agents:
            st.json(a)
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur agents : {e}")

st.subheader("Message à un agent")
agent_id = st.selectbox("Choisir un agent", ["agent-001", "agent-002", "agent-003"], key="selected_agent_id")
st.text_input(f"Message à {agent_id}", key="agent_message_input")

if st.button("Envoyer à l'agent"):
    msg = st.session_state.agent_message_input.strip()
    if msg:
        payload = {"text": msg}
        try:
            res = requests.post(f"{FASTAPI_BASE_URL}/agents/interact/{agent_id}", json=payload)
            res.raise_for_status()
            data = res.json()
            st.info(f"Réponse de {data.get('agent_name', agent_id)} :")
            st.success(data.get("response", "Aucune réponse"))
            st.session_state.messages.append({
                "user_id": data.get("agent_name", agent_id),
                "text": data.get("response", ""),
                "timestamp": datetime.datetime.now().isoformat() + "Z"
            })
            st.session_state.agent_message_input = ""
            st.rerun()
        except requests.exceptions.RequestException as e:
            st.error(f"Erreur interaction : {e}")
    else:
        st.warning("Message vide")
