import pandas as pd
import missingno as msno
import matplotlib.pyplot as plt
import os

file_original = "./resources/data-all.csv"
file_cleaned = "./resources/cleaned_data.csv"
output_original = "./resources/report_original.png"
output_cleaned = "./resources/report_cleaned.png"

if not os.path.exists(file_original) or not os.path.exists(file_cleaned):
    print("ERREUR : L'un des fichiers CSV est manquant dans ./resources/")
    print("Lancer cleaner.py avant !")
else:
    df_original = pd.read_csv(file_original)
    df_cleaned = pd.read_csv(file_cleaned)

    # --- IMAGE 1 : ORIGINAL ---
    print("Affichage de l'état original (500 échantillons)...")
    msno.matrix(df_original.sample(500))
    plt.title("AVANT : Données brutes avec NaN", fontsize=20)
    plt.savefig(output_original)
    print(f"Image 1 sauvegardée : {output_original}")
    plt.close()

    # --- IMAGE 2 : CLEANED ---
    print("Affichage de l'état nettoyé (500 échantillons)...")
    msno.matrix(df_cleaned.sample(500))
    plt.title("APRÈS : Nettoyage IQR + Imputation KNN", fontsize=20)
    plt.savefig(output_cleaned)
    print(f"Image 2 sauvegardée : {output_cleaned}")
    plt.close()