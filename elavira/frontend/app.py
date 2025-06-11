# Votre_script_streamlit.py (là où vous avez votre code Streamlit actuel)

import streamlit as st
import base64
import os
import requests # <-- AJOUTEZ CETTE LIGNE

current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, "images", "4 - Elavira (1).png")

def add_bg_from_local(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: 47% auto;   /* taille fixe largeur 47% */
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

st.title("Bienvenue sur Elavira 🤖")

add_bg_from_local(image_path)

st.write("---") # Ligne de séparation pour la clarté

# --- Exemple de communication avec FastAPI ---

# URL de base de votre API FastAPI
FASTAPI_BASE_URL = "http://127.0.0.1:8000"

st.header("Tester la connexion à l'API FastAPI")

if st.button("Obtenir le statut du chat de l'API"):
    try:
        # Fait une requête GET à l'endpoint /chat/ de votre FastAPI
        response = requests.get(f"{FASTAPI_BASE_URL}/chat/")
        response.raise_for_status() # Lève une exception pour les codes d'erreur HTTP
        data = response.json()
        st.success(f"Statut de l'API (Chat) : {data['message']}")
        st.json(data) # Affiche les données JSON brutes
    except requests.exceptions.ConnectionError:
        st.error(f"Erreur de connexion : Assurez-vous que votre API FastAPI est lancée sur {FASTAPI_BASE_URL}")
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la requête API : {e}")

# Vous pouvez ajouter d'autres éléments Streamlit pour interagir avec d'autres endpoints
# Par exemple, un champ de texte pour envoyer un message
# message_to_send = st.text_input("Message à envoyer au chat :")
# if st.button("Envoyer le message"):
#     payload = {"message": message_to_send, "user_id": 1} # user_id est un exemple
#     try:
#         response = requests.post(f"{FASTAPI_BASE_URL}/chat/send_message/", json=payload)
#         response.raise_for_status()
#         st.success("Message envoyé avec succès !")
#         st.json(response.json())
#     except requests.exceptions.RequestException as e:
#         st.error(f"Erreur lors de l'envoi du message : {e}")