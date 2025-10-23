#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ETL Script: Compute Contrast Proxies
=====================================
Pour les candidats sans mesure de contraste directe, calcule un proxy
basé sur quantum yield (QY), extinction coefficient (ε), brightness.

Input: data/interim/external_candidates.parquet
       data/interim/pmc_contrast_measurements.parquet
Output: data/interim/external_candidates.parquet (updated with contrast_proxy)
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Paths
CANDIDATES_FILE = Path("data/interim/external_candidates.parquet")
MEASUREMENTS_FILE = Path("data/interim/pmc_contrast_measurements.parquet")

def compute_brightness_proxy(qy: float, ext_coef: float) -> float:
    """
    Calcule un proxy de contraste basé sur brightness.
    Brightness = QY × ε
    
    Normalise entre 0-10 (arbitrary scale for contrast proxy)
    """
    if pd.isna(qy) or pd.isna(ext_coef):
        return np.nan
    
    brightness = qy * ext_coef
    
    # Normaliser (typiquement ε ~ 10^4-10^5, QY ~ 0.1-1.0)
    # brightness ~ 10^3 - 10^5
    # On log-scale puis normalise
    if brightness <= 0:
        return np.nan
    
    # Log scale
    log_bright = np.log10(brightness)
    
    # Normaliser entre 1-10
    # Supposons log(brightness) entre 3-5 pour la plupart des FPs
    normalized = (log_bright - 3) / 2 * 9 + 1  # Map [3,5] -> [1,10]
    normalized = np.clip(normalized, 1, 10)
    
    return normalized

def main():
    """Point d'entrée."""
    print("=" * 70)
    print("Compute Contrast Proxies Pipeline")
    print("=" * 70)
    
    if not CANDIDATES_FILE.exists():
        print(f"ERROR: {CANDIDATES_FILE} not found!", file=sys.stderr)
        sys.exit(1)
    
    # Load candidates
    df = pd.read_parquet(CANDIDATES_FILE)
    print(f"Loaded {len(df)} candidates")
    
    # Load measurements if exist
    if MEASUREMENTS_FILE.exists():
        measurements_df = pd.read_parquet(MEASUREMENTS_FILE)
        print(f"Loaded {len(measurements_df)} PMC measurements")
        
        # Merge measurements into candidates
        # Group by SystemID, aggregate (mean) contrast_ratio
        agg_measurements = measurements_df.groupby('SystemID').agg({
            'contrast_ratio': 'mean',
            'pmcid': 'first',
            'doi': 'first',
            'condition_text': 'first'
        }).reset_index()
        
        df = df.merge(agg_measurements, on='SystemID', how='left')
    else:
        print("No PMC measurements found")
        df['contrast_ratio'] = np.nan
    
    # Compute proxies for those without measured contrast
    df['contrast_proxy'] = df.apply(
        lambda row: compute_brightness_proxy(
            row.get('quantum_yield'), 
            row.get('extinction_coef')
        ) if pd.isna(row.get('contrast_ratio')) else np.nan,
        axis=1
    )
    
    # Set contrast_source
    df['contrast_source'] = df.apply(
        lambda row: 'measured' if pd.notna(row.get('contrast_ratio'))
                    else ('computed' if pd.notna(row.get('contrast_proxy')) else 'none'),
        axis=1
    )
    
    # Merge contrast_ratio and proxy into single column for simplicity
    df['contrast_final'] = df.apply(
        lambda row: row.get('contrast_ratio') if pd.notna(row.get('contrast_ratio'))
                    else row.get('contrast_proxy'),
        axis=1
    )
    
    # Stats
    n_measured = (df['contrast_source'] == 'measured').sum()
    n_computed = (df['contrast_source'] == 'computed').sum()
    n_none = (df['contrast_source'] == 'none').sum()
    
    print(f"\nContrast coverage:")
    print(f"  Measured: {n_measured}")
    print(f"  Computed: {n_computed}")
    print(f"  None: {n_none}")
    
    # Save
    df.to_parquet(CANDIDATES_FILE, index=False)
    print(f"\nUpdated {CANDIDATES_FILE}")
    
    print("\n✓ Contrast proxies computed!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

