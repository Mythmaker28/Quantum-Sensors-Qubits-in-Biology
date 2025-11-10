#!/usr/bin/env python3
"""
Validation script for non-optical qubit candidate datasets.

Checks:
- Required columns present
- No duplicate IDs
- DOI format (basic)
- Required fields non-empty
- Plausible value ranges
"""

import pandas as pd
import sys
from pathlib import Path

def validate_csv(file_path, required_fields, numeric_ranges=None):
    """Validate a single CSV file."""
    errors = []
    warnings = []
    
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        return [f"[ERROR] FATAL: Cannot read {file_path}: {e}"], []
    
    # Check for empty dataframe
    if len(df) == 0:
        warnings.append(f"[WARN] {file_path.name}: No data rows (headers only)")
        return errors, warnings
    
    # Check required fields
    for field in required_fields:
        if field not in df.columns:
            errors.append(f"[ERROR] {file_path.name}: Missing required column '{field}'")
        elif df[field].isna().any() or (df[field] == '').any():
            empty_count = df[field].isna().sum() + (df[field] == '').sum()
            errors.append(f"[ERROR] {file_path.name}: Column '{field}' has {empty_count} empty values")
    
    # Check for duplicate IDs
    if 'id' in df.columns:
        duplicates = df['id'].duplicated()
        if duplicates.any():
            dup_ids = df.loc[duplicates, 'id'].tolist()
            errors.append(f"[ERROR] {file_path.name}: Duplicate IDs found: {dup_ids}")
    
    # Validate DOI format (basic)
    if 'doi' in df.columns:
        for idx, doi in df['doi'].items():
            if pd.notna(doi) and not str(doi).startswith('10.'):
                errors.append(f"[ERROR] {file_path.name}: Row {idx+2} has invalid DOI format: {doi}")
    
    # Validate evidence_level
    if 'evidence_level' in df.columns:
        valid_levels = ['A', 'B', 'C']
        for idx, level in df['evidence_level'].items():
            if pd.notna(level) and level not in valid_levels:
                errors.append(f"[ERROR] {file_path.name}: Row {idx+2} has invalid evidence_level: {level}")
    
    # Validate numeric ranges
    if numeric_ranges:
        for col, (min_val, max_val, unit) in numeric_ranges.items():
            if col in df.columns:
                values = pd.to_numeric(df[col], errors='coerce')
                out_of_range = values[(values < min_val) | (values > max_val)]
                if len(out_of_range) > 0:
                    warnings.append(f"[WARN] {file_path.name}: Column '{col}' has {len(out_of_range)} values outside plausible range [{min_val}-{max_val} {unit}]")
    
    return errors, warnings

def main():
    repo_root = Path(__file__).parent.parent.parent
    
    # Define validation rules for each file
    validations = {
        'data/staging/spin_qubit_candidates.csv': {
            'required': ['id', 'label', 'system_type', 'host_material', 'measurement_method', 'doi', 'evidence_level', 'curator'],
            'ranges': {
                'T2_microseconds': (0.01, 1e9, 'µs'),
                'T1_microseconds': (0.01, 1e12, 'µs'),
                'temperature_K': (0.1, 400, 'K'),
                'magnetic_sensitivity_nT_rtHz': (0.001, 1e6, 'nT/√Hz')
            }
        },
        'data/staging/radical_pair_candidates.csv': {
            'required': ['id', 'protein_or_complex', 'observable', 'doi', 'evidence_level', 'curator'],
            'ranges': {
                'timescale_ns': (1, 1e9, 'ns'),
                'field_sensitivity_uT': (0.01, 1e6, 'µT'),
                'mfe_percent': (0, 100, '%'),
                'temperature_K': (4, 400, 'K')
            }
        },
        'data/staging/nuclear_spin_candidates.csv': {
            'required': ['id', 'nucleus', 'host', 'system_type', 'measurement_method', 'doi', 'evidence_level', 'curator'],
            'ranges': {
                'T2_milliseconds': (0.001, 1e9, 'ms'),
                'T1_milliseconds': (0.001, 1e12, 'ms'),
                'temperature_K': (0.1, 400, 'K'),
                'coupling_strength_Hz': (1, 1e9, 'Hz')
            }
        }
    }
    
    all_errors = []
    all_warnings = []
    total_systems = 0
    
    print("=" * 80)
    print("VALIDATING NON-OPTICAL QUBIT CANDIDATE DATASETS")
    print("=" * 80)
    print()
    
    for file_rel, rules in validations.items():
        file_path = repo_root / file_rel
        if not file_path.exists():
            all_errors.append(f"[ERROR] FATAL: File not found: {file_rel}")
            continue
        
        print(f"[CHECK] Validating: {file_rel}")
        errors, warnings = validate_csv(file_path, rules['required'], rules.get('ranges'))
        
        if not errors and not warnings:
            df = pd.read_csv(file_path)
            count = len(df)
            total_systems += count
            print(f"   [PASS] OK ({count} systems)")
        else:
            if errors:
                all_errors.extend(errors)
                for err in errors:
                    print(f"   {err}")
            if warnings:
                all_warnings.extend(warnings)
                for warn in warnings:
                    print(f"   {warn}")
            
            df = pd.read_csv(file_path)
            count = len(df)
            total_systems += count
        
        print()
    
    print("=" * 80)
    print(f"SUMMARY: {total_systems} total non-optical systems")
    print(f"  Errors: {len(all_errors)}")
    print(f"  Warnings: {len(all_warnings)}")
    print("=" * 80)
    
    if all_errors:
        print("\n[ERROR] VALIDATION FAILED")
        return 1
    elif all_warnings:
        print("\n[WARN] VALIDATION PASSED WITH WARNINGS")
        return 0
    else:
        print("\n[PASS] VALIDATION PASSED")
        return 0

if __name__ == '__main__':
    sys.exit(main())

