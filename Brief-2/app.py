import streamlit as st
import requests
from loguru import logger

st.set_page_config(page_title="Brief-2", layout="centered")

st.title("Brief-2")

logger.add("logs/streamlit_debug.log", rotation="1 MB", level="DEBUG")

API_URL = "http://127.0.0.1:9000/chat"

# historique parce que streamit est stateless
if "messages" not in st.session_state:
    st.session_state.messages = []

def draw_assistant_message(msg):
    with st.chat_message("assistant"):
        st.write(msg["content"])
        with st.expander("Analyse"):
            st.write(f"Traduction : {msg['translation']}")
            st.write(f"Sentiment : {msg['sentiment']} (Score: {msg['score']})")

for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg["content"])
    else:
        draw_assistant_message(msg)

user_input = st.chat_input("Écrivez votre message ici...")

if user_input:
    logger.info(f"Message recu : {user_input}")
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    try:
        response = requests.post(API_URL, json={"text": user_input})

        if response.status_code == 200:
            data = response.json()

            logger.info(f"Reponse generé : {data}")

            msg = {
                "role": "assistant",
                "content": data["response"],
                "translation": data["translation"],
                "sentiment": data["sentiment"],
                "score": data["score"]
            }

            st.session_state.messages.append(msg)

            draw_assistant_message(msg)

        else:
            st.error("Erreur de communication avec l'API.")

    except Exception as e:
        logger.error(f"Erreur de connexion : {e}")
        st.error("L'API ne répond pas. Vérifiez que uvicorn est lancé.")