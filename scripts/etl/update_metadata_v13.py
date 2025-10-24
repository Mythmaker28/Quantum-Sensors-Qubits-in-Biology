#!/usr/bin/env python3
"""
Update TRAINING.METADATA.v1.3.json with correct counts
"""

import json
import pandas as pd
from pathlib import Path
import time
import hashlib

def compute_sha256(file_path):
    """Compute SHA256 checksum."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest().upper()

def main():
    # Load atlas
    atlas_path = Path("data/processed/atlas_fp_optical_v1_3.csv")
    df = pd.read_csv(atlas_path)
    
    # Compute metrics
    N_total = int(len(df))
    N_measured = int(df['contrast_value'].notna().sum())
    N_tier_A = int((df['quality_tier'] == 'A').sum()) if 'quality_tier' in df.columns else 0
    N_tier_B = int((df['quality_tier'] == 'B').sum()) if 'quality_tier' in df.columns else 0
    N_tier_C = int((df['quality_tier'] == 'C').sum()) if 'quality_tier' in df.columns else 0
    
    metadata = {
        'version': '1.3.0-beta',
        'generated': time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime()),
        'schema_version': '1.3',
        'release_type': 'beta',
        'note': 'Hybrid curated strategy (v1.2.1 base + conservative extraction)',
        
        'counts': {
            'N_total': N_total,
            'N_measured': N_measured,
            'N_tier_A': N_tier_A,
            'N_tier_B': N_tier_B,
            'N_tier_C': N_tier_C
        },
        
        'sources': {
            'v1_2_1_curated': 53,
            'v1_3_conservative_extraction': 8,
            'specialist_dbs': 43,
            'pmc_fulltext_interim': 8
        },
        
        'quality': 'All values manually validated or conservatively extracted',
        'license': 'All entries CC-BY or CC0',
        
        'schema': {
            'SystemID': 'Unique identifier',
            'protein_name': 'Protein name',
            'family': 'Protein family',
            'is_biosensor': '1=biosensor, 0=standard FP',
            'contrast_value': 'Measured contrast',
            'contrast_unit': 'fold/deltaF_F0/percent',
            'contrast_normalized': 'Normalized to fold-change',
            'quality_tier': 'A (with CI/n), B (precise), C (computed)',
            'context': 'Experimental context',
            'temperature_K': 'Temperature (Kelvin)',
            'pH': 'pH value',
            'doi': 'DOI reference',
            'pmcid': 'PubMed Central ID',
            'license': 'License (CC-BY/CC0)',
            'source_note': 'Source description'
        }
    }
    
    # Save metadata
    metadata_path = Path("data/processed/TRAINING.METADATA.v1.3.json")
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"Updated metadata: {metadata_path}")
    print(f"  N_total: {N_total}")
    print(f"  N_measured: {N_measured}")
    
    # Update checksums
    checksums = {
        'atlas_fp_optical_v1_3.csv': compute_sha256(Path("data/processed/atlas_fp_optical_v1_3.csv")),
        'atlas_fp_optical_v1_3.parquet': compute_sha256(Path("data/processed/atlas_fp_optical_v1_3.parquet")),
        'TRAINING.METADATA.v1.3.json': compute_sha256(metadata_path)
    }
    
    checksum_path = Path("data/processed/SHA256SUMS_v1.3.txt")
    with open(checksum_path, 'w', encoding='utf-8') as f:
        for filename, checksum in checksums.items():
            f.write(f"{checksum}  {filename}\n")
    
    print(f"Updated checksums: {checksum_path}")
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())

