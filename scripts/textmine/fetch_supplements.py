#!/usr/bin/env python3
"""
PMC Supplementary Files Fetcher v1.3
=====================================

Download supplementary files (Excel, CSV, ZIP) from PMC Open Access articles.

Author: Biological Qubit Atlas Team
License: MIT
"""

import requests
import json
from typing import Dict, List
from pathlib import Path
import time
import yaml

def load_config() -> Dict:
    """Load provider configuration."""
    with open("config/providers.yml", 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

CONFIG = load_config()
PMC_CONFIG = CONFIG['europe_pmc']
PMC_API_URL = PMC_CONFIG['api_url']

def fetch_supplementary_files(pmcid: str) -> List[Dict]:
    """
    Fetch list of supplementary files for a PMC article.
    
    Args:
        pmcid: PMC ID (e.g., 'PMC1234567')
        
    Returns:
        List of supplementary file metadata
    """
    url = f"{PMC_API_URL}{pmcid}/supplementaryFiles"
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if 'result' in data:
                return data['result']
        return []
    except Exception as e:
        print(f"ERROR fetching supplements for {pmcid}: {e}")
        return []

def download_supplement(pmcid: str, filename: str, url: str) -> Optional[str]:
    """
    Download a supplementary file.
    
    Args:
        pmcid: PMC ID
        filename: Name of the file
        url: Download URL
        
    Returns:
        Path to downloaded file or None
    """
    output_dir = Path(f"data/raw/oa_supp/{pmcid}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = output_dir / filename
    
    try:
        response = requests.get(url, timeout=60)
        if response.status_code == 200:
            output_path.write_bytes(response.content)
            return str(output_path)
        return None
    except Exception as e:
        print(f"ERROR downloading {filename}: {e}")
        return None

def main():
    """Main fetcher."""
    print("=" * 60)
    print("PMC Supplementary Files Fetcher v1.3")
    print("=" * 60)
    
    # Load PMC IDs from previous mining
    pmc_contrasts_path = Path("data/interim/pmc_contrasts.json")
    if pmc_contrasts_path.exists():
        with open(pmc_contrasts_path, 'r', encoding='utf-8') as f:
            pmc_data = json.load(f)
        
        # Extract unique PMC IDs
        pmcids = set()
        for protein, measurements in pmc_data.items():
            for m in measurements:
                pmcids.add(m['pmcid'])
        
        print(f"Found {len(pmcids)} unique PMC IDs")
    else:
        print("No PMC contrasts data found, using seed PMCIDs...")
        # Pre-seeded PMCIDs with known supplements
        pmcids = [
            'PMC3695640',  # GCaMP6 paper (Chen et al. 2013)
            'PMC8016657',  # jGCaMP7 paper
            'PMC5898971',  # dLight1 paper
            'PMC7395770',  # GRAB-DA2 paper
        ]
    
    downloaded = []
    
    for pmcid in pmcids:
        print(f"\nFetching supplements for {pmcid}...")
        
        supplements = fetch_supplementary_files(pmcid)
        print(f"  Found {len(supplements)} supplementary files")
        
        for supp in supplements:
            filename = supp.get('fileName', '')
            url = supp.get('url', '')
            
            # Filter for data files only
            if any(ext in filename.lower() for ext in ['.xlsx', '.xls', '.csv', '.zip']):
                print(f"  Downloading {filename}...")
                path = download_supplement(pmcid, filename, url)
                if path:
                    downloaded.append({
                        'pmcid': pmcid,
                        'filename': filename,
                        'path': path
                    })
                    print(f"    OK Downloaded to {path}")
        
        time.sleep(1)  # Rate limiting
    
    # Save download log
    log_path = Path("data/raw/oa_supp/download_log.json")
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump({
            'downloaded': downloaded,
            'count': len(downloaded),
            'timestamp': time.time()
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\nOK Total files downloaded: {len(downloaded)}")
    print(f"OK Log saved to: {log_path}")

if __name__ == "__main__":
    main()

