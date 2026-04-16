#!/usr/bin/env python3
"""
Enrichissement de l'atlas via FPbase API - REELS systèmes seulement.

Utilise l'API REST FPbase pour trouver des biosenseurs non encore dans l'atlas.
"""
import requests
import pandas as pd
from pathlib import Path
import time
import sys

FPBASE_API_URL = "https://www.fpbase.org/api/proteins/"
MAX_CANDIDATES = 30  # Limite conservatrice

def get_current_atlas():
    """Charge l'atlas actuel."""
    csv_path = Path("data/processed/atlas_fp_optical_v2_2.csv")
    df = pd.read_csv(csv_path)
    # Normaliser les noms pour comparaison
    current_names = set(df['protein_name'].str.lower().str.strip())
    return df, current_names

def fetch_fpbase_proteins(limit=100):
    """
    Récupère des protéines depuis FPbase API.
    """
    print(f"[*] Interrogation de FPbase API: {FPBASE_API_URL}")
    
    try:
        # Paramètres: biosenseurs uniquement
        params = {
            'is_sensor': 'true',
            'limit': limit
        }
        
        response = requests.get(FPBASE_API_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        results = data.get('results', [])
        print(f"[OK] {len(results)} proteines recues de FPbase")
        return results
        
    except requests.exceptions.RequestException as e:
        print(f"[ERREUR] Impossible de contacter FPbase API: {e}")
        return None
    except Exception as e:
        print(f"[ERREUR] Erreur lors du parsing: {e}")
        return None

def extract_candidate_data(fp_data):
    """
    Extrait les données d'un candidat FPbase.
    Retourne None si données insuffisantes.
    """
    name = fp_data.get('name')
    if not name:
        return None
    
    # Vérifier données essentielles
    doi = fp_data.get('primary_reference', {}).get('doi') if fp_data.get('primary_reference') else None
    if not doi:
        return None  # Pas de DOI = pas d'inclusion
    
    # Extraire metadata
    candidate = {
        'protein_name': name,
        'family': fp_data.get('sensor_target', 'Unknown'),  # ex: Calcium, Voltage
        'is_biosensor': 1.0,
        'doi': doi,
        'excitation_nm': fp_data.get('ex_max'),
        'emission_nm': fp_data.get('em_max'),
        'curator': 'fpbase_api_v2.2.2',
        'method': 'fluorescence',
        'license': 'CC BY-SA 4.0',  # FPbase license
        'source_note': f"FPbase API - {name}"
    }
    
    # Stokes shift
    if candidate['excitation_nm'] and candidate['emission_nm']:
        candidate['stokes_shift_nm'] = candidate['emission_nm'] - candidate['excitation_nm']
    
    return candidate

def enrich_atlas():
    """
    Enrichit l'atlas avec de nouveaux systèmes depuis FPbase.
    """
    # 1. Charger atlas actuel
    df, current_names = get_current_atlas()
    initial_count = len(df)
    print(f"[*] Atlas actuel: {initial_count} systemes")
    
    # 2. Interroger FPbase
    fp_proteins = fetch_fpbase_proteins(limit=100)
    if fp_proteins is None:
        print("[ERREUR] Pas de donnees FPbase disponibles")
        return 0
    
    # 3. Filtrer et extraire candidats
    candidates = []
    print(f"\n[*] Analyse de {len(fp_proteins)} proteines FPbase...")
    
    for fp_data in fp_proteins:
        name = fp_data.get('name', '').lower().strip()
        
        # Déjà dans l'atlas ?
        if name in current_names:
            continue
        
        # Extraire données
        candidate = extract_candidate_data(fp_data)
        if candidate is None:
            continue
        
        # Vérifier si pas déjà ajouté (doublons dans FPbase)
        if any(c['protein_name'].lower() == candidate['protein_name'].lower() for c in candidates):
            continue
        
        candidates.append(candidate)
        
        if len(candidates) >= MAX_CANDIDATES:
            break
    
    print(f"[OK] {len(candidates)} nouveaux candidats identifies")
    
    if len(candidates) == 0:
        print("[INFO] Aucun nouveau systeme a ajouter")
        return 0
    
    # 4. Afficher aperçu
    print("\n[*] Apercu des nouveaux systemes:")
    for i, c in enumerate(candidates[:10], 1):
        print(f"    {i}. {c['protein_name']} ({c['family']}) - DOI: {c['doi']}")
    if len(candidates) > 10:
        print(f"    ... et {len(candidates)-10} autres")
    
    # 5. Convertir en DataFrame et fusionner
    new_df = pd.DataFrame(candidates)
    
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
    new_df['SystemID'] = [f'FP_{next_id+i:04d}' for i in range(len(new_df))]
    
    # Fusionner
    df_enriched = pd.concat([df, new_df], ignore_index=True)
    
    # 6. Sauvegarder
    csv_path = Path("data/processed/atlas_fp_optical_v2_2.csv")
    df_enriched.to_csv(csv_path, index=False)
    
    print(f"\n[OK] Atlas enrichi sauvegarde")
    print(f"    Avant: {initial_count} systemes")
    print(f"    Apres: {len(df_enriched)} systemes")
    print(f"    Ajoutes: {len(candidates)} systemes")
    
    return len(candidates)

if __name__ == "__main__":
    try:
        added = enrich_atlas()
        sys.exit(0)
    except Exception as e:
        print(f"[ERREUR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)










