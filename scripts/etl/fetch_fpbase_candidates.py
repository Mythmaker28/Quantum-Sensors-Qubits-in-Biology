#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ETL Script: Fetch FPbase Candidates
====================================
Récupère les protéines fluorescentes et biosenseurs depuis l'API FPbase.
Licence: FPbase BY-SA (pointer-only, attribution requise)

Output: data/raw/external/fpbase/*.json
Log: reports/EXTERNAL_HARVEST_LOG.md (append)
"""

import json
import hashlib
import os
import sys
from pathlib import Path
from datetime import datetime
import requests
from typing import List, Dict, Any

# Configuration
FPBASE_API_BASE = "https://www.fpbase.org/api"
OUTPUT_DIR = Path("data/raw/external/fpbase")
LOG_FILE = Path("reports/EXTERNAL_HARVEST_LOG.md")

def compute_sha256(data: str) -> str:
    """Calcule le SHA256 d'une chaîne."""
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def fetch_proteins() -> List[Dict[str, Any]]:
    """Récupère la liste des protéines depuis FPbase API."""
    url = f"{FPBASE_API_BASE}/proteins/"
    proteins = []
    
    print(f"Fetching proteins from {url}...")
    
    while url:
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # Extraire les résultats
            results = data.get('results', [])
            proteins.extend(results)
            
            # Pagination
            url = data.get('next')
            print(f"  Retrieved {len(results)} proteins (total: {len(proteins)})")
            
        except requests.exceptions.RequestException as e:
            print(f"ERROR fetching {url}: {e}", file=sys.stderr)
            break
    
    return proteins

def fetch_fluorophore_details(slug: str) -> Dict[str, Any]:
    """Récupère les détails d'un fluorophore spécifique."""
    url = f"{FPBASE_API_BASE}/proteins/{slug}/"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"WARNING: Could not fetch details for {slug}: {e}", file=sys.stderr)
        return {}

def enrich_proteins(proteins: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Enrichit chaque protéine avec ses détails complets."""
    enriched = []
    
    for i, protein in enumerate(proteins, 1):
        slug = protein.get('slug', '')
        if slug:
            print(f"Enriching {i}/{len(proteins)}: {slug}")
            details = fetch_fluorophore_details(slug)
            if details:
                enriched.append(details)
        else:
            enriched.append(protein)
    
    return enriched

def save_results(proteins: List[Dict[str, Any]]) -> str:
    """Sauvegarde les résultats et retourne le SHA256."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Sauvegarder en JSON
    output_file = OUTPUT_DIR / "fpbase_proteins.json"
    json_str = json.dumps(proteins, indent=2, ensure_ascii=False)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(json_str)
    
    # Calculer SHA256
    sha256 = compute_sha256(json_str)
    
    print(f"\nSaved {len(proteins)} proteins to {output_file}")
    print(f"SHA256: {sha256}")
    
    return sha256

def update_log(count: int, sha256: str):
    """Met à jour le log de harvest."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Créer ou append au log
    mode = 'a' if LOG_FILE.exists() else 'w'
    
    with open(LOG_FILE, mode, encoding='utf-8') as f:
        if mode == 'w':
            f.write("# External Harvest Log\n\n")
            f.write("Ce fichier trace toutes les acquisitions de données externes.\n\n")
        
        f.write(f"\n## FPbase Harvest — {datetime.now().isoformat()}\n\n")
        f.write(f"- **Source**: FPbase API (https://www.fpbase.org/api)\n")
        f.write(f"- **Licence**: CC BY-SA 4.0 (pointer-only, attribution requise)\n")
        f.write(f"- **Items récupérés**: {count} protéines/fluorophores\n")
        f.write(f"- **SHA256**: `{sha256}`\n")
        f.write(f"- **Fichier**: `data/raw/external/fpbase/fpbase_proteins.json`\n")
        f.write(f"- **Notes**: Données brutes incluant FP, biosenseurs FRET, photoswitches\n")
        f.write("\n")
    
    print(f"Log updated: {LOG_FILE}")

def main():
    """Point d'entrée principal."""
    print("=" * 70)
    print("FPbase Harvest Pipeline")
    print("=" * 70)
    
    # Fetch proteins
    proteins = fetch_proteins()
    
    if not proteins:
        print("ERROR: No proteins retrieved!", file=sys.stderr)
        sys.exit(1)
    
    # Enrich with details (optional, peut être long)
    # Pour accélérer, on peut skipper l'enrichissement si la liste de base suffit
    # enriched = enrich_proteins(proteins[:10])  # Test sur 10 premiers
    
    # Save
    sha256 = save_results(proteins)
    
    # Update log
    update_log(len(proteins), sha256)
    
    print("\nOK FPbase harvest completed successfully!")
    print(f"  Total proteins: {len(proteins)}")
    print(f"  SHA256: {sha256}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

