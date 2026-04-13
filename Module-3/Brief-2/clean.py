import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer

# 0. Load CSV
df = pd.read_csv('./resources/nouvelle-source-de-données.csv')

print("=== DEBUG 0 (Initial State) ===")
print(f"Table size: {df.shape[0]} rows x {df.shape[1]} columns")

# 0.a. On dégage ce qui identifie sans apporter de valeur au risque
col_to_drop = ['nom', 'prenom', 'nationalité_francaise', 'sexe', 'region', 'smoker', 'poids', 'taille', 'orientation_sexuelle']

for col in col_to_drop:
    if col in df.columns:
        print(f"Anonymisation : Suppression de {col}")
        df = df.drop(columns=col)

print(f"=== DEBUG 0.a (Ethic Filter) ===\nColonnes supprimées pour l'équité : {col_to_drop}")

# 1. Drop empty columns (missing values > 50%)
empty_col_to_drop = [col for col in df.columns if df[col].isnull().mean() > 0.50]
df_clean = df.drop(columns=empty_col_to_drop).copy()

# --- SÉCURITÉ : Forçage manuel des types pour le KNN ---
cols_numeriques = ['age', 'revenu_estime_mois', 'loyer_mensuel', 'montant_pret', 'risque_personnel', 'nb_enfants', 'quotient_caf']
for col in cols_numeriques:
    if col in df_clean.columns:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

# 2. Drop the 2% most incomplete rows
n_lines_to_delete = int(df.shape[0] * 0.02)
df_clean['nan_count'] = df_clean.isnull().sum(axis=1)
rows_to_drop = df_clean.sort_values('nan_count', ascending=False).head(n_lines_to_delete).index
df_clean = df_clean.drop(index=rows_to_drop).drop(columns=['nan_count'])

# 3. Outliers
# 3.1 Replace incoherent values with NaN (Business Logic)
df_clean.loc[df_clean['age'] < 18, 'age'] = np.nan
df_clean.loc[df_clean['loyer_mensuel'] < 0, 'loyer_mensuel'] = np.nan
df_clean.loc[df_clean['revenu_estime_mois'] <= 0, 'revenu_estime_mois'] = np.nan
df_clean.loc[df_clean['montant_pret'] <= 0, 'montant_pret'] = np.nan

# 3.2 Statistical outlier detection using the IQR method (1.5x)
# On définit num_cols pour appliquer l'IQR uniquement sur les chiffres
num_cols = df_clean.select_dtypes(include=['number']).columns

for col in num_cols:
    Q1 = df_clean[col].quantile(0.25)
    Q3 = df_clean[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    # On transforme les valeurs hors-normes en NaN pour le KNN
    df_clean.loc[(df_clean[col] < lower) | (df_clean[col] > upper), col] = np.nan

print("=== DEBUG 4 (Outliers IQR set to NaN) ===")

# 4. KNN Imputation (k=5)
# A. On gère le texte d'abord (car KNN ne le lit pas)
cat_cols = df_clean.select_dtypes(include=['object', 'string']).columns
for col in cat_cols:
    df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])

# B. On lance le KNN sur les chiffres (num_cols contient nos trous initiaux + trous IQR)
imputer = KNNImputer(n_neighbors=5)
df_clean[num_cols] = imputer.fit_transform(df_clean[num_cols])

print("=== DEBUG 5 (KNN Imputation complete) ===")

# 5. Export cleaned data
df_clean.to_csv('./resources/cleaned_data.csv', index=False)
print("Fichier sauvegardé : ./resources/cleaned_data.csv")