import pandas as pd
from app.database import SessionLocal, engine
from app.models import User, Finance

# 1. Créer une session pour parler à la base
db = SessionLocal()

# 2. Charger ton CSV propre
df = pd.read_csv("./resources/cleaned_data.csv", parse_dates=['date_creation_compte'])
print(f"Début de la migration de {len(df)} lignes...")

try:
    for index, row in df.iterrows():
        # 3. Création conditionnelle de l'objet Finance
        # On vérifie si les colonnes financières ne sont pas vides (NaN)

        # transfoemer oui / non en bool
        is_sportif = str(row['sport_licence']).lower() in ['oui']

        new_finance = None
        if pd.notna(row['revenu_estime_mois']):
            new_finance = Finance(
                revenu_estime_mois=row['revenu_estime_mois'],
                loyer_mensuel=row['loyer_mensuel'],
                montant_pret=row['montant_pret'],
                score_credit=row.get('score_credit'), # .get au cas où la colonne manque
                risque_personnel=row['risque_personnel']
            )

        # 4. Création de l'User
        # On lui passe l'objet new_finance direct (SQLAlchemy gère l'ID seul)
        new_user = User(
            age=row['age'],
            situation_familiale=row['situation_familiale'],
            niveau_etude=row['niveau_etude'],
            sport_licence=is_sportif,
            date_creation_compte=row['date_creation_compte'],
            finance=new_finance # Sera soit l'objet Finance, soit None (ton 0,1)
        )

        db.add(new_user)

        # 5. Commit intermédiaire (Optionnel mais conseillé pour les gros volumes)
        if index % 100 == 0:
            db.commit()
            print(f"{index} lignes insérées...")

    db.commit()
    print("Migration terminée avec succès !")

except Exception as e:
    db.rollback() # Annule tout en cas d'erreur pour ne pas salir la DB
    print(f"Erreur pendant la migration : {e}")
finally:
    db.close() # On ferme toujours la connexion