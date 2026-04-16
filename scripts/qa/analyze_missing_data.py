#!/usr/bin/env python3
"""
Analyse détaillée des données manquantes dans l'atlas.
"""
import pandas as pd
from pathlib import Path

def analyze_missing():
    csv_path = Path("data/processed/atlas_fp_optical_v2_2.csv")
    df = pd.read_csv(csv_path)
    
    critical_cols = ['family', 'is_biosensor', 'contrast_normalized', 
                     'quality_tier', 'temperature_K', 'doi', 
                     'license', 'method', 'curator']
    
    print(f"Total systemes: {len(df)}\n")
    print("=" * 80)
    
    # Analyse par colonne
    for col in critical_cols:
        missing_count = df[col].isna().sum()
        if missing_count > 0:
            print(f"\n{col}: {missing_count} manquants")
            missing_rows = df[df[col].isna()]
            
            # Montrer quelques exemples
            print("  Exemples:")
            for idx, row in missing_rows.head(3).iterrows():
                sid = row.get('SystemID', 'NO_ID')
                name = row.get('protein_name', 'NO_NAME')
                doi = row.get('doi', 'NO_DOI')
                print(f"    [{idx}] {sid} | {name} | DOI: {doi}")
    
    print("\n" + "=" * 80)
    print("\nLignes SANS SystemID:")
    no_id = df[df['SystemID'].isna()]
    print(f"  Count: {len(no_id)}")
    if len(no_id) > 0:
        print(no_id[['protein_name', 'family', 'doi']].head(10))
    
    print("\n" + "=" * 80)
    print("\nLignes SANS DOI:")
    no_doi = df[df['doi'].isna()]
    print(f"  Count: {len(no_doi)}")
    if len(no_doi) > 0:
        print(no_doi[['SystemID', 'protein_name', 'family']].head(10))
    
    print("\n" + "=" * 80)
    print("\nSTATISTIQUES:")
    print(f"  Lignes avec DOI valide: {df['doi'].notna().sum()}")
    print(f"  Lignes avec license: {df['license'].notna().sum()}")
    print(f"  Lignes avec curator: {df['curator'].notna().sum()}")
    print(f"  Lignes avec temperature_K: {df['temperature_K'].notna().sum()}")
    print(f"  Lignes avec method: {df['method'].notna().sum()}")
    
    # Lignes avec DOI MAIS sans metadata
    has_doi_no_meta = df[df['doi'].notna() & (df['curator'].isna() | df['method'].isna())]
    print(f"\n  Lignes avec DOI MAIS sans curator/method: {len(has_doi_no_meta)}")

if __name__ == "__main__":
    analyze_missing()










