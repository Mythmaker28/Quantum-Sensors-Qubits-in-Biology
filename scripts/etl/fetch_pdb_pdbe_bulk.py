#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ETL Script: Fetch PDB/PDBe Bulk
================================
Récupère les structures PDB pour les protéines fluorescentes.
Licence: CC0 (domaine public)

Output: data/raw/external/pdb/*.json
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
RCSB_SEARCH_API = "https://search.rcsb.org/rcsbsearch/v2/query"
PDBE_API_BASE = "https://www.ebi.ac.uk/pdbe/api"
OUTPUT_DIR = Path("data/raw/external/pdb")
LOG_FILE = Path("reports/EXTERNAL_HARVEST_LOG.md")

def compute_sha256(data: str) -> str:
    """Calcule SHA256."""
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def search_rcsb_pdb() -> List[str]:
    """Recherche les PDB IDs de protéines fluorescentes via RCSB."""
    query = {
        "query": {
            "type": "group",
            "logical_operator": "or",
            "nodes": [
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "struct.title",
                        "operator": "contains_phrase",
                        "value": "fluorescent protein"
                    }
                },
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "rcsb_entity_source_organism.taxonomy_lineage.name",
                        "operator": "exact_match",
                        "value": "Aequorea victoria"
                    }
                },
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "struct.title",
                        "operator": "contains_words",
                        "value": "GFP mCherry mRFP CFP YFP"
                    }
                }
            ]
        },
        "return_type": "entry",
        "request_options": {
            "return_all_hits": True
        }
    }
    
    print("Searching RCSB PDB for fluorescent proteins...")
    
    try:
        response = requests.post(RCSB_SEARCH_API, json=query, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        pdb_ids = [hit['identifier'] for hit in data.get('result_set', [])]
        print(f"  Found {len(pdb_ids)} PDB entries")
        
        return pdb_ids
        
    except requests.exceptions.RequestException as e:
        print(f"ERROR searching RCSB: {e}", file=sys.stderr)
        return []

def fetch_pdbe_summary(pdb_ids: List[str]) -> List[Dict[str, Any]]:
    """Récupère les summary depuis PDBe pour chaque PDB ID."""
    summaries = []
    
    # PDBe permet des batch requests
    # On fait des chunks de 20
    chunk_size = 20
    
    for i in range(0, len(pdb_ids), chunk_size):
        chunk = pdb_ids[i:i+chunk_size]
        pdb_list = ','.join(chunk)
        
        url = f"{PDBE_API_BASE}/pdb/entry/summary/{pdb_list}"
        
        print(f"Fetching PDBe summaries {i+1}-{min(i+chunk_size, len(pdb_ids))}/{len(pdb_ids)}...")
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # data est un dict {pdb_id: [summary_info]}
            for pdb_id, info_list in data.items():
                if info_list:
                    summaries.append({
                        'pdb_id': pdb_id.upper(),
                        'summary': info_list[0] if info_list else {}
                    })
            
        except requests.exceptions.RequestException as e:
            print(f"WARNING: Could not fetch PDBe summaries for chunk: {e}", file=sys.stderr)
        
        time.sleep(0.5)  # Rate limiting
    
    return summaries

def save_results(summaries: List[Dict[str, Any]]) -> str:
    """Sauvegarde les résultats."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    output_file = OUTPUT_DIR / "pdb_fluorescent_proteins.json"
    json_str = json.dumps(summaries, indent=2, ensure_ascii=False)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(json_str)
    
    sha256 = compute_sha256(json_str)
    
    print(f"\nSaved {len(summaries)} PDB entries to {output_file}")
    print(f"SHA256: {sha256}")
    
    return sha256

def update_log(count: int, sha256: str):
    """Met à jour le log."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"\n## PDB/PDBe Harvest — {datetime.now().isoformat()}\n\n")
        f.write(f"- **Source**: RCSB PDB + PDBe API\n")
        f.write(f"- **Licence**: CC0 (domaine public)\n")
        f.write(f"- **Items récupérés**: {count} structures PDB\n")
        f.write(f"- **SHA256**: `{sha256}`\n")
        f.write(f"- **Fichier**: `data/raw/external/pdb/pdb_fluorescent_proteins.json`\n")
        f.write(f"- **Notes**: Structures cristallographiques avec métadonnées\n")
        f.write("\n")
    
    print(f"Log updated: {LOG_FILE}")

def main():
    """Point d'entrée."""
    print("=" * 70)
    print("PDB/PDBe Harvest Pipeline")
    print("=" * 70)
    
    pdb_ids = search_rcsb_pdb()
    
    if not pdb_ids:
        print("WARNING: No PDB IDs found!", file=sys.stderr)
        summaries = []
    else:
        summaries = fetch_pdbe_summary(pdb_ids)
    
    sha256 = save_results(summaries)
    update_log(len(summaries), sha256)
    
    print("\n✓ PDB/PDBe harvest completed!")
    print(f"  Total structures: {len(summaries)}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

