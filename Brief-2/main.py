from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
from loguru import logger
import json

logger.add("logs/api_debug.log", rotation="1 MB", level="DEBUG")

app = FastAPI(title="FastIA AI Service")

class Message(BaseModel):
    text: str

models = {}

try:
    logger.debug("Chargement des modèles Hugging Face...")

    # device -1 macOS GPU junk
    models["chat"] = pipeline("text-generation", model="microsoft/DialoGPT-small", device=-1)
    logger.debug("Modèle microsoft/DialoGPT-small chargé")

    models["translator"] = pipeline("translation_fr_to_en", model="Helsinki-NLP/opus-mt-fr-en")
    logger.debug("Modèle Helsinki-NLP/opus-mt-fr-en chargé")

    models["sentiment"] = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
    logger.debug("Modèle nlptown/bert-base-multilingual-uncased-sentiment chargé")

    logger.success("Tous les modèles sont prêts !")
except Exception as e:
    logger.critical(f"Erreur au chargement des modèles : {e}")

@app.post("/chat")
async def chat_with_bot(input_data: Message):
    logger.debug(f"Message reçu depuis l'app (objet pydantic input_data): \n {json.dumps(input_data.model_dump() , indent=4)}")

    try:
        sentiment = models["sentiment"](input_data.text)[0]
        logger.debug(f"sentiment dictionaire: \n {json.dumps(sentiment , indent=4)}")

        translation = models["translator"](input_data.text)[0]['translation_text']
        logger.debug(f"translation dictionaire: \n {json.dumps(translation , indent=4)}")

        response = models["chat"](translation)[0]['generated_text']
        logger.debug(f"response dictionaire: \n {json.dumps(response , indent=4)}")

        logger.success(f"Réponse générée: {response}")

        return {
            "response": response,
            "translation": translation,
            "sentiment": sentiment['label'],
            "score": sentiment['score']
        }
    except Exception as e:
        logger.error(f"Erreur lors du traitement : {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")