import streamlit as st
import base64
import os
import requests
from streamlit_mic_recorder import mic_recorder
from datetime import datetime
import uuid
import json

# --- Configuration ---
st.set_page_config(page_title="Elavira - Formations", layout="wide")

# --- CSS pour style esthétique et corrections ---
st.markdown("""
    <style>
    /* General App Styling */
    .stApp {
        font-family: 'Segoe UI', sans-serif;
        background-color: #fefefe;
        display: flex;
        flex-direction: column;
        height: 100vh;
        margin: 0;
        padding: 0;
    }
    .main .block-container {
        flex: 1;
        display: flex;
        flex-direction: column;
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    div.st-emotion-cache-z5fcl4.ezrtsby0, div.st-emotion-cache-1cypd85.e1g8p9l0 {
        padding-left: 1rem;
        padding-right: 1rem;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #2c3e50;
        font-weight: 600;
    }
    .stButton button {
        border-radius: 20px;
        padding: 8px 20px;
        background-color: #3b82f6;
        color: white;
        border: none;
        margin-top: 8px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .stButton button:hover:not(:disabled) {
        background-color: #2e6bb4;
    }
    .stButton button:disabled {
        background-color: #a0a0a0;
        cursor: not-allowed;
    }
    .stTextInput > div > div > input {
        border-radius: 20px;
        padding: 12px 18px;
        background-color: #ffffff;
        border: 1px solid #dcdcdc;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.08);
    }
    .stTextInput > label {
        font-weight: 600;
        color: #34495e;
    }
    /* Chat Messages Styling */
    .chat-message-row {
        display: flex;
        width: 100%;
        margin-bottom: 12px;
    }
    .chat-message {
        border-radius: 20px;
        padding: 10px 18px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        max-width: 80%;
        word-wrap: break-word;
        display: flex;
        align-items: flex-start;
        gap: 12px;
        line-height: 1.4;
    }
    /* CORRECTION ICI : Inversion des couleurs et de l'alignement */
    .user-message {
        background-color: #dcfce7; /* Vert clair pour l'utilisateur */
        border-bottom-right-radius: 5px;
        margin-left: auto;
        flex-direction: row-reverse;
    }
    .assistant-message {
        background-color: #e1f0ff; /* Bleu clair pour l'assistant */
        border-bottom-left-radius: 5px;
        margin-right: auto;
    }
    .chat-message b {
        font-weight: 700;
        color: #2c3e50;
    }
    .chat-message .message-content {
        flex-grow: 1;
    }
    .chat-message .timestamp {
        font-size: 0.8em;
        color: #777;
        margin-left: 5px;
    }
    .user-message .timestamp {
        text-align: right; /* Le timestamp de l'utilisateur est à droite */
    }
    .assistant-message .timestamp {
        text-align: left; /* Le timestamp de l'assistant est à gauche */
    }
    /* Avatar Styling */
    .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        object-fit: cover;
        flex-shrink: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 1.2em;
        font-weight: bold;
        color: white;
        background-color: #ccc;
        border: 2px solid #ffffff;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .user-avatar {
        background-color: #3b82f6;
    }
    .assistant-avatar {
        background-color: #88c0d0;
    }
    .user-avatar-image {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #ffffff;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        flex-shrink: 0;
    }
    /* Thinking/Transcribing Indicators */
    .typing-indicator {
        font-style: italic;
        color: #666;
        padding: 8px 15px;
        border-radius: 15px;
        background-color: #f0f0f0;
        display: inline-block;
        max-width: fit-content;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        position: relative;
        animation: pulse 1.5s infinite;
    }
    .typing-indicator.user-side {
        margin-right: auto;
        margin-left: 12px;
    }
    .typing-indicator.assistant-thinking {
        margin-left: auto;
        margin-right: 12px;
    }
    @keyframes pulse {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.02); opacity: 0.9; }
        100% { transform: scale(1); opacity: 1; }
    }
    .st-emotion-cache-1q1n031.e1pxm3cf4 {
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        background-color: #ffffff;
        padding: 15px;
        flex-grow: 1;
        overflow-y: auto;
        min-height: 200px;
        max-height: calc(100vh - 250px);
        margin-bottom: 15px;
    }
    /* CORRECTION ICI : Ajustement de la hauteur du champ de saisie */
    .fixed-bottom-input {
        position: sticky;
        bottom: 0;
        background-color: #fefefe;
        padding: 15px 0 0;
        border-top: 1px solid #eee;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
        z-index: 100;
        width: 100%;
        min-height: 80px; /* Ajout d'une hauteur minimale */
    }
    .stVerticalBlock {
        gap: 0px;
    }
    .stButton {
        width: 100%;
    }
    .stButton > button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# --- Utilitaire image base64 ---
def get_image_base64(path):
    script_dir = os.path.dirname(__file__)
    full_path = os.path.join(script_dir, path)
    if not os.path.exists(full_path):
        return ""
    try:
        with open(full_path, "rb") as img:
            return base64.b64encode(img.read()).decode()
    except Exception as e:
        return ""

# --- Arrière-plan image ---
def add_bg(image_file_name):
    script_dir = os.path.dirname(__file__)
    image_file_path = os.path.join(script_dir, "images", image_file_name)
    if os.path.exists(image_file_path):
        try:
            with open(image_file_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
            st.markdown(f"""
                <style>
                .stApp {{
                    background-image: url("data:image/png;base64,{encoded}");
                    background-size: cover;
                    background-position: center top;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                }}
                </style>
            """, unsafe_allow_html=True)
        except Exception as e:
            print(f"[DEBUG] Erreur lors de l'ajout de l'image de fond {image_file_path}: {e}")
    else:
        print(f"[DEBUG] Image de fond non trouvée : {image_file_path}")

# --- Init session_state ---
def init_session():
    defaults = {
        "page": "auth",
        "messages": [],
        "access_token": None,
        "logged_in_user": None,
        "selected_agent_id": "agent-001",
        "transcribing": False,
        "thinking": False,
        "prefill_login_username": "",
        "prefill_login_password": "",
        "last_suggested_prompts": [],
        "display_suggestions": False,
        "message_input": "",
        "audio_enabled": True, # Ajout de l'état pour l'audio
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

# --- API endpoints ---
FASTAPI_BASE_URL = "http://localhost:8000"

def send_message_to_api(text):
    if not text.strip():
        return None

    response_json = None
    try:
        if st.session_state.selected_agent_id == "agent-001":
            # Endpoint pour Elavira
            endpoint = f"{FASTAPI_BASE_URL}/chat/send_message/"
            payload = {
                "text": text,
                "user_id": st.session_state.logged_in_user or "Guest",
                "agent_id": st.session_state.selected_agent_id
            }
            print(f"[DEBUG] Envoi du message à Elavira: {payload}")
            r = requests.post(endpoint, json=payload, timeout=120)
            r.raise_for_status()
            response_json = r.json()
        elif st.session_state.selected_agent_id == "agent-002":
            # Endpoint pour Solenys
            endpoint = f"{FASTAPI_BASE_URL}/solenys/solenys_query"
            print(f"[DEBUG] Envoi du message à Solenys: {text}")
            r = requests.get(endpoint, params={"q": text}, timeout=120)
            r.raise_for_status()
            response_json = r.json().get("answer")
        else:
            st.error("Agent sélectionné inconnu.")
            return None
    except requests.exceptions.Timeout:
        st.error("Délai de connexion à l'API dépassé. Veuillez réessayer.")
        return None
    except requests.exceptions.ConnectionError:
        st.error("Impossible de se connecter au serveur backend FastAPI. Assurez-vous qu'il est en cours d'exécution.")
        st.error("Veuillez lancer votre backend FastAPI avec la commande : `uvicorn main:app --reload` dans le dossier de votre API.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de l'envoi du message à l'API: {e}")
        return None
    
    if not isinstance(response_json, dict) or "text" not in response_json:
        st.error(f"Réponse de l'API inattendue pour l'agent {st.session_state.selected_agent_id}: {response_json}")
        return {
            "id": datetime.now().isoformat() + "_error_" + str(uuid.uuid4())[:8],
            "text": f"Désolé, une erreur s'est produite avec la réponse de {st.session_state.selected_agent_id}.",
            "user_id": "Assistant",
            "timestamp": datetime.now().isoformat()
        }

    if "id" not in response_json or not response_json["id"]:
        response_json["id"] = datetime.now().isoformat() + "_assistant_response_" + str(uuid.uuid4())[:8]

    st.session_state.last_suggested_prompts = response_json.get("suggested_prompts", [])
    st.session_state.display_suggestions = False
        
    return response_json

def fetch_chat_history():
    try:
        user_id_param = st.session_state.logged_in_user or "Guest"
        r = requests.get(f"{FASTAPI_BASE_URL}/chat/history/?agent_id={st.session_state.selected_agent_id}&user_id={user_id_param}", timeout=60)
        r.raise_for_status()
        history_messages = r.json()
        for msg in history_messages:
            if "id" not in msg or not msg["id"]:
                msg["id"] = datetime.now().isoformat() + "_history_" + str(uuid.uuid4())[:8]
            if msg.get("user_id") == "Solenys":
                msg["user_id"] = "Solenys Assistant"
            elif msg.get("user_id") == "Elavira":
                msg["user_id"] = "Elavira Assistant"
        st.session_state.messages = history_messages
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la récupération de l'historique: {e}")
        st.session_state.messages = []

def transcribe_audio(audio_bytes):
    files = {'audio_file': ("audio.wav", audio_bytes, "audio/wav")}
    try:
        r = requests.post(f"{FASTAPI_BASE_URL}/chat/transcribe_audio/", files=files, timeout=120)
        r.raise_for_status()
        return r.json().get("transcribed_text", "")
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la transcription audio: {e}")
        return None

def handle_send_click():
    user_message_text = st.session_state.message_input.strip()
    if user_message_text:
        current_time_iso = datetime.now().isoformat()
        st.session_state.messages.append({
            "id": current_time_iso + "_user_msg_" + str(uuid.uuid4())[:8],
            "text": user_message_text,
            "user_id": st.session_state.logged_in_user or "Vous",
            "timestamp": current_time_iso
        })
        st.session_state.message_input = ""
        st.session_state.thinking = True
        st.session_state.display_suggestions = False
        st.rerun()

def process_message_and_get_response():
    if st.session_state.thinking or st.session_state.transcribing:
        last_user_message = None
        for i in reversed(range(len(st.session_state.messages))):
            msg = st.session_state.messages[i]
            if msg.get("user_id") == (st.session_state.logged_in_user or "Vous"):
                has_assistant_response = any(
                    st.session_state.messages[j].get("user_id") in ["Elavira Assistant", "Solenys Assistant"]
                    for j in range(i + 1, len(st.session_state.messages))
                )
                if not has_assistant_response:
                    last_user_message = msg
                    break

        if last_user_message:
            assistant_response = send_message_to_api(last_user_message["text"])
            if assistant_response:
                st.session_state.messages.append(assistant_response)
        
        st.session_state.thinking = False
        st.session_state.transcribing = False
        st.rerun()

def handle_mic_input(audio_bytes):
    if audio_bytes:
        st.session_state.transcribing = True
        st.session_state.thinking = False
        st.rerun()
        transcribed_text = transcribe_audio(audio_bytes)
        if transcribed_text:
            current_time_iso = datetime.now().isoformat()
            st.session_state.messages.append({
                "id": current_time_iso + "_mic_user_msg_" + str(uuid.uuid4())[:8],
                "text": transcribed_text,
                "user_id": st.session_state.logged_in_user or "Vous",
                "timestamp": current_time_iso
            })
            st.session_state.message_input = ""
            st.session_state.transcribing = False
            st.session_state.thinking = True
            st.session_state.display_suggestions = False
            st.rerun()

# --- Auth UI ---
def auth_ui():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("Bienvenue sur Elavira 👋")
        st.subheader("Connectez-vous")
        st.text_input("Nom d'utilisateur", key="login_input_username", placeholder="Votre nom d'utilisateur")
        st.text_input("Mot de passe", type="password", key="login_input_password", placeholder="Votre mot de passe")
        if st.button("Se connecter", key="login_button"):
            if st.session_state.login_input_username and st.session_state.login_input_password:
                try:
                    response = requests.post(f"{FASTAPI_BASE_URL}/users/login/", json={
                        "username": st.session_state.login_input_username,
                        "password": st.session_state.login_input_password
                    })
                    response.raise_for_status()
                    if response.status_code == 200:
                        st.session_state.access_token = response.json().get("access_token")
                        st.session_state.logged_in_user = st.session_state.login_input_username
                        st.session_state.page = "chat"
                        fetch_chat_history()
                        st.rerun()
                except requests.exceptions.HTTPError as err:
                    st.error("Nom d'utilisateur ou mot de passe incorrect." if err.response.status_code == 401 else f"Erreur de connexion: {err.response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Impossible de se connecter au serveur backend FastAPI. Erreur : {e}")
            else:
                st.warning("Veuillez remplir tous les champs.")

        st.markdown("---")
        st.subheader("Nouvel utilisateur ?")
        st.write("Créez un compte pour accéder à toutes les fonctionnalités.")
        with st.expander("S'inscrire", expanded=False):
            st.text_input("Nouveau nom d'utilisateur", key="register_new_username", placeholder="Choisissez un nom d'utilisateur")
            st.text_input("Nouveau mot de passe", type="password", key="register_new_password", placeholder="Choisissez un mot de passe")
            if st.button("Créer mon compte", key="register_button_expander"):
                if st.session_state.register_new_username and st.session_state.register_new_password:
                    try:
                        response = requests.post(f"{FASTAPI_BASE_URL}/users/register/", json={
                            "username": st.session_state.register_new_username,
                            "password": st.session_state.register_new_password
                        })
                        response.raise_for_status()
                        if response.status_code == 201:
                            st.success("Compte créé avec succès ! Vous pouvez maintenant vous connecter.")
                            st.session_state.prefill_login_username = st.session_state.register_new_username
                            st.session_state.prefill_login_password = st.session_state.register_new_password
                            st.rerun()
                    except requests.exceptions.HTTPError as err:
                        st.warning("Ce nom d'utilisateur est déjà pris." if err.response.status_code == 400 else f"Erreur lors de l'inscription: {err.response.text}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Impossible de se connecter au serveur backend FastAPI. Erreur : {e}")
                else:
                    st.warning("Veuillez remplir tous les champs.")

# --- Chat UI ---
def chat_ui():
    st.title("Messagerie intelligente 💬")
    col_header_left, col_header_right = st.columns([3, 1])
    with col_header_left:
        st.write(f"Connecté en tant que **{st.session_state.logged_in_user}**")
    with col_header_right:
        if st.button("Se déconnecter", key="logout_button_chat_page"):
            st.session_state.page = "auth"
            st.session_state.logged_in_user = None
            st.session_state.messages = []
            st.session_state.access_token = None
            st.session_state.last_suggested_prompts = []
            st.session_state.display_suggestions = False
            st.rerun()

    agent_options = [("Elavira", "agent-001"), ("Solenys", "agent-002")]
    current_agent_index = next((i for i, (_, id_val) in enumerate(agent_options) if id_val == st.session_state.selected_agent_id), 0)
    selected_agent_display, selected_agent_id_new = st.selectbox(
        "Choisissez votre assistant :",
        options=agent_options,
        format_func=lambda x: x[0],
        index=current_agent_index,
        key="agent_selector"
    )

    if st.session_state.selected_agent_id != selected_agent_id_new:
        st.session_state.selected_agent_id = selected_agent_id_new
        st.session_state.messages = []
        st.session_state.last_suggested_prompts = []
        st.session_state.display_suggestions = False
        fetch_chat_history()
        st.rerun()

    st.write("---")

    chat_history_display_container = st.container(height=500, border=False)

    with chat_history_display_container:
        if not st.session_state.messages and not st.session_state.thinking and not st.session_state.transcribing:
            st.info("Aucun message dans l'historique. Commencez la conversation ci-dessous !")

        for msg in st.session_state.messages:
            if "id" not in msg or not msg["id"]:
                msg["id"] = datetime.now().isoformat() + "_display_fallback_" + str(uuid.uuid4())[:8]

            is_assistant_message = msg.get("user_id") in ["Elavira Assistant", "Solenys Assistant"]
            style_class = "assistant-message" if is_assistant_message else "user-message"
            
            timestamp_raw = msg.get("timestamp", "")
            timestamp = ""
            if timestamp_raw:
                try:
                    dt_obj = datetime.fromisoformat(timestamp_raw.replace('Z', '+00:00'))
                    timestamp = dt_obj.strftime("%H:%M")
                except ValueError:
                    timestamp = timestamp_raw[11:16] if len(timestamp_raw) >= 16 else timestamp_raw

            elavira_avatar_b64 = get_image_base64(os.path.join("images", "elavira_assistant.png"))
            solenys_avatar_b64 = get_image_base64(os.path.join("images", "solenys_assistant.png"))
            user_avatar_b64 = get_image_base64(os.path.join("images", "4 - Elavira (1).png"))

            if is_assistant_message:
                avatar_html = ""
                if msg.get("user_id") == "Elavira Assistant" and elavira_avatar_b64:
                    avatar_html = f'<img src="data:image/png;base64,{elavira_avatar_b64}" class="avatar">'
                elif msg.get("user_id") == "Solenys Assistant" and solenys_avatar_b64:
                    avatar_html = f'<img src="data:image/png;base64,{solenys_avatar_b64}" class="avatar">'
                else:
                    avatar_html = '<div class="avatar assistant-avatar">?</div>'

                st.markdown(f'''
                    <div class="chat-message-row" style="justify-content: flex-start;">
                        <div class="chat-message {style_class}">
                            {avatar_html}
                            <div class="message-content">
                                <b>{msg.get("user_id", "Assistant")}</b> <span class="timestamp">({timestamp})</span><br>{msg.get("text", "...")}
                            </div>
                        </div>
                    </div>
                ''', unsafe_allow_html=True)
            else: # Message utilisateur
                avatar_html = ""
                if user_avatar_b64:
                    avatar_html = f'<img src="data:image/png;base64,{user_avatar_b64}" class="user-avatar-image">'
                else:
                    user_initial = st.session_state.logged_in_user[0].upper() if st.session_state.logged_in_user else "U"
                    avatar_html = f'<div class="avatar user-avatar">{user_initial}</div>'

                st.markdown(f'''
                    <div class="chat-message-row" style="justify-content: flex-end;">
                        <div class="chat-message {style_class}">
                            <div class="message-content">
                                <b>{msg.get("user_id", "Vous")}</b> <span class="timestamp">({timestamp})</span><br>{msg.get("text", "...")}
                            </div>
                            {avatar_html}
                        </div>
                    </div>
                ''', unsafe_allow_html=True)

            if is_assistant_message and msg.get("audio_base64") and st.session_state.audio_enabled:
                try:
                    audio_bytes = base64.b64decode(msg['audio_base64'])
                    st.audio(audio_bytes, format="audio/mp3")
                except Exception as e:
                    st.error(f"Erreur de décodage audio pour le message de {msg.get('user_id')}: {e}")

        if st.session_state.thinking:
            st.markdown(f'''<div class="chat-message-row" style="justify-content: flex-end;"><div class="typing-indicator assistant-thinking">⏳ Réflexion en cours...</div></div>''', unsafe_allow_html=True)
        if st.session_state.transcribing:
            st.markdown(f'''<div class="chat-message-row" style="justify-content: flex-start;"><div class="typing-indicator user-side">🎙️ Transcription en cours...</div></div>''', unsafe_allow_html=True)

    if st.session_state.last_suggested_prompts and not st.session_state.display_suggestions:
        st.markdown('<div style="text-align: center; margin-top: 15px; margin-bottom: 5px;">', unsafe_allow_html=True)
        if st.button("Afficher les suggestions de prompt", key="show_suggested_prompts_button"):
            st.session_state.display_suggestions = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.display_suggestions and st.session_state.last_suggested_prompts:
        st.markdown('<div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 5px; margin-bottom: 15px; justify-content: center;">', unsafe_allow_html=True)
        def handle_suggested_prompt_click(prompt_text):
            st.session_state.message_input = prompt_text
            st.session_state.display_suggestions = False
        for i, prompt in enumerate(st.session_state.last_suggested_prompts):
            st.button(prompt, key=f"displayed_suggested_prompt_{i}", on_click=handle_suggested_prompt_click, args=(prompt,))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="fixed-bottom-input">', unsafe_allow_html=True)
        col_input, col_mic, col_send, col_audio = st.columns([10, 1, 1, 1])
        input_disabled = st.session_state.thinking or st.session_state.transcribing
        send_disabled = input_disabled or not st.session_state.message_input
        with col_input:
            st.text_input("Votre message", key="message_input", placeholder="Écrivez votre message ici...", label_visibility="collapsed", disabled=input_disabled, on_change=handle_send_click)
        with col_mic:
            mic_recorder(start_prompt="🎙️", stop_prompt="⏹️", just_once=True, use_container_width=True, callback=handle_mic_input, key="mic_recorder", disabled=input_disabled)
        with col_send:
            st.button("🚀", key="send_button", on_click=handle_send_click, use_container_width=True, disabled=send_disabled)
        with col_audio:
            if st.session_state.audio_enabled:
                if st.button("🔊", key="disable_audio_button", use_container_width=True):
                    st.session_state.audio_enabled = False
                    st.rerun()
            else:
                if st.button("🔇", key="enable_audio_button", use_container_width=True):
                    st.session_state.audio_enabled = True
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    try:
        init_session()
        add_bg("fond_vagues_elavira.png")
        if st.session_state.page == "auth":
            auth_ui()
        elif st.session_state.page == "chat":
            chat_ui()
            process_message_and_get_response()
    except Exception as e:
        st.error(f"Une erreur inattendue s'est produite: {e}")
        st.stop()

if __name__ == "__main__":
    main()