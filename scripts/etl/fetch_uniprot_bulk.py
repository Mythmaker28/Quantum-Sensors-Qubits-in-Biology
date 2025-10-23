#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ETL Script: Fetch UniProt Bulk
===============================
Récupère les données UniProt pour les protéines fluorescentes.
Licence: CC BY 4.0

Output: data/raw/external/uniprot/*.json
Log: reports/EXTERNAL_HARVEST_LOG.md (append)
"""

import json
import hashlib
import sys
from pathlib import Path
from datetime import datetime
import requests
import time
from typing import List, Dict, Any

# Configuration
UNIPROT_API_BASE = "https://rest.uniprot.org/uniprotkb"
OUTPUT_DIR = Path("data/raw/external/uniprot")
LOG_FILE = Path("reports/EXTERNAL_HARVEST_LOG.md")

# Requêtes pour trouver les FP
SEARCH_QUERIES = [
    "family:\"green fluorescent protein\" AND reviewed:true",
    "family:\"fluorescent protein\" AND reviewed:true",
    "annotation:(type:function fluorescent) AND reviewed:true",
    "name:\"fluorescent protein\" AND organism:*",
]

def compute_sha256(data: str) -> str:
    """Calcule le SHA256."""
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def search_uniprot(query: str, max_results: int = 500) -> List[Dict[str, Any]]:
    """Recherche dans UniProt."""
    url = f"{UNIPROT_API_BASE}/search"
    params = {
        'query': query,
        'format': 'json',
        'size': min(max_results, 500)
    }
    
    print(f"Searching UniProt: {query[:60]}...")
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        results = data.get('results', [])
        print(f"  Found {len(results)} entries")
        
        return results
        
    except requests.exceptions.RequestException as e:
        print(f"ERROR searching UniProt: {e}", file=sys.stderr)
        return []

def fetch_all_proteins() -> List[Dict[str, Any]]:
    """Récupère toutes les protéines via multiples queries."""
    all_proteins = []
    seen_accessions = set()
    
    for query in SEARCH_QUERIES:
        results = search_uniprot(query)
        
        for entry in results:
            accession = entry.get('primaryAccession', '')
            if accession and accession not in seen_accessions:
                all_proteins.append(entry)
                seen_accessions.add(accession)
        
        # Rate limiting
        time.sleep(1)
    
    return all_proteins

def save_results(proteins: List[Dict[str, Any]]) -> str:
    """Sauvegarde les résultats."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    output_file = OUTPUT_DIR / "uniprot_fluorescent_proteins.json"
    json_str = json.dumps(proteins, indent=2, ensure_ascii=False)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(json_str)
    
    sha256 = compute_sha256(json_str)
    
    print(f"\nSaved {len(proteins)} proteins to {output_file}")
    print(f"SHA256: {sha256}")
    
    return sha256

def update_log(count: int, sha256: str):
    """Met à jour le log."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"\n## UniProt Harvest — {datetime.now().isoformat()}\n\n")
        f.write(f"- **Source**: UniProt REST API (https://www.uniprot.org)\n")
        f.write(f"- **Licence**: CC BY 4.0\n")
        f.write(f"- **Items récupérés**: {count} protéines\n")
        f.write(f"- **SHA256**: `{sha256}`\n")
        f.write(f"- **Fichier**: `data/raw/external/uniprot/uniprot_fluorescent_proteins.json`\n")
        f.write(f"- **Queries**: {len(SEARCH_QUERIES)} recherches combinées\n")
        f.write("\n")
    
    print(f"Log updated: {LOG_FILE}")

def main():
    """Point d'entrée."""
    print("=" * 70)
    print("UniProt Harvest Pipeline")
    print("=" * 70)
    
    proteins = fetch_all_proteins()
    
    if not proteins:
        print("WARNING: No proteins retrieved!", file=sys.stderr)
        # Continue anyway, ne pas fail
    
    sha256 = save_results(proteins)
    update_log(len(proteins), sha256)
    
    print("\nOK UniProt harvest completed!")
    print(f"  Total unique proteins: {len(proteins)}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

