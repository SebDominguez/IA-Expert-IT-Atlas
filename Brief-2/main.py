from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
from loguru import logger

logger.add("logs/api_debug.log", rotation="1 MB", level="DEBUG")

app = FastAPI(title="FastIA AI Service")

class Message(BaseModel):
    text: str

models = {}

try:
    logger.info("Chargement des modèles Hugging Face...")

    # device -1 macOS GPU junk
    models["chat"] = pipeline("text-generation", model="microsoft/DialoGPT-small", device=-1)
    logger.info("Modèle microsoft/DialoGPT-small chargé")

    models["translator"] = pipeline("translation_fr_to_en", model="Helsinki-NLP/opus-mt-fr-en")
    logger.info("Modèle Helsinki-NLP/opus-mt-fr-en chargé")

    models["sentiment"] = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
    logger.info("Modèle nlptown/bert-base-multilingual-uncased-sentiment chargé")

    logger.success("Tous les modèles sont prêts !")
except Exception as e:
    logger.critical(f"Erreur au chargement des modèles : {e}")

@app.get("/")
async def root():
    return {"message": "Bienvenue sur l'API de FastIA"}

@app.post("/chat")
async def chat_with_bot(input_data: Message):
    logger.info(f"Message reçu : {input_data.text}")

    try:
        sentiment = models["sentiment"](input_data.text)[0]

        translation = models["translator"](input_data.text)[0]['translation_text']

        response = models["chat"](translation)[0]['generated_text']

        logger.success(f"Réponse générée: {response}")

        return {
            "user_message": input_data.text,
            "response": response,
            "translation": translation,
            "sentiment": sentiment['label'],
            "score": sentiment['score']
        }
    except Exception as e:
        logger.error(f"Erreur lors du traitement : {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")