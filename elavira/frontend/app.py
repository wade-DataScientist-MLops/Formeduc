import streamlit as st
import base64
import os
import requests
from streamlit_mic_recorder import mic_recorder
from datetime import datetime
import uuid
 
# --- Configuration ---
st.set_page_config(page_title="Elavira - Formations", layout="wide")

# --- CSS pour style esthétique ---
st.markdown("""
    <style>
    /* General App Styling - Use flexbox for the entire app */
    .stApp {
        font-family: 'Segoe UI', sans-serif;
        background-color: #fefefe; /* Very light grey */
        display: flex;
        flex-direction: column;
        height: 100vh; /* Make app take full viewport height */
        margin: 0;
        padding: 0;
    }

    /* Target the main content area of Streamlit */
    /* This class might change with Streamlit versions, inspect browser if needed */
    .main .block-container {
        flex: 1; /* Allow this container to grow and take available vertical space */
        display: flex;
        flex-direction: column;
        padding-top: 1rem; /* Adjust padding as needed */
        padding-bottom: 0rem; /* Remove default bottom padding as input is handled by sticky footer */
    }

    /* Adjust default padding around the main content */
    div.st-emotion-cache-z5fcl4.ezrtsby0, div.st-emotion-cache-1cypd85.e1g8p9l0 {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #2c3e50; /* Darker text for headers */
        font-weight: 600;
    }
    .stButton button {
        border-radius: 20px;
        padding: 8px 20px;
        background-color: #3b82f6; /* Streamlit blue, vibrant */
        color: white;
        border: none;
        margin-top: 8px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .stButton button:hover:not(:disabled) {
        background-color: #2e6bb4; /* Darker blue on hover */
    }
    .stButton button:disabled {
        background-color: #a0a0a0; /* Grey out disabled buttons */
        cursor: not-allowed;
    }

    .stTextInput > div > div > input { /* Targeting the actual input field */
        border-radius: 20px;
        padding: 12px 18px; /* More padding */
        background-color: #ffffff;
        border: 1px solid #dcdcdc; /* Lighter border */
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.08); /* Subtle inner shadow */
    }
    .stTextInput > label {
        font-weight: 600; /* Bolder labels */
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
        padding: 10px 18px; /* Adjusted padding */
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        max-width: 80%; /* Slightly smaller max width */
        word-wrap: break-word;
        display: flex;
        align-items: flex-start;
        gap: 12px; /* Increased gap between avatar and message */
        line-height: 1.4; /* Better readability */
    }

    /* ASSISTANT MESSAGES (Now on RIGHT) */
    .assistant-message {
        background-color: #e1f0ff; /* Light blue, for assistant */
        border-bottom-right-radius: 5px; /* Sharper corner at the tail side */
        margin-left: auto; /* Push to right */
        flex-direction: row-reverse; /* Puts avatar on the right */
    }

    /* USER MESSAGES (Now on LEFT) */
    .user-message {
        background-color: #dcfce7; /* Light green, for user */
        border-bottom-left-radius: 5px; /* Sharper corner at the tail side */
        margin-right: auto; /* Push to left */
        /* No flex-direction: row-reverse; needed as avatar is already at the start */
    }

    .chat-message b {
        font-weight: 700; /* Bolder names */
        color: #2c3e50;
    }
    .chat-message .message-content { /* New class for message content div */
        flex-grow: 1; /* Allow message content to take available space */
    }
    .chat-message .timestamp {
        font-size: 0.8em;
        color: #777;
        margin-left: 5px; /* Space from message */
    }
    /* Align user timestamp to the left for consistency if user messages are left */
    .user-message .timestamp {
        text-align: left;
    }
    /* Align assistant timestamp to the right for consistency if assistant messages are right */
    .assistant-message .timestamp {
        text-align: right;
    }


    /* Avatar Styling */
    .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        object-fit: cover;
        flex-shrink: 0; /* Prevent avatar from shrinking */
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 1.2em;
        font-weight: bold;
        color: white;
        background-color: #ccc; /* Default fallback background */
        border: 2px solid #ffffff; /* White border around avatars */
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .user-avatar {
        background-color: #3b82f6; /* User blue */
    }
    .assistant-avatar {
        background-color: #88c0d0; /* Elavira blue/grey */
    }

    /* Style pour l'image de profil utilisateur */
    .user-avatar-image {
        width: 30px; /* Taille de l'image (vous pouvez ajuster) */
        height: 30px; /* Conserve l'aspect ratio */
        border-radius: 50%; /* Pour une forme circulaire */
        object-fit: cover; /* Assure que l'image remplit le cercle sans déformation */
        border: 2px solid #ffffff; /* Bordure blanche autour de l'avatar */
        box-shadow: 0 1px 3px rgba(0,0,0,0.1); /* Légère ombre */
        flex-shrink: 0; /* Empêche l'image de rétrécir */
    }

    /* Thinking/Transcribing Indicators */
    .typing-indicator {
        font-style: italic;
        color: #666;
        padding: 8px 15px; /* Added padding */
        border-radius: 15px; /* Rounded corners */
        background-color: #f0f0f0; /* Light background */
        display: inline-block; /* To apply width/padding correctly */
        max-width: fit-content; /* Adjust width to content */
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        position: relative; /* For the thought bubble tail */
        animation: pulse 1.5s infinite; /* Gentle pulse animation */
    }

    /* User side typing indicator (now on LEFT) */
    .typing-indicator.user-side {
        margin-right: auto; /* Push to left for user side */
        margin-left: 12px;
    }
    /* Thought Bubble Tail for User Thinking (now on LEFT) */
    .typing-indicator.user-side::before {
        content: '';
        position: absolute;
        bottom: 0;
        left: -10px; /* Adjust to place the tail near the avatar */
        width: 0;
        height: 0;
        border: 10px solid transparent;
        border-bottom-color: #f0f0f0;
        border-left-color: #f0f0f0;
        border-radius: 0 0 0 10px;
        transform: rotate(45deg);
        transform-origin: bottom right;
    }


    /* Assistant thinking indicator (now on RIGHT) */
    .typing-indicator.assistant-thinking {
        margin-left: auto; /* Push to right for assistant side */
        margin-right: 12px;
    }
    /* Thought Bubble Tail for Assistant Thinking (now on RIGHT) */
    .typing-indicator.assistant-thinking::before {
        content: '';
        position: absolute;
        bottom: 0;
        right: -10px; /* Adjust to place the tail near the avatar */
        width: 0;
        height: 0;
        border: 10px solid transparent;
        border-bottom-color: #f0f0f0;
        border-right-color: #f0f0f0;
        border-radius: 0 0 10px 0; /* For a slightly curved tail base */
        transform: rotate(-45deg); /* Rotate to make it point downwards-right */
        transform-origin: bottom left; /* Rotate around this point */
    }


    /* Keyframe animation for pulse */
    @keyframes pulse {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.02); opacity: 0.9; }
        100% { transform: scale(1); opacity: 1; }
    }

    /* Container for chat messages with scroll */
    .st-emotion-cache-1q1n031.e1pxm3cf4 { /* This is a common class for st.container, check in browser if needed */
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        background-color: #ffffff;
        padding: 15px;
        flex-grow: 1; /* Allow it to take available space */
        overflow-y: auto; /* Enable vertical scrolling */
        min-height: 200px; /* Minimum height */
        max-height: calc(100vh - 250px); /* Adjust based on header/footer total height */
        margin-bottom: 15px; /* Space between chat history and input area */
    }


    /* Fixed Footer for input area - Position sticky to stick to bottom of its parent (main .block-container) */
    .fixed-bottom-input {
        position: sticky;
        bottom: 0; /* Stick to the bottom of the visible area */
        background-color: #fefefe; /* Match app background */
        padding: 15px 0 0; /* Padding above, none on sides/bottom */
        border-top: 1px solid #eee; /* Subtle border at the top */
        box-shadow: 0 -2px 10px rgba(0,0,0,0.05); /* Shadow above */
        z-index: 100; /* Ensure it stays on top */
        width: 100%; /* Take full width of its parent column */
    }

    /* Remove default gaps between Streamlit elements */
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
        print(f"[DEBUG] Image non trouvée à : {full_path}")
        return ""
    try:
        with open(full_path, "rb") as img:
            return base64.b64encode(img.read()).decode()
    except Exception as e:
        print(f"[DEBUG] Erreur de lecture de l'image {full_path}: {e}")
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
        "chat_input_text": "", # Cette clé est maintenant plus pour stocker la "valeur par défaut"
        "register_new_username": "",
        "register_new_password": "",
        "login_input_username": "",
        "login_input_password": "",
        "selected_agent_id": "agent-001",
        "transcribing": False,
        "thinking": False,
        "prefill_login_username": "",
        "prefill_login_password": "",
        "last_suggested_prompts": [],
        "display_suggestions": False,
        "message_input": "", # Nouvelle clé pour le contenu de l'input texte
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

# --- API endpoints ---
FASTAPI_BASE_URL = "http://localhost:8000"

def send_message_to_api(text):
    if not text.strip():
        print("[DEBUG] Tentative d'envoi de message vide, ignoré.")
        return None

    payload = {
        "text": text,
        "user_id": st.session_state.logged_in_user or "Guest",
        "agent_id": st.session_state.selected_agent_id
    }

    print(f"[DEBUG] Envoi du message à l'API : {payload}")
    try:
        r = requests.post(f"{FASTAPI_BASE_URL}/chat/send_message/", json=payload, timeout=120)
        r.raise_for_status()

        response_json = r.json()
        print(f"[DEBUG] Réponse de l'API : {response_json}")

        if "id" not in response_json or not response_json["id"]:
            response_json["id"] = datetime.now().isoformat() + "_assistant_response_" + str(uuid.uuid4())[:8]
            print(f"[DEBUG] ID de l'assistant généré: {response_json['id']}")

        if response_json.get("suggested_prompts"):
            st.session_state.last_suggested_prompts = response_json["suggested_prompts"]
            st.session_state.display_suggestions = False
        else:
            st.session_state.last_suggested_prompts = []
            st.session_state.display_suggestions = False

        return response_json
    except requests.exceptions.Timeout:
        st.error("Délai de connexion à l'API dépassé. Veuillez réessayer.")
        print("[ERROR] Timeout lors de l'envoi du message.")
        return None
    except requests.exceptions.ConnectionError:
        st.error("Impossible de se connecter au serveur backend FastAPI. Assurez-vous qu'il est en cours d'exécution.")
        st.error("Veuillez lancer votre backend FastAPI avec la commande : `uvicorn main:app --reload` dans le dossier de votre API.")
        print("[ERROR] Erreur de connexion au backend.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de l'envoi du message à l'API: {e}")
        print(f"[ERROR] Erreur de requête générale : {e}")
        return None
    finally:
        pass


def fetch_chat_history():
    print(f"[DEBUG] Récupération de l'historique pour user_id={st.session_state.logged_in_user} et agent_id={st.session_state.selected_agent_id}")
    try:
        user_id_param = st.session_state.logged_in_user or "Guest"
        r = requests.get(f"{FASTAPI_BASE_URL}/chat/history/?agent_id={st.session_state.selected_agent_id}&user_id={user_id_param}", timeout=60)
        r.raise_for_status()

        history_messages = r.json()

        for msg in history_messages:
            if "id" not in msg or not msg["id"]:
                msg["id"] = datetime.now().isoformat() + "_history_" + str(uuid.uuid4())[:8]

        st.session_state.messages = history_messages
        print(f"[DEBUG] Historique récupéré ({len(st.session_state.messages)} messages).")
    except requests.exceptions.Timeout:
        st.error("Délai de connexion à l'API dépassé lors de la récupération de l'historique.")
        st.session_state.messages = []
        print("[ERROR] Timeout lors de la récupération de l'historique.")
    except requests.exceptions.ConnectionError:
        st.error("Impossible de se connecter au serveur backend FastAPI pour l'historique. Assurez-vous qu'il est en cours d'exécution.")
        st.error("Veuillez lancer votre backend FastAPI avec la commande : `uvicorn main:app --reload` dans le dossier de votre API.")
        st.session_state.messages = []
        print("[ERROR] Erreur de connexion au backend pour l'historique.")
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la récupération de l'historique: {e}")
        st.session_state.messages = []
        print(f"[ERROR] Erreur de requête générale pour l'historique : {e}")

def transcribe_audio(audio_bytes):
    files = {'audio_file': ("audio.wav", audio_bytes, "audio/wav")}
    print("[DEBUG] Envoi de l'audio pour transcription.")
    try:
        r = requests.post(f"{FASTAPI_BASE_URL}/chat/transcribe_audio/", files=files, timeout=120)
        r.raise_for_status()
        transcribed_text = r.json().get("transcribed_text", "")
        print(f"[DEBUG] Texte transcrit : '{transcribed_text}'")
        return transcribed_text
    except requests.exceptions.Timeout:
        st.error("Délai de connexion à l'API dépassé lors de la transcription audio.")
        print("[ERROR] Timeout lors de la transcription audio.")
        return None
    except requests.exceptions.ConnectionError:
        st.error("Impossible de se connecter au serveur backend FastAPI pour la transcription. Assurez-vous qu'il est en cours d'exécution.")
        st.error("Veuillez lancer votre backend FastAPI avec la commande : `uvicorn main:app --reload` dans le dossier de votre API.")
        print("[ERROR] Erreur de connexion au backend pour la transcription.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la transcription audio: {e}")
        print(f"[ERROR] Erreur de requête générale pour la transcription : {e}")
        return None
    finally:
        pass

# --- Callback pour l'envoi de message texte via le bouton ---
def handle_send_click():
    """Gère l'envoi du message texte depuis le bouton."""
    # Récupère le texte de l'input en utilisant sa clé (ici, "message_input")
    user_message_text = st.session_state.message_input.strip()

    if user_message_text:
        print(f"[DEBUG] handle_send_click appelé avec texte: '{user_message_text}'")

        current_time_iso = datetime.now().isoformat()
        st.session_state.messages.append({
            "id": current_time_iso + "_user_msg_" + str(uuid.uuid4())[:8],
            "text": user_message_text,
            "user_id": st.session_state.logged_in_user or "Vous",
            "timestamp": current_time_iso
        })

        # Efface le contenu du champ de saisie en réinitialisant la valeur de sa clé
        st.session_state.message_input = "" # C'est la ligne clé pour effacer le widget
        # st.session_state.chat_input_text = "" # Plus nécessaire si message_input est la source unique

        st.session_state.thinking = True
        st.session_state.display_suggestions = False
        # Ne pas faire de st.rerun() ici, on_click est exécuté au début du rerun de Streamlit.
        # process_message_and_get_response() sera appelé dans le corps principal après.
    else:
        print("[DEBUG] Message texte vide, ignoré.")


def process_message_and_get_response():
    if st.session_state.thinking or st.session_state.transcribing:
        last_user_message = None
        for i in reversed(range(len(st.session_state.messages))):
            msg = st.session_state.messages[i]
            if msg.get("user_id") == (st.session_state.logged_in_user or "Vous"):
                has_assistant_response = False
                for j in range(i + 1, len(st.session_state.messages)):
                    if st.session_state.messages[j].get("user_id") in ["Elavira Assistant", "Solenys"]:
                        has_assistant_response = True
                        break
                if not has_assistant_response:
                    last_user_message = msg
                    break

        if last_user_message:
            last_user_message_text = last_user_message["text"]
            assistant_response = send_message_to_api(last_user_message_text)

            if assistant_response:
                st.session_state.messages.append(assistant_response)

        st.session_state.thinking = False
        st.session_state.transcribing = False
        st.rerun()


# --- Callback pour l'enregistrement micro ---
def handle_mic_input(audio_bytes):
    if audio_bytes:
        print("[DEBUG] handle_mic_input appelé avec des données audio.")
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
            # Lors de la transcription, on vide aussi le champ de texte principal
            st.session_state.message_input = ""
            # st.session_state.chat_input_text = "" # Plus nécessaire


            st.session_state.transcribing = False
            st.session_state.thinking = True
            st.session_state.display_suggestions = False
            st.rerun()


# --- Auth UI ---
def auth_ui():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # L'image d'Elavira pour l'authentification est volontairement retirée ici.
        st.title("Bienvenue sur Elavira 🤖")

        if st.session_state.get("prefill_login_username"):
            st.session_state.login_input_username = st.session_state.prefill_login_username
            del st.session_state.prefill_login_username

        if st.session_state.get("prefill_login_password"):
            st.session_state.login_input_password = st.session_state.prefill_login_password
            del st.session_state.prefill_login_password

        st.subheader("Connectez-vous")
        login_username_value = st.session_state.get("login_input_username", "")
        login_password_value = st.session_state.get("login_input_password", "")

        st.text_input("Nom d'utilisateur", key="login_input_username", placeholder="Votre nom d'utilisateur", value=login_username_value)
        st.text_input("Mot de passe", type="password", key="login_input_password", placeholder="Votre mot de passe", value=login_password_value)

        if st.button("Se connecter", key="login_button"):
            if st.session_state.login_input_username and st.session_state.login_input_password:
                response = requests.post(f"{FASTAPI_BASE_URL}/users/login/", json={
                    "username": st.session_state.login_input_username,
                    "password": st.session_state.login_input_password
                })
                if response.status_code == 200:
                    token = response.json().get("access_token")
                    st.session_state.access_token = token
                    st.session_state.logged_in_user = st.session_state.login_input_username
                    st.session_state.page = "chat"
                    fetch_chat_history()
                    st.rerun()
                elif response.status_code == 401:
                    st.error("Nom d'utilisateur ou mot de passe incorrect.")
                else:
                    st.error(f"Erreur de connexion: {response.status_code} - {response.text}")
            else:
                st.warning("Veuillez remplir tous les champs pour la connexion.")

        st.markdown("---")

        st.subheader("Nouvel utilisateur ?")
        st.write("Créez un compte pour accéder à toutes les fonctionnalités.")

        with st.expander("S'inscrire", expanded=False):
            st.text_input("Nouveau nom d'utilisateur", key="register_new_username", placeholder="Choisissez un nom d'utilisateur")
            st.text_input("Nouveau mot de passe", type="password", key="register_new_password", placeholder="Choisissez un mot de passe")

            if st.button("Créer mon compte", key="register_button_expander"):
                if st.session_state.register_new_username and st.session_state.register_new_password:
                    response = requests.post(f"{FASTAPI_BASE_URL}/users/register/", json={
                        "username": st.session_state.register_new_username,
                        "password": st.session_state.register_new_password
                    })
                    if response.status_code == 201:
                        st.success("Compte créé avec succès ! Vous pouvez maintenant vous connecter.")
                        st.session_state.prefill_login_username = st.session_state.register_new_username
                        st.session_state.prefill_login_password = st.session_state.register_new_password
                        st.rerun()
                    elif response.status_code == 400:
                        st.warning("Ce nom d'utilisateur est déjà pris.")
                    else:
                        st.error(f"Erreur lors de l'inscription: {response.status_code} - {response.text}")
                else:
                    st.warning("Veuillez remplir tous les champs pour l'inscription.")


# --- Chat UI ---
def chat_ui():
    # --- TOP SECTION (HEADER) ---
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

    agent_options = [
        ("Elavira", "agent-001"),
        ("Solenys", "agent-002")
    ]
    current_agent_index = 0
    for i, (name, id_val) in enumerate(agent_options):
        if id_val == st.session_state.selected_agent_id:
            current_agent_index = i
            break

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


    # --- MIDDLE SECTION (CHAT HISTORY) ---
    chat_history_display_container = st.container(height=500, border=False)

    with chat_history_display_container:
        if not st.session_state.messages and not st.session_state.thinking and not st.session_state.transcribing:
            st.info("Aucun message dans l'historique pour le moment. Commencez la conversation ci-dessous !")

        for msg in st.session_state.messages:
            if "id" not in msg or not msg["id"]:
                msg["id"] = datetime.now().isoformat() + "_display_fallback_" + str(uuid.uuid4())[:8]

            is_assistant_message = msg.get("user_id") in ["Elavira Assistant", "Solenys"]
            style_class = "assistant-message" if is_assistant_message else "user-message"

            timestamp_raw = msg.get("timestamp", "")
            timestamp = ""
            if timestamp_raw:
                try:
                    dt_obj = datetime.fromisoformat(timestamp_raw.replace('Z', '+00:00'))
                    timestamp = dt_obj.strftime("%H:%M")
                except ValueError:
                    timestamp = timestamp_raw[11:16] if len(timestamp_raw) >= 16 else timestamp_raw
            else:
                timestamp = datetime.now().strftime("%H:%M")

            # Définir les chemins d'avatar une seule fois
            elavira_avatar_path = os.path.join("images", "elavira_assistant.png")
            elavira_avatar_b64 = get_image_base64(elavira_avatar_path)

            user_avatar_file = "4 - Elavira (1).png" # Assurez-vous que c'est bien l'avatar de l'utilisateur
            user_avatar_path = os.path.join("images", user_avatar_file)
            user_avatar_b64 = get_image_base64(user_avatar_path)

            if is_assistant_message:
                # Messages de l'assistant (maintenant à droite)
                avatar_html = ""
                if elavira_avatar_b64:
                    avatar_html = f'<img src="data:image/png;base64,{elavira_avatar_b64}" class="avatar">'
                else:
                    avatar_html = '<div class="avatar assistant-avatar">E</div>'

                st.markdown(f'''
                    <div class="chat-message-row" style="justify-content: flex-end;">
                        <div class="chat-message {style_class}">
                            <div class="message-content">
                                <b>{msg.get("user_id", "Assistant")}</b> <span class="timestamp">({timestamp})</span><br>{msg.get("text", "...")}
                            </div>
                            {avatar_html}
                        </div>
                    </div>
                ''', unsafe_allow_html=True)


            else: # Messages de l'utilisateur (maintenant à gauche)
                avatar_html = ""
                if user_avatar_b64:
                    avatar_html = f'<img src="data:image/png;base64,{user_avatar_b64}" class="user-avatar-image">'
                else:
                    user_initial = st.session_state.logged_in_user[0].upper() if st.session_state.logged_in_user else "U"
                    avatar_html = f'<div class="avatar user-avatar">{user_initial}</div>'

                st.markdown(f'''
                    <div class="chat-message-row" style="justify-content: flex-start;">
                        <div class="chat-message {style_class}">
                            {avatar_html}
                            <div class="message-content">
                                <b>{msg.get("user_id", "Vous")}</b> <span class="timestamp">({timestamp})</span><br>{msg.get("text", "...")}
                            </div>
                        </div>
                    </div>
                ''', unsafe_allow_html=True)

            if is_assistant_message and msg.get("audio_base64"):
                try:
                    audio_bytes = base64.b64decode(msg['audio_base64'])
                    st.audio(audio_bytes, format="audio/mp3")
                except Exception as e:
                    print(f"[DEBUG] Impossible de décoder l'audio pour le message de {msg.get('user_id')}: {e}")

        if st.session_state.thinking:
            # Assistant thinking indicator (now on RIGHT)
            st.markdown(f'''
                <div class="chat-message-row" style="justify-content: flex-end;">
                    <div class="typing-indicator assistant-thinking">
                        ⏳ Elavira réfléchit...
                    </div>
                </div>
            ''', unsafe_allow_html=True)
        if st.session_state.transcribing:
            # User transcribing indicator (now on LEFT)
            st.markdown(f'''
                <div class="chat-message-row" style="justify-content: flex-start;">
                    <div class="typing-indicator user-side">
                        🎙️ Transcription en cours...
                    </div>
                </div>
            ''', unsafe_allow_html=True)


    if st.session_state.last_suggested_prompts and not st.session_state.display_suggestions:
        st.markdown('<div style="text-align: center; margin-top: 15px; margin-bottom: 5px;">', unsafe_allow_html=True)
        if st.button("Afficher les suggestions de prompt", key="show_suggested_prompts_button"):
            st.session_state.display_suggestions = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.display_suggestions and st.session_state.last_suggested_prompts:
        st.markdown('<div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 5px; margin-bottom: 15px; justify-content: center;">', unsafe_allow_html=True)
        for i, prompt in enumerate(st.session_state.last_suggested_prompts):
            st.button(
                prompt,
                key=f"displayed_suggested_prompt_{i}",
                on_click=lambda p=prompt: (
                    st.session_state.__setitem__("message_input", p), # Mettre le prompt dans le nouveau champ de texte
                    handle_send_click() # Envoyer le message
                )
            )
        st.markdown('</div>', unsafe_allow_html=True)

    # --- SECTION INFÉRIEURE (ZONE DE SAISIE - FIXE) ---
    with st.container():
        st.markdown('<div class="fixed-bottom-input">', unsafe_allow_html=True)

        input_col_fixed, send_col_fixed = st.columns([5, 1])
        with input_col_fixed:
            # Utilisez la nouvelle clé 'message_input' pour le widget text_input
            # La valeur sera lue/écrite depuis st.session_state.message_input
            st.text_input(
                "Votre message ici...",
                key="message_input", # Clé du widget
                value=st.session_state.message_input, # Initialise la valeur du widget
                placeholder="Écrivez votre message...",
                max_chars=500
            )
        with send_col_fixed:
            # Le bouton "Envoyer" déclenchera la fonction handle_send_click
            if st.button("Envoyer", key="send_message_button", on_click=handle_send_click):
                pass # L'action est gérée par le callback on_click

        # Bouton micro (DÉPLACÉ ICI, SOUS LE CHAMP DE SAISIE DE TEXTE)
        mic_output = mic_recorder(
            start_prompt="Parler avec Elavira 🎧",
            stop_prompt="Arrêter l'enregistrement 🔝",
            key="mic_input"
        )

        if mic_output and mic_output["bytes"]:
            handle_mic_input(mic_output["bytes"])

        st.markdown('</div>', unsafe_allow_html=True)

# --- Exécution principale ---
if __name__ == "__main__":
    init_session()
    # add_bg('your_background_image.png') # Décommenter si vous avez une image de fond dans 'images/'

    if st.session_state.page == "auth":
        auth_ui()
    elif st.session_state.page == "chat":
        chat_ui()
        process_message_and_get_response()  