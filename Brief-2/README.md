# Brief 2 - Intégration d'une IA simple dans une Application Web - Un défi un peu plus compliqué

## Architecture du Projet
```
├── app.py
├── main.py
├── README.md
└── requirements.txt
```

## Installation et Configuration

1. **Clonage du projet :**
   `git clone git@github.com:SebDominguez/IA-Expert-IT-Atlas.git`

2. **Changer de repertoire :**
    `cd brief-2`

3. **Creation de l'environnement virtuel :**
   `python -m venv .venv`

4. **Activation de l'environnement :**
   * macOS/Linux : `source .venv/bin/activate`
   * Windows : `¯\_(ツ)_/¯ `

5. **Installation des dependances :**
   `pip install -r requirements.txt`

## Lancement de l'Application

### 1. Demarrer l'API
`uvicorn main:app --port 9000 --reload`

**Note :** Si l'erreur `ModuleNotFoundError: No module named 'fastapi'` persiste malgre l'activation de l'environnement virtuel, forcez l'utilisation du binaire Python de l'environnement :
`./.venv/bin/python -m uvicorn main:app --reload --port 9000`

### 2. Demarrer l'Interface
`streamlit run app.py --server.runOnSave true`

## API

Endpoint: `/chat`

MéthodeMéthode: `POST`

### Requête standard :

Format attendu:

```json
{
  "text": "string"
}
```
```bash
curl -X POST "http://127.0.0.1:9000/chat" \
    -H "Content-Type: application/json" \
    -d '{"text": "test"}'
```

Réponse (Succès) :

```json
{
    "response": "test mathematrix",
    "translation": "test",
    "sentiment": "5 stars",
    "score": 0.3676360845565796
}
```

### Gestion des erreurs (Mauvaise requête) :

```bash
curl -X POST "http://127.0.0.1:9000/chat" \
    -H "Content-Type: application/json" \
    -d '{"whatever": "test"}'
```

Réponse d'erreur :

```json
{
    "detail": [
        {
            "type": "missing",
            "loc": [
                "body",
                "text"
            ],
            "msg": "Field required",
            "input": {
                "whatever": "test"
            }
        }
    ]
}
```