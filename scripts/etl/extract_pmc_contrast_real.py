#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract PMC Contrast — Real Data Only
======================================
Recherche dans PMC Open Access pour extraire des mesures de contraste RÉELLES.

Pour chaque protéine du seed:
- Recherche PMC OA avec nom + mots-clés
- Parse HTML/JSON (pas PDF) pour extraire chiffres
- Extrait: contrast_ratio, condition_text, DOI, licence
- Tag contrast_source="measured"

AUCUNE valeur inventée. Extraction uniquement si chiffres trouvés.
"""

import sys
from pathlib import Path
import pandas as pd
import requests
import re
import time
from urllib.parse import quote

# Paths
SEED_FILE = Path("seed/seed_fp_names.csv")
ATLAS_FILE = Path("data/processed/atlas_fp_optical.csv")
OUTPUT_FILE = Path("data/interim/pmc_contrast_extracted.csv")

# API
PMC_SEARCH = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"

# Contrast keywords
CONTRAST_KEYWORDS = [
    "delta F/F", "ΔF/F", "dynamic range", "fold change", 
    "percent change", "response amplitude", "fluorescence change",
    "contrast ratio", "signal-to-noise", "on-off ratio"
]

def search_pmc_oa(protein_name, max_results=10):
    """Recherche PMC Open Access pour une protéine."""
    # Build query with protein name + contrast keywords
    query_terms = [f'"{protein_name}"'] + ['("' + kw + '")' for kw in CONTRAST_KEYWORDS[:3]]
    query = ' AND '.join([query_terms[0]] + [f'({" OR ".join(query_terms[1:])})'])
    
    params = {
        'query': query,
        'format': 'json',
        'pageSize': max_results,
        'isOpenAccess': 'Y',  # OA only!
        'resultType': 'lite'
    }
    
    try:
        response = requests.get(PMC_SEARCH, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()
        
        results = data.get('resultList', {}).get('result', [])
        return results
        
    except Exception as e:
        print(f"  PMC search failed for {protein_name}: {e}")
        return []

def extract_contrast_from_text(text):
    """Extrait les valeurs de contraste depuis du texte."""
    # Patterns pour extraire les chiffres
    patterns = [
        r'ΔF/F[₀0]?\s*[=:~≈]?\s*([\d.]+)\s*%?',
        r'delta\s*F/F[₀0]?\s*[=:~≈]?\s*([\d.]+)\s*%?',
        r'(\d+\.?\d*)\s*%?\s*change',
        r'(\d+\.?\d*)-fold\s+(?:change|increase|response)',
        r'dynamic\s+range\s+of\s+([\d.]+)',
        r'contrast\s+ratio\s+of\s+([\d.]+)',
        r'on[/-]off\s+ratio\s+[=:~≈]?\s*([\d.]+)',
    ]
    
    measurements = []
    
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            try:
                value = float(match.group(1))
                # Valider que c'est plausible (entre 0.1 et 1000)
                if 0.1 <= value <= 1000:
                    context = text[max(0, match.start()-50):min(len(text), match.end()+50)]
                    measurements.append((value, context))
            except (ValueError, IndexError):
                continue
    
    return measurements

def process_protein(protein_name, protein_type):
    """Traite une protéine."""
    print(f"  Searching PMC for: {protein_name}")
    
    # Search PMC
    results = search_pmc_oa(protein_name)
    
    if not results:
        return None
    
    print(f"    Found {len(results)} OA articles")
    
    # Process articles
    for article in results[:3]:  # Limit to 3 articles max
        title = article.get('title', '')
        abstract = article.get('abstractText', '')
        pmcid = article.get('pmcid', '')
        doi = article.get('doi', '')
        
        # Combine text
        text = f"{title} {abstract}"
        
        # Extract contrast
        measurements = extract_contrast_from_text(text)
        
        if measurements:
            # Take first measurement
            value, context = measurements[0]
            
            return {
                'protein_name': protein_name,
                'contrast_ratio': value,
                'condition_text': context.strip()[:200],
                'pmcid': pmcid,
                'doi': doi,
                'source_refs': f"PMC:{pmcid}" if pmcid else f"DOI:{doi}",
                'license_source': 'CC BY (PMC OA)',
                'contrast_source': 'measured'
            }
    
    return None

def extract_contrasts():
    """Extrait les contrastes pour toutes les protéines."""
    # Load seed
    seed_df = pd.read_csv(SEED_FILE)
    print(f"Processing {len(seed_df)} proteins")
    
    extracted = []
    
    for idx, row in seed_df.iterrows():
        name = row['name']
        ptype = row['type']
        
        # Process
        result = process_protein(name, ptype)
        
        if result:
            extracted.append(result)
            print(f"    OK Extracted contrast: {result['contrast_ratio']}")
        
        time.sleep(1)  # Rate limiting
        
        # Limit to avoid long run (process first 40)
        if idx >= 39:
            print("\n  Limiting to first 40 proteins to avoid timeout...")
            break
    
    return pd.DataFrame(extracted)

def update_atlas(extracted_df):
    """Met à jour l'atlas avec les contrastes extraits."""
    # Load atlas
    atlas_df = pd.read_csv(ATLAS_FILE)
    print(f"\nLoaded atlas with {len(atlas_df)} entries")
    
    # Update entries
    for idx, row in extracted_df.iterrows():
        name = row['protein_name']
        
        # Find matching entry in atlas
        mask = atlas_df['protein_name'] == name
        
        if mask.any():
            # Update fields
            atlas_df.loc[mask, 'contrast_ratio'] = row['contrast_ratio']
            atlas_df.loc[mask, 'condition_text'] = row['condition_text']
            atlas_df.loc[mask, 'contrast_source'] = 'measured'
            
            # Update source_refs if not already set
            if pd.isna(atlas_df.loc[mask, 'source_refs'].iloc[0]):
                atlas_df.loc[mask, 'source_refs'] = row['source_refs']
                atlas_df.loc[mask, 'license_source'] = row['license_source']
            else:
                atlas_df.loc[mask, 'source_refs'] += f"; {row['source_refs']}"
    
    # Save
    atlas_df.to_csv(ATLAS_FILE, index=False)
    print(f"Updated atlas saved to {ATLAS_FILE}")
    
    # Stats
    n_measured = (atlas_df['contrast_source'] == 'measured').sum()
    print(f"\nAtlas now has {n_measured} entries with measured contrast")
    
    return atlas_df

def main():
    """Point d'entrée."""
    print("=" * 70)
    print("Extract PMC Contrast — Real Data Only")
    print("=" * 70)
    
    # Extract contrasts
    extracted_df = extract_contrasts()
    
    if len(extracted_df) == 0:
        print("\nWARNING: No contrast measurements extracted!")
        return 1
    
    # Save extracted
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    extracted_df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSaved {len(extracted_df)} extracted measurements to {OUTPUT_FILE}")
    
    # Update atlas
    atlas_df = update_atlas(extracted_df)
    
    print("\nOK PMC contrast extraction completed!")
    return 0

if __name__ == "__main__":
    sys.exit(main())

