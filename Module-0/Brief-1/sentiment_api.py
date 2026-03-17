from fastapi import FastAPI
from pydantic import BaseModel
import nltk
import ssl #to avoid CERTIFICATE_VERIFY_FAILED
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from loguru import logger

logger.add("logs/sentiment_api.log", rotation="100 MB", level="INFO")

# see https://github.com/gunthercox/ChatterBot/issues/930
# [nltk_data] Error loading vader_lexicon: <urlopen error [SSL:
# [nltk_data]     CERTIFICATE_VERIFY_FAILED] certificate verify failed:
# [nltk_data]     unable to get local issuer certificate (_ssl.c:1006)>
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('vader_lexicon')

app = FastAPI()
sia = SentimentIntensityAnalyzer()


# Modèle pour recevoir le texte
class Texte(BaseModel):
    texte: str


@app.post("/analyse_sentiment/")
async def analyse_sentiment(texte_object: Texte):
    logger.info(f"Analyse du texte: {texte_object.texte}")
    try:
        sentiment = sia.polarity_scores(texte_object.texte)
        logger.info(f"Résultats: {sentiment}")
        return {
          "neg": sentiment["neg"],
          "neu": sentiment["neu"],
          "pos": sentiment["pos"],
          "compound": sentiment["compound"]
        }
        #return sentiment
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse: {e}")
        raise HTTPException(status_code=500, detail=str(e))

