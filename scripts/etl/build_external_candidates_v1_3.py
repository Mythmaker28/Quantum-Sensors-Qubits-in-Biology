#!/usr/bin/env python3
"""
ETL Script: Build External Candidates v1.3
===========================================

Merge all sources with advanced deduplication:
- FPbase GraphQL
- Specialist DBs (GECI, voltage, neurotransmitter, metabolic)
- PMC full-text contrasts
- Supplementary spreadsheets
- UniProt
- PDB

Features:
- Fuzzy matching (Levenshtein)
- Alias mapping
- Evidence tier-based conflict resolution
- License tracking per row

Author: Biological Qubit Atlas Team
License: MIT
"""

import json
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import re
from typing import List, Dict, Any, Optional
from Levenshtein import distance as levenshtein_distance
import yaml

def load_config() -> Dict:
    """Load configuration."""
    with open("config/providers.yml", 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

CONFIG = load_config()

def normalize_name(name: str) -> str:
    """Normalize protein name."""
    if not name or pd.isna(name):
        return ""
    normalized = str(name).lower().strip()
    normalized = re.sub(r'[^\w\s-]', '', normalized)
    normalized = re.sub(r'\s+', '_', normalized)
    return normalized

def load_fpbase() -> pd.DataFrame:
    """Load FPbase data."""
    fp_path = Path("data/raw/fpbase/fpbase_full.json")
    
    if not fp_path.exists():
        print("WARNING: FPbase data not found, skipping")
        return pd.DataFrame()
    
    with open(fp_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    proteins = data.get('proteins', [])
    
    records = []
    for p in proteins:
        # Extract DOI from references
        dois = []
        refs = p.get('references', {}).get('edges', [])
        for ref_edge in refs:
            ref = ref_edge.get('node', {})
            doi = ref.get('doi')
            if doi:
                dois.append(doi)
        
        record = {
            'protein_name': p.get('name', ''),
            'normalized_name': normalize_name(p.get('name', '')),
            'fpbase_slug': p.get('slug', ''),
            'family': p.get('switchType', 'FP'),
            'excitation_nm': p.get('exMax'),
            'emission_nm': p.get('emMax'),
            'quantum_yield': p.get('quantumYield'),
            'extinction_coef': p.get('extinctionCoefficient'),
            'brightness_relative': p.get('brightness'),
            'photostability': p.get('photostability'),
            'lifetime_ns': p.get('lifetime'),
            'pka': p.get('pka'),
            'maturation_time_hours': p.get('maturationTime'),
            'pdb_id': p.get('structure', {}).get('pdb'),
            'is_biosensor': 1 if 'sensor' in p.get('name', '').lower() else 0,
            'source': 'fpbase_graphql',
            'source_refs': '; '.join(dois) if dois else None,
            'license_source': 'CC BY-SA 4.0 (FPbase pointer-only)'
        }
        records.append(record)
    
    df = pd.DataFrame(records)
    print(f"Loaded {len(df)} from FPbase GraphQL")
    return df

def load_specialist() -> pd.DataFrame:
    """Load specialist database data."""
    spec_path = Path("data/raw/specialist/specialist_all.json")
    
    if not spec_path.exists():
        print("WARNING: Specialist data not found, skipping")
        return pd.DataFrame()
    
    with open(spec_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    records = []
    for result in data.get('results', []):
        if result['status'] != 'success':
            continue
        
        for biosensor in result.get('biosensors', []):
            record = {
                'protein_name': biosensor.get('name'),
                'normalized_name': normalize_name(biosensor.get('name')),
                'family': biosensor.get('family'),
                'is_biosensor': 1,
                'source': result['source'],
                'source_refs': biosensor.get('doi'),
                'license_source': 'varies (see DOI)'
            }
            records.append(record)
    
    df = pd.DataFrame(records)
    print(f"Loaded {len(df)} from specialist DBs")
    return df

def load_pmc_contrasts() -> pd.DataFrame:
    """Load PMC full-text contrast measurements."""
    pmc_path = Path("data/interim/pmc_contrasts.json")
    
    if not pmc_path.exists():
        print("WARNING: PMC contrasts not found, skipping")
        return pd.DataFrame()
    
    with open(pmc_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    records = []
    for protein_name, measurements in data.items():
        # Group by PMCID and keep best measurement
        best_per_pmcid = {}
        for m in measurements:
            pmcid = m['pmcid']
            section_priority = {'table': 1, 'caption': 2, 'paragraph': 3}
            priority = section_priority.get(m['section_type'], 4)
            
            if pmcid not in best_per_pmcid or priority < best_per_pmcid[pmcid]['priority']:
                best_per_pmcid[pmcid] = {
                    **m,
                    'priority': priority,
                    'protein_name': protein_name
                }
        
        for pmcid, m in best_per_pmcid.items():
            record = {
                'protein_name': m['protein_name'],
                'normalized_name': normalize_name(m['protein_name']),
                'contrast_value': m['value'],
                'contrast_unit': m['metric_type'],
                'n': m.get('n'),
                'sd': m.get('sd'),
                'sem': m.get('sem'),
                'ci_low': m.get('ci_low'),
                'ci_high': m.get('ci_high'),
                'condition_text': m.get('context'),
                'evidence_type': m['section_type'],
                'source': 'pmc_fulltext',
                'source_refs': f"PMCID:{pmcid}",
                'license_source': 'CC BY/CC0 (PMC OA)'
            }
            records.append(record)
    
    df = pd.DataFrame(records)
    print(f"Loaded {len(df)} from PMC full-text")
    return df

def load_supplement_contrasts() -> pd.DataFrame:
    """Load supplementary spreadsheet contrasts."""
    supp_path = Path("data/interim/supplement_contrasts.json")
    
    if not supp_path.exists():
        print("WARNING: Supplement contrasts not found, skipping")
        return pd.DataFrame()
    
    with open(supp_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    measurements = data.get('measurements', [])
    
    records = []
    for m in measurements:
        record = {
            'protein_name': m.get('protein_name'),
            'normalized_name': normalize_name(m.get('protein_name')) if m.get('protein_name') else '',
            'contrast_value': m['value'],
            'contrast_unit': m['metric_type'],
            'n': m.get('n'),
            'sd': m.get('sd'),
            'sem': m.get('sem'),
            'ci_low': m.get('ci_low'),
            'ci_high': m.get('ci_high'),
            'evidence_type': 'supplement_table',
            'source': 'pmc_supplement',
            'source_refs': f"PMCID:{m['pmcid']} {m['source_file']} sheet:{m['sheet']} row:{m['row']}",
            'license_source': 'CC BY/CC0 (PMC OA)'
        }
        records.append(record)
    
    df = pd.DataFrame(records)
    print(f"Loaded {len(df)} from supplementary files")
    return df

def fuzzy_match_names(df: pd.DataFrame, threshold: int = 2) -> pd.DataFrame:
    """
    Fuzzy match protein names within a group.
    
    Args:
        df: DataFrame with normalized_name column
        threshold: Max Levenshtein distance
        
    Returns:
        DataFrame with canonical_name column
    """
    unique_names = df['normalized_name'].unique()
    name_groups = {}
    
    for name in unique_names:
        if not name:
            continue
        
        # Find existing group within threshold
        matched = False
        for canonical, group in name_groups.items():
            if levenshtein_distance(name, canonical) <= threshold:
                group.append(name)
                matched = True
                break
        
        if not matched:
            name_groups[name] = [name]
    
    # Create mapping
    name_to_canonical = {}
    for canonical, group in name_groups.items():
        for name in group:
            name_to_canonical[name] = canonical
    
    df['canonical_name'] = df['normalized_name'].map(name_to_canonical)
    
    print(f"Fuzzy matching: {len(unique_names)} names → {len(name_groups)} canonical groups")
    
    return df

def deduplicate_advanced(df: pd.DataFrame) -> pd.DataFrame:
    """
    Advanced deduplication with evidence tiers.
    
    Priority:
    1. supplement_table
    2. main_table
    3. caption
    4. paragraph
    5. specialist_db
    6. fpbase
    
    Returns:
        Deduplicated DataFrame
    """
    # Evidence tier mapping
    evidence_tiers = CONFIG['evidence_tiers']
    tier_map = {v: int(k) for k, v in evidence_tiers.items()}
    
    def get_tier(source, evidence_type):
        if evidence_type:
            return tier_map.get(evidence_type, 999)
        elif source == 'fpbase_graphql':
            return 6
        elif 'specialist' in source:
            return 7
        else:
            return 999
    
    df['tier'] = df.apply(lambda row: get_tier(row.get('source'), row.get('evidence_type')), axis=1)
    
    # Group by canonical_name and keep best row
    df = df.sort_values(by=['canonical_name', 'tier', 'contrast_value'], na_position='last')
    
    # For rows with same canonical_name, merge data
    grouped = df.groupby('canonical_name', as_index=False).agg({
        'protein_name': 'first',
        'normalized_name': 'first',
        'fpbase_slug': 'first',
        'family': 'first',
        'excitation_nm': 'first',
        'emission_nm': 'first',
        'quantum_yield': 'first',
        'extinction_coef': 'first',
        'brightness_relative': 'first',
        'photostability': 'first',
        'lifetime_ns': 'first',
        'pka': 'first',
        'maturation_time_hours': 'first',
        'pdb_id': 'first',
        'is_biosensor': 'max',
        'contrast_value': 'first',
        'contrast_unit': 'first',
        'n': 'first',
        'sd': 'first',
        'sem': 'first',
        'ci_low': 'first',
        'ci_high': 'first',
        'condition_text': 'first',
        'evidence_type': 'first',
        'source': 'first',
        'source_refs': lambda x: '; '.join([str(v) for v in x if pd.notna(v)]),
        'license_source': 'first',
        'tier': 'min'
    })
    
    print(f"Deduplication: {len(df)} rows → {len(grouped)} unique systems")
    
    return grouped

def assign_system_ids(df: pd.DataFrame) -> pd.DataFrame:
    """Assign unique SystemIDs."""
    df = df.reset_index(drop=True)
    df['SystemID'] = ['FP_' + str(i+1).zfill(4) for i in range(len(df))]
    return df

def main():
    """Main pipeline."""
    print("=" * 70)
    print("Build External Candidates v1.3 - Advanced Deduplication")
    print("=" * 70)
    
    # Load all sources
    fpbase_df = load_fpbase()
    specialist_df = load_specialist()
    pmc_df = load_pmc_contrasts()
    supp_df = load_supplement_contrasts()
    
    # Concatenate
    all_df = pd.concat([fpbase_df, specialist_df, pmc_df, supp_df], ignore_index=True)
    print(f"\nTotal raw records: {len(all_df)}")
    
    # Fuzzy matching
    all_df = fuzzy_match_names(all_df, threshold=CONFIG['validation']['fuzzy_match']['threshold'])
    
    # Deduplicate
    final_df = deduplicate_advanced(all_df)
    
    # Assign IDs
    final_df = assign_system_ids(final_df)
    
    # Save
    output_path = Path("data/interim/external_candidates_v1_3.parquet")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    final_df.to_parquet(output_path, index=False)
    
    print(f"\nOK Candidates built successfully!")
    print(f"   Total unique systems: {len(final_df)}")
    print(f"   With contrast measured: {final_df['contrast_value'].notna().sum()}")
    print(f"   Saved to: {output_path}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

