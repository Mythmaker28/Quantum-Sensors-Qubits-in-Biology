#!/usr/bin/env python3
"""
Supplementary Spreadsheet Parser v1.3
======================================

Parse contrast data from Excel/CSV supplementary files.

Auto-detects columns with synonyms:
- ΔF/F₀, dF/F0, delta_f_over_f0, fold_change, percent_change, etc.

Author: Biological Qubit Atlas Team
License: MIT
"""

import json
from typing import Dict, List, Optional
from pathlib import Path
import pandas as pd
import re

# Column synonyms for contrast metrics
CONTRAST_COLUMN_SYNONYMS = {
    'deltaF_F0': [
        'ΔF/F₀', 'ΔF/F0', 'dF/F0', 'dF/F', 'delta_f_over_f0', 
        'df_f0', 'df_f', 'fluorescence_change', 'ΔF'
    ],
    'fold': [
        'fold_change', 'fold', 'dynamic_range', 'on_off_ratio', 
        'ratio', 'response', 'fmax/fmin'
    ],
    'percent': [
        'percent_change', '%_change', 'percent', 'pct_change'
    ]
}

# Column synonyms for protein names
NAME_COLUMN_SYNONYMS = [
    'protein', 'name', 'sensor', 'indicator', 'variant', 'construct'
]

# Column synonyms for statistical info
STATS_COLUMN_SYNONYMS = {
    'n': ['n', 'sample_size', 'trials', 'replicates'],
    'sd': ['sd', 'std', 'stdev', 'standard_deviation'],
    'sem': ['sem', 'se', 'standard_error'],
    'ci_low': ['ci_low', 'ci_lower', 'lower_ci', '95_ci_low'],
    'ci_high': ['ci_high', 'ci_upper', 'upper_ci', '95_ci_high']
}

def detect_column(df: pd.DataFrame, synonyms: List[str]) -> Optional[str]:
    """
    Detect a column by synonyms (case-insensitive).
    
    Args:
        df: DataFrame
        synonyms: List of possible column names
        
    Returns:
        Actual column name or None
    """
    columns_lower = {col.lower(): col for col in df.columns}
    
    for syn in synonyms:
        syn_lower = syn.lower()
        if syn_lower in columns_lower:
            return columns_lower[syn_lower]
    
    return None

def parse_spreadsheet(file_path: Path, pmcid: str) -> List[Dict]:
    """
    Parse contrast data from a spreadsheet.
    
    Args:
        file_path: Path to Excel or CSV file
        pmcid: PMC ID for provenance
        
    Returns:
        List of extracted contrast measurements
    """
    measurements = []
    
    try:
        # Load spreadsheet
        if file_path.suffix.lower() in ['.xlsx', '.xls']:
            # Try all sheets
            xls = pd.ExcelFile(file_path)
            sheets = {sheet: pd.read_excel(xls, sheet) for sheet in xls.sheet_names}
        else:
            sheets = {'data': pd.read_csv(file_path)}
        
        # Process each sheet
        for sheet_name, df in sheets.items():
            # Skip if too small
            if df.shape[0] < 2 or df.shape[1] < 2:
                continue
            
            # Detect protein name column
            name_col = detect_column(df, NAME_COLUMN_SYNONYMS)
            
            # Detect contrast column
            contrast_col = None
            metric_type = None
            for metric, synonyms in CONTRAST_COLUMN_SYNONYMS.items():
                col = detect_column(df, synonyms)
                if col:
                    contrast_col = col
                    metric_type = metric
                    break
            
            if not contrast_col:
                continue  # No contrast data in this sheet
            
            # Detect stats columns
            stats_cols = {}
            for stat_name, synonyms in STATS_COLUMN_SYNONYMS.items():
                col = detect_column(df, synonyms)
                if col:
                    stats_cols[stat_name] = col
            
            # Extract rows
            for idx, row in df.iterrows():
                try:
                    value = float(row[contrast_col])
                    
                    # Get name if available
                    name = row[name_col] if name_col else None
                    
                    # Get stats if available
                    stats = {}
                    for stat_name, stat_col in stats_cols.items():
                        try:
                            stats[stat_name] = float(row[stat_col])
                        except:
                            pass
                    
                    measurements.append({
                        'value': value,
                        'metric_type': metric_type,
                        'protein_name': name,
                        'pmcid': pmcid,
                        'source_file': file_path.name,
                        'sheet': sheet_name,
                        'row': idx + 2,  # Excel row number
                        'n': stats.get('n'),
                        'sd': stats.get('sd'),
                        'sem': stats.get('sem'),
                        'ci_low': stats.get('ci_low'),
                        'ci_high': stats.get('ci_high'),
                        'evidence_type': 'supplement_table'
                    })
                except (ValueError, TypeError):
                    continue
    
    except Exception as e:
        print(f"ERROR parsing {file_path}: {e}")
    
    return measurements

def main():
    """Main parser."""
    print("=" * 60)
    print("Supplementary Spreadsheet Parser v1.3")
    print("=" * 60)
    
    # Load download log
    log_path = Path("data/raw/oa_supp/download_log.json")
    if not log_path.exists():
        print("ERROR: No download log found")
        print("Run scripts/textmine/fetch_supplements.py first")
        return
    
    with open(log_path, 'r', encoding='utf-8') as f:
        log_data = json.load(f)
    
    downloaded = log_data.get('downloaded', [])
    print(f"Processing {len(downloaded)} supplementary files...")
    
    all_measurements = []
    
    for item in downloaded:
        file_path = Path(item['path'])
        pmcid = item['pmcid']
        
        if not file_path.exists():
            continue
        
        print(f"\nParsing {file_path.name}...")
        measurements = parse_spreadsheet(file_path, pmcid)
        
        if measurements:
            all_measurements.extend(measurements)
            print(f"  Found {len(measurements)} measurements")
    
    # Save results
    output_path = Path("data/interim/supplement_contrasts.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            'measurements': all_measurements,
            'count': len(all_measurements),
            'timestamp': time.time()
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\nOK Total measurements extracted: {len(all_measurements)}")
    print(f"OK Saved to: {output_path}")

if __name__ == "__main__":
    import time
    main()

