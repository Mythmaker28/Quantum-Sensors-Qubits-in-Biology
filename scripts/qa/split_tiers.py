#!/usr/bin/env python3
"""
Non-destructive tier splitting - reproducible classification.
See docs/DATA_TIERS.md for tier definitions.
"""
import pandas as pd
from pathlib import Path
import sys

def split_tiers():
    """Split atlas into 3 tiers without data loss."""
    
    # Paths
    input_csv = Path("data/processed/atlas_fp_optical_v2_2.csv")
    output_curated = Path("data/processed/atlas_fp_optical_v2_2_curated.csv")
    output_candidates = Path("data/staging/atlas_fp_optical_v2_2_candidates.csv")
    output_unknown = Path("data/staging/atlas_fp_optical_v2_2_unknown.csv")
    
    print("[*] Loading atlas...")
    df = pd.read_csv(input_csv)
    initial_count = len(df)
    print(f"    Total systems: {initial_count}")
    
    # === TIER 1: CURATED_CORE ===
    # Family known + DOI + (spectra OR meaningful contrast)
    tier1_mask = (
        (df['family'] != 'Unknown') &
        (df['doi'].notna()) &
        (
            (df['excitation_nm'].notna()) |
            (df['emission_nm'].notna()) |
            (df['contrast_normalized'] > 1.5)
        )
    )
    
    tier1 = df[tier1_mask].copy()
    
    # === TIER 3: UNKNOWN/NOISY ===
    # Unknown family OR missing DOI OR placeholder triple
    tier3_mask = (
        (df['family'] == 'Unknown') |
        (df['doi'].isna()) |
        (
            (df['contrast_normalized'] == 1.0) &
            (df['excitation_nm'].isna()) &
            (df['emission_nm'].isna())
        )
    )
    
    tier3 = df[tier3_mask].copy()
    
    # === TIER 2: CANDIDATES_STAGING ===
    # Everything else (has DOI + known family but incomplete)
    tier2_mask = ~tier1_mask & ~tier3_mask
    tier2 = df[tier2_mask].copy()
    
    # Verify no data loss
    total_split = len(tier1) + len(tier2) + len(tier3)
    
    print(f"\n[*] Tier classification:")
    print(f"    TIER 1 (CURATED):   {len(tier1):3d} systems")
    print(f"    TIER 2 (CANDIDATES): {len(tier2):3d} systems")
    print(f"    TIER 3 (UNKNOWN):    {len(tier3):3d} systems")
    print(f"    TOTAL:               {total_split:3d} systems")
    
    if total_split != initial_count:
        print(f"[ERROR] Data loss detected! {initial_count} -> {total_split}")
        sys.exit(1)
    
    print(f"[OK] No data loss: {initial_count} == {total_split}")
    
    # Check for overlaps
    overlap_12 = set(tier1.index) & set(tier2.index)
    overlap_13 = set(tier1.index) & set(tier3.index)
    overlap_23 = set(tier2.index) & set(tier3.index)
    
    if overlap_12 or overlap_13 or overlap_23:
        print(f"[ERROR] Overlaps detected!")
        print(f"    T1-T2: {len(overlap_12)}, T1-T3: {len(overlap_13)}, T2-T3: {len(overlap_23)}")
        sys.exit(1)
    
    print(f"[OK] No overlaps between tiers")
    
    # Save files
    print(f"\n[*] Saving tier files...")
    
    tier1.to_csv(output_curated, index=False)
    print(f"    [TIER 1] {output_curated}")
    
    output_candidates.parent.mkdir(parents=True, exist_ok=True)
    tier2.to_csv(output_candidates, index=False)
    print(f"    [TIER 2] {output_candidates}")
    
    tier3.to_csv(output_unknown, index=False)
    print(f"    [TIER 3] {output_unknown}")
    
    # Summary statistics
    print(f"\n[*] TIER 1 (CURATED) characteristics:")
    print(f"    Families: {tier1['family'].nunique()} unique")
    print(f"    Top families: {', '.join(tier1['family'].value_counts().head(5).index.tolist())}")
    print(f"    Has spectra: {tier1['excitation_nm'].notna().sum()} with excitation")
    print(f"    Mean contrast: {tier1['contrast_normalized'].mean():.2f}")
    
    print(f"\n[*] TIER 2 (CANDIDATES) characteristics:")
    if len(tier2) > 0:
        print(f"    Families: {tier2['family'].nunique()} unique")
        print(f"    Missing spectra: {tier2['excitation_nm'].isna().sum()}")
    else:
        print(f"    (Empty - all systems classified as T1 or T3)")
    
    print(f"\n[*] TIER 3 (UNKNOWN) characteristics:")
    print(f"    Unknown family: {(tier3['family'] == 'Unknown').sum()}")
    print(f"    Placeholder contrast=1.0: {(tier3['contrast_normalized'] == 1.0).sum()}")
    print(f"    Source breakdown:")
    if 'curator' in tier3.columns:
        for curator_pattern in ['deep_harvest', 'api_harvest', 'fpbase_csv']:
            count = tier3[tier3['curator'].str.contains(curator_pattern, case=False, na=False)].shape[0]
            if count > 0:
                print(f"      {curator_pattern:15s}: {count:3d}")
    
    print(f"\n[OK] Tier splitting complete")
    print(f"[*] Original file preserved: {input_csv}")
    
    return {
        'total': initial_count,
        'tier1': len(tier1),
        'tier2': len(tier2),
        'tier3': len(tier3)
    }

if __name__ == "__main__":
    try:
        counts = split_tiers()
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

