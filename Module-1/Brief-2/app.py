import streamlit as st
import requests
from loguru import logger
import pandas as pd

import os

BASE_URL = os.getenv("API_URL", "http://localhost:9000")


logger.add("logs/app.log", rotation="10 MB")

@st.cache_data # Pour ne pas relire le fichier à chaque clic
def get_categories():
    file_path = "data/df_new.csv"
    logger.info(f"Tentative de lecture du fichier : {file_path}")
    df = pd.read_csv(file_path)
    return {
        "regions": df['region'].unique().tolist(),
        "etudes": df['niveau_etude'].unique().tolist(),
        "sexes": df['sexe'].unique().tolist()
    }

categories = get_categories()

with st.form("loan_form"):
    st.subheader("Infos")
    age = st.number_input("Âge", step=1)
    taille = st.number_input("Taille cm")
    sexe = st.selectbox("Sexe", categories["sexes"])
    poids = st.number_input("Poids (kg)")
    nationalite = st.selectbox("Nationalité Française", ["Oui", "Non"])
    smoker = st.selectbox("Fumeur", ["Oui", "Non"])

    revenu = st.number_input("Revenu mensuel")
    region = st.selectbox("Région", categories["regions"] + ["Autre"])
    etudes = st.selectbox("Niveau d'étude", categories["etudes"] + ["Autre"])
    sport = st.selectbox("Licence de sport", ["Oui", "Non"])

    submit = st.form_submit_button("let's goooo")

if submit:
    payload = {
        "age": age,
        "taille": taille,
        "poids": poids,
        "revenu_estime_mois": float(revenu),
        "sexe": sexe,
        "sport_licence": sport,
        "niveau_etude": etudes,
        "region": region,
        "smoker": smoker,
        "nationalité_francaise": nationalite
    }

    try:
        response = requests.post(f"{BASE_URL}/predict", json=payload)

        if response.status_code == 200:
            result = response.json()["prediction"]
            st.metric("Estimation du prêt accordable", f"{result:,.2f} €")

        else:
            st.error(f"Erreur API ({response.status_code}) : {response.text}")

    except Exception as e:
        st.error(f"Impossible de contacter l'API : {e}")
        logger.error(f"Erreur de connexion Streamlit -> FastAPI : {e}")