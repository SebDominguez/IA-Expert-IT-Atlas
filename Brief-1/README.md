# Brief 1 - Integration d'une IA simple dans une Application Web

## Architecture du Projet
```
├── conftest.py              # sans ça pytest explose
├── README.md                # Documentation du projet
├── requirements.txt         # Liste des dependances Python
├── sentiment_api.py         # API
├── sentiment_streamlit.py   # webGUI
└── tests/                   # Dossier des tests automatises
    └── test_sentiment.py
```
## Installation et Configuration

1. **Clonage du projet :**
   `git clone git@github.com:SebDominguez/IA-Expert-IT-Atlas.git`

2. **Creation de l'environnement virtuel :**
   `python -m venv .venv`

3. **Activation de l'environnement :**
   * macOS/Linux : `source .venv/bin/activate`
   * Windows : `¯\_(ツ)_/¯ `

4. **Installation des dependances :**
   `pip install -r requirements.txt`

5. **Telechargement du lexique VADER (manuellement) :**
   `python -c "import nltk; nltk.download('vader_lexicon')"`

---

## Lancement de l'Application

### 1. Demarrer l'API (Backend)
`uvicorn sentiment_api:app --host 127.0.0.1 --port 9000 --reload`

**Note :** Si l'erreur `ModuleNotFoundError: No module named 'fastapi'` persiste malgre l'activation de l'environnement virtuel, forcez l'utilisation du binaire Python de l'environnement :
`./.venv/bin/python -m uvicorn sentiment_api:app --reload --port 9000`

### 2. Demarrer l'Interface (Frontend)
`streamlit run sentiment_streamlit.py`

---

## Tests Unitaires
Pour verifier le bon fonctionnement de l'API et du modele, lancez la suite de tests :
`pytest`

## Journalisation
L'application et l'API generent des journaux d'activite. Les fichiers sont stockes dans le dossier `./logs/`.


## API

POST /analyse_sentiment/
Description : Analyse le texte via VADER.

- Request Body (JSON) : { "texte": "string" }
- Response 200 : { "neg": 0.0, "neu": 0.0, "pos": 0.0, "compound": 0.0 }
- Error 422 : Validation Error (format incorrect ou champ manquant)

### Test avec curl

```bash
curl -X POST "http://127.0.0.1:9000/analyse_sentiment/" \
     -H "Content-Type: application/json" \
     -d '{"texte": "good"}'
```
resultat :
```json
{"neg":0.0,"neu":0.0,"pos":1.0,"compound":0.4404}
```

Test mauvaise clé (message)

```bash
curl -X POST "http://127.0.0.1:9000/analyse_sentiment/" \
     -H "Content-Type: application/json" \
     -d '{"message": "Test d erreur"}'
```
resultat :

```json
{"detail":[{"type":"missing","loc":["body","texte"],"msg":"Field required","input":{"message":"Test d erreur"}}]}
```