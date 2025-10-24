#!/usr/bin/env python3
"""
Pipeline automatisé d'extraction PubMed/FPbase pour expansion vers 200+ systèmes
Licence: MIT
Auteur: Biological Qubits Atlas v2.0
"""

import requests
import pandas as pd
import time
from typing import List, Dict, Optional
from dataclasses import dataclass
import re
import os

@dataclass
class BiologicalQubit:
    """Système quantique extrait"""
    name: str
    family: str
    t2_us: Optional[float]
    contrast_pct: Optional[float]
    temperature_k: float
    doi: str
    pmcid: Optional[str]
    source_confidence: float  # 0-1

class AutoHarvester:
    """Pipeline automatisé d'extraction multi-sources"""
    
    def __init__(self, api_keys: Dict[str, str]):
        self.ncbi_api_key = api_keys.get('ncbi')
        self.fpbase_api_key = api_keys.get('fpbase')
        self.email = api_keys.get('email', 'your@email.com')
        
    def search_pubmed(self, query: str, max_results: int = 500) -> List[str]:
        """
        Recherche PubMed avec mots-clés ciblés
        
        Args:
            query: Requête PubMed (ex: "nitrogen vacancy diamond" AND "biological")
            max_results: Nombre max de résultats
            
        Returns:
            Liste de PMIDs
        """
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        params = {
            'db': 'pubmed',
            'term': query,
            'retmax': max_results,
            'retmode': 'json',
            'api_key': self.ncbi_api_key,
            'email': self.email
        }
        
        try:
            response = requests.get(base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            pmids = data.get('esearchresult', {}).get('idlist', [])
            print(f"✅ Trouvé {len(pmids)} publications pour '{query}'")
            return pmids
        except Exception as e:
            print(f"⚠️ Erreur PubMed: {e}")
            return []
    
    def fetch_pmc_fulltext(self, pmcid: str) -> str:
        """
        Récupère texte intégral depuis PMC (Open Access uniquement)
        
        Args:
            pmcid: ID PMC (ex: 'PMC123456')
            
        Returns:
            XML du texte intégral
        """
        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        params = {
            'db': 'pmc',
            'id': pmcid.replace('PMC', ''),
            'retmode': 'xml',
            'api_key': self.ncbi_api_key
        }
        
        time.sleep(0.34)  # Rate limit NCBI (3 req/s avec API key)
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"⚠️ Erreur PMC {pmcid}: {e}")
            return ""
    
    def extract_quantum_metrics(self, xml_text: str) -> Optional[Dict]:
        """
        Extraction NLP basique de métriques quantiques depuis XML PMC
        
        Patterns détectés:
        - T2 = X µs/ms/ns
        - Coherence time: X µs
        - Contrast: X%
        
        Returns:
            Dict avec métriques extraites (ou None si non trouvé)
        """
        metrics = {
            't2_us': None,
            'contrast_pct': None,
            'temperature_k': None,
            'confidence': 0.0
        }
        
        # Pattern T2
        t2_patterns = [
            r'T[_\s]?2[_\s]*[=:≈~]\s*([0-9.]+)\s*(µs|us|μs|microsecond)',
            r'coherence\s+time[:\s]+([0-9.]+)\s*(µs|us|μs|microsecond)',
            r'T[_\s]?2[_\s]*[=:≈~]\s*([0-9.]+)\s*(ms|millisecond)',
        ]
        
        for pattern in t2_patterns:
            match = re.search(pattern, xml_text, re.IGNORECASE)
            if match:
                value = float(match.group(1))
                unit = match.group(2).lower()
                
                if 'ms' in unit or 'millisecond' in unit:
                    value *= 1000
                    
                metrics['t2_us'] = value
                metrics['confidence'] += 0.4
                break
        
        # Pattern Contraste
        contrast_patterns = [
            r'contrast[:\s]+([0-9.]+)\s*%',
            r'contrast[:\s]*[=:]\s*([0-9.]+)',
        ]
        
        for pattern in contrast_patterns:
            match = re.search(pattern, xml_text, re.IGNORECASE)
            if match:
                value = float(match.group(1))
                if value < 1:
                    value *= 100
                metrics['contrast_pct'] = value
                metrics['confidence'] += 0.3
                break
        
        # Température
        temp_patterns = [
            (r'room\s+temperature', 295),
            (r'physiological\s+temperature', 310),
            (r'([0-9.]+)\s*K\b', None),
        ]
        
        for pattern, conversion in temp_patterns:
            match = re.search(pattern, xml_text, re.IGNORECASE)
            if match:
                if conversion is None:
                    metrics['temperature_k'] = float(match.group(1))
                else:
                    metrics['temperature_k'] = conversion
                metrics['confidence'] += 0.2
                break
        
        return metrics if metrics['confidence'] > 0.3 else None
    
    def fetch_fpbase_biosensors(self, family: str = None) -> pd.DataFrame:
        """
        Extraction FPbase GraphQL (protéines fluorescentes biosenseurs)
        
        Args:
            family: Famille spécifique (ex: 'Calcium', 'Voltage') ou None pour toutes
            
        Returns:
            DataFrame avec protéines et métriques optiques
        """
        query = """
        query($family: String) {
          proteins(family: $family, limit: 200) {
            name
            seq
            agg
            switchType
            spectra {
              exMax
              emMax
              extCoeff
              qy
            }
            states {
              name
              lifetime
            }
            references {
              doi
            }
          }
        }
        """
        
        url = "https://www.fpbase.org/graphql/"
        headers = {'Authorization': f'Bearer {self.fpbase_api_key}'} if self.fpbase_api_key else {}
        
        try:
            response = requests.post(
                url,
                json={'query': query, 'variables': {'family': family}},
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            proteins = data.get('data', {}).get('proteins', [])
            print(f"✅ FPbase: {len(proteins)} protéines extraites")
            
            rows = []
            for p in proteins:
                spectra = p.get('spectra', [{}])[0]
                states = p.get('states', [{}])[0]
                refs = p.get('references', [])
                
                rows.append({
                    'name': p.get('name'),
                    'family': family or 'Unknown',
                    'ex_max_nm': spectra.get('exMax'),
                    'em_max_nm': spectra.get('emMax'),
                    'qy': spectra.get('qy'),
                    'lifetime_ns': states.get('lifetime'),
                    'doi': refs[0].get('doi') if refs else None,
                    'source': 'fpbase'
                })
            
            return pd.DataFrame(rows)
        
        except Exception as e:
            print(f"⚠️ Erreur FPbase API: {e}")
            return pd.DataFrame()
    
    def run_full_harvest(self, output_path: str = "data/interim/auto_harvest_v2.csv"):
        """
        Pipeline complet d'extraction multi-sources
        
        Étapes:
        1. PubMed: systèmes NV/SiC/défauts solides
        2. PMC: extraction texte intégral (Open Access)
        3. FPbase: protéines fluorescentes biosenseurs
        4. Déduplication et scoring
        5. Export CSV
        """
        all_candidates = []
        
        # ÉTAPE 1: PubMed NV/SiC
        print("\n🔬 ÉTAPE 1: Recherche PubMed...")
        queries = [
            '"nitrogen vacancy" AND (biological OR cell OR vivo)',
            '"silicon vacancy" AND (biological OR biocompatible)',
            '"silicon carbide" AND ODMR AND (cell OR biological)',
            '"quantum sensor" AND (fluorescent protein OR biosensor)',
        ]
        
        for query in queries:
            pmids = self.search_pubmed(query, max_results=100)
            print(f"  → {len(pmids)} PMIDs pour '{query[:40]}...'")
        
        # ÉTAPE 2: FPbase Biosensors
        print("\n🧬 ÉTAPE 2: Extraction FPbase...")
        families = ['Calcium', 'Voltage', 'Dopamine', 'Glutamate', 'pH']
        
        for family in families:
            df = self.fetch_fpbase_biosensors(family)
            if not df.empty:
                all_candidates.append(df)
        
        # ÉTAPE 3: Consolidation
        if all_candidates:
            final_df = pd.concat(all_candidates, ignore_index=True)
            final_df = final_df.drop_duplicates(subset=['name'])
            
            print(f"\n✅ Total candidates: {len(final_df)}")
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            final_df.to_csv(output_path, index=False)
            print(f"📁 Exporté vers: {output_path}")
            
            return final_df
        else:
            print("⚠️ Aucun candidat extrait")
            return pd.DataFrame()

if __name__ == "__main__":
    # Configuration (remplacer par vos clés API)
    api_keys = {
        'ncbi': os.getenv('NCBI_API_KEY', 'VOTRE_CLE_NCBI'),
        'fpbase': os.getenv('FPBASE_API_KEY'),
        'email': os.getenv('NCBI_EMAIL', 'votre@email.com')
    }
    
    harvester = AutoHarvester(api_keys)
    df = harvester.run_full_harvest()
    
    print("\n📊 Statistiques:")
    print(f"  - Candidats uniques: {len(df)}")
    print(f"  - Avec DOI: {df['doi'].notna().sum()}")
    print(f"  - Familles: {df['family'].nunique()}")


