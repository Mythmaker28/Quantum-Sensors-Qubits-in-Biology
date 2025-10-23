#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Normalize and Tier Contrasts
=============================
Ajoute deux colonnes dérivées:
- contrast_normalized: Tout converti en ΔF/F₀ (ratio)
- contrast_quality_tier: A (CI/n), B (measured), C (computed)
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

ATLAS_FILE = Path("data/processed/atlas_fp_optical.csv")

def normalize_contrast(row):
    """Convertit toutes les mesures en ΔF/F₀ normalisé."""
    ratio = row.get('contrast_ratio')
    
    if pd.isna(ratio):
        return np.nan
    
    measure_type = row.get('measure_type', 'unknown')
    
    # Already ΔF/F₀
    if 'delta_F' in str(measure_type) or 'ratio' in str(measure_type):
        return ratio
    
    # Fold-change → ΔF/F₀ = fold - 1
    if 'fold' in str(measure_type):
        return ratio - 1.0 if ratio > 1 else ratio
    
    # Percent → ratio
    if 'percent' in str(measure_type):
        return ratio / 100.0
    
    # Dynamic range → assume it's already a ratio
    if 'dynamic' in str(measure_type):
        return ratio
    
    # Brightness proxy → keep as is (not a real contrast)
    if 'brightness' in str(measure_type):
        return np.nan
    
    # Default: assume it's already normalized
    return ratio

def assign_quality_tier(row):
    """Assigne un tier de qualité."""
    source = row.get('contrast_source', 'none')
    
    if source == 'none':
        return None
    
    # Check for CI or n in condition_text
    condition = str(row.get('condition_text', ''))
    
    has_ci = 'CI' in condition or '95%' in condition
    has_n = 'n=' in condition or 'N=' in condition
    has_sd = '±' in condition or 'SD' in condition
    
    if source == 'measured' and (has_ci or has_n or has_sd):
        return 'A'  # Highest quality
    elif source == 'measured':
        return 'B'  # Measured but no stats
    elif source == 'computed':
        return 'C'  # Computed proxy
    else:
        return None

def main():
    """Point d'entrée."""
    print("=" * 70)
    print("Normalize and Tier Contrasts")
    print("=" * 70)
    
    # Load atlas
    df = pd.read_csv(ATLAS_FILE)
    print(f"Loaded {len(df)} entries")
    
    # Add normalized column
    df['contrast_normalized'] = df.apply(normalize_contrast, axis=1)
    
    # Add quality tier
    df['contrast_quality_tier'] = df.apply(assign_quality_tier, axis=1)
    
    # Stats
    print("\nNormalization results:")
    print(f"  With normalized contrast: {df['contrast_normalized'].notna().sum()}")
    
    print("\nQuality tier distribution:")
    print(df['contrast_quality_tier'].value_counts().to_string())
    
    # Save
    df.to_csv(ATLAS_FILE, index=False)
    print(f"\nUpdated {ATLAS_FILE}")
    
    print("\nOK Normalization and tiering completed!")
    return 0

if __name__ == "__main__":
    sys.exit(main())

