from app.database import engine, Base
import app.models

print("Connexion à PostgreSQL...")
try:
    # Cette commande compare tes modèles avec la DB et crée ce qui manque
    Base.metadata.create_all(bind=engine)
    print("Succès ! Les tables 'users' et 'finance' ont été créées.")
except Exception as e:
    print(f"Erreur lors de l'initialisation : {e}")