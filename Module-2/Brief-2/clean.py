import pandas as pd
from sklearn.preprocessing import StandardScaler, OrdinalEncoder

# 1. Chargement de l'original (on n'y touche pas)
df = pd.read_csv('./data/fichier-de-donnees-mixtes.csv')

# --- PRÉPARATION COMMUNE (Nettoyage des erreurs et des vides) ---
# Correction du loyer négatif
df.loc[df['loyer_mensuel'] < 0, 'loyer_mensuel'] = df['loyer_mensuel'].median()

# Remplissage des cases vides pour que l'IA ne plante pas
df['situation_familiale'] = df['situation_familiale'].fillna(df['situation_familiale'].mode()[0])
df['score_credit'] = df['score_credit'].fillna(df['score_credit'].median())
df['historique_credits'] = df['historique_credits'].fillna(0)

# Encodage des études (Ordinal)
education_order = ['aucun', 'bac', 'bac+2', 'master', 'doctorat']
ord_enc = OrdinalEncoder(categories=[education_order])
df['niveau_etude_encoded'] = ord_enc.fit_transform(df[['niveau_etude']])

# --- 2. GÉNÉRATION DU FICHIER "NETTOYÉ" (V1 TECHNIQUE) ---
# On garde tout mais on transforme en chiffres pour les calculs
df_nettoye = pd.get_dummies(df, columns=['sexe', 'region', 'smoker', 'nationalité_francaise', 'situation_familiale'], drop_first=True)
# On enlève juste les colonnes de texte inutiles (noms, dates)
df_nettoye = df_nettoye.drop(columns=['nom', 'prenom', 'date_creation_compte', 'niveau_etude'])

# Sauvegarde du premier fichier avec la bonne orthographe
df_nettoye.to_csv('./data/nettoye.csv', index=False)

# --- 3. GÉNÉRATION DU FICHIER "ÉTHIQUE" (V2 RESPONSABLE) ---
# On repart de l'original mais on SUPPRIME les données sensibles AVANT transformation
# colonnes_sensibles = ['nom', 'prenom', 'sexe', 'nationalité_francaise', 'date_creation_compte', 'niveau_etude']

colonnes_sensibles = ['nom', 'prenom', 'sexe', 'nationalité_francaise']

df_ethique_raw = df.drop(columns=colonnes_sensibles)

# Encodage uniquement des colonnes autorisées (on a enlevé sexe et nationalité)
df_ethique = pd.get_dummies(df_ethique_raw, columns=['region', 'smoker', 'situation_familiale'], drop_first=True)

# Sauvegarde du deuxième fichier
df_ethique.to_csv('./data/ethique.csv', index=False)

print("'nettoye.csv' crée.")
print("'ethique.csv' crée.")

