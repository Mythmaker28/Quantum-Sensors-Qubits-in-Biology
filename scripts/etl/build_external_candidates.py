#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ETL Script: Build External Candidates
======================================
Fusionne les harvests FPbase + UniProt + PDB, normalise les noms/aliases,
déduplique et crée la liste de candidats externes.

Input: data/raw/external/{fpbase,uniprot,pdb}/*.json
Output: data/interim/external_candidates.parquet
"""

import json
import sys
from pathlib import Path
import pandas as pd
import re
from typing import List, Dict, Any, Optional

# Paths
FPBASE_FILE = Path("data/raw/external/fpbase/fpbase_proteins.json")
UNIPROT_FILE = Path("data/raw/external/uniprot/uniprot_fluorescent_proteins.json")
PDB_FILE = Path("data/raw/external/pdb/pdb_fluorescent_proteins.json")
OUTPUT_FILE = Path("data/interim/external_candidates.parquet")

def normalize_name(name: str) -> str:
    """Normalise un nom de protéine."""
    if not name:
        return ""
    # Lowercase, strip, remove special chars
    normalized = name.lower().strip()
    normalized = re.sub(r'[^\w\s-]', '', normalized)
    normalized = re.sub(r'\s+', '_', normalized)
    return normalized

def load_fpbase() -> pd.DataFrame:
    """Charge et parse les données FPbase."""
    if not FPBASE_FILE.exists():
        print(f"WARNING: {FPBASE_FILE} not found, skipping")
        return pd.DataFrame()
    
    with open(FPBASE_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    records = []
    for item in data:
        # Extraire les champs pertinents
        record = {
            'protein_name': item.get('name', ''),
            'normalized_name': normalize_name(item.get('name', '')),
            'family': item.get('agg', ''),  # aggregation state ou family
            'excitation_nm': item.get('ex_max'),
            'emission_nm': item.get('em_max'),
            'quantum_yield': item.get('qy'),
            'extinction_coef': item.get('ext_coef'),
            'source': 'fpbase',
            'fpbase_slug': item.get('slug', ''),
            'is_biosensor': 1 if 'sensor' in item.get('name', '').lower() else 0,
            'license_source': 'CC BY-SA 4.0 (FPbase pointer-only)'
        }
        records.append(record)
    
    df = pd.DataFrame(records)
    print(f"Loaded {len(df)} candidates from FPbase")
    return df

def load_uniprot() -> pd.DataFrame:
    """Charge et parse UniProt."""
    if not UNIPROT_FILE.exists():
        print(f"WARNING: {UNIPROT_FILE} not found, skipping")
        return pd.DataFrame()
    
    with open(UNIPROT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    records = []
    for entry in data:
        protein_name = entry.get('proteinDescription', {}).get('recommendedName', {}).get('fullName', {}).get('value', '')
        
        # Extraire organism
        organism = ''
        if 'organism' in entry:
            organism = entry['organism'].get('scientificName', '')
        
        record = {
            'protein_name': protein_name,
            'normalized_name': normalize_name(protein_name),
            'uniprot_id': entry.get('primaryAccession', ''),
            'organism': organism,
            'sequence': entry.get('sequence', {}).get('value', ''),
            'source': 'uniprot',
            'license_source': 'CC BY 4.0 (UniProt)'
        }
        records.append(record)
    
    df = pd.DataFrame(records)
    print(f"Loaded {len(df)} candidates from UniProt")
    return df

def load_pdb() -> pd.DataFrame:
    """Charge et parse PDB."""
    if not PDB_FILE.exists():
        print(f"WARNING: {PDB_FILE} not found, skipping")
        return pd.DataFrame()
    
    with open(PDB_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    records = []
    for item in data:
        pdb_id = item.get('pdb_id', '')
        summary = item.get('summary', {})
        
        title = summary.get('title', '')
        
        record = {
            'protein_name': title,
            'normalized_name': normalize_name(title),
            'pdb_id': pdb_id,
            'source': 'pdb',
            'license_source': 'CC0 (PDB)'
        }
        records.append(record)
    
    df = pd.DataFrame(records)
    print(f"Loaded {len(df)} candidates from PDB")
    return df

def merge_sources(fpbase_df: pd.DataFrame, uniprot_df: pd.DataFrame, pdb_df: pd.DataFrame) -> pd.DataFrame:
    """Fusionne les 3 sources et déduplique."""
    
    # Concatenate all
    all_df = pd.concat([fpbase_df, uniprot_df, pdb_df], ignore_index=True)
    
    # Deduplicate based on normalized_name + (excitation_nm, emission_nm) tuple
    # Pour PDB/UniProt sans ex/em, on garde quand même
    
    # Stratégie: groupby normalized_name, garder le record le plus complet
    all_df = all_df.sort_values(by=['normalized_name', 'excitation_nm', 'emission_nm'], 
                                  na_position='last')
    
    # Pour simplifier, on déduplique juste sur normalized_name pour l'instant
    # (une vraie déduplication nécessiterait fuzzy matching)
    dedup_df = all_df.drop_duplicates(subset=['normalized_name'], keep='first')
    
    print(f"After deduplication: {len(dedup_df)} unique candidates (from {len(all_df)} total)")
    
    return dedup_df

def assign_system_id(df: pd.DataFrame) -> pd.DataFrame:
    """Assigne des SystemID uniques."""
    df = df.reset_index(drop=True)
    df['SystemID'] = ['FP_EXT_' + str(i+1).zfill(4) for i in range(len(df))]
    return df

def save_candidates(df: pd.DataFrame):
    """Sauvegarde les candidats."""
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUTPUT_FILE, index=False)
    print(f"\nSaved {len(df)} candidates to {OUTPUT_FILE}")

def main():
    """Point d'entrée."""
    print("=" * 70)
    print("Build External Candidates Pipeline")
    print("=" * 70)
    
    # Load sources
    fpbase_df = load_fpbase()
    uniprot_df = load_uniprot()
    pdb_df = load_pdb()
    
    # Merge
    merged_df = merge_sources(fpbase_df, uniprot_df, pdb_df)
    
    # Assign IDs
    final_df = assign_system_id(merged_df)
    
    # Save
    save_candidates(final_df)
    
    print("\n✓ External candidates built successfully!")
    print(f"  Total candidates: {len(final_df)}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

