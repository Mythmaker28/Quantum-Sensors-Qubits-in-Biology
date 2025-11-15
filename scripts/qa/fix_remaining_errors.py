#!/usr/bin/env python3
"""
Correction finale: supprimer lignes sans family/is_biosensor obligatoires.
"""
import pandas as pd
from pathlib import Path

csv_path = Path("data/processed/atlas_fp_optical_v2_2.csv")
df = pd.read_csv(csv_path)

print(f"[*] Avant correction: {len(df)} systemes")

# Identifier lignes problematiques
problematic = df[df['family'].isna() | df['is_biosensor'].isna()]
print(f"\n[*] Lignes a supprimer (family ou is_biosensor manquants):")
for idx, row in problematic.iterrows():
    print(f"    [{idx}] {row['SystemID']} | {row['protein_name']} | DOI: {row['doi']}")

# Supprimer (car fields obligatoires et pas de moyen automatise de verifier)
df = df[df['family'].notna() & df['is_biosensor'].notna()].copy()

print(f"\n[OK] Apres correction: {len(df)} systemes")

# Sauvegarder
df.to_csv(csv_path, index=False)
print(f"[OK] Sauvegarde: {csv_path}")








