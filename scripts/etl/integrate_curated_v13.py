#!/usr/bin/env python3
"""
Integrate curated contrasts into final build
=============================================
"""

import pandas as pd
import sys
from pathlib import Path

def main():
    """Integrate curated data with candidates."""
    
    # Load curated contrasts
    curated_path = Path("data/curated_contrasts_v1_3.csv")
    if not curated_path.exists():
        print(f"ERROR: {curated_path} not found")
        return 1
    
    df_curated = pd.read_csv(curated_path)
    print(f"Loaded {len(df_curated)} curated entries")
    
    # Load external candidates (from specialists + PMC)
    candidates_path = Path("data/interim/external_candidates_v1_3.parquet")
    if candidates_path.exists():
        df_candidates = pd.read_parquet(candidates_path)
        print(f"Loaded {len(df_candidates)} candidate entries")
        
        # Merge curated into candidates by protein_name
        # Curated takes priority
        merged = pd.merge(
            df_candidates,
            df_curated,
            on='protein_name',
            how='outer',
            suffixes=('_candidate', '_curated')
        )
        
        # Coalesce: prefer curated values
        for col in ['family', 'contrast_value', 'doi', 'pmcid', 'license']:
            col_curated = f'{col}_curated'
            col_candidate = f'{col}_candidate'
            if col_curated in merged.columns and col_candidate in merged.columns:
                merged[col] = merged[col_curated].fillna(merged[col_candidate])
            elif col_curated in merged.columns:
                merged[col] = merged[col_curated]
            elif col_candidate in merged.columns:
                merged[col] = merged[col_candidate]
        
        # Keep curated-specific columns
        curated_cols = ['contrast_unit', 'contrast_normalized', 'quality_tier', 
                       'context', 'temperature_K', 'pH', 'is_biosensor']
        for col in curated_cols:
            if col in df_curated.columns:
                curated_map = df_curated.set_index('protein_name')[col].to_dict()
                if col not in merged.columns:
                    merged[col] = merged['protein_name'].map(curated_map)
                else:
                    # Fill missing values from curated
                    merged[col] = merged[col].fillna(merged['protein_name'].map(curated_map))
        
        # Clean up suffixed columns
        merged = merged[[c for c in merged.columns if not c.endswith('_candidate') and not c.endswith('_curated')]]
        
        final_df = merged
    else:
        # No candidates, use curated only
        print("No external candidates found, using curated data only")
        final_df = df_curated
    
    # Add SystemID
    final_df = final_df.reset_index(drop=True)
    final_df['SystemID'] = ['FP_' + str(i+1).zfill(4) for i in range(len(final_df))]
    
    # Reorder columns
    col_order = ['SystemID', 'protein_name', 'family', 'is_biosensor', 
                 'contrast_value', 'contrast_unit', 'contrast_normalized', 'quality_tier',
                 'context', 'temperature_K', 'pH',
                 'doi', 'pmcid', 'license', 'source', 'source_note']
    
    # Keep only existing columns in order
    final_cols = [c for c in col_order if c in final_df.columns]
    remaining_cols = [c for c in final_df.columns if c not in final_cols]
    final_df = final_df[final_cols + remaining_cols]
    
    # Save final atlas
    output_csv = Path("data/processed/atlas_fp_optical_v1_3.csv")
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    final_df.to_csv(output_csv, index=False)
    print(f"\nSaved final atlas: {output_csv}")
    print(f"  Total systems: {len(final_df)}")
    print(f"  Measured: {final_df['contrast_value'].notna().sum()}")
    
    # Save parquet
    output_parquet = Path("data/processed/atlas_fp_optical_v1_3.parquet")
    final_df.to_parquet(output_parquet, index=False)
    print(f"Saved parquet: {output_parquet}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

