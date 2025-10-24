#!/usr/bin/env python3
"""
Intègre specialist database dans atlas v2.0
Ajoute biosenseurs non déjà présents
Licence: Apache-2.0
"""

import pandas as pd
import json

# Charger atlas actuel
atlas = pd.read_csv('data/processed/atlas_fp_optical_v2_0.csv')
print(f"[LOAD] Atlas actuel: {len(atlas)} systemes")

# Charger specialist
with open('data/raw/specialist/specialist_all.json') as f:
    specialist = json.load(f)

print(f"[LOAD] Specialist DB: {len(specialist)} systemes")

# Convertir specialist en DataFrame
specialist_df = pd.DataFrame(specialist)

# Trouver nouveaux (pas déjà dans atlas)
existing_names = set(atlas['protein_name'].str.lower())
new_systems = []

for _, row in specialist_df.iterrows():
    name = str(row.get('name', '')).lower()
    if name and name not in existing_names:
        new_systems.append(row)

print(f"[NEW] {len(new_systems)} systemes nouveaux trouves")

# Ajouter au dataset
if new_systems:
    new_df = pd.DataFrame(new_systems)
    combined = pd.concat([atlas, new_df], ignore_index=True)
    combined.to_csv('data/processed/atlas_fp_optical_v2_0_expanded.csv', index=False)
    print(f"[SAVE] {len(combined)} systemes total (atlas + specialist)")
else:
    print("[INFO] Aucun nouveau systeme (deja tous presents)")

