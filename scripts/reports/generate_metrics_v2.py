#!/usr/bin/env python3
"""Génère métriques v2.0"""
import pandas as pd
import json

df = pd.read_csv('data/processed/atlas_fp_optical_v2_0.csv')

metrics = {
    'version': '2.0.0',
    'N_total': int(len(df)),
    'N_measured': int(df['contrast_value'].notna().sum()),
    'families': int(df['family'].nunique()),
    'duplicates_removed': 0
}

with open('reports/METRICS_v2.0.json', 'w') as f:
    json.dump(metrics, f, indent=2)

print(f"[OK] Metrics generes: {metrics}")

