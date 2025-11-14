#!/usr/bin/env python3
"""
Critical analysis of atlas quality and composition.
NO modifications - pure analysis.
"""
import pandas as pd
from pathlib import Path

csv_path = Path("data/processed/atlas_fp_optical_v2_2.csv")
df = pd.read_csv(csv_path)

print("=" * 80)
print("ATLAS QUALITY ANALYSIS - NO MODIFICATIONS")
print("=" * 80)

print(f"\n[1] TOTAL ROWS: {len(df)}")

print(f"\n[2] FAMILY DISTRIBUTION (top 10):")
print(df['family'].value_counts().head(10))

print(f"\n[3] DATA QUALITY INDICATORS:")
print(f"    Unknown family: {(df['family'] == 'Unknown').sum()}")
print(f"    Missing is_biosensor: {df['is_biosensor'].isna().sum()}")
print(f"    Contrast exactly 1.0: {(df['contrast_normalized'] == 1.0).sum()}")
print(f"    Missing excitation: {df['excitation_nm'].isna().sum()}")
print(f"    Missing emission: {df['emission_nm'].isna().sum()}")
print(f"    Has DOI: {df['doi'].notna().sum()}")
print(f"    Missing DOI: {df['doi'].isna().sum()}")

print(f"\n[4] PLACEHOLDER ANALYSIS:")
placeholder = df[(df['family'] == 'Unknown') & (df['contrast_normalized'] == 1.0)]
print(f"    Unknown + contrast=1.0 (placeholder): {len(placeholder)}")

print(f"\n[5] SOURCE ANALYSIS (curator field):")
if 'curator' in df.columns:
    print("    Curator patterns:")
    for pattern in ['v1.2.1', 'v1.3', 'v2.0', 'v2.1', 'v2.2.2_cleanup', 
                    'api_harvest', 'deep_harvest', 'fpbase']:
        count = df[df['curator'].str.contains(pattern, case=False, na=False)].shape[0]
        if count > 0:
            print(f"      {pattern:20s}: {count:3d}")

print(f"\n[6] TIER CLASSIFICATION (provisional):")

# Tier 1: High confidence - curated with full metadata
tier1 = df[
    (df['family'] != 'Unknown') & 
    (df['doi'].notna()) & 
    (
        (df['excitation_nm'].notna()) | 
        (df['emission_nm'].notna()) | 
        (df['contrast_normalized'] > 1.5)
    )
]

# Tier 2: Candidates - has DOI but incomplete
tier2 = df[
    (df['doi'].notna()) &
    ~df.index.isin(tier1.index) &
    (df['family'] != 'Unknown')
]

# Tier 3: Unknown/placeholder
tier3 = df[
    (df['family'] == 'Unknown') | 
    (df['doi'].isna()) |
    ((df['contrast_normalized'] == 1.0) & 
     (df['excitation_nm'].isna()) & 
     (df['emission_nm'].isna()))
]

# Remove overlap
tier3 = df[~df.index.isin(tier1.index) & ~df.index.isin(tier2.index)]

print(f"    TIER 1 (CURATED_CORE):       {len(tier1):3d} systems")
print(f"    TIER 2 (CANDIDATES_STAGING): {len(tier2):3d} systems")
print(f"    TIER 3 (UNKNOWN/NOISY):      {len(tier3):3d} systems")
print(f"    TOTAL:                       {len(tier1) + len(tier2) + len(tier3):3d}")

print(f"\n[7] COMPARISON WITH fp-qubit-design REPORT:")
print(f"    fp-qubit-design reported: ~193 usable, ~103 noisy")
print(f"    Our Tier 1 (curated):     {len(tier1)}")
print(f"    Our Tier 3 (unknown):     {len(tier3)}")
print(f"    Match: {'YES' if abs(len(tier1) - 193) < 10 and abs(len(tier3) - 103) < 10 else 'NEEDS INVESTIGATION'}")

print(f"\n[8] RECOMMENDED ACTION:")
if len(tier3) > 50:
    print(f"    HIGH: {len(tier3)} systems need isolation/staging")
    print(f"    Create tier structure to separate curated from auto-harvested")
else:
    print(f"    LOW: Only {len(tier3)} systems need attention")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE - NO FILES MODIFIED")
print("=" * 80)







