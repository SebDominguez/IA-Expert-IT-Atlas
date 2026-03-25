# Méthodologie de Nettoyage de Données & Choix Techniques

## 1. Réduction Dimensionnelle (Nettoyage Vertical / colones)
- **Action :** Suppression des colonnes contenant plus de **50 % de valeurs manquantes**.
- **Impact :** Les variables `historique_credits` et `score_credit` ont été supprimées.
- **Justification :** Imputer plus de la moitié des données d'une colonne introduit un biais statistique significatif et compromet la fiabilité de tout futur modèle prédictif.

## 2. Filtrage des Lignes (Nettoyage Horizontal / lignes)
- **Action :** Suppression des **2 % des lignes les plus incomplètes (200 lignes)**.
- **Processus :** Nous avons calculé un compteur de valeurs manquantes (`nan_count`) par ligne et supprimé les 200 profils les plus "vides".
- **Justification :** Des profils trop incomplets ne fournissent pas assez de contexte pour que l'algorithme KNN puisse effectuer une imputation précise. Supprimer ces "coquilles vides" améliore la densité et la qualité globale du jeu de données.

## 3. Validation de la Logique Métier (Valeurs Incohérentes)
Avant l'analyse statistique, nous avons appliqué des contrôles de cohérence basés sur des contraintes réelles. Les valeurs échouant à ces tests ont été définies comme `NaN` (Not a Number) pour être réparées lors de l'étape finale :
* **Âge :** Minimum **18 ans** (exigence légale pour une demande de prêt).
* **Poids :** Minimum **30 kg** (seuil physiologique pour des adultes).
* **Taille :** Minimum **50 cm**.
* **Finances :** Les revenus mensuels et les montants de prêt doivent être **strictement positifs (> 0)**.
* **Loyer :** Le loyer mensuel ne peut pas être négatif.
* **Score de Risque :** Doit être strictement compris entre **0 et 1**.

## 4. Détection Statistique des Outliers (Méthode IQR)
Pour protéger le modèle des valeurs extrêmes qui faussent les distributions, nous avons appliqué la méthode de l'**Écart Interquartile (IQR)** à toutes les colonnes numériques :
- **Calcul :** Pour chaque colonne, nous avons défini une "zone normale" entre $[Q1 - 1.5 \times IQR]$ et $[Q3 + 1.5 \times IQR]$.
- **Action :** Toute valeur tombant en dehors de ces bornes a été neutralisée (définie à `NaN`).
- **Colonnes concernées :** `taille`, `loyer_mensuel`, `poids`, `revenu_estime_mois`, `montant_pret`, `risque_personnel` et `age`.

## 5. Imputation Avancée des Données (KNN)
Au lieu d'utiliser un remplacement simple par la moyenne ou la médiane (ce qui réduit la variance), nous avons implémenté l'algorithme des **K-Plus Proches Voisins (KNN)** :
- **Paramètres :** `k=5` voisins.
- **Processus :** Chaque `NaN` (qu'il soit d'origine ou créé lors de nos étapes de nettoyage) est remplacé par une valeur calculée en fonction des 5 profils les plus similaires dans le jeu de données.
- **Résultat :** Cela garantit qu'une valeur de "revenu" manquante est estimée à l'aide de données connexes comme "l'âge" ou le "montant du prêt", maintenant une cohérence logique dans tout le fichier.