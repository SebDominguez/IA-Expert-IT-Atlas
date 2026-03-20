from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd


from loguru import logger

# Import des fonctions du brief 1
from models.models import model_predict
from modules.preprocess import preprocessing

app = FastAPI(title="Brief 2")

logger.add("logs/api.log", rotation="10 MB")

# Chargement du modèle 2026
try:
    model = joblib.load('models/model_2026.pkl')
    logger.info("Modèle 2026 chargé avec succès.")
except Exception as e:
    logger.error(f"Erreur de chargement du modèle : {e}")

try:
    preprocessor = joblib.load('models/preprocessor.pkl')
    logger.info("preprocessor chargé avec succès.")
except Exception as e:
    logger.error(f"Erreur de chargement du preprocessor : {e}")

# Schéma des données d'entrée
class LoanData(BaseModel):
    age: int
    taille: int
    poids: int
    revenu_estime_mois: float
    sexe: str
    sport_licence: str
    niveau_etude: str
    region: str
    smoker: str
    nationalité_francaise: str

@app.get("/health") # Route de santé [cite: 34]
def health_check():
    logger.info("Health check requested")
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/predict") # Route de prédiction [cite: 34]
def predict(data: LoanData):
    if model is None:
        raise HTTPException(status_code=500, detail="Modèle non chargé")

    # Transformation en DataFrame pour ton preprocessing
    df = pd.DataFrame([data.model_dump()])

    X_processed = preprocessor.transform(df)

    prediction = model.predict(X_processed)
    logger.info(f"Prédiction : {prediction[0][0]}")
    return {"prediction": float(prediction[0][0])}

@app.post("/train") # Route de réentraînement [cite: 35]
def train_route():
    # Todo train IA
    logger.warning("Route de réentraînement appelée (non implémentée)")
    return {"message": "Réentraînement lancé (simulation)"}