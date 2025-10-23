#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Apply Curated Contrasts — Real Data from Literature
====================================================
Applique les mesures de contraste curées depuis la littérature.

Toutes les valeurs proviennent d'articles peer-reviewed OA avec DOI.
"""

import sys
from pathlib import Path
import pandas as pd

# Paths
CURATED_FILE = Path("data/curated_contrasts.csv")
ATLAS_FILE = Path("data/processed/atlas_fp_optical.csv")

def apply_curated():
    """Applique les contrastes curés à l'atlas."""
    # Load curated
    curated_df = pd.read_csv(CURATED_FILE)
    print(f"Loaded {len(curated_df)} curated measurements")
    
    # Load atlas
    atlas_df = pd.read_csv(ATLAS_FILE)
    print(f"Loaded atlas with {len(atlas_df)} entries")
    
    # Apply each curated measurement
    updated = 0
    for _, row in curated_df.iterrows():
        name = row['protein_name']
        
        # Find in atlas
        mask = atlas_df['protein_name'] == name
        
        if mask.any():
            # Update contrast fields
            atlas_df.loc[mask, 'contrast_ratio'] = row['contrast_ratio']
            atlas_df.loc[mask, 'contrast_source'] = 'measured'
            atlas_df.loc[mask, 'condition_text'] = row['condition_text']
            atlas_df.loc[mask, 'source_refs'] = row['source_refs']
            atlas_df.loc[mask, 'license_source'] = row['license_source']
            
            updated += 1
            print(f"  Updated: {name} = {row['contrast_ratio']}")
        else:
            print(f"  WARNING: {name} not found in atlas (will skip)")
    
    # Save
    atlas_df.to_csv(ATLAS_FILE, index=False)
    print(f"\nUpdated {updated} entries in atlas")
    
    # Stats
    n_measured = (atlas_df['contrast_source'] == 'measured').sum()
    n_total = len(atlas_df)
    
    print(f"\nFinal stats:")
    print(f"  N_fp_like_total = {n_total}")
    print(f"  N_fp_like_with_contrast_measured = {n_measured}")
    
    return n_total, n_measured

def main():
    """Point d'entrée."""
    print("=" * 70)
    print("Apply Curated Contrasts — Literature Values")
    print("=" * 70)
    
    n_total, n_measured = apply_curated()
    
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    print(f"N_fp_like_total = {n_total}")
    print(f"N_fp_like_with_contrast_measured = {n_measured}")
    print("=" * 70)
    
    if n_measured >= 25:
        print("\nOK Threshold MET (>=25)!")
        return 0
    else:
        print(f"\nWARNING: Need {25 - n_measured} more measurements to reach threshold")
        return 1

if __name__ == "__main__":
    sys.exit(main())

