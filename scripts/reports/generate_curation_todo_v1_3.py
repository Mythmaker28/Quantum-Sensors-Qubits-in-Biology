#!/usr/bin/env python3
"""
Generate CURATION_TODO_v1.3.tsv - List of biosensors without measured contrast
===============================================================================

Identifies biosensors in the atlas that lack contrast measurements and 
provides context to guide manual curation.

Author: Biological Qubit Atlas Team
License: MIT
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

def load_atlas() -> pd.DataFrame:
    """Load atlas dataset."""
    atlas_path = Path("data/processed/atlas_fp_optical_v1_3.csv")
    
    if not atlas_path.exists():
        print(f"ERROR: {atlas_path} not found")
        sys.exit(1)
    
    return pd.read_csv(atlas_path)

def extract_curation_todos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract biosensors/FPs without measured contrast.
    
    Returns:
        DataFrame with curation TODO list
    """
    # Filter: no contrast value OR quality tier C (computed/unreliable)
    needs_curation = df[
        (df['contrast_value'].isna()) | 
        (df.get('contrast_quality_tier', '') == 'C')
    ].copy()
    
    # Prioritize biosensors
    needs_curation['priority'] = needs_curation['is_biosensor'].apply(lambda x: 'HIGH' if x == 1 else 'MEDIUM')
    
    # Extract context
    def guess_context(row):
        """Guess experimental context from available fields."""
        contexts = []
        if pd.notna(row.get('condition_text')):
            return str(row['condition_text'])
        
        # Infer from family
        family = row.get('family', '')
        if family in ['Calcium', 'Dopamine', 'Glutamate', 'Acetylcholine', 'Serotonin', 'Norepinephrine']:
            contexts.append('neurons')
        elif family in ['cAMP', 'ATP/ADP', 'ATP', 'H2O2', 'Redox']:
            contexts.append('cells')
        elif family == 'Voltage':
            contexts.append('neurons/voltage_clamp')
        elif family == 'pH':
            contexts.append('cells/organelles')
        
        return ' '.join(contexts) if contexts else 'unknown'
    
    def guess_host(row):
        """Guess typical host organism."""
        family = row.get('family', '')
        if family in ['Calcium', 'Dopamine', 'Glutamate', 'Voltage']:
            return 'neurons(mouse/rat)'
        elif family in ['cAMP', 'ATP', 'H2O2', 'Redox', 'pH']:
            return 'HEK293/HeLa'
        else:
            return 'unknown'
    
    def extract_first_doi(refs):
        """Extract first DOI from source_refs."""
        if pd.isna(refs):
            return ''
        
        refs_str = str(refs)
        # Look for DOI patterns
        import re
        doi_match = re.search(r'10\.\d{4,}/[^\s;]+', refs_str)
        if doi_match:
            return doi_match.group(0)
        
        return ''
    
    def extract_candidate_dois(refs):
        """Extract all DOIs from source_refs."""
        if pd.isna(refs):
            return ''
        
        refs_str = str(refs)
        import re
        dois = re.findall(r'10\.\d{4,}/[^\s;]+', refs_str)
        return '; '.join(dois[:3]) if dois else ''  # Limit to top 3
    
    # Build TODO table
    todo_df = pd.DataFrame({
        'protein_name': needs_curation['protein_name'],
        'family': needs_curation['family'],
        'is_biosensor': needs_curation['is_biosensor'],
        'context_guess': needs_curation.apply(guess_context, axis=1),
        'host_guess': needs_curation.apply(guess_host, axis=1),
        'first_doi': needs_curation.get('source_refs', '').apply(extract_first_doi),
        'candidate_dois': needs_curation.get('source_refs', '').apply(extract_candidate_dois),
        'priority': needs_curation['priority'],
        'note': 'needs_measured_contrast'
    })
    
    # Sort by priority, then family
    todo_df = todo_df.sort_values(by=['priority', 'family', 'protein_name'])
    
    return todo_df

def main():
    """Main function."""
    print("=" * 70)
    print("Generate CURATION_TODO v1.3")
    print("=" * 70)
    
    # Load atlas
    df = load_atlas()
    print(f"Loaded {len(df)} systems from atlas")
    
    # Extract TODOs
    todo_df = extract_curation_todos(df)
    
    print(f"Found {len(todo_df)} systems needing curation")
    print(f"  - HIGH priority (biosensors): {(todo_df['priority'] == 'HIGH').sum()}")
    print(f"  - MEDIUM priority (FPs): {(todo_df['priority'] == 'MEDIUM').sum()}")
    
    # Save TSV
    output_path = Path("reports/CURATION_TODO_v1.3.tsv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    todo_df.to_csv(output_path, sep='\t', index=False)
    
    print(f"\nOK Curation TODO saved to: {output_path}")
    
    # Print top 10 priorities
    print("\n" + "=" * 70)
    print("TOP 10 CURATION PRIORITIES (HIGH)")
    print("=" * 70)
    
    top_10 = todo_df[todo_df['priority'] == 'HIGH'].head(10)
    for i, row in top_10.iterrows():
        print(f"\n{row['protein_name']} ({row['family']})")
        print(f"  Context: {row['context_guess']}")
        print(f"  Host: {row['host_guess']}")
        if row['first_doi']:
            print(f"  DOI: {row['first_doi']}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

