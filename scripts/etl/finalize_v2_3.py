#!/usr/bin/env python3
"""Finalisation corrections v2.3"""
import pandas as pd
import sys
from pathlib import Path

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

df = pd.read_csv('data/qubits/quantum_systems_unified_v2_3.csv')

# Correction silicon (bulk)
mask = df['Hote_contexte'] == 'silicon (bulk)'
if mask.sum() > 0:
    df.loc[mask, 'Hote_contexte'] = 'bulk'
    print(f"Correction: {mask.sum()} système(s) 'silicon (bulk)' -> 'bulk'")

# Vérifier systèmes hyperpolarisés pour in_vivo
hyper_mask = df['Systeme'].str.contains('hyperpolar', case=False, na=False) | df['Notes'].str.contains('hyperpolar', case=False, na=False)
hyper = df[hyper_mask].copy()

print(f"\nSystèmes hyperpolarisés trouvés: {len(hyper)}")
for idx, row in hyper.iterrows():
    notes = str(row.get('Notes', ''))
    if 'in vivo' in notes.lower() or 'fda' in notes.lower() or 'clinical' in notes.lower():
        if row['Hote_contexte'] != 'in_vivo':
            print(f"  Correction: {row['Systeme'][:50]} -> in_vivo (d'après Notes)")
            df.loc[idx, 'Hote_contexte'] = 'in_vivo'

# Sauvegarder
df.to_csv('data/qubits/quantum_systems_unified_v2_3.csv', index=False, encoding='utf-8')
print(f"\nDataset v2.3 finalisé: {len(df)} systèmes")
print(f"Systèmes bulk: {len(df[df['Hote_contexte'] == 'bulk'])}")
print(f"Systèmes unknown: {len(df[~df['Hote_contexte'].str.contains('in_vitro|in_cellulo|in_vivo|ex_vivo|bulk', case=False, na=False)])}")

