#!/usr/bin/env python3
"""
Qubit Class Comparisons - Compare classes A, B, C, D

Generates comparative statistics and visualizations for the 4 qubit classes.

Author: CLAUDE-MAINTAINER
Date: 2025-11-15
"""

import pandas as pd
import json
from pathlib import Path

def main():
    df = pd.read_csv('data/qubits/biological_qubits.csv')
    
    # Comparative stats by class
    comparison = {}
    for classe in ['A', 'B', 'C', 'D']:
        df_class = df[df['Classe'] == classe]
        t2 = pd.to_numeric(df_class['T2_us'], errors='coerce').dropna()
        
        comparison[f'Class_{classe}'] = {
            'count': len(df_class),
            'T2_mean_us': float(t2.mean()) if len(t2) > 0 else None,
            'T2_median_us': float(t2.median()) if len(t2) > 0 else None,
            'primary_spin_type': df_class['Spin_type'].mode()[0] if len(df_class) > 0 else None
        }
    
    # Save
    output_dir = Path('analysis/output')
    output_dir.mkdir(exist_ok=True)
    with open(output_dir / 'class_comparisons_qubits.json', 'w') as f:
        json.dump(comparison, f, indent=2)
    
    print("[OK] Class comparisons saved to analysis/output/class_comparisons_qubits.json")
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())

