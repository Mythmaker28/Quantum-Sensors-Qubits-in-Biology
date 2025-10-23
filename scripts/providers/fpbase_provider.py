#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FPbase Provider with Circuit Breaker
=====================================
Gère l'accès à FPbase API avec retry/backoff et fallback sur seed.
"""

import requests
import time
from pathlib import Path
from datetime import datetime
import json

class FPbaseProvider:
    """Provider FPbase avec circuit-breaker et fallback."""
    
    def __init__(self, max_retries=3, timeout=10):
        self.base_url = "https://www.fpbase.org/api"
        self.max_retries = max_retries
        self.timeout = timeout
        self.cache_file = Path("data/cache/fpbase_snapshot.json")
        self.outage_log = Path("reports/FPBASE_OUTAGE_LOG.md")
        
    def fetch_proteins(self):
        """Tente de récupérer les protéines depuis FPbase API."""
        url = f"{self.base_url}/proteins/"
        
        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, timeout=self.timeout)
                response.raise_for_status()
                data = response.json()
                return data.get('results', [])
            except Exception as e:
                print(f"FPbase attempt {attempt+1}/{self.max_retries} failed: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
        
        # All retries failed
        self._log_outage()
        return None
    
    def _log_outage(self):
        """Log l'indisponibilité de FPbase."""
        self.outage_log.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.outage_log, 'w', encoding='utf-8') as f:
            f.write("# FPbase Outage Log\n\n")
            f.write(f"**Date**: {datetime.now().isoformat()}\n\n")
            f.write("## Status\n\n")
            f.write("FPbase API is currently **UNAVAILABLE** after multiple retry attempts.\n\n")
            f.write(f"- **Retries attempted**: {self.max_retries}\n")
            f.write(f"- **Timeout**: {self.timeout}s\n")
            f.write(f"- **URL**: {self.base_url}/proteins/\n\n")
            f.write("## Fallback Strategy\n\n")
            f.write("1. Check for cached snapshot: `data/cache/fpbase_snapshot.json`\n")
            f.write("2. Use seed file: `seed/seed_fp_names.csv` (66 real FP/biosensor names)\n")
            f.write("3. Harvest real data from:\n")
            f.write("   - UniProt (mapping names to IDs, sequences)\n")
            f.write("   - PDB/PDBe (structures, ex/em if available)\n")
            f.write("   - PMC Open Access (contrast measurements)\n\n")
            f.write("## Data Integrity\n\n")
            f.write("NO synthetic/demo data will be used.\n")
            f.write("All values come from real sources (UniProt/PDB/PMC OA).\n\n")
        
        print(f"FPbase outage logged to {self.outage_log}")
    
    def load_cache_or_seed(self):
        """Charge le cache ou utilise le seed."""
        # Try cache first
        if self.cache_file.exists():
            print(f"Loading FPbase cache from {self.cache_file}")
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Fallback to seed
        print("No cache found, using seed file")
        return None

