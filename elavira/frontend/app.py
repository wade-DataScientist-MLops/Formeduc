import streamlit as st
import base64
import os
import requests
from streamlit_mic_recorder import mic_recorder

# --- Configuration ---
st.set_page_config(page_title="Elavira - Formations", layout="wide")

# --- CSS pour style esthétique ---
st.markdown("""
    <style>
    .stApp {
        font-family: 'Segoe UI', sans-serif;
        background-color: #fefefe;
    }
    .chat-message {
        background-color: #f9f9f9;
        border-radius: 20px;
        padding: 10px 20px;
        margin-bottom: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        max-width: 90%;
        word-wrap: break-word;
    }
    .assistant-message {
        background-color: #e1f0ff;
        align-self: flex-start;
    }
    .user-message {
        background-color: #dcfce7;
        align-self: flex-end;
    }
    .typing-indicator {
        font-style: italic;
        color: #666;
        margin: 8px 0 14px 0;
        padding-left: 8px;
    }
    .stTextInput > div > input {
        border-radius: 20px;
        padding: 12px;
        background-color: #ffffff;
        border: 1px solid #ccc;
    }
    .stButton button {
        border-radius: 20px;
        padding: 8px 20px;
        background-color: #3b82f6;
        color: white;
        border: none;
        margin-top: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Arrière-plan image (optionnel) ---
def add_bg(image_file):
    if os.path.exists(image_file):
        with open(image_file, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{encoded}");
                background-size: contain;
                background-position: center top;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            </style>
        """, unsafe_allow_html=True)

# --- Init session_state ---
def init_session():
    defaults = {
        "page": "auth",
        "messages": [],
        "access_token": None,
        "logged_in_user": None,
        "chat_input": "",
        "chat_message_input_final": "",
        "register_new_username": "",
        "register_new_password": "",
        "login_input_username": "",
        "login_input_password": "",
        "selected_agent_id": "agent-001",
        "transcribing": False,
        "thinking": False
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

# --- API endpoints ---
FASTAPI_BASE_URL = "http://127.0.0.1:8000"

def send_message_to_api(text):
    payload = {
        "text": text,
        "user_id": st.session_state.logged_in_user or "Guest",
        "agent_id": st.session_state.selected_agent_id
    }
    try:
        st.session_state.thinking = True
        r = requests.post(f"{FASTAPI_BASE_URL}/chat/send_message/", json=payload)
        r.raise_for_status()
        return r.json()
    except:
        return None
    finally:
        st.session_state.thinking = False

def fetch_chat_history():
    try:
        r = requests.get(f"{FASTAPI_BASE_URL}/chat/history/?agent_id={st.session_state.selected_agent_id}")
        r.raise_for_status()
        st.session_state.messages = r.json()
    except:
        st.session_state.messages = []

def transcribe_audio(audio_bytes):
    files = {'audio_file': ("audio.wav", audio_bytes, "audio/wav")}
    try:
        r = requests.post(f"{FASTAPI_BASE_URL}/chat/transcribe_audio/", files=files)
        r.raise_for_status()
        return r.json().get("transcribed_text", "")
    except:
        return None

# --- Auth UI ---
def auth_ui():
    st.title("Bienvenue sur Elavira 🤖")
    add_bg(os.path.join(os.path.dirname(__file__), "images", "4 - Elavira (1).png"))
    st.subheader("Connexion ou inscription")
    col1, col2 = st.columns(2)

    with col1:
        st.text_input("Nom d'utilisateur", key="register_new_username")
        st.text_input("Mot de passe", type="password", key="register_new_password")
        if st.button("S'inscrire"):
            if st.session_state.register_new_username and st.session_state.register_new_password:
                response = requests.post(f"{FASTAPI_BASE_URL}/users/register/", json={
                    "username": st.session_state.register_new_username,
                    "password": st.session_state.register_new_password
                })
                if response.status_code == 201:
                    st.success("Compte créé !")
                    st.session_state.page = "chat"
                    st.session_state.logged_in_user = st.session_state.register_new_username
                    st.rerun()
                elif response.status_code == 400:
                    st.warning("Ce nom d'utilisateur est déjà pris.")
                else:
                    st.error("Erreur lors de l'inscription.")

    with col2:
        st.text_input("Nom d'utilisateur", key="login_input_username")
        st.text_input("Mot de passe", type="password", key="login_input_password")
        if st.button("Se connecter"):
            if st.session_state.login_input_username and st.session_state.login_input_password:
                response = requests.post(f"{FASTAPI_BASE_URL}/users/login/", json={
                    "username": st.session_state.login_input_username,
                    "password": st.session_state.login_input_password
                })
                if response.status_code == 200:
                    token = response.json().get("access_token")
                    st.session_state.access_token = token
                    st.session_state.page = "chat"
                    st.session_state.logged_in_user = st.session_state.login_input_username
                    st.rerun()
                elif response.status_code == 401:
                    st.error("Nom d'utilisateur ou mot de passe incorrect.")
                else:
                    st.error("Erreur de connexion.")

# --- Chat UI ---
def chat_ui():
    st.title("Messagerie intelligente 💬")
    st.write(f"Connecté en tant que **{st.session_state.logged_in_user}**")

    agent = st.selectbox("Choisissez votre assistant :", [
        ("Elavira", "agent-001"),
        ("Solenys", "agent-002")
    ], format_func=lambda x: x[0])
    st.session_state.selected_agent_id = agent[1]

    if st.button("Se déconnecter"):
        st.session_state.page = "auth"
        st.session_state.logged_in_user = None
        st.session_state.messages = []
        st.rerun()

    st.write("---")

    # Historique messages
    for msg in st.session_state.messages:
        role = "assistant" if msg["user_id"] in ["Elavira Assistant", "Solenys"] else "user"
        style_class = "assistant-message" if role == "assistant" else "user-message"
        with st.chat_message(role):
            st.markdown(
                f'<div class="chat-message {style_class}"><b>{msg["user_id"]}</b> ({msg["timestamp"]})<br>{msg["text"]}</div>',
                unsafe_allow_html=True
            )
            if role == "assistant" and msg.get("audio_base64"):
                audio_bytes = base64.b64decode(msg['audio_base64'])
                st.audio(audio_bytes, format="audio/mp3")

    # ⏳ Indicateur de réflexion
    if st.session_state.thinking:
        with st.chat_message("assistant"):
            st.markdown('<div class="typing-indicator">⏳ Elavira réfléchit...</div>', unsafe_allow_html=True)

    # 🎤 Micro
    mic_data = mic_recorder("🎧 Démarrer", "🔝 Stop", key="mic")
    if mic_data and "bytes" in mic_data and not st.session_state.transcribing:
        st.session_state.transcribing = True
        text = transcribe_audio(mic_data["bytes"])
        if text:
            st.session_state.chat_input = text
            send_message_to_api(text)
            fetch_chat_history()
        st.session_state.transcribing = False
        st.rerun()

    # Champ de message
    st.text_input("Votre message ici...", key="chat_message_input_final", value=st.session_state.chat_input, on_change=lambda: setattr(st.session_state, "chat_input", st.session_state.chat_message_input_final))
    if st.button("Envoyer"):
        if st.session_state.chat_input:
            send_message_to_api(st.session_state.chat_input)
            st.session_state.chat_input = ""
            fetch_chat_history()
            st.rerun()

# --- Main ---
init_session()
if st.session_state.page == "auth":
    auth_ui()
elif st.session_state.page == "chat":
    chat_ui()
