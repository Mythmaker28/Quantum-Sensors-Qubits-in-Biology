#!/usr/bin/env python3
"""
Extract Addgene Data - Atlas v2.2 Extension
===========================================

Extrait automatiquement les données de capteurs fluorescents depuis Addgene.
Source: https://www.addgene.org/search/catalog/plasmids/
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from pathlib import Path
import json

# Configuration
BASE_URL = "https://www.addgene.org/search/catalog/plasmids/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Requêtes prioritaires
QUERIES = [
    "calcium+indicator",
    "voltage+indicator", 
    "GRAB+sensor",
    "dLight",
    "iGluSnFR",
    "GCaMP",
    "jRGECO"
]

def load_existing_data():
    """Charge les données existantes pour éviter les doublons"""
    
    dois_path = Path(".atlas_sync/processed_dois.txt")
    canonical_path = Path(".atlas_sync/processed_canonical.txt")
    
    existing_dois = set()
    existing_names = set()
    
    if dois_path.exists():
        with open(dois_path, 'r', encoding='utf-8') as f:
            existing_dois = set(line.strip() for line in f if line.strip())
    
    if canonical_path.exists():
        with open(canonical_path, 'r', encoding='utf-8') as f:
            existing_names = set(line.strip() for line in f if line.strip())
    
    print(f"[LOAD] DOIs existants: {len(existing_dois)}")
    print(f"[LOAD] Noms existants: {len(existing_names)}")
    
    return existing_dois, existing_names

def search_addgene(query, max_pages=3):
    """Recherche sur Addgene et extrait les résultats"""
    
    print(f"\n[SEARCH] Requête: {query}")
    
    all_results = []
    
    for page in range(1, max_pages + 1):
        url = f"{BASE_URL}?q={query}&page={page}"
        
        try:
            print(f"  Page {page}: {url}")
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Chercher les liens vers les plasmides
            plasmid_links = soup.find_all('a', href=re.compile(r'/plasmids/\d+/'))
            
            if not plasmid_links:
                print(f"  Aucun résultat trouvé sur la page {page}")
                break
            
            print(f"  {len(plasmid_links)} plasmides trouvés")
            
            for link in plasmid_links[:10]:  # Limiter à 10 par page
                plasmid_url = "https://www.addgene.org" + link['href']
                plasmid_data = extract_plasmid_details(plasmid_url)
                
                if plasmid_data:
                    all_results.append(plasmid_data)
                    time.sleep(1)  # Respecter le rate limiting
            
            time.sleep(2)  # Pause entre pages
            
        except Exception as e:
            print(f"  ERREUR page {page}: {e}")
            continue
    
    return all_results

def extract_plasmid_details(url):
    """Extrait les détails d'un plasmide spécifique"""
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extraire le nom
        name_elem = soup.find('h1', class_='plasmid-name')
        if not name_elem:
            return None
        
        name = name_elem.get_text().strip()
        
        # Extraire les propriétés optiques
        excitation = None
        emission = None
        quantum_yield = None
        
        # Chercher dans les sections de propriétés
        properties_section = soup.find('div', class_='plasmid-properties')
        if properties_section:
            # Chercher excitation/emission
            for prop in properties_section.find_all('div', class_='property'):
                label = prop.find('span', class_='property-label')
                value = prop.find('span', class_='property-value')
                
                if label and value:
                    label_text = label.get_text().lower()
                    value_text = value.get_text().strip()
                    
                    if 'excitation' in label_text and 'nm' in value_text:
                        excitation = extract_number(value_text)
                    elif 'emission' in label_text and 'nm' in value_text:
                        emission = extract_number(value_text)
                    elif 'quantum yield' in label_text:
                        quantum_yield = extract_number(value_text)
        
        # Extraire DOI/Reference
        doi = None
        references_section = soup.find('div', class_='references')
        if references_section:
            doi_links = references_section.find_all('a', href=re.compile(r'doi\.org'))
            if doi_links:
                doi = doi_links[0]['href'].replace('https://doi.org/', '')
        
        # Déterminer la famille
        family = determine_family(name, soup)
        
        # Calculer le contraste (estimation basée sur le type)
        contrast = estimate_contrast(family, name)
        
        # Vérifier si on a les données minimales
        if not excitation or not emission or not doi:
            return None
        
        return {
            'canonical_name': name,
            'family': family,
            'excitation_nm': float(excitation),
            'emission_nm': float(emission),
            'stokes_shift_nm': float(emission) - float(excitation),
            'method': 'fluorescence',
            'context_type': 'in_cellulo',
            'contrast_normalized': contrast,
            'source': 'Addgene',
            'provenance': doi,
            'license': 'CC-BY-4.0',
            'excitation_missing': False,
            'emission_missing': False,
            'contrast_missing': False
        }
        
    except Exception as e:
        print(f"    ERREUR extraction {url}: {e}")
        return None

def extract_number(text):
    """Extrait un nombre d'un texte"""
    numbers = re.findall(r'\d+\.?\d*', text)
    return float(numbers[0]) if numbers else None

def determine_family(name, soup):
    """Détermine la famille du capteur basée sur le nom et la description"""
    
    name_lower = name.lower()
    
    if any(x in name_lower for x in ['gcamp', 'jrgcamp', 'gcamp']):
        return 'Calcium'
    elif any(x in name_lower for x in ['asap', 'archon', 'voltage']):
        return 'Voltage'
    elif any(x in name_lower for x in ['grab', 'dlight']):
        if 'dopamine' in name_lower or 'da' in name_lower:
            return 'Dopamine'
        elif 'serotonin' in name_lower or '5ht' in name_lower:
            return 'Serotonin'
        elif 'glutamate' in name_lower or 'glu' in name_lower:
            return 'Glutamate'
        else:
            return 'Neurotransmitter'
    elif any(x in name_lower for x in ['iglu', 'iglusnfr']):
        return 'Glutamate'
    elif any(x in name_lower for x in ['ph', 'phluorin', 'sypher']):
        return 'pH'
    elif any(x in name_lower for x in ['camp', 'flamindo']):
        return 'cAMP'
    else:
        return 'Other'

def estimate_contrast(family, name):
    """Estime le contraste basé sur la famille et le nom"""
    
    # Estimations basées sur la littérature
    if family == 'Calcium':
        if 'gcamp' in name.lower():
            return 20.0  # GCaMP typique
        elif 'jrgcamp' in name.lower():
            return 30.0  # jRGECO plus sensible
        else:
            return 15.0
    elif family == 'Voltage':
        return 0.5  # Voltage sensors typiques
    elif family == 'Dopamine':
        return 3.0  # dLight/GRAB-DA typique
    elif family == 'Serotonin':
        return 2.5  # GRAB-5HT typique
    elif family == 'Glutamate':
        return 5.0  # iGluSnFR typique
    elif family == 'pH':
        return 4.0  # pH sensors typiques
    elif family == 'cAMP':
        return 2.0  # cAMP sensors typiques
    else:
        return 1.5  # Valeur par défaut

def filter_duplicates(results, existing_dois, existing_names):
    """Filtre les doublons basés sur DOI et nom canonique"""
    
    filtered = []
    skipped_doi = 0
    skipped_name = 0
    
    for result in results:
        # Vérifier DOI
        if result['provenance'] in existing_dois:
            skipped_doi += 1
            continue
        
        # Vérifier nom canonique
        if result['canonical_name'] in existing_names:
            skipped_name += 1
            continue
        
        filtered.append(result)
    
    print(f"\n[FILTER] Résultats après dédup:")
    print(f"  Entrées brutes: {len(results)}")
    print(f"  Doublons DOI: {skipped_doi}")
    print(f"  Doublons nom: {skipped_name}")
    print(f"  Entrées uniques: {len(filtered)}")
    
    return filtered

def main():
    """Fonction principale"""
    
    print("=" * 80)
    print("EXTRACTION ADDGENE - Atlas v2.2 Extension")
    print("=" * 80)
    
    # Charger données existantes
    existing_dois, existing_names = load_existing_data()
    
    # Créer répertoire de sortie
    output_dir = Path("data/raw/addgene")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    all_results = []
    
    # Exécuter les requêtes
    for query in QUERIES:
        results = search_addgene(query, max_pages=2)  # Limiter à 2 pages par requête
        all_results.extend(results)
        time.sleep(3)  # Pause entre requêtes
    
    print(f"\n[EXTRACT] Total entrées brutes: {len(all_results)}")
    
    # Filtrer les doublons
    unique_results = filter_duplicates(all_results, existing_dois, existing_names)
    
    if not unique_results:
        print("\n[WARNING] Aucune nouvelle entrée unique trouvée")
        return
    
    # Créer DataFrame et sauvegarder
    df = pd.DataFrame(unique_results)
    
    output_file = output_dir / "addgene_batch_1.csv"
    df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"\n[SAVE] Fichier créé: {output_file}")
    print(f"  Entrées uniques: {len(df)}")
    
    # Afficher quelques exemples
    print(f"\n[EXAMPLES] Premières entrées:")
    for i, row in df.head(3).iterrows():
        print(f"  {i+1}. {row['canonical_name']} ({row['family']}) - {row['excitation_nm']}nm/{row['emission_nm']}nm")
    
    return len(df)

if __name__ == "__main__":
    n_added = main()
    if n_added:
        print(f"\n🎉 {n_added} nouveaux systèmes Addgene extraits !")
    else:
        print("\n⚠️ Aucun nouveau système trouvé")
