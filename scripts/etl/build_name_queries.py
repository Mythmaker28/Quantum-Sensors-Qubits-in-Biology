#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build Name Queries — Auto-Research
===================================
Génère des variantes de noms pour améliorer le matching UniProt/PDB/PMC.

Pour chaque nom seed:
- Variantes casse/accents/hyphens/underscores
- Variantes avec contexte (+ "fluorescent", "sensor", etc.)
- Suffixes/préfixes (j, m, E, s, f, etc.)
"""

import sys
import csv
import re
from pathlib import Path
import pandas as pd

SEED_FILE = Path("seed/seed_fp_names.csv")
OUTPUT_FILE = Path("data/interim/name_queries.parquet")
CHANGES_LOG = Path("reports/ALIAS_CHANGES.md")

def generate_name_variants(name):
    """Génère des variantes d'un nom."""
    variants = set([name])  # Original
    
    # 1. Casse
    variants.add(name.lower())
    variants.add(name.upper())
    variants.add(name.capitalize())
    
    # 2. Hyphens/underscores/spaces
    variants.add(name.replace('-', ''))
    variants.add(name.replace('-', ' '))
    variants.add(name.replace('-', '_'))
    variants.add(name.replace(' ', ''))
    variants.add(name.replace(' ', '-'))
    variants.add(name.replace(' ', '_'))
    
    # 3. Préfixes communs (m, E, sf, j, Tag)
    if name.startswith('m') and len(name) > 1:
        # mCherry → m-Cherry, m Cherry
        variants.add('m-' + name[1:])
        variants.add('m ' + name[1:])
    
    if name.startswith('E') and len(name) > 1:
        # EGFP → E-GFP, E GFP
        variants.add('E-' + name[1:])
        variants.add('E ' + name[1:])
    
    if name.startswith('sf') and len(name) > 2:
        # sfGFP → sf-GFP, sf GFP
        variants.add('sf-' + name[2:])
        variants.add('sf ' + name[2:])
    
    if name.startswith('j') and len(name) > 1:
        # jGCaMP7s → j-GCaMP7s, j GCaMP7s
        variants.add('j-' + name[1:])
        variants.add('j ' + name[1:])
    
    if name.startswith('Tag') and len(name) > 3:
        # TagRFP → Tag-RFP, Tag RFP
        variants.add('Tag-' + name[3:])
        variants.add('Tag ' + name[3:])
    
    # 4. Suffixes numériques avec espaces
    # GCaMP6s → GCaMP 6s, G-CaMP6s, G CaMP 6 s
    match = re.match(r'([a-zA-Z]+)(\d+)([a-zA-Z]*)', name)
    if match:
        prefix, num, suffix = match.groups()
        variants.add(f"{prefix} {num}{suffix}")
        variants.add(f"{prefix}{num} {suffix}")
        variants.add(f"{prefix} {num} {suffix}")
    
    return list(variants)

def generate_context_variants(name, protein_type, family):
    """Génère des variantes avec contexte."""
    context_variants = []
    
    # Contexte pour FPs
    if protein_type == "FP":
        context_variants.append(f"{name} fluorescent protein")
        context_variants.append(f"{name} FP")
        context_variants.append(f"{name} GFP")  # Many are GFP variants
        
    # Contexte pour biosensors
    elif protein_type == "Biosensor":
        context_variants.append(f"{name} biosensor")
        context_variants.append(f"{name} sensor")
        context_variants.append(f"{name} fluorescent sensor")
        context_variants.append(f"{name} indicator")
        context_variants.append(f"{name} FRET sensor")
    
    return context_variants

def build_queries():
    """Construit toutes les variantes de queries."""
    if not SEED_FILE.exists():
        print(f"ERROR: Seed file not found: {SEED_FILE}")
        sys.exit(1)
    
    # Load seed
    seed_df = pd.read_csv(SEED_FILE)
    print(f"Loaded {len(seed_df)} seed names")
    
    all_queries = []
    
    for idx, row in seed_df.iterrows():
        name = row['name']
        ptype = row['type']
        family = row['family']
        
        # Generate variants
        name_variants = generate_name_variants(name)
        context_variants = generate_context_variants(name, ptype, family)
        
        all_variants = name_variants + context_variants
        
        for variant in all_variants:
            all_queries.append({
                'original_name': name,
                'query_variant': variant,
                'type': ptype,
                'family': family,
                'variant_type': 'context' if variant in context_variants else 'name'
            })
        
        print(f"  {name}: {len(all_variants)} variants")
    
    # Convert to DataFrame
    queries_df = pd.DataFrame(all_queries)
    
    # Save
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    queries_df.to_parquet(OUTPUT_FILE, index=False)
    
    print(f"\nSaved {len(queries_df)} query variants to {OUTPUT_FILE}")
    print(f"  Unique original names: {queries_df['original_name'].nunique()}")
    print(f"  Total query strings: {len(queries_df)}")
    
    return queries_df

def log_changes():
    """Log les changements d'alias."""
    CHANGES_LOG.parent.mkdir(parents=True, exist_ok=True)
    
    with open(CHANGES_LOG, 'w', encoding='utf-8') as f:
        f.write("# Alias Changes Log\n\n")
        f.write(f"**Date**: {pd.Timestamp.now().isoformat()}\n\n")
        f.write("## Auto-generated Name Variants\n\n")
        f.write("Name variants generated automatically by `build_name_queries.py`:\n\n")
        f.write("- Case variations (lower, upper, capitalize)\n")
        f.write("- Hyphen/underscore/space substitutions\n")
        f.write("- Prefix variations (m, E, sf, j, Tag)\n")
        f.write("- Suffix numeric spacing\n")
        f.write("- Context additions (fluorescent, sensor, biosensor, etc.)\n\n")
        f.write("**Purpose**: Improve matching with UniProt, PDB, and PMC databases.\n\n")
        f.write("**No manual edits**: All variants are algorithmically generated.\n\n")
    
    print(f"Alias changes logged to {CHANGES_LOG}")

def main():
    """Point d'entrée."""
    print("=" * 70)
    print("Build Name Queries — Auto-Research")
    print("=" * 70)
    
    queries_df = build_queries()
    log_changes()
    
    print("\nOK Name queries built successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main())

