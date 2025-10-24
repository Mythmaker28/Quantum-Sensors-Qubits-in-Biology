#!/usr/bin/env python3
"""
Dédoublonnage Atlas v2.0
Détecte et retire doublons sur clé canonique (SystemID + DOI)
Licence: Apache-2.0
"""

import pandas as pd
import os
from pathlib import Path

def deduplicate_atlas(input_csv, output_csv):
    """Dédoublonne atlas sur SystemID + DOI"""
    
    df = pd.read_csv(input_csv)
    print(f"[LOAD] {len(df)} systemes charges")
    
    # Identifier doublons
    initial_count = len(df)
    
    # Méthode 1: Doublons exacts sur SystemID
    duplicates_systemid = df[df.duplicated(subset=['SystemID'], keep=False)]
    if len(duplicates_systemid) > 0:
        print(f"[WARN] {len(duplicates_systemid)} doublons SystemID detectes")
        for sid in duplicates_systemid['SystemID'].unique():
            print(f"  - {sid}: {len(duplicates_systemid[duplicates_systemid['SystemID']==sid])} occurrences")
    
    # Retirer doublons (garder première occurrence)
    df = df.drop_duplicates(subset=['SystemID'], keep='first')
    
    # Méthode 2: Doublons protein_name + DOI
    duplicates_name_doi = df[df.duplicated(subset=['protein_name', 'doi'], keep=False)]
    if len(duplicates_name_doi) > 0:
        print(f"[WARN] {len(duplicates_name_doi)} doublons protein_name+DOI")
    
    df = df.drop_duplicates(subset=['protein_name', 'doi'], keep='first')
    
    final_count = len(df)
    removed = initial_count - final_count
    
    print(f"[DEDUP] {removed} doublons retires")
    print(f"[FINAL] {final_count} systemes uniques")
    
    # Sauvegarder
    df.to_csv(output_csv, index=False)
    print(f"[SAVE] {output_csv}")
    
    return df, removed

if __name__ == "__main__":
    input_path = "data/processed/atlas_fp_optical_v1_3.csv"
    output_path = "data/processed/atlas_fp_optical_v2_0.csv"
    
    if os.path.exists(input_path):
        df, removed = deduplicate_atlas(input_path, output_path)
        print(f"\n[OK] Dedoublonnage termine: {removed} doublons retires")
    else:
        print(f"[ERROR] Fichier non trouve: {input_path}")

