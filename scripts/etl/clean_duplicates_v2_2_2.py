#!/usr/bin/env python3
"""
Clean Duplicates - Atlas v2.2.2
================================

Nettoie les doublons du dataset avant l'équilibrage.
Garde la première occurrence de chaque système.
"""

import pandas as pd
from pathlib import Path

def clean_duplicates():
    """Nettoie les doublons du dataset"""
    
    print("=" * 80)
    print("NETTOYAGE DOUBLONS - Atlas v2.2.2")
    print("=" * 80)
    
    # Charger le dataset
    training_path = Path("data/processed/TRAINING_TABLE_v2_2.csv")
    df = pd.read_csv(training_path)
    
    print(f"[LOAD] Dataset original: {len(df)} systèmes")
    
    # Identifier les doublons
    duplicates = df['canonical_name'].duplicated()
    n_duplicates = duplicates.sum()
    
    print(f"[DUPLICATES] Doublons détectés: {n_duplicates}")
    
    if n_duplicates > 0:
        # Afficher les doublons
        duplicate_names = df[duplicates]['canonical_name'].unique()
        print(f"  Systèmes dupliqués: {list(duplicate_names)}")
        
        # Garder la première occurrence de chaque système
        df_clean = df.drop_duplicates(subset=['canonical_name'], keep='first')
        
        print(f"[CLEAN] Dataset nettoyé: {len(df_clean)} systèmes")
        print(f"  Systèmes supprimés: {len(df) - len(df_clean)}")
        
        # Sauvegarder le dataset nettoyé
        df_clean.to_csv(training_path, index=False, encoding='utf-8')
        print(f"[SAVE] Dataset nettoyé sauvegardé: {training_path}")
        
        return df_clean
    else:
        print("[CLEAN] Aucun doublon détecté")
        return df

def main():
    """Fonction principale"""
    
    df_clean = clean_duplicates()
    
    print("\n" + "=" * 80)
    print("NETTOYAGE TERMINÉ")
    print("=" * 80)
    print(f"Systèmes finaux: {len(df_clean)}")
    
    # Vérifier qu'il n'y a plus de doublons
    remaining_duplicates = df_clean['canonical_name'].duplicated().sum()
    print(f"Doublons restants: {remaining_duplicates}")
    
    if remaining_duplicates == 0:
        print("[SUCCESS] Dataset nettoyé avec succès !")
        return True
    else:
        print("[WARNING] Des doublons persistent")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n[SUCCESS] Nettoyage des doublons réussi !")
    else:
        print("\n[WARNING] Nettoyage des doublons partiellement réussi")
