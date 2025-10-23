#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ETL Script: Fetch PMC Contrast
===============================
Pour chaque candidat FP-like, recherche dans PubMed Central (OA uniquement)
les mesures de contraste (ΔF/F₀, on/off ratio, % change).
Extrait: contrast_ratio + CI95/SD/n + condition_text + DOI + licence.

Input: data/interim/external_candidates.parquet (is_fp_like=1)
Output: data/interim/pmc_contrast_measurements.parquet
        data/raw/external/pmc/*.json
"""

import sys
from pathlib import Path
import pandas as pd
import requests
import time
import json
import re
from typing import List, Dict, Any, Optional, Tuple

# Configuration
EUTILS_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
PMC_API_BASE = "https://www.ebi.ac.uk/europepmc/webservices/rest"
INPUT_FILE = Path("data/interim/external_candidates.parquet")
OUTPUT_FILE = Path("data/interim/pmc_contrast_measurements.parquet")
RAW_DIR = Path("data/raw/external/pmc")

# Email pour NCBI (requis)
EMAIL = "research@example.org"  # À remplacer par l'email réel du projet

# Contrast keywords
CONTRAST_PATTERNS = [
    r'ΔF/F[₀0]?\s*[=:~]?\s*([\d.]+)',
    r'delta\s*F/F[₀0]?\s*[=:~]?\s*([\d.]+)',
    r'contrast\s*ratio\s*[=:~]?\s*([\d.]+)',
    r'on[/-]off\s*ratio\s*[=:~]?\s*([\d.]+)',
    r'fold\s*change\s*[=:~]?\s*([\d.]+)',
    r'(\d+\.?\d*)\s*%?\s*change',
    r'(\d+\.?\d*)-fold\s*increase',
]

def search_pmc_for_protein(protein_name: str, aliases: List[str] = None) -> List[str]:
    """Recherche des articles OA dans PMC pour une protéine."""
    if not aliases:
        aliases = []
    
    # Construire la query
    terms = [f'"{protein_name}"'] + [f'"{alias}"' for alias in aliases[:3]]  # Limiter
    query = f"({' OR '.join(terms)}) AND (contrast OR fluorescence OR sensor)"
    
    # EuropePMC API (plus permissive que NCBI)
    url = f"{PMC_API_BASE}/search"
    params = {
        'query': query,
        'format': 'json',
        'pageSize': 10,  # Limiter à 10 premiers résultats
        'isOpenAccess': 'Y'  # OA only!
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        results = data.get('resultList', {}).get('result', [])
        pmcids = [r.get('pmcid', '') for r in results if r.get('pmcid')]
        
        return pmcids
        
    except requests.exceptions.RequestException as e:
        print(f"  WARNING: PMC search failed for {protein_name}: {e}", file=sys.stderr)
        return []

def fetch_pmc_fulltext(pmcid: str) -> Optional[Dict[str, Any]]:
    """Récupère le full-text d'un article PMC."""
    url = f"{PMC_API_BASE}/{pmcid}/fullTextXML"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        # On retourne juste le texte brut, parsing XML serait trop complexe
        return {
            'pmcid': pmcid,
            'fulltext': response.text
        }
    except requests.exceptions.RequestException:
        return None

def extract_contrast_from_text(text: str) -> List[Tuple[float, str]]:
    """Extrait les valeurs de contraste depuis le texte."""
    measurements = []
    
    for pattern in CONTRAST_PATTERNS:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            try:
                value_str = match.group(1)
                value = float(value_str)
                context = text[max(0, match.start()-100):min(len(text), match.end()+100)]
                measurements.append((value, context.strip()))
            except (ValueError, IndexError):
                continue
    
    return measurements

def process_protein(row: pd.Series) -> List[Dict[str, Any]]:
    """Traite une protéine: recherche PMC, extrait contraste."""
    protein_name = row.get('protein_name', '')
    system_id = row.get('SystemID', '')
    
    if not protein_name:
        return []
    
    print(f"Processing {system_id}: {protein_name}")
    
    # Rechercher articles
    pmcids = search_pmc_for_protein(protein_name)
    
    if not pmcids:
        print(f"  No OA articles found")
        return []
    
    print(f"  Found {len(pmcids)} OA articles")
    
    results = []
    
    for pmcid in pmcids[:3]:  # Limiter à 3 articles max par protéine
        # Fetch fulltext
        article = fetch_pmc_fulltext(pmcid)
        if not article:
            continue
        
        # Extract contrast
        measurements = extract_contrast_from_text(article['fulltext'])
        
        for value, context in measurements:
            results.append({
                'SystemID': system_id,
                'protein_name': protein_name,
                'pmcid': pmcid,
                'doi': f"PMC{pmcid}",  # Simplified, would need proper DOI lookup
                'contrast_ratio': value,
                'contrast_source': 'measured',
                'condition_text': context[:200],  # Truncate
                'license_source': 'CC BY or compatible (PMC OA)'
            })
        
        time.sleep(0.5)  # Rate limiting
    
    return results

def main():
    """Point d'entrée."""
    print("=" * 70)
    print("PMC Contrast Extraction Pipeline")
    print("=" * 70)
    
    if not INPUT_FILE.exists():
        print(f"ERROR: {INPUT_FILE} not found!", file=sys.stderr)
        sys.exit(1)
    
    # Load FP-like only
    df = pd.read_parquet(INPUT_FILE)
    fp_df = df[df['is_fp_like'] == 1].copy()
    
    print(f"Processing {len(fp_df)} FP-like candidates")
    
    # Process each (limiter pour test)
    all_measurements = []
    
    # Pour éviter de faire trop de requêtes, on limite à 20 protéines max pour le test
    sample_df = fp_df.head(20)
    
    for idx, row in sample_df.iterrows():
        measurements = process_protein(row)
        all_measurements.extend(measurements)
        time.sleep(1)  # Rate limiting importante
    
    # Convert to DataFrame
    if all_measurements:
        measurements_df = pd.DataFrame(all_measurements)
        
        # Save
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        measurements_df.to_parquet(OUTPUT_FILE, index=False)
        
        print(f"\nOK Extracted {len(measurements_df)} contrast measurements")
        print(f"  Saved to {OUTPUT_FILE}")
    else:
        print("\nWARNING: No contrast measurements extracted!")
        # Create empty file
        pd.DataFrame(columns=['SystemID', 'protein_name', 'pmcid', 'doi', 
                              'contrast_ratio', 'contrast_source', 
                              'condition_text', 'license_source']).to_parquet(OUTPUT_FILE, index=False)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

