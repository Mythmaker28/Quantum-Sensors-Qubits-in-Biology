#!/usr/bin/env python3
"""
FP Atlas Descriptive Statistics

Overall descriptive statistics for the curated FP atlas.

Author: CLAUDE-MAINTAINER
Date: 2025-11-15
"""

import pandas as pd
import json
from pathlib import Path

def main():
    df = pd.read_csv('data/processed/atlas_fp_optical_v2_2_curated.csv')
    
    stats = {
        'total_systems': len(df),
        'families': df['family'].nunique(),
        'biosensors': int(df['is_biosensor'].sum()) if 'is_biosensor' in df.columns else None,
        'tiers': df['quality_tier'].value_counts().to_dict() if 'quality_tier' in df.columns else {},
        'contrast': {
            'mean': float(df['contrast_normalized'].mean()),
            'median': float(df['contrast_normalized'].median()),
            'min': float(df['contrast_normalized'].min()),
            'max': float(df['contrast_normalized'].max())
        }
    }
    
    output_dir = Path('analysis/output')
    output_dir.mkdir(exist_ok=True)
    with open(output_dir / 'descriptive_stats_fp.json', 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"[OK] FP descriptive stats: {stats['total_systems']} systems, {stats['families']} families")
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())

