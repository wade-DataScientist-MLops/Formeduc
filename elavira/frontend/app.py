
import streamlit as st
import base64
import os

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
