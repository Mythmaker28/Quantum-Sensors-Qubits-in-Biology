#!/usr/bin/env python3
"""
Nettoyage conservateur de l'atlas - SANS fabrication de données.

Actions:
1. Supprimer lignes sans DOI (invalides)
2. Générer SystemID manquants (identifiant technique)
3. Remplir curator manquants (métadonnée technique)
4. Laisser temperature_K, method, license vides si inconnus
"""
import pandas as pd
from pathlib import Path
import sys

def clean_atlas():
    csv_path = Path("data/processed/atlas_fp_optical_v2_2.csv")
    backup_path = Path("data/processed/atlas_fp_optical_v2_2.csv.backup")
    
    print("[*] Chargement de l'atlas...")
    df = pd.read_csv(csv_path)
    initial_count = len(df)
    print(f"    Initial: {initial_count} systemes")
    
    # Backup
    df.to_csv(backup_path, index=False)
    print(f"[OK] Backup cree: {backup_path}")
    
    # 1. SUPPRIMER lignes sans DOI (INVALIDES)
    invalid_no_doi = df[df['doi'].isna()]
    print(f"\n[*] Suppression de {len(invalid_no_doi)} lignes SANS DOI:")
    for idx, row in invalid_no_doi.iterrows():
        print(f"    - [{idx}] {row.get('protein_name', 'NO_NAME')}")
    
    df = df[df['doi'].notna()].copy()
    print(f"[OK] Apres suppression: {len(df)} systemes")
    
    # 2. GENERER SystemID manquants (identifiant technique)
    no_systemid = df['SystemID'].isna()
    if no_systemid.any():
        print(f"\n[*] Generation de SystemID pour {no_systemid.sum()} lignes...")
        
        # Trouver le prochain ID disponible
        existing_ids = df[df['SystemID'].notna()]['SystemID'].tolist()
        existing_nums = []
        for sid in existing_ids:
            if isinstance(sid, str) and sid.startswith('FP_'):
                try:
                    num = int(sid.split('_')[1])
                    existing_nums.append(num)
                except:
                    pass
        
        next_id = max(existing_nums) + 1 if existing_nums else 200
        
        for idx in df[no_systemid].index:
            df.at[idx, 'SystemID'] = f'FP_{next_id:04d}'
            next_id += 1
        
        print(f"[OK] SystemID generes: FP_XXXX de {max(existing_nums)+1 if existing_nums else 200} a {next_id-1}")
    
    # 3. REMPLIR curator manquants (metadonnee technique)
    no_curator = df['curator'].isna()
    if no_curator.any():
        print(f"\n[*] Remplissage curator pour {no_curator.sum()} lignes...")
        df.loc[no_curator, 'curator'] = 'v2.2.2_cleanup'
        print(f"[OK] Curator rempli: 'v2.2.2_cleanup'")
    
    # 4. LAISSER vides: license, temperature_K, method si inconnus
    # (PAS de fabrication de valeurs scientifiques)
    print(f"\n[INFO] Champs laisses vides si inconnus (pas de fabrication):")
    print(f"    - license: {df['license'].isna().sum()} vides")
    print(f"    - temperature_K: {df['temperature_K'].isna().sum()} vides")
    print(f"    - method: {df['method'].isna().sum()} vides")
    
    # 5. SAUVEGARDER
    df.to_csv(csv_path, index=False)
    print(f"\n[OK] Atlas nettoye sauvegarde: {csv_path}")
    print(f"    Avant: {initial_count} systemes")
    print(f"    Apres: {len(df)} systemes")
    print(f"    Supprimes: {initial_count - len(df)}")
    
    return len(df)

if __name__ == "__main__":
    try:
        final_count = clean_atlas()
        sys.exit(0)
    except Exception as e:
        print(f"[ERREUR] {e}")
        sys.exit(1)







