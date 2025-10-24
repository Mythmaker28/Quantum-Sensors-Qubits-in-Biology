#!/usr/bin/env python3
"""
PMC Full-Text Contrast Miner v1.3
==================================

Mine contrast measurements from PMC Open Access full-text articles (XML/PDF).

Extracts:
- ΔF/F₀, fold-change, percent change, dynamic range
- n, CI, SD if present
- Context (temperature, pH, host, figure/table ref)

Author: Biological Qubit Atlas Team
License: MIT
"""

import requests
import json
import re
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import time
import yaml
from xml.etree import ElementTree as ET

def load_config() -> Dict:
    """Load provider configuration."""
    with open("config/providers.yml", 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

CONFIG = load_config()
PMC_CONFIG = CONFIG['europe_pmc']
PMC_API_URL = PMC_CONFIG['api_url']

# Contrast patterns (regex)
CONTRAST_PATTERNS = [
    # ΔF/F₀ patterns
    (r'ΔF/F[₀0]\s*=\s*([0-9.]+)([%±]?\s*[0-9.]*)?', 'deltaF_F0'),
    (r'dF/F[₀0]?\s*=\s*([0-9.]+)([%±]?\s*[0-9.]*)?', 'deltaF_F0'),
    (r'ΔR/R[₀0]\s*=\s*([0-9.]+)([%±]?\s*[0-9.]*)?', 'deltaR_R0'),
    
    # Fold change
    (r'([0-9.]+)[-\s]fold\s+(?:change|increase|response)', 'fold'),
    (r'fold[-\s]change\s*[:=]?\s*([0-9.]+)', 'fold'),
    
    # Percent change
    (r'([0-9.]+)%\s+(?:change|increase|response|ΔF)', 'percent'),
    (r'percent\s+change\s*[:=]?\s*([0-9.]+)', 'percent'),
    
    # Dynamic range
    (r'dynamic\s+range\s*[:=]?\s*([0-9.]+)', 'fold'),
    (r'on/off\s+ratio\s*[:=]?\s*([0-9.]+)', 'fold'),
]

# Statistical info patterns
STATS_PATTERNS = {
    'n': r'n\s*=\s*([0-9]+)',
    'sd': r'SD\s*=\s*([0-9.]+)',
    'sem': r'SEM\s*=\s*([0-9.]+)',
    'ci_low': r'\[([0-9.]+)[-–,]\s*[0-9.]+\]',  # [low, high]
    'ci_high': r'\[[0-9.]+[-–,]\s*([0-9.]+)\]',
}

def search_pmc_for_protein(protein_name: str, family: str = None) -> List[str]:
    """
    Search PMC Open Access for articles about a protein.
    
    Args:
        protein_name: Name of the protein
        family: Optional family name for context
        
    Returns:
        List of PMCIDs
    """
    query_terms = [protein_name]
    if family:
        query_terms.append(family)
    
    # Add contrast keywords
    query_terms.extend(['ΔF/F0', 'fold change', 'response', 'fluorescence'])
    
    query = ' AND '.join([f'"{term}"' for term in query_terms])
    
    url = f"{PMC_API_URL}search"
    params = {
        'query': query,
        'format': 'json',
        'pageSize': 25,
        'isOpenAccess': 'Y',
        'hasTextMinedTerms': 'Y'
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if 'resultList' in data and 'result' in data['resultList']:
                pmcids = [
                    result.get('pmcid') 
                    for result in data['resultList']['result'] 
                    if result.get('pmcid')
                ]
                return pmcids
        return []
    except Exception as e:
        print(f"ERROR searching PMC for {protein_name}: {e}")
        return []

def fetch_pmc_fulltext_xml(pmcid: str) -> Optional[str]:
    """
    Fetch full-text XML from PMC.
    
    Args:
        pmcid: PMC ID (e.g., 'PMC1234567')
        
    Returns:
        XML content as string or None
    """
    url = f"{PMC_API_URL}{pmcid}/fullTextXML"
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            # Save to file
            output_dir = Path(f"data/raw/oa/{pmcid}")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            xml_path = output_dir / "fulltext.xml"
            xml_path.write_text(response.text, encoding='utf-8')
            
            return response.text
        return None
    except Exception as e:
        print(f"ERROR fetching XML for {pmcid}: {e}")
        return None

def extract_contrast_from_xml(xml_content: str, pmcid: str) -> List[Dict]:
    """
    Extract contrast measurements from PMC XML.
    
    Args:
        xml_content: Full-text XML content
        pmcid: PMC ID
        
    Returns:
        List of contrast measurements
    """
    measurements = []
    
    try:
        root = ET.fromstring(xml_content)
        
        # Search in tables
        for table in root.findall('.//table'):
            table_text = ET.tostring(table, encoding='unicode', method='text')
            hits = extract_contrast_from_text(table_text, pmcid, 'table')
            measurements.extend(hits)
        
        # Search in paragraphs
        for para in root.findall('.//p'):
            para_text = ET.tostring(para, encoding='unicode', method='text')
            hits = extract_contrast_from_text(para_text, pmcid, 'paragraph')
            measurements.extend(hits)
        
        # Search in figure captions
        for caption in root.findall('.//caption'):
            caption_text = ET.tostring(caption, encoding='unicode', method='text')
            hits = extract_contrast_from_text(caption_text, pmcid, 'caption')
            measurements.extend(hits)
    
    except ET.ParseError as e:
        print(f"ERROR parsing XML for {pmcid}: {e}")
    
    return measurements

def extract_contrast_from_text(text: str, pmcid: str, section_type: str) -> List[Dict]:
    """
    Extract contrast values from text using regex patterns.
    
    Args:
        text: Text to search
        pmcid: PMC ID
        section_type: Type of section (table/paragraph/caption)
        
    Returns:
        List of measurements
    """
    measurements = []
    
    for pattern, metric_type in CONTRAST_PATTERNS:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            value_str = match.group(1)
            try:
                value = float(value_str)
                
                # Extract statistical info nearby (±50 chars)
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end]
                
                stats = {}
                for stat_name, stat_pattern in STATS_PATTERNS.items():
                    stat_match = re.search(stat_pattern, context, re.IGNORECASE)
                    if stat_match:
                        stats[stat_name] = float(stat_match.group(1))
                
                measurements.append({
                    'value': value,
                    'metric_type': metric_type,
                    'pmcid': pmcid,
                    'section_type': section_type,
                    'context': context.strip(),
                    'n': stats.get('n'),
                    'sd': stats.get('sd'),
                    'sem': stats.get('sem'),
                    'ci_low': stats.get('ci_low'),
                    'ci_high': stats.get('ci_high')
                })
            except ValueError:
                continue
    
    return measurements

def mine_protein_contrasts(protein_name: str, family: str = None) -> List[Dict]:
    """
    Mine contrast measurements for a protein.
    
    Args:
        protein_name: Name of the protein
        family: Optional family name
        
    Returns:
        List of contrast measurements
    """
    print(f"Mining contrasts for {protein_name}...")
    
    # Search PMC
    pmcids = search_pmc_for_protein(protein_name, family)
    if not pmcids:
        print(f"  No PMC articles found")
        return []
    
    print(f"  Found {len(pmcids)} PMC articles")
    
    all_measurements = []
    
    # Fetch and mine each article
    for pmcid in pmcids[:5]:  # Limit to 5 articles per protein
        print(f"  Mining {pmcid}...")
        
        xml_content = fetch_pmc_fulltext_xml(pmcid)
        if xml_content:
            measurements = extract_contrast_from_xml(xml_content, pmcid)
            all_measurements.extend(measurements)
            print(f"    Found {len(measurements)} measurements")
        
        time.sleep(1)  # Rate limiting
    
    return all_measurements

def main():
    """Main miner."""
    print("=" * 60)
    print("PMC Full-Text Contrast Miner v1.3")
    print("=" * 60)
    
    # Load seed proteins
    seed_path = Path("seed/seed_fp_names.csv")
    if not seed_path.exists():
        print("ERROR: seed/seed_fp_names.csv not found")
        return
    
    import csv
    with open(seed_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        seeds = list(reader)
    
    print(f"Mining {len(seeds)} proteins...")
    
    all_results = {}
    
    for seed in seeds[:20]:  # Process first 20 for now
        name = seed['name']
        family = seed.get('family')
        
        measurements = mine_protein_contrasts(name, family)
        if measurements:
            all_results[name] = measurements
    
    # Save results
    output_path = Path("data/interim/pmc_contrasts.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    total_measurements = sum(len(m) for m in all_results.values())
    print(f"\nOK Total measurements extracted: {total_measurements}")
    print(f"OK Saved to: {output_path}")

if __name__ == "__main__":
    main()

