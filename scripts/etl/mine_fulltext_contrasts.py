#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mine Full-Text Contrasts — Real Data Only
==========================================
Extrait les mesures de contraste depuis les full-text XML d'articles OA.

Stratégie:
1. Pour chaque protéine du seed
2. Chercher articles OA dans Europe PMC
3. Télécharger full-text XML
4. Parser tables + figures pour trouver mesures de contraste
5. Extraire valeur + contexte + DOI + licence
6. Agréger meilleure mesure par protéine
"""

import sys
import re
import time
from pathlib import Path
import pandas as pd
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional, Tuple

# Add providers to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from providers.europe_pmc import EuropePMCProvider

# Paths
SEED_FILE = Path("seed/seed_fp_names.csv")
ATLAS_FILE = Path("data/processed/atlas_fp_optical.csv")
OUTPUT_FILE = Path("data/interim/fulltext_contrasts.csv")
EVIDENCE_FILE = Path("reports/EVIDENCE_SAMPLES.md")
OA_LOG = Path("reports/OA_FETCH_LOG.md")

# Contrast patterns (more comprehensive)
CONTRAST_PATTERNS = [
    (r'ΔF/F[₀0]?\s*[=:~≈]?\s*([\d.]+)\s*%?', 'delta_F_F0'),
    (r'dF/F[₀0]?\s*[=:~≈]?\s*([\d.]+)\s*%?', 'delta_F_F0'),
    (r'(\d+\.?\d*)\s*%\s*change', 'percent_change'),
    (r'(\d+\.?\d*)-fold\s+(?:change|increase|response)', 'fold_change'),
    (r'dynamic\s+range[:\s]+([\d.]+)', 'dynamic_range'),
    (r'on[/-]off\s+ratio[:\s]+([\d.]+)', 'on_off_ratio'),
    (r'response\s+amplitude[:\s]+([\d.]+)', 'response_amp'),
]

def extract_numbers_from_text(text: str) -> List[Tuple[float, str, str]]:
    """Extrait les mesures de contraste depuis du texte."""
    measurements = []
    
    for pattern, measure_type in CONTRAST_PATTERNS:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            try:
                value = float(match.group(1))
                # Validate plausible range
                if measure_type == 'percent_change' and (value < 0 or value > 10000):
                    continue
                if measure_type == 'fold_change' and (value < 0.1 or value > 1000):
                    continue
                if measure_type in ['delta_F_F0', 'on_off_ratio'] and (value < 0.01 or value > 100):
                    continue
                
                # Get context
                start = max(0, match.start() - 100)
                end = min(len(text), match.end() + 100)
                context = text[start:end].strip()
                
                measurements.append((value, measure_type, context))
            except (ValueError, IndexError):
                continue
    
    return measurements

def parse_xml_for_contrasts(xml_text: str, protein_name: str) -> List[Dict]:
    """Parse XML pour trouver mesures de contraste."""
    measurements = []
    
    try:
        # Parse XML
        root = ET.fromstring(xml_text)
        
        # Search in tables
        for table in root.iter('table'):
            table_text = ET.tostring(table, encoding='unicode', method='text')
            
            # Check if protein mentioned in table
            if protein_name.lower() in table_text.lower():
                # Extract measurements
                found = extract_numbers_from_text(table_text)
                for value, mtype, context in found:
                    measurements.append({
                        'value': value,
                        'measure_type': mtype,
                        'context': context[:200],
                        'source_section': 'table',
                        'evidence_type': 'xml_table'
                    })
        
        # Search in figure captions
        for fig in root.iter('fig'):
            caption = fig.find('.//caption')
            if caption is not None:
                caption_text = ET.tostring(caption, encoding='unicode', method='text')
                
                if protein_name.lower() in caption_text.lower():
                    found = extract_numbers_from_text(caption_text)
                    for value, mtype, context in found:
                        measurements.append({
                            'value': value,
                            'measure_type': mtype,
                            'context': context[:200],
                            'source_section': 'figure',
                            'evidence_type': 'xml_figure'
                        })
        
        # Search in results paragraphs
        for p in root.iter('p'):
            p_text = ET.tostring(p, encoding='unicode', method='text')
            
            # Only if protein mentioned nearby
            if protein_name.lower() in p_text.lower():
                found = extract_numbers_from_text(p_text)
                for value, mtype, context in found[:1]:  # Max 1 per paragraph
                    measurements.append({
                        'value': value,
                        'measure_type': mtype,
                        'context': context[:200],
                        'source_section': 'paragraph',
                        'evidence_type': 'xml_text'
                    })
    
    except Exception as e:
        print(f"    XML parsing failed: {e}")
    
    return measurements

def process_protein(protein_name: str, provider: EuropePMCProvider) -> Optional[Dict]:
    """Traite une protéine et retourne la meilleure mesure."""
    print(f"\n  Processing: {protein_name}")
    
    # Search PMC
    articles = provider.search_protein_contrast(protein_name, max_results=10)
    
    if not articles:
        print(f"    No OA articles found")
        return None
    
    print(f"    Found {len(articles)} OA articles")
    
    all_measurements = []
    
    # Process each article
    for i, article in enumerate(articles[:3], 1):  # Limit to 3 articles
        pmcid = article.get('pmcid', '')
        doi = article.get('doi', '')
        title = article.get('title', '')
        
        if not pmcid:
            continue
        
        print(f"    [{i}] {pmcid}")
        
        # Get full-text XML
        xml_text = provider.get_fulltext_xml(pmcid)
        
        if not xml_text:
            print(f"        No XML available")
            continue
        
        # Parse for contrasts
        measurements = parse_xml_for_contrasts(xml_text, protein_name)
        
        if measurements:
            print(f"        Found {len(measurements)} measurements")
            for m in measurements:
                m['pmcid'] = pmcid
                m['doi'] = doi
                m['protein_name'] = protein_name
                all_measurements.append(m)
        
        time.sleep(0.5)  # Rate limiting
    
    if not all_measurements:
        return None
    
    # Select best measurement (prefer table/figure, highest value if tie)
    best = sorted(all_measurements, 
                  key=lambda x: (
                      x['source_section'] in ['table', 'figure'],  # Prefer structured
                      x['value']  # Then by value
                  ), reverse=True)[0]
    
    return {
        'protein_name': protein_name,
        'contrast_ratio': best['value'],
        'measure_type': best['measure_type'],
        'condition_text': best['context'],
        'pmcid': best['pmcid'],
        'doi': best['doi'],
        'source_refs': f"PMC:{best['pmcid']}" if best['pmcid'] else f"DOI:{best['doi']}",
        'license_source': 'CC BY (PMC OA)',
        'contrast_source': 'measured',
        'evidence_type': best['evidence_type'],
        'source_section': best['source_section']
    }

def mine_contrasts():
    """Mine contrasts pour toutes les protéines."""
    # Load seed
    seed_df = pd.read_csv(SEED_FILE)
    print(f"Mining contrasts for {len(seed_df)} proteins...")
    
    provider = EuropePMCProvider()
    
    results = []
    
    # Process each protein
    for idx, row in seed_df.iterrows():
        name = row['name']
        
        result = process_protein(name, provider)
        
        if result:
            results.append(result)
            print(f"    OK Extracted: {result['contrast_ratio']} ({result['measure_type']})")
        
        # Limit to avoid very long run (process first 50)
        if idx >= 49:
            print("\n  Limiting to first 50 proteins...")
            break
        
        time.sleep(1)  # Rate limiting
    
    return pd.DataFrame(results)

def update_atlas(contrasts_df: pd.DataFrame):
    """Met à jour l'atlas avec les contrastes extraits."""
    # Load atlas
    atlas_df = pd.read_csv(ATLAS_FILE)
    print(f"\nUpdating atlas ({len(atlas_df)} entries)...")
    
    # Update each protein
    updated = 0
    for _, row in contrasts_df.iterrows():
        name = row['protein_name']
        
        mask = atlas_df['protein_name'] == name
        
        if mask.any():
            # Only update if no existing measured value
            existing = atlas_df.loc[mask, 'contrast_source'].iloc[0]
            
            if existing != 'measured':
                atlas_df.loc[mask, 'contrast_ratio'] = row['contrast_ratio']
                atlas_df.loc[mask, 'condition_text'] = row['condition_text']
                atlas_df.loc[mask, 'contrast_source'] = 'measured'
                
                # Update source refs
                if pd.isna(atlas_df.loc[mask, 'source_refs'].iloc[0]):
                    atlas_df.loc[mask, 'source_refs'] = row['source_refs']
                    atlas_df.loc[mask, 'license_source'] = row['license_source']
                else:
                    atlas_df.loc[mask, 'source_refs'] += f"; {row['source_refs']}"
                
                updated += 1
    
    # Save
    atlas_df.to_csv(ATLAS_FILE, index=False)
    print(f"Updated {updated} entries in atlas")
    
    # Stats
    n_measured = (atlas_df['contrast_source'] == 'measured').sum()
    print(f"\nAtlas now has {n_measured} entries with measured contrast")
    
    return atlas_df, n_measured

def generate_evidence_report(contrasts_df: pd.DataFrame):
    """Génère le rapport de preuves."""
    EVIDENCE_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(EVIDENCE_FILE, 'w', encoding='utf-8') as f:
        f.write("# Evidence Samples — Measured Contrasts\n\n")
        f.write(f"**Date**: {pd.Timestamp.now().isoformat()}\n\n")
        f.write(f"**Total measurements extracted**: {len(contrasts_df)}\n\n")
        
        f.write("## Sample Evidences\n\n")
        f.write("| Protein | Value | Type | Section | Context Snippet | PMC | DOI |\n")
        f.write("|---------|-------|------|---------|----------------|-----|-----|\n")
        
        for _, row in contrasts_df.head(25).iterrows():
            snippet = row['condition_text'][:80].replace('|', '/')
            pmcid = row['pmcid'] if pd.notna(row['pmcid']) else 'N/A'
            doi = row['doi'] if pd.notna(row['doi']) else 'N/A'
            
            f.write(f"| {row['protein_name']} | {row['contrast_ratio']:.2f} | {row['measure_type']} | {row['source_section']} | {snippet}... | {pmcid} | {doi} |\n")
        
        f.write("\n")
    
    print(f"Evidence report saved to {EVIDENCE_FILE}")

def main():
    """Point d'entrée."""
    print("=" * 70)
    print("Mine Full-Text Contrasts — Real Data Only")
    print("=" * 70)
    
    # Mine contrasts
    contrasts_df = mine_contrasts()
    
    if len(contrasts_df) == 0:
        print("\nWARNING: No contrasts extracted!")
        return 1
    
    # Save extracted
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    contrasts_df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSaved {len(contrasts_df)} measurements to {OUTPUT_FILE}")
    
    # Update atlas
    atlas_df, n_measured = update_atlas(contrasts_df)
    
    # Generate evidence report
    generate_evidence_report(contrasts_df)
    
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    print(f"Measurements extracted: {len(contrasts_df)}")
    print(f"Atlas entries with measured contrast: {n_measured}")
    print("=" * 70)
    
    print("\nOK Full-text mining completed!")
    return 0

if __name__ == "__main__":
    sys.exit(main())

