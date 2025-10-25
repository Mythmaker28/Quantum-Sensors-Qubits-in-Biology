#!/usr/bin/env python3
"""Tests v2.2 - Validation stricte"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path

TRAINING_FILE = Path("data/processed/TRAINING_TABLE_v2_2.csv")
METADATA_FILE = Path("data/processed/TRAINING.METADATA_v2_2.json")

def test_files_exist():
    assert TRAINING_FILE.exists()
    assert METADATA_FILE.exists()

def test_n_useful_ge_150():
    df = pd.read_csv(TRAINING_FILE)
    assert len(df) >= 150, f"N_useful={len(df)} < 150"

def test_optical_coverage_ge_85():
    df = pd.read_csv(TRAINING_FILE)
    cov = (~df['excitation_missing']).sum() / len(df)
    assert cov >= 0.85, f"Coverage={cov:.1%} < 85%"

def test_duplicates_le_5():
    df = pd.read_csv(TRAINING_FILE)
    dups = df['canonical_name'].duplicated().sum()
    assert dups <= 5, f"Duplicates={dups} > 5"

def test_provenance_complete():
    df = pd.read_csv(TRAINING_FILE)
    missing = df['provenance'].isna().sum()
    rate = missing / len(df)
    assert rate < 0.05, f"Missing provenance={rate:.1%}"

def test_license_complete():
    df = pd.read_csv(TRAINING_FILE)
    missing = df['license'].isna().sum()
    rate = missing / len(df)
    assert rate < 0.05, f"Missing license={rate:.1%}"

def test_schema_contract():
    df = pd.read_csv(TRAINING_FILE)
    required_cols = [
        'canonical_name', 'family', 'excitation_nm', 'emission_nm',
        'stokes_shift_nm', 'method', 'context_type', 'contrast_normalized',
        'source', 'provenance', 'license', 'excitation_missing',
        'emission_missing', 'contrast_missing'
    ]
    for col in required_cols:
        assert col in df.columns, f"Missing column: {col}"

def test_v2_2_summary():
    """Résumé v2.2"""
    df = pd.read_csv(TRAINING_FILE)
    print(f"\nATLAS v2.2 - {len(df)} systemes utiles")
    print(f"Couverture: {(~df['excitation_missing']).sum()/len(df):.1%}")
    assert True

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])

