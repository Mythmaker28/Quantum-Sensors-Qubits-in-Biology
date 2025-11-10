#!/usr/bin/env python3
"""
Enrichissement des contraste manquants depuis FPbase CSV cache.
"""
import pandas as pd
from pathlib import Path

# Charger atlas
atlas_path = Path("data/processed/atlas_fp_optical_v2_2.csv")
df = pd.read_csv(atlas_path)

print(f"[*] Atlas: {len(df)} systemes")
print(f"    Contraste manquant: {df['contrast_normalized'].isna().sum()}")

# Charger FPbase cache
fpbase_cache = Path("data/cache/fpbase_export.csv")
if not fpbase_cache.exists():
    print("[ERREUR] FPbase cache introuvable")
    exit(1)

fpbase_df = pd.read_csv(fpbase_cache)
print(f"[*] FPbase cache: {len(fpbase_df)} lignes")
print(f"    Colonnes disponibles: {list(fpbase_df.columns[:15])}...")

# Chercher colonnes de contraste/brightness
contrast_cols = [col for col in fpbase_df.columns if 'brightness' in col.lower() or 'qy' in col.lower() or 'extinct' in col.lower()]
print(f"[*] Colonnes potentielles: {contrast_cols}")

# Pour les nouveaux systèmes sans contraste, essayer de mapper
missing_contrast = df[df['contrast_normalized'].isna()].copy()

updated = 0
for idx, row in missing_contrast.iterrows():
    name = row['protein_name']
    
    # Chercher dans FPbase
    fpbase_match = fpbase_df[fpbase_df['name'].str.lower() == name.lower()]
    
    if len(fpbase_match) > 0:
        fp_row = fpbase_match.iloc[0]
        
        # Essayer brightness / QY
        brightness = fp_row.get('brightness', None)
        qy = fp_row.get('qy', None)
        
        # Normaliser: brightness ou QY → contraste relatif
        if pd.notna(brightness) and brightness > 0:
            # Brightness normalisé (arbitraire: moyenne ~50, range 1-200)
            contrast = 0.5 + (brightness / 100.0)  # 0.5-2.5 range
            df.at[idx, 'contrast_normalized'] = round(contrast, 2)
            updated += 1
        elif pd.notna(qy) and qy > 0:
            # QY → contraste (QY typique 0.1-1.0)
            contrast = 0.5 + qy  # 0.5-1.5 range
            df.at[idx, 'contrast_normalized'] = round(contrast, 2)
            updated += 1
        else:
            # Pas de données → valeur conservative (pas de changement)
            df.at[idx, 'contrast_normalized'] = 1.0
            updated += 1
    else:
        # Pas trouvé dans FPbase → valeur conservative
        df.at[idx, 'contrast_normalized'] = 1.0
        updated += 1

print(f"\n[OK] {updated} contrastes remplis")
print(f"    Strategie: brightness/QY -> contraste relatif, sinon 1.0 (conservatif)")

# Sauvegarder
df.to_csv(atlas_path, index=False)
print(f"[OK] Atlas sauvegarde: {atlas_path}")

