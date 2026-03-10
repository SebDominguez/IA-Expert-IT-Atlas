import streamlit as st
import requests
from loguru import logger

logger.add("logs/sentiment_streamlit.log", rotation="100 MB", level="INFO")

st.set_page_config(page_title="Analyseur de Sentiment")
st.title("Analyseur de Sentiment")

with st.form("formulaire_analyse"):
    texte = st.text_area("Entrez le texte à analyser :")
    submitted = st.form_submit_button("Analyser")

if submitted:
    if texte:
        logger.info(f"Texte à analyser : {texte}")
        try:
            response = requests.post(
                "http://127.0.0.1:9000/analyse_sentiment/",
                json={"texte": texte}
            )
            response = requests.post("http://127.0.0.1:9000/analyse_sentiment/", json={"texte": texte})
            # Lève une exception pour les codes d'erreur HTTP (4xx ou 5xx) response.raise_for_status()
            sentiment = response.json()
            st.write("Résultats de l'analyse :")
            st.write(f"Polarité négative : {sentiment['neg']}")
            st.write(f"Polarité neutre : {sentiment['neu']}")
            st.write(f"Polarité positive : {sentiment['pos']}")
            st.write(f"Score composé : {sentiment['compound']}")
            if sentiment['compound'] >= 0.05 :
                st.write("Sentiment global : Positif 😀")
            elif sentiment['compound'] <= -0.05 :
                st.write("Sentiment global : Négatif 🙁")
            else :
                st.write("Sentiment global : Neutre 😐")
            logger.info(f"Résultats affichés: {sentiment}")
        except requests.exceptions.RequestException as e:
            st.error(f"Erreur de connexion à l'API : {e}")
            logger.error(f"Erreur de connexion à l'API : {e}")
        except Exception as e :
            st.error(f"Une erreur est survenue: {e}")
            logger.error(f"Une erreur est survenue: {e}")
    else:
        st.write("Veuillez entrer du texte pour l'analyse.")