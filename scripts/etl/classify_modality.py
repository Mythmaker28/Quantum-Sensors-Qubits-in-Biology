#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ETL Script: Classify Modality
==============================
Classifie les candidats externes selon leur modalité:
- is_fp_like=1 pour FP/FP-biosensors (fluorescence, FRET)
- is_fp_like=0 pour color centers (NV, SiV), NMR, ESR, magnéto, etc.

Input: data/interim/external_candidates.parquet
Output: data/interim/external_candidates.parquet (updated)
        reports/MODALITY_SPLIT.md
"""

import sys
from pathlib import Path
import pandas as pd
import re

# Paths
INPUT_FILE = Path("data/interim/external_candidates.parquet")
OUTPUT_FILE = INPUT_FILE  # Update in place
REPORT_FILE = Path("reports/MODALITY_SPLIT.md")

# Classification keywords
FP_KEYWORDS = [
    'fluorescent', 'gfp', 'rfp', 'cfp', 'yfp', 'mcherry', 'tdtomato',
    'fret', 'biosensor', 'chromophore', 'photoswitch', 'optical',
    'emission', 'excitation', 'quantum yield', 'brightness'
]

EXCLUDE_KEYWORDS = [
    'nv center', 'nv-center', 'silicon vacancy', 'siv', 'diamond',
    'nmr', 'esr', 'epr', 'magneto', 'spin', 'radical', 'paramagnetic'
]

def classify_fp_like(row: pd.Series) -> int:
    """Détermine si un candidat est FP-like."""
    text = f"{row.get('protein_name', '')} {row.get('family', '')}".lower()
    
    # Exclure d'abord
    for kw in EXCLUDE_KEYWORDS:
        if kw in text:
            return 0
    
    # Puis vérifier inclusion FP
    for kw in FP_KEYWORDS:
        if kw in text:
            return 1
    
    # Si ex/em présents, probablement FP
    if pd.notna(row.get('excitation_nm')) and pd.notna(row.get('emission_nm')):
        return 1
    
    # Par défaut, considérer comme non-FP si ambiguë
    return 0

def generate_report(df: pd.DataFrame):
    """Génère le rapport de split par modalité."""
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    fp_like_df = df[df['is_fp_like'] == 1]
    not_fp_df = df[df['is_fp_like'] == 0]
    
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write("# Modality Classification Report\n\n")
        f.write(f"**Date**: {pd.Timestamp.now().isoformat()}\n\n")
        
        f.write("## Summary\n\n")
        f.write(f"- **Total candidates**: {len(df)}\n")
        f.write(f"- **FP-like (optical, fluorescence, FRET)**: {len(fp_like_df)} ({len(fp_like_df)/len(df)*100:.1f}%)\n")
        f.write(f"- **Non-FP (color centers, NMR, ESR, etc.)**: {len(not_fp_df)} ({len(not_fp_df)/len(df)*100:.1f}%)\n\n")
        
        f.write("## FP-like Breakdown\n\n")
        if not fp_like_df.empty:
            f.write("| Source | Count |\n")
            f.write("|--------|-------|\n")
            for source, count in fp_like_df['source'].value_counts().items():
                f.write(f"| {source} | {count} |\n")
        
        f.write("\n## Non-FP Breakdown\n\n")
        if not not_fp_df.empty:
            f.write("| Source | Count |\n")
            f.write("|--------|-------|\n")
            for source, count in not_fp_df['source'].value_counts().items():
                f.write(f"| {source} | {count} |\n")
        
        f.write("\n## Sample FP-like Entries\n\n")
        if not fp_like_df.empty:
            f.write("```\n")
            f.write(fp_like_df[['SystemID', 'protein_name', 'source']].head(10).to_string(index=False))
            f.write("\n```\n")
    
    print(f"Report saved to {REPORT_FILE}")

def main():
    """Point d'entrée."""
    print("=" * 70)
    print("Classify Modality Pipeline")
    print("=" * 70)
    
    if not INPUT_FILE.exists():
        print(f"ERROR: {INPUT_FILE} not found!", file=sys.stderr)
        print("Run build_external_candidates.py first.", file=sys.stderr)
        sys.exit(1)
    
    # Load
    df = pd.read_parquet(INPUT_FILE)
    print(f"Loaded {len(df)} candidates")
    
    # Classify
    df['is_fp_like'] = df.apply(classify_fp_like, axis=1)
    
    # Stats
    n_fp = (df['is_fp_like'] == 1).sum()
    n_non_fp = (df['is_fp_like'] == 0).sum()
    
    print(f"\nClassification results:")
    print(f"  FP-like: {n_fp}")
    print(f"  Non-FP: {n_non_fp}")
    
    # Save updated
    df.to_parquet(OUTPUT_FILE, index=False)
    print(f"\nUpdated {OUTPUT_FILE}")
    
    # Generate report
    generate_report(df)
    
    print("\n✓ Modality classification completed!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

