#!/usr/bin/env python3
"""
ETL Script: Build Atlas Tables v1.3
====================================

Build final tables:
- atlas_fp_optical_v1_3.csv (all FP/biosensors)
- atlas_fp_optical_v1_3.parquet (optimized format)
- TRAINING.METADATA.json (schema + provenance)

Features:
- Contrast normalization (all → fold-change)
- Quality tiering (A/B/C)
- 22+ guaranteed columns

Author: Biological Qubit Atlas Team
License: MIT
"""

import json
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import yaml
import time
import hashlib

def load_config() -> dict:
    """Load configuration."""
    with open("config/providers.yml", 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

CONFIG = load_config()

def normalize_contrast(row: pd.Series) -> float:
    """
    Normalize contrast to fold-change.
    
    Mappings:
    - fold → fold
    - deltaF_F0 → fold = deltaF_F0 + 1
    - percent → fold = 1 + percent/100
    
    Args:
        row: DataFrame row with contrast_value and contrast_unit
        
    Returns:
        Normalized fold-change value
    """
    value = row.get('contrast_value')
    unit = row.get('contrast_unit')
    
    if pd.isna(value):
        return np.nan
    
    if unit == 'fold':
        return value
    elif unit in ['deltaF_F0', 'deltaR_R0']:
        return value + 1.0
    elif unit == 'percent':
        return 1.0 + (value / 100.0)
    else:
        return value  # Unknown unit, keep as-is

def assign_quality_tier(row: pd.Series) -> str:
    """
    Assign quality tier based on statistical info.
    
    Tiers:
    - A: measured with n or CI
    - B: measured without n/CI
    - C: computed or no measurement
    
    Args:
        row: DataFrame row
        
    Returns:
        Quality tier (A/B/C)
    """
    if pd.isna(row.get('contrast_value')):
        return 'C'  # No measurement
    
    if pd.notna(row.get('n')) or pd.notna(row.get('ci_low')):
        return 'A'  # With confidence info
    elif row.get('evidence_type') in ['supplement_table', 'main_table', 'caption', 'paragraph']:
        return 'B'  # Measured but no stats
    else:
        return 'C'  # Computed or uncertain

def build_fp_optical_table(candidates_df: pd.DataFrame) -> pd.DataFrame:
    """
    Build final FP optical table.
    
    Args:
        candidates_df: Deduplicated candidates
        
    Returns:
        Final FP optical DataFrame
    """
    # Normalize contrasts
    candidates_df['contrast_normalized'] = candidates_df.apply(normalize_contrast, axis=1)
    
    # Assign quality tiers
    candidates_df['contrast_quality_tier'] = candidates_df.apply(assign_quality_tier, axis=1)
    
    # Select and order columns
    columns = [
        'SystemID',
        'protein_name',
        'normalized_name',
        'canonical_name',
        'family',
        'is_biosensor',
        'fpbase_slug',
        'pdb_id',
        'excitation_nm',
        'emission_nm',
        'quantum_yield',
        'extinction_coef',
        'brightness_relative',
        'photostability',
        'lifetime_ns',
        'pka',
        'maturation_time_hours',
        'contrast_value',
        'contrast_unit',
        'contrast_normalized',
        'contrast_quality_tier',
        'n',
        'sd',
        'sem',
        'ci_low',
        'ci_high',
        'condition_text',
        'evidence_type',
        'source',
        'source_refs',
        'license_source'
    ]
    
    # Add missing columns
    for col in columns:
        if col not in candidates_df.columns:
            candidates_df[col] = np.nan
    
    final_df = candidates_df[columns].copy()
    
    return final_df

def build_training_metadata(df: pd.DataFrame) -> dict:
    """
    Build TRAINING.METADATA.json.
    
    Args:
        df: Final FP optical DataFrame
        
    Returns:
        Metadata dictionary
    """
    metadata = {
        'version': '1.3.0',
        'generated': time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime()),
        'schema_version': '1.3',
        
        'counts': {
            'N_total': len(df),
            'N_measured': df['contrast_value'].notna().sum(),
            'N_with_ci': df['ci_low'].notna().sum(),
            'N_tier_A': (df['contrast_quality_tier'] == 'A').sum(),
            'N_tier_B': (df['contrast_quality_tier'] == 'B').sum(),
            'N_tier_C': (df['contrast_quality_tier'] == 'C').sum(),
            'N_is_biosensor': df['is_biosensor'].sum()
        },
        
        'families': df.groupby('family').size().to_dict(),
        
        'sources': df.groupby('source').size().to_dict(),
        
        'licenses': {
            'fpbase': 'CC BY-SA 4.0 (pointer-only)',
            'uniprot': 'CC BY 4.0',
            'pdb': 'CC0',
            'pmc_oa': 'CC BY / CC0 (Open Access)',
            'specialist_dbs': 'varies (see DOI)'
        },
        
        'schema': {
            'SystemID': 'Unique system identifier',
            'protein_name': 'Protein name',
            'normalized_name': 'Normalized name (lowercase, no special chars)',
            'canonical_name': 'Canonical name after fuzzy matching',
            'family': 'Protein family (GFP-like, Calcium, Voltage, etc.)',
            'is_biosensor': 'Binary flag: 1=biosensor, 0=standard FP',
            'fpbase_slug': 'FPbase slug identifier',
            'pdb_id': 'PDB structure ID',
            'excitation_nm': 'Excitation maximum (nm)',
            'emission_nm': 'Emission maximum (nm)',
            'quantum_yield': 'Quantum yield (0.0-1.0)',
            'extinction_coef': 'Molar extinction coefficient (M-1 cm-1)',
            'brightness_relative': 'Brightness relative to EGFP',
            'photostability': 'Photostability (relative)',
            'lifetime_ns': 'Fluorescence lifetime (ns)',
            'pka': 'pKa value',
            'maturation_time_hours': 'Maturation time (hours)',
            'contrast_value': 'Measured contrast value',
            'contrast_unit': 'Original unit (fold/deltaF_F0/percent)',
            'contrast_normalized': 'Normalized to fold-change',
            'contrast_quality_tier': 'A (with CI/n), B (measured), C (computed/none)',
            'n': 'Sample size',
            'sd': 'Standard deviation',
            'sem': 'Standard error of the mean',
            'ci_low': 'Confidence interval lower bound',
            'ci_high': 'Confidence interval upper bound',
            'condition_text': 'Experimental context',
            'evidence_type': 'Evidence source type',
            'source': 'Data source',
            'source_refs': 'DOI/PMCID/URL references',
            'license_source': 'License for this data'
        },
        
        'contrast_normalization': {
            'target_unit': 'fold',
            'mappings': {
                'fold': 'fold',
                'deltaF_F0': 'fold = deltaF_F0 + 1',
                'percent': 'fold = 1 + percent/100'
            }
        },
        
        'quality_tiers': {
            'A': 'Measured with confidence intervals or sample size',
            'B': 'Measured but without statistical info',
            'C': 'Computed or no measurement'
        }
    }
    
    return metadata

def compute_sha256(file_path: Path) -> str:
    """Compute SHA256 checksum."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest().upper()

def main():
    """Main pipeline."""
    print("=" * 70)
    print("Build Atlas Tables v1.3")
    print("=" * 70)
    
    # Load candidates
    candidates_path = Path("data/interim/external_candidates_v1_3.parquet")
    if not candidates_path.exists():
        print(f"ERROR: {candidates_path} not found")
        print("Run scripts/etl/build_external_candidates_v1_3.py first")
        return 1
    
    candidates_df = pd.read_parquet(candidates_path)
    print(f"Loaded {len(candidates_df)} candidates")
    
    # Build table
    final_df = build_fp_optical_table(candidates_df)
    
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
    metadata = build_training_metadata(final_df)
    
    # Save metadata
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
    print("SUMMARY")
    print("=" * 70)
    print(f"N_total:    {metadata['counts']['N_total']}")
    print(f"N_measured: {metadata['counts']['N_measured']}")
    print(f"N_tier_A:   {metadata['counts']['N_tier_A']}")
    print(f"N_tier_B:   {metadata['counts']['N_tier_B']}")
    print(f"N_tier_C:   {metadata['counts']['N_tier_C']}")
    print(f"\nFiles created:")
    print(f"  - {csv_path}")
    print(f"  - {parquet_path}")
    print(f"  - {metadata_path}")
    print(f"  - {checksum_path}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

