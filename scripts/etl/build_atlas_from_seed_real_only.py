#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build Atlas From Seed — Real Data Only
=======================================
Crée les 66 entrées du seed dans atlas_fp_optical.csv.
Les champs sont NULL par défaut, remplis uniquement avec données réelles trouvées.

AUCUNE valeur inventée. Strict sourcing requis.
"""

import sys
import json
from pathlib import Path
import pandas as pd
import numpy as np

# Paths
SEED_FILE = Path("seed/seed_fp_names.csv")
UNIPROT_FILE = Path("data/raw/external/uniprot/uniprot_from_seed.json")
PDB_FILE = Path("data/raw/external/pdb/pdb_from_seed.json")
OUTPUT_FP = Path("data/processed/atlas_fp_optical.csv")
OUTPUT_ALL = Path("data/processed/atlas_all_real.csv")
METADATA_FILE = Path("data/processed/TRAINING.METADATA.json")

def load_seed():
    """Charge le seed."""
    seed_df = pd.read_csv(SEED_FILE)
    print(f"Loaded {len(seed_df)} seed entries")
    return seed_df

def load_external_data():
    """Charge les données externes récoltées."""
    uniprot_data = []
    pdb_data = []
    
    if UNIPROT_FILE.exists():
        with open(UNIPROT_FILE, 'r', encoding='utf-8') as f:
            uniprot_data = json.load(f)
        print(f"Loaded {len(uniprot_data)} UniProt matches")
    
    if PDB_FILE.exists():
        with open(PDB_FILE, 'r', encoding='utf-8') as f:
            pdb_data = json.load(f)
        print(f"Loaded {len(pdb_data)} PDB matches")
    
    return uniprot_data, pdb_data

def create_base_entries(seed_df):
    """Crée les 66 entrées de base avec champs NULL."""
    entries = []
    
    for idx, row in seed_df.iterrows():
        entry = {
            'SystemID': f"FP_SEED_{idx+1:04d}",
            'protein_name': row['name'],
            'variant': None,  # NULL par défaut
            'family': row['family'],
            'is_biosensor': 1 if row['type'] == 'Biosensor' else 0,
            'uniprot_id': None,
            'pdb_id': None,
            'excitation_nm': None,
            'emission_nm': None,
            'temperature_K': None,
            'pH': None,
            'contrast_ratio': None,
            'contrast_ci_low': None,
            'contrast_ci_high': None,
            'contrast_source': 'none',
            'condition_text': None,
            'source_refs': None,
            'license_source': None
        }
        entries.append(entry)
    
    return pd.DataFrame(entries)

def enrich_with_uniprot(df, uniprot_data):
    """Enrichit avec données UniProt réelles."""
    # Map seed_name → uniprot_id
    uniprot_map = {}
    for item in uniprot_data:
        seed_name = item['seed_name']
        uniprot_entry = item['uniprot_data']
        uniprot_id = uniprot_entry.get('primaryAccession')
        if uniprot_id:
            uniprot_map[seed_name] = uniprot_id
    
    # Update DataFrame
    for idx, row in df.iterrows():
        name = row['protein_name']
        if name in uniprot_map:
            df.at[idx, 'uniprot_id'] = uniprot_map[name]
            df.at[idx, 'source_refs'] = f"UniProt:{uniprot_map[name]}"
            df.at[idx, 'license_source'] = "CC BY 4.0 (UniProt)"
    
    enriched_count = df['uniprot_id'].notna().sum()
    print(f"Enriched {enriched_count} entries with UniProt IDs")
    
    return df

def enrich_with_pdb(df, pdb_data):
    """Enrichit avec données PDB réelles."""
    # Map seed_name → pdb_id (prendre le premier)
    pdb_map = {}
    for item in pdb_data:
        seed_name = item['seed_name']
        pdb_id = item['pdb_id']
        if seed_name not in pdb_map:
            pdb_map[seed_name] = pdb_id
    
    # Update DataFrame
    for idx, row in df.iterrows():
        name = row['protein_name']
        if name in pdb_map:
            df.at[idx, 'pdb_id'] = pdb_map[name]
            if pd.isna(df.at[idx, 'source_refs']):
                df.at[idx, 'source_refs'] = f"PDB:{pdb_map[name]}"
                df.at[idx, 'license_source'] = "CC0 (PDB)"
            else:
                df.at[idx, 'source_refs'] += f"; PDB:{pdb_map[name]}"
    
    enriched_count = df['pdb_id'].notna().sum()
    print(f"Enriched {enriched_count} entries with PDB IDs")
    
    return df

def save_atlas(df):
    """Sauvegarde l'atlas."""
    OUTPUT_FP.parent.mkdir(parents=True, exist_ok=True)
    
    # Save FP optical
    df.to_csv(OUTPUT_FP, index=False)
    print(f"\nSaved {len(df)} entries to {OUTPUT_FP}")
    
    # atlas_all_real is same for now (no legacy multi-modality data)
    df.to_csv(OUTPUT_ALL, index=False)
    print(f"Saved {len(df)} entries to {OUTPUT_ALL}")
    
    # Metadata
    metadata = {
        "version": "1.2.0",
        "date": pd.Timestamp.now().isoformat(),
        "description": "FP Optical Atlas — Real Data Only (seed-based, fallback from FPbase outage)",
        "datasets": {
            "atlas_fp_optical": {
                "file": "atlas_fp_optical.csv",
                "rows": len(df),
                "description": "FP and optical biosensors (seed-based with real data enrichment)",
                "columns": list(df.columns)
            }
        },
        "quality_metrics": {
            "total_entries": int(len(df)),
            "with_uniprot_id": int(df['uniprot_id'].notna().sum()),
            "with_pdb_id": int(df['pdb_id'].notna().sum()),
            "with_measured_contrast": int((df['contrast_source'] == 'measured').sum()),
            "with_computed_contrast": int((df['contrast_source'] == 'computed').sum()),
            "with_any_contrast": int((df['contrast_source'] != 'none').sum())
        },
        "data_integrity": {
            "no_synthetic_values": True,
            "null_for_missing_data": True,
            "all_sources_documented": True
        }
    }
    
    with open(METADATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Saved metadata to {METADATA_FILE}")
    
    return metadata

def main():
    """Point d'entrée."""
    print("=" * 70)
    print("Build Atlas From Seed — Real Data Only")
    print("=" * 70)
    
    # Load seed
    seed_df = load_seed()
    
    # Load external data
    uniprot_data, pdb_data = load_external_data()
    
    # Create base entries (all 66, with NULL fields)
    df = create_base_entries(seed_df)
    print(f"\nCreated {len(df)} base entries with NULL fields")
    
    # Enrich with real data
    df = enrich_with_uniprot(df, uniprot_data)
    df = enrich_with_pdb(df, pdb_data)
    
    # Save
    metadata = save_atlas(df)
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"N_fp_like_total = {metadata['quality_metrics']['total_entries']}")
    print(f"N_fp_like_with_contrast_measured = {metadata['quality_metrics']['with_measured_contrast']}")
    print(f"N_fp_like_with_contrast_any = {metadata['quality_metrics']['with_any_contrast']}")
    print(f"\nWith UniProt ID: {metadata['quality_metrics']['with_uniprot_id']}")
    print(f"With PDB ID: {metadata['quality_metrics']['with_pdb_id']}")
    print("=" * 70)
    
    print("\nOK Atlas built successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main())

