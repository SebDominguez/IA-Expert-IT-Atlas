from fastapi.testclient import TestClient
from sentiment_api import app

client = TestClient(app)

def test_analyse_positive():
    # On teste l'envoi d'une phrase positive
    response = client.post("/analyse_sentiment/", json={"texte": "happy"})
    assert response.status_code == 200
    data = response.json()
    assert data["compound"] >= 0.0
    assert "pos" in data

def test_analyse_negative():
    # On teste l'envoi d'une phrase positive
    response = client.post("/analyse_sentiment/", json={"texte": "sad"})
    assert response.status_code == 200
    data = response.json()
    assert data["compound"] <= -0.05
    assert "neg" in data

def test_analyse_neutral():
    # On teste l'envoi d'une phrase positive
    response = client.post("/analyse_sentiment/", json={"texte": "cat"})
    assert response.status_code == 200
    data = response.json()
    assert data["compound"] == 0
    assert "neg" in data

def test_analyse_vide():
    # On teste le comportement avec un texte vide
    response = client.post("/analyse_sentiment/", json={"texte": ""})
    assert response.status_code == 200
    assert response.json()["compound"] == 0