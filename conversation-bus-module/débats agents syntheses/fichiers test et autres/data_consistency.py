#!/usr/bin/env python3
# encoding: utf-8

import pandas as pd
from pathlib import Path

def check_data_consistency():
    """
    Analyse le jeu de données pour identifier des incohérences potentielles.
    """
    data_file = Path("data/processed/atlas_fp_optical_v2_2_curated.csv")

    if not data_file.exists():
        print(f"ERREUR : Fichier de données non trouvé : {data_file}")
        return

    print(f"Chargement des données depuis '{data_file}'...")
    df = pd.read_csv(data_file)
    
    print("\n" + "="*80)
    print("             VÉRIFICATION DE LA COHÉRENCE DES DONNÉES")
    print("="*80)

    # Test 1: Incohérence entre famille et nom du système
    print("\n[TEST 1] Recherche d'incohérences entre 'family' et 'system_name'...")
    inconsistencies = []
    # Exemple simple : si 'Calcium' est dans la famille, on s'attend à voir 'Ca' ou 'GCaMP' dans le nom
    calcium_keywords = ['Ca', 'GCaMP', 'RCaMP', 'jRGECO', 'jGCaMP']
    voltage_keywords = ['Voltage', 'ASAP', 'ArcLight', 'VSFP']
    
    calcium_df = df[df['family'] == 'Calcium']
    for index, row in calcium_df.iterrows():
        if not any(keyword in row['system_name'] for keyword in calcium_keywords):
            inconsistencies.append(f"  - Ligne {index}: Famille 'Calcium' mais nom '{row['system_name']}' ne contient pas de mot-clé attendu.")
            
    voltage_df = df[df['family'] == 'Voltage']
    for index, row in voltage_df.iterrows():
        if not any(keyword in row['system_name'] for keyword in voltage_keywords):
            inconsistencies.append(f"  - Ligne {index}: Famille 'Voltage' mais nom '{row['system_name']}' ne contient pas de mot-clé attendu.")

    if inconsistencies:
        print("Incohérences trouvées :")
        for line in inconsistencies:
            print(line)
    else:
        print("Aucune incohérence évidente trouvée entre la famille et le nom du système.")

    # Test 2: Détection de valeurs aberrantes simples pour le rendement quantique (q_yield)
    print("\n[TEST 2] Détection de valeurs aberrantes pour le rendement quantique (q_yield)...")
    if 'q_yield' in df.columns:
        q_yield_stats = df['q_yield'].describe()
        mean = q_yield_stats['mean']
        std = q_yield_stats['std']
        # Définir une valeur aberrante comme étant > 3 écarts-types de la moyenne
        outlier_threshold = mean + 3 * std
        outliers = df[df['q_yield'] > outlier_threshold]

        if not outliers.empty:
            print(f"Valeurs potentiellement aberrantes trouvées (q_yield > {outlier_threshold:.2f}):")
            print(outliers[['system_name', 'family', 'q_yield']])
        else:
            print("Aucune valeur aberrante évidente détectée pour le rendement quantique.")
    else:
        print("La colonne 'q_yield' n'existe pas, test ignoré.")

    print("\n" + "="*80)
    print("                      FIN DE LA VÉRIFICATION")
    print("="*80)

if __name__ == "__main__":
    check_data_consistency()
