#!/usr/bin/env python3
"""
FP Atlas Class Comparisons - Compare FP families/classes

Generates comparative statistics for fluorescent protein families.

Author: CLAUDE-MAINTAINER
Date: 2025-11-15
"""

import pandas as pd
import json
from pathlib import Path

def main():
    # Load curated FP dataset
    df = pd.read_csv('data/processed/atlas_fp_optical_v2_2_curated.csv')
    
    # Comparative stats by family
    comparison = {}
    for family in df['family'].unique():
        if pd.isna(family):
            continue
        df_fam = df[df['family'] == family]
        contrast = pd.to_numeric(df_fam['contrast_normalized'], errors='coerce').dropna()
        
        comparison[family] = {
            'count': len(df_fam),
            'contrast_mean': float(contrast.mean()) if len(contrast) > 0 else None,
            'contrast_median': float(contrast.median()) if len(contrast) > 0 else None,
            'is_biosensor': int(df_fam['is_biosensor'].sum()) if 'is_biosensor' in df_fam.columns else None
        }
    
    # Save
    output_dir = Path('analysis/output')
    output_dir.mkdir(exist_ok=True)
    with open(output_dir / 'class_comparisons_fp.json', 'w') as f:
        json.dump(comparison, f, indent=2)
    
    print(f"[OK] FP class comparisons saved (analysis {len(comparison)} families)")
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())

