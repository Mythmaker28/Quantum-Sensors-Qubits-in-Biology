#!/usr/bin/env python3
"""
Récupération agressive de biosenseurs via APIs multiples.
"""
import requests
import pandas as pd
from pathlib import Path
import time
import json
import sys

def get_current_atlas():
    """Charge l'atlas actuel."""
    csv_path = Path("data/processed/atlas_fp_optical_v2_2.csv")
    df = pd.read_csv(csv_path)
    current_names = set(df['protein_name'].str.lower().str.strip())
    current_dois = set(df['doi'].dropna().str.lower().str.strip())
    return df, current_names, current_dois

def try_fpbase_graphql():
    """Tente l'API GraphQL de FPbase."""
    print("\n[*] Tentative FPbase GraphQL...")
    
    url = "https://www.fpbase.org/graphql/"
    
    # Query pour biosenseurs
    query = """
    query {
      proteins(isSensor: true, first: 50) {
        edges {
          node {
            name
            slug
            seq
            agg
            switchType
            primaryReference {
              doi
              title
            }
            states {
              exMax
              emMax
            }
          }
        }
      }
    }
    """
    
    try:
        response = requests.post(
            url, 
            json={'query': query},
            headers={'Content-Type': 'application/json'},
            timeout=20
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and data['data']:
                proteins = data['data'].get('proteins', {}).get('edges', [])
                print(f"[OK] FPbase GraphQL: {len(proteins)} proteines recues")
                
                candidates = []
                for edge in proteins:
                    node = edge.get('node', {})
                    name = node.get('name')
                    doi_ref = node.get('primaryReference', {})
                    doi = doi_ref.get('doi') if doi_ref else None
                    
                    if name and doi:
                        states = node.get('states', [])
                        ex_max = states[0].get('exMax') if states else None
                        em_max = states[0].get('emMax') if states else None
                        
                        candidates.append({
                            'protein_name': name,
                            'doi': doi,
                            'excitation_nm': ex_max,
                            'emission_nm': em_max,
                            'source': 'fpbase_graphql'
                        })
                
                return candidates
        
        print(f"[WARN] FPbase GraphQL: status {response.status_code}")
        return []
        
    except Exception as e:
        print(f"[WARN] FPbase GraphQL failed: {e}")
        return []

def try_uniprot_api(query_terms):
    """Tente UniProt API pour protéines fluorescentes."""
    print("\n[*] Tentative UniProt API...")
    
    url = "https://rest.uniprot.org/uniprotkb/search"
    
    candidates = []
    
    for term in query_terms:
        try:
            params = {
                'query': f'(protein_name:{term}) AND (reviewed:true)',
                'format': 'json',
                'size': 20
            }
            
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                
                for entry in results:
                    name = entry.get('proteinDescription', {}).get('recommendedName', {}).get('fullName', {}).get('value')
                    uniprot_id = entry.get('primaryAccession')
                    
                    # Chercher DOI dans references
                    references = entry.get('references', [])
                    doi = None
                    for ref in references:
                        citation = ref.get('citation', {})
                        if 'doi' in citation.get('citationCrossReferences', [{}])[0].get('database', '').lower():
                            doi = citation['citationCrossReferences'][0].get('id')
                            break
                    
                    if name and doi:
                        candidates.append({
                            'protein_name': name,
                            'doi': doi,
                            'uniprot_id': uniprot_id,
                            'source': 'uniprot'
                        })
                
                print(f"[OK] UniProt '{term}': {len(results)} resultats")
                time.sleep(0.5)  # Rate limiting
            
        except Exception as e:
            print(f"[WARN] UniProt '{term}' failed: {e}")
    
    return candidates

def try_fpbase_csv_fallback():
    """Tente de télécharger le CSV export de FPbase."""
    print("\n[*] Tentative FPbase CSV export...")
    
    # URL alternative
    csv_urls = [
        "https://www.fpbase.org/api/proteins/?format=csv",
        "https://www.fpbase.org/proteins/table/?output=csv"
    ]
    
    for url in csv_urls:
        try:
            print(f"    Essai: {url}")
            response = requests.get(url, timeout=20)
            
            if response.status_code == 200 and 'text/csv' in response.headers.get('Content-Type', ''):
                # Sauvegarder temporairement
                cache_path = Path("data/cache/fpbase_export.csv")
                cache_path.parent.mkdir(parents=True, exist_ok=True)
                cache_path.write_text(response.text, encoding='utf-8')
                
                # Parser
                df = pd.read_csv(cache_path)
                print(f"[OK] FPbase CSV: {len(df)} lignes")
                
                # Filtrer biosenseurs
                if 'switch_type' in df.columns:
                    biosensors = df[df['switch_type'].notna()]
                    print(f"    Biosenseurs detectes: {len(biosensors)}")
                    return biosensors
                
                return df
                
        except Exception as e:
            print(f"    Failed: {e}")
    
    return None

def fetch_new_systems():
    """Orchestre la récupération depuis toutes les APIs."""
    print("[*] Recuperation agressive de nouveaux systemes...")
    
    # Charger atlas actuel
    df, current_names, current_dois = get_current_atlas()
    print(f"[*] Atlas actuel: {len(df)} systemes")
    
    all_candidates = []
    
    # 1. FPbase GraphQL
    fpbase_candidates = try_fpbase_graphql()
    all_candidates.extend(fpbase_candidates)
    
    # 2. UniProt
    search_terms = [
        'GCaMP', 'jGCaMP', 'RCaMP', 'XCaMP',  # Calcium
        'ASAP', 'VSFP', 'Ace',  # Voltage
        'GRAB', 'dLight', 'iGlu', 'iGABA',  # Neurotransmitters
        'pHluorin', 'pHuji',  # pH
        'HyPer', 'roGFP'  # Redox
    ]
    
    uniprot_candidates = try_uniprot_api(search_terms)
    all_candidates.extend(uniprot_candidates)
    
    # 3. FPbase CSV fallback
    fpbase_csv = try_fpbase_csv_fallback()
    if fpbase_csv is not None and len(fpbase_csv) > 0:
        # Convertir en format candidat
        for _, row in fpbase_csv.head(30).iterrows():
            name = row.get('name', row.get('protein_name'))
            if pd.notna(name):
                all_candidates.append({
                    'protein_name': name,
                    'doi': row.get('primary_reference_doi', row.get('doi')),
                    'source': 'fpbase_csv'
                })
    
    # Filtrer nouveaux systemes
    print(f"\n[*] Analyse de {len(all_candidates)} candidats...")
    
    new_systems = []
    for candidate in all_candidates:
        name_raw = candidate.get('protein_name', '')
        name = str(name_raw).lower().strip() if pd.notna(name_raw) else ''
        
        doi_raw = candidate.get('doi')
        doi = str(doi_raw).lower().strip() if pd.notna(doi_raw) and doi_raw else None
        
        # Déjà présent ?
        if name in current_names:
            continue
        
        if doi and doi in current_dois:
            continue
        
        # DOI obligatoire
        if not doi or doi == '':
            continue
        
        # Pas déjà dans new_systems
        if any(s['protein_name'].lower() == name for s in new_systems):
            continue
        
        new_systems.append(candidate)
    
    print(f"[OK] {len(new_systems)} nouveaux systemes identifies")
    
    # Afficher aperçu
    if new_systems:
        print("\n[*] Apercu des nouveaux systemes:")
        for i, sys in enumerate(new_systems[:15], 1):
            print(f"    {i}. {sys['protein_name']} | DOI: {sys.get('doi', 'N/A')} | Source: {sys.get('source')}")
        if len(new_systems) > 15:
            print(f"    ... et {len(new_systems)-15} autres")
    
    return new_systems

def add_systems_to_atlas(new_systems):
    """Ajoute les nouveaux systèmes à l'atlas."""
    if not new_systems:
        print("[INFO] Aucun nouveau systeme a ajouter")
        return 0
    
    df, _, _ = get_current_atlas()
    
    # Générer SystemID
    existing_ids = df['SystemID'].tolist()
    existing_nums = []
    for sid in existing_ids:
        if isinstance(sid, str) and sid.startswith('FP_'):
            try:
                num = int(sid.split('_')[1])
                existing_nums.append(num)
            except:
                pass
    
    next_id = max(existing_nums) + 1 if existing_nums else 400
    
    # Préparer nouvelles lignes
    new_rows = []
    for sys in new_systems:
        row = {
            'SystemID': f'FP_{next_id:04d}',
            'protein_name': sys['protein_name'],
            'doi': sys.get('doi'),
            'excitation_nm': sys.get('excitation_nm'),
            'emission_nm': sys.get('emission_nm'),
            'curator': f"api_harvest_{sys.get('source', 'unknown')}",
            'is_biosensor': 1.0,  # Conservative: assume biosensor from APIs
            'family': 'Unknown',  # To be curated manually
            'license': 'unknown',
            'source_note': f"API harvest from {sys.get('source')}"
        }
        
        new_rows.append(row)
        next_id += 1
    
    # Ajouter à l'atlas
    new_df = pd.DataFrame(new_rows)
    df_enriched = pd.concat([df, new_df], ignore_index=True)
    
    # Sauvegarder
    csv_path = Path("data/processed/atlas_fp_optical_v2_2.csv")
    df_enriched.to_csv(csv_path, index=False)
    
    print(f"\n[OK] Atlas enrichi!")
    print(f"    Avant: {len(df)} systemes")
    print(f"    Apres: {len(df_enriched)} systemes")
    print(f"    Ajoutes: {len(new_rows)} systemes")
    
    return len(new_rows)

if __name__ == "__main__":
    try:
        new_systems = fetch_new_systems()
        added = add_systems_to_atlas(new_systems)
        
        if added > 0:
            print(f"\n[SUCCESS] {added} systemes ajoutes via APIs")
            print("[*] Lancez: python scripts/validate_atlas.py")
        else:
            print("\n[INFO] Aucun nouveau systeme trouve")
        
        sys.exit(0)
        
    except Exception as e:
        print(f"\n[ERREUR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

