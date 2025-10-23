#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Europe PMC Provider — Full-Text Access
=======================================
Recherche et télécharge les full-text OA (XML/PDF) depuis Europe PMC.
"""

import requests
import time
from pathlib import Path
from typing import List, Dict, Optional

class EuropePMCProvider:
    """Provider pour Europe PMC avec accès full-text."""
    
    def __init__(self):
        self.search_api = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
        self.fulltext_api = "https://www.ebi.ac.uk/europepmc/webservices/rest"
        
    def search_protein_contrast(self, protein_name: str, max_results=20) -> List[Dict]:
        """Recherche articles OA avec mesures de contraste."""
        # Keywords pour contraste
        contrast_kw = [
            "ΔF/F0", "dF/F0", "dF/F", "delta F/F", 
            "fold change", "percent change", "response amplitude",
            "on/off ratio", "dynamic range"
        ]
        
        # Build query
        contrast_query = " OR ".join([f'"{kw}"' for kw in contrast_kw[:4]])
        query = f'("{protein_name}") AND ({contrast_query})'
        
        params = {
            'query': query,
            'format': 'json',
            'pageSize': max_results,
            'isOpenAccess': 'Y',
            'hasTextMinedTerms': 'Y',  # Prefer text-mined articles
            'resultType': 'core'  # Full metadata
        }
        
        try:
            response = requests.get(self.search_api, params=params, timeout=20)
            response.raise_for_status()
            data = response.json()
            
            results = data.get('resultList', {}).get('result', [])
            
            # Filter for CC-BY licenses
            oa_results = []
            for article in results:
                license_type = article.get('license', '').upper()
                if 'CC' in license_type or 'OPEN' in license_type:
                    oa_results.append(article)
            
            return oa_results
            
        except Exception as e:
            print(f"  Europe PMC search failed: {e}")
            return []
    
    def get_fulltext_xml(self, pmcid: str) -> Optional[str]:
        """Récupère le full-text XML."""
        url = f"{self.fulltext_api}/{pmcid}/fullTextXML"
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except:
            return None
    
    def download_fulltext_pdf(self, pmcid: str, output_path: Path) -> bool:
        """Télécharge le PDF OA."""
        url = f"https://europepmc.org/articles/{pmcid}?pdf=render"
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            return True
        except:
            return False

