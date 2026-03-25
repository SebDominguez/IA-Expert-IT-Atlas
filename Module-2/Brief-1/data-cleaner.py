import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer

# 0. Load CSV
df = pd.read_csv('./resources/fichier-de-donnees-numeriques.csv')

print("=== DEBUG 1 (Initial State) ===")
print(f"Table size: {df.shape[0]} rows x {df.shape[1]} columns")
print(df.head(3))
print("-" * 50)

# 1. Drop empty columns (missing values > 50%)
columns_to_drop = [col for col in df.columns if df[col].isnull().mean() > 0.50]
df_clean = df.drop(columns=columns_to_drop)

print("=== DEBUG 2 (Columns cleaned) ===")
print(f"Table size: {df_clean.shape[0]} rows x {df_clean.shape[1]} columns")
print(df_clean.head(100))
print("-" * 50)

# At this point, 'historique_credits' and 'score_credit' are deleted

# 2. Drop the 2% most incomplete rows

n_lines_to_delete = int(df.shape[0] * 0.02)

print(f"=== DEBUG 3 (Deleting the {n_lines_to_delete} most incomplete rows) ===")

df_clean['nan_count'] = df_clean.isnull().sum(axis=1)
rows_to_drop = df_clean.sort_values('nan_count', ascending=False).head(n_lines_to_delete).index
df_clean = df_clean.drop(index=rows_to_drop).drop(columns=['nan_count'])

print(f"Table size: {df_clean.shape[0]} rows x {df_clean.shape[1]} columns")
print(df_clean.head(100))
print("-" * 50)

# 3. Outliers
# 3.1 Replace incoherent values with NaN (Business Logic)
df_clean.loc[df_clean['taille'] <= 50, 'taille'] = np.nan
df_clean.loc[df_clean['age'] < 18, 'age'] = np.nan
df_clean.loc[df_clean['loyer_mensuel'] < 0, 'loyer_mensuel'] = np.nan
df_clean.loc[df_clean['poids'] < 30, 'poids'] = np.nan
df_clean.loc[df_clean['revenu_estime_mois'] <= 0, 'revenu_estime_mois'] = np.nan
df_clean.loc[df_clean['montant_pret'] <= 0, 'montant_pret'] = np.nan
df_clean.loc[(df_clean['risque_personnel'] < 0) | (df_clean['risque_personnel'] > 1), 'risque_personnel'] = np.nan

# 3.2 Statistical outlier detection using the IQR method
outlier_cols = ['taille', 'loyer_mensuel', 'poids', 'revenu_estime_mois', 'montant_pret', 'risque_personnel', 'age']

for col in outlier_cols:
    Q1 = df_clean[col].quantile(0.25)
    Q3 = df_clean[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    # Transform values outside the normal range into NaN
    df_clean.loc[(df_clean[col] < lower) | (df_clean[col] > upper), col] = np.nan

print(f"=== DEBUG 4 (Outliers and IQR set to NaN) ===")

print(f"Table size: {df_clean.shape[0]} rows x {df_clean.shape[1]} columns")
print(df_clean.head(100))
print("-" * 50)

# 4. KNN Imputation (k=5)

imputer = KNNImputer(n_neighbors=5)
# Fill missing values (NaNs) using the k-nearest neighbors algorithm
df_clean = pd.DataFrame(imputer.fit_transform(df_clean), columns=df_clean.columns)

print(f"=== DEBUG 5 (KNN Imputation complete) ===")

print(f"Table size: {df_clean.shape[0]} rows x {df_clean.shape[1]} columns")
print(df_clean.head(100))
print("-" * 50)

# 5. Export cleaned data

df_clean.to_csv('./resources/cleaned_data.csv', index=False)