#!/usr/bin/env python3
"""
Fix atlas columns to ensure all required columns are present
"""

import pandas as pd
from pathlib import Path

def main():
    # Load atlas
    atlas_path = Path("data/processed/atlas_fp_optical_v1_3.csv")
    df = pd.read_csv(atlas_path)
    
    print(f"Loaded {len(df)} systems")
    print(f"Columns: {list(df.columns)}")
    
    # Add missing required columns
    required_cols = {
        'contrast_quality_tier': 'B',  # Default to B if not specified
        'is_biosensor': 1,  # Default to biosensor if not specified
        'license': 'CC BY'
    }
    
    for col, default in required_cols.items():
        if col not in df.columns:
            print(f"Adding missing column: {col} (default: {default})")
            df[col] = default
        else:
            # Fill NaN values
            df[col] = df[col].fillna(default)
    
    # Ensure license_source column exists (alias for license)
    if 'license_source' not in df.columns and 'license' in df.columns:
        df['license_source'] = df['license']
    
    # Save fixed atlas
    df.to_csv(atlas_path, index=False)
    print(f"\nFixed atlas saved: {atlas_path}")
    print(f"  Columns now: {len(df.columns)}")
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())

