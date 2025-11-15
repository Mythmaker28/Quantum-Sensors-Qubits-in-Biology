#!/usr/bin/env python3
# encoding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def plot_family_distribution():
    """
    Charge les données de l'atlas, génère un graphique de la distribution
    des systèmes par famille et le sauvegarde.
    """
    # Chemins
    data_file = Path("data/processed/atlas_fp_optical_v2_2_curated.csv")
    output_dir = Path("figures/generated")
    output_file = output_dir / "family_distribution.png"

    # Vérification des fichiers et répertoires
    if not data_file.exists():
        print(f"ERREUR : Fichier de données non trouvé : {data_file}")
        return
    output_dir.mkdir(parents=True, exist_ok=True)

    # Chargement des données
    print(f"Chargement des données depuis '{data_file}'...")
    df = pd.read_csv(data_file)

    # Calcul de la distribution
    family_counts = df['family'].value_counts()

    # Création du graphique
    print("Génération du graphique...")
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 8))
    
    family_counts.plot(kind='barh', ax=ax, color='skyblue')
    
    # Amélioration de l'esthétique
    ax.set_title('Distribution des Systèmes par Famille dans l\'Atlas', fontsize=16)
    ax.set_xlabel('Nombre de Systèmes', fontsize=12)
    ax.set_ylabel('Famille', fontsize=12)
    ax.invert_yaxis()  # La famille la plus nombreuse en haut
    ax.grid(axis='x', linestyle='--', alpha=0.7)

    # Ajouter le nombre exact à côté de chaque barre
    for index, value in enumerate(family_counts):
        ax.text(value, index, f' {value}', va='center')

    plt.tight_layout()

    # Sauvegarde du graphique
    print(f"Sauvegarde du graphique dans '{output_file}'...")
    plt.savefig(output_file, dpi=300)
    plt.close()

    print("\nGraphique généré avec succès !")

if __name__ == "__main__":
    plot_family_distribution()
