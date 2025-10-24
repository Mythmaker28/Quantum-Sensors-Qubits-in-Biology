#!/usr/bin/env python3
"""
Fallback Atlas Builder v1.3
============================

Build Atlas v1.3 using existing v1.2.1 data + specialist DBs + curated additions.
Used when external APIs (FPbase, PMC) are unavailable.

Author: Biological Qubit Atlas Team
License: MIT
"""

import json
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import hashlib
import time

def load_v1_2_1_data() -> pd.DataFrame:
    """Load existing v1.2.1 atlas data."""
    v121_path = Path("data/processed/atlas_fp_optical.csv")
    
    if not v121_path.exists():
        print("WARNING: v1.2.1 data not found, starting from scratch")
        return pd.DataFrame()
    
    df = pd.read_csv(v121_path)
    print(f"Loaded {len(df)} systems from v1.2.1")
    
    # Ensure required columns exist
    if 'contrast_normalized' not in df.columns and 'contrast_value' in df.columns:
        df['contrast_normalized'] = df['contrast_value']
    
    if 'contrast_quality_tier' not in df.columns:
        df['contrast_quality_tier'] = df.apply(
            lambda row: 'A' if pd.notna(row.get('n')) or pd.notna(row.get('ci_low')) 
            else ('B' if pd.notna(row.get('contrast_value')) else 'C'),
            axis=1
        )
    
    return df

def load_specialist_data() -> pd.DataFrame:
    """Load specialist database biosensors."""
    spec_path = Path("data/raw/specialist/specialist_all.json")
    
    if not spec_path.exists():
        print("WARNING: Specialist data not found")
        return pd.DataFrame()
    
    with open(spec_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    records = []
    for result in data.get('results', []):
        if result['status'] != 'success':
            continue
        
        for biosensor in result.get('biosensors', []):
            record = {
                'protein_name': biosensor.get('name'),
                'family': biosensor.get('family'),
                'is_biosensor': 1,
                'source': result['source'],
                'source_refs': biosensor.get('doi'),
                'license_source': 'varies (see DOI)',
                'contrast_quality_tier': 'C'  # No measurements yet
            }
            records.append(record)
    
    df = pd.DataFrame(records)
    print(f"Loaded {len(df)} specialist biosensors")
    return df

def create_extended_fp_list() -> pd.DataFrame:
    """Create extended list of standard FPs to reach 200+ total."""
    # Well-known FPs from literature (real, no invented data)
    fps = [
        # GFP variants
        {'protein_name': 'EGFP', 'family': 'GFP-like', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'sfGFP', 'family': 'GFP-like', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'mNeonGreen', 'family': 'GFP-like', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'mClover3', 'family': 'GFP-like', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'mCitrine', 'family': 'GFP-like', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'mVenus', 'family': 'GFP-like', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'YFP', 'family': 'GFP-like', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'SYFP2', 'family': 'GFP-like', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'mWasabi', 'family': 'GFP-like', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'mEmerald', 'family': 'GFP-like', 'is_biosensor': 0, 'source': 'literature'},
        
        # CFP/BFP variants
        {'protein_name': 'mTurquoise2', 'family': 'CFP-like', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'ECFP', 'family': 'CFP-like', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'mCerulean3', 'family': 'CFP-like', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'mTFP1', 'family': 'Teal', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'TagBFP2', 'family': 'BFP-like', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'EBFP2', 'family': 'BFP-like', 'is_biosensor': 0, 'source': 'literature'},
        
        # RFP variants
        {'protein_name': 'mCherry', 'family': 'RFP', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'mScarlet', 'family': 'RFP', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'mScarlet-I', 'family': 'RFP', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'mScarlet-H', 'family': 'RFP', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'mApple', 'family': 'RFP', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'mRuby2', 'family': 'RFP', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'mRuby3', 'family': 'RFP', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'mKO2', 'family': 'Orange', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'mOrange2', 'family': 'Orange', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'tdTomato', 'family': 'RFP-dimer', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'DsRed2', 'family': 'RFP-dimer', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'mTagRFP-T', 'family': 'RFP', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'mTagRFP', 'family': 'RFP', 'is_biosensor': 0, 'source': 'literature'},
        
        # Far-red/NIR
        {'protein_name': 'mKate2', 'family': 'Far-red', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'FusionRed', 'family': 'RFP', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'Katushka', 'family': 'Far-red', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'eqFP650', 'family': 'Far-red', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'iRFP670', 'family': 'NIR', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'iRFP713', 'family': 'NIR', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'mCardinal', 'family': 'Far-red', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'mPlum', 'family': 'Far-red', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'mMaroon1', 'family': 'Far-red', 'is_biosensor': 0, 'source': 'literature'},
        
        # Photoactivatable/Photoswitchable
        {'protein_name': 'PA-GFP', 'family': 'Photoactivatable', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'PA-mCherry', 'family': 'Photoactivatable', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'Dronpa', 'family': 'Photoswitchable', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'Dendra2', 'family': 'Photoconvertible', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'mEos2', 'family': 'Photoconvertible', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'mEos3.2', 'family': 'Photoconvertible', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'mEos4b', 'family': 'Photoconvertible', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'Kaede', 'family': 'Photoconvertible', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'KikGR', 'family': 'Photoconvertible', 'is_biosensor': 0, 'source': 'literature'},
        
        # Timer FPs
        {'protein_name': 'mCherry-Timer', 'family': 'Timer', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'Fast-FT', 'family': 'Timer', 'is_biosensor': 0, 'source': 'literature'},
        {'protein_name': 'Slow-FT', 'family': 'Timer', 'is_biosensor': 0, 'source': 'literature'},
    ]
    
    for fp in fps:
        fp['license_source'] = 'literature (FPbase CC BY-SA 4.0 pointer-only)'
        fp['contrast_quality_tier'] = 'C'
    
    df = pd.DataFrame(fps)
    print(f"Added {len(df)} standard FP variants")
    return df

def merge_and_deduplicate(v121_df: pd.DataFrame, specialist_df: pd.DataFrame, extended_df: pd.DataFrame) -> pd.DataFrame:
    """Merge all sources and deduplicate."""
    # Concatenate
    all_df = pd.concat([v121_df, specialist_df, extended_df], ignore_index=True)
    
    # Deduplicate by protein_name (case-insensitive)
    all_df['name_lower'] = all_df['protein_name'].str.lower().str.strip()
    all_df = all_df.drop_duplicates(subset=['name_lower'], keep='first')
    all_df = all_df.drop(columns=['name_lower'])
    
    print(f"After deduplication: {len(all_df)} unique systems")
    
    return all_df

def assign_system_ids(df: pd.DataFrame) -> pd.DataFrame:
    """Assign SystemIDs."""
    df = df.reset_index(drop=True)
    df['SystemID'] = ['FP_' + str(i+1).zfill(4) for i in range(len(df))]
    return df

def compute_sha256(file_path: Path) -> str:
    """Compute SHA256."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest().upper()

def main():
    """Main fallback builder."""
    print("=" * 70)
    print("Atlas v1.3 Fallback Builder (FPbase/PMC unavailable)")
    print("=" * 70)
    
    # Load sources
    v121_df = load_v1_2_1_data()
    specialist_df = load_specialist_data()
    extended_df = create_extended_fp_list()
    
    # Merge
    merged_df = merge_and_deduplicate(v121_df, specialist_df, extended_df)
    
    # Assign IDs
    final_df = assign_system_ids(merged_df)
    
    # Ensure required columns
    required_cols = [
        'SystemID', 'protein_name', 'family', 'is_biosensor',
        'contrast_value', 'contrast_normalized', 'contrast_quality_tier',
        'source', 'source_refs', 'license_source'
    ]
    
    for col in required_cols:
        if col not in final_df.columns:
            final_df[col] = np.nan
    
    # Save CSV
    csv_path = Path("data/processed/atlas_fp_optical_v1_3.csv")
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    final_df.to_csv(csv_path, index=False)
    print(f"\nOK CSV saved: {csv_path}")
    
    # Save Parquet
    parquet_path = Path("data/processed/atlas_fp_optical_v1_3.parquet")
    final_df.to_parquet(parquet_path, index=False)
    print(f"OK Parquet saved: {parquet_path}")
    
    # Build metadata
    N_measured = final_df['contrast_value'].notna().sum()
    N_tier_A = (final_df['contrast_quality_tier'] == 'A').sum()
    N_tier_B = (final_df['contrast_quality_tier'] == 'B').sum()
    N_tier_C = (final_df['contrast_quality_tier'] == 'C').sum()
    
    metadata = {
        'version': '1.3.0-fallback',
        'generated': time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime()),
        'note': 'Built with fallback strategy due to FPbase/PMC API outage',
        'counts': {
            'N_total': int(len(final_df)),
            'N_measured': int(N_measured),
            'N_tier_A': int(N_tier_A),
            'N_tier_B': int(N_tier_B),
            'N_tier_C': int(N_tier_C)
        },
        'sources': {
            'v1.2.1_base': int(len(v121_df)),
            'specialist_dbs': int(len(specialist_df)),
            'extended_fps': int(len(extended_df))
        }
    }
    
    metadata_path = Path("data/processed/TRAINING.METADATA.v1.3.json")
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"OK Metadata saved: {metadata_path}")
    
    # Compute checksums
    checksums = {
        'atlas_fp_optical_v1_3.csv': compute_sha256(csv_path),
        'atlas_fp_optical_v1_3.parquet': compute_sha256(parquet_path),
        'TRAINING.METADATA.v1.3.json': compute_sha256(metadata_path)
    }
    
    checksum_path = Path("data/processed/SHA256SUMS_v1.3.txt")
    with open(checksum_path, 'w', encoding='utf-8') as f:
        for filename, checksum in checksums.items():
            f.write(f"{checksum}  {filename}\n")
    print(f"OK Checksums saved: {checksum_path}")
    
    # Print summary
    print("\n" + "=" * 70)
    print("SUMMARY (Fallback Build)")
    print("=" * 70)
    print(f"N_total:    {metadata['counts']['N_total']}")
    print(f"N_measured: {metadata['counts']['N_measured']}")
    print(f"N_tier_A:   {metadata['counts']['N_tier_A']}")
    print(f"N_tier_B:   {metadata['counts']['N_tier_B']}")
    print(f"N_tier_C:   {metadata['counts']['N_tier_C']}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

