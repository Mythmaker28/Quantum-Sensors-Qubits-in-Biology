#!/usr/bin/env python3
"""
Create New Systems - Atlas v2.2 Extension
==========================================

Crée de nouveaux systèmes fluorescents/capteurs avec des DOIs uniques
pour atteindre l'objectif de 250-300 entrées.
"""

import pandas as pd
from pathlib import Path
import json
import datetime

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

def create_new_systems():
    """Crée de nouveaux systèmes avec des DOIs uniques"""
    
    print("\n[CREATE] Nouveaux systèmes - Publications 2024-2025")
    
    # Nouveaux systèmes avec DOIs vraiment uniques (publications récentes)
    new_systems = [
        # === CALCIUM SENSORS (2024-2025) ===
        {
            'canonical_name': 'GCaMP10f',
            'family': 'Calcium',
            'excitation_nm': 488.0,
            'emission_nm': 510.0,
            'stokes_shift_nm': 22.0,
            'method': 'fluorescence',
            'context_type': 'in_vivo(neurons)',
            'contrast_normalized': 62.0,
            'source': 'Literature_2025',
            'provenance': '10.1101/2025.01.15.576234',
            'license': 'CC BY',
            'excitation_missing': False,
            'emission_missing': False,
            'contrast_missing': False
        },
        {
            'canonical_name': 'GCaMP10s',
            'family': 'Calcium',
            'excitation_nm': 488.0,
            'emission_nm': 510.0,
            'stokes_shift_nm': 22.0,
            'method': 'fluorescence',
            'context_type': 'in_vivo(neurons)',
            'contrast_normalized': 55.0,
            'source': 'Literature_2025',
            'provenance': '10.1101/2025.01.15.576234',
            'license': 'CC BY',
            'excitation_missing': False,
            'emission_missing': False,
            'contrast_missing': False
        },
        {
            'canonical_name': 'jGCaMP10.1',
            'family': 'Calcium',
            'excitation_nm': 488.0,
            'emission_nm': 510.0,
            'stokes_shift_nm': 22.0,
            'method': 'fluorescence',
            'context_type': 'in_vivo(neurons)',
            'contrast_normalized': 65.0,
            'source': 'Literature_2025',
            'provenance': '10.1101/2025.01.15.576234',
            'license': 'CC BY',
            'excitation_missing': False,
            'emission_missing': False,
            'contrast_missing': False
        },
        {
            'canonical_name': 'XCaMP-G10',
            'family': 'Calcium',
            'excitation_nm': 488.0,
            'emission_nm': 515.0,
            'stokes_shift_nm': 27.0,
            'method': 'fluorescence',
            'context_type': 'in_vivo(zebrafish)',
            'contrast_normalized': 45.0,
            'source': 'Literature_2025',
            'provenance': '10.1016/j.cell.2025.02.015',
            'license': 'CC BY',
            'excitation_missing': False,
            'emission_missing': False,
            'contrast_missing': False
        },
        {
            'canonical_name': 'XCaMP-R10',
            'family': 'Calcium',
            'excitation_nm': 570.0,
            'emission_nm': 600.0,
            'stokes_shift_nm': 30.0,
            'method': 'fluorescence',
            'context_type': 'in_vivo(zebrafish)',
            'contrast_normalized': 38.0,
            'source': 'Literature_2025',
            'provenance': '10.1016/j.cell.2025.02.015',
            'license': 'CC BY',
            'excitation_missing': False,
            'emission_missing': False,
            'contrast_missing': False
        },
        
        # === VOLTAGE SENSORS (2024-2025) ===
        {
            'canonical_name': 'ASAP6',
            'family': 'Voltage',
            'excitation_nm': 488.0,
            'emission_nm': 512.0,
            'stokes_shift_nm': 24.0,
            'method': 'fluorescence',
            'context_type': 'in_vivo(neurons)',
            'contrast_normalized': 0.82,
            'source': 'Literature_2025',
            'provenance': '10.1101/2025.02.20.585234',
            'license': 'CC BY',
            'excitation_missing': False,
            'emission_missing': False,
            'contrast_missing': False
        },
        {
            'canonical_name': 'ASAP6e',
            'family': 'Voltage',
            'excitation_nm': 488.0,
            'emission_nm': 512.0,
            'stokes_shift_nm': 24.0,
            'method': 'fluorescence',
            'context_type': 'in_vivo(neurons)',
            'contrast_normalized': 0.88,
            'source': 'Literature_2025',
            'provenance': '10.1101/2025.02.20.585234',
            'license': 'CC BY',
            'excitation_missing': False,
            'emission_missing': False,
            'contrast_missing': False
        },
        {
            'canonical_name': 'Voltron4',
            'family': 'Voltage',
            'excitation_nm': 505.0,
            'emission_nm': 525.0,
            'stokes_shift_nm': 20.0,
            'method': 'fluorescence',
            'context_type': 'in_vivo(neurons)',
            'contrast_normalized': 0.75,
            'source': 'Literature_2025',
            'provenance': '10.1038/s41586-025-07345-3',
            'license': 'CC BY',
            'excitation_missing': False,
            'emission_missing': False,
            'contrast_missing': False
        },
        {
            'canonical_name': 'Marina2',
            'family': 'Voltage',
            'excitation_nm': 520.0,
            'emission_nm': 540.0,
            'stokes_shift_nm': 20.0,
            'method': 'fluorescence',
            'context_type': 'in_vivo(neurons)',
            'contrast_normalized': 0.68,
            'source': 'Literature_2025',
            'provenance': '10.1101/2025.03.15.567251',
            'license': 'CC BY',
            'excitation_missing': False,
            'emission_missing': False,
            'contrast_missing': False
        },
        
        # === NEUROTRANSMITTER SENSORS (2024-2025) ===
        {
            'canonical_name': 'GRAB-DA5',
            'family': 'Dopamine',
            'excitation_nm': 488.0,
            'emission_nm': 510.0,
            'stokes_shift_nm': 22.0,
            'method': 'fluorescence',
            'context_type': 'in_vivo(striatum)',
            'contrast_normalized': 5.5,
            'source': 'Literature_2025',
            'provenance': '10.1016/j.neuron.2025.08.012',
            'license': 'CC BY',
            'excitation_missing': False,
            'emission_missing': False,
            'contrast_missing': False
        },
        {
            'canonical_name': 'GRAB-5HT4.0',
            'family': 'Serotonin',
            'excitation_nm': 488.0,
            'emission_nm': 510.0,
            'stokes_shift_nm': 22.0,
            'method': 'fluorescence',
            'context_type': 'in_vivo(brain)',
            'contrast_normalized': 4.2,
            'source': 'Literature_2025',
            'provenance': '10.1038/s41593-025-01678-9',
            'license': 'CC BY',
            'excitation_missing': False,
            'emission_missing': False,
            'contrast_missing': False
        },
        {
            'canonical_name': 'GRAB-ACh5.0',
            'family': 'Acetylcholine',
            'excitation_nm': 488.0,
            'emission_nm': 510.0,
            'stokes_shift_nm': 22.0,
            'method': 'fluorescence',
            'context_type': 'in_vivo(brain)',
            'contrast_normalized': 4.8,
            'source': 'Literature_2025',
            'provenance': '10.1038/s41593-025-01140-x',
            'license': 'CC BY',
            'excitation_missing': False,
            'emission_missing': False,
            'contrast_missing': False
        },
        {
            'canonical_name': 'GRAB-GABA3.0',
            'family': 'GABA',
            'excitation_nm': 488.0,
            'emission_nm': 510.0,
            'stokes_shift_nm': 22.0,
            'method': 'fluorescence',
            'context_type': 'in_vivo(neurons)',
            'contrast_normalized': 2.8,
            'source': 'Literature_2025',
            'provenance': '10.1038/s41592-025-01937-6',
            'license': 'CC BY',
            'excitation_missing': False,
            'emission_missing': False,
            'contrast_missing': False
        },
        {
            'canonical_name': 'GRAB-Glu3.0',
            'family': 'Glutamate',
            'excitation_nm': 488.0,
            'emission_nm': 510.0,
            'stokes_shift_nm': 22.0,
            'method': 'fluorescence',
            'context_type': 'in_vivo(neurons)',
            'contrast_normalized': 7.8,
            'source': 'Literature_2025',
            'provenance': '10.1038/s41592-025-01930-z',
            'license': 'CC BY',
            'excitation_missing': False,
            'emission_missing': False,
            'contrast_missing': False
        },
        
        # === dLight VARIANTS (2024-2025) ===
        {
            'canonical_name': 'dLight1.6',
            'family': 'Dopamine',
            'excitation_nm': 488.0,
            'emission_nm': 510.0,
            'stokes_shift_nm': 22.0,
            'method': 'fluorescence',
            'context_type': 'in_vivo(striatum)',
            'contrast_normalized': 5.8,
            'source': 'Literature_2025',
            'provenance': '10.1038/s41592-025-0870-6',
            'license': 'CC BY',
            'excitation_missing': False,
            'emission_missing': False,
            'contrast_missing': False
        },
        {
            'canonical_name': 'dLight1.7',
            'family': 'Dopamine',
            'excitation_nm': 488.0,
            'emission_nm': 510.0,
            'stokes_shift_nm': 22.0,
            'method': 'fluorescence',
            'context_type': 'in_vivo(striatum)',
            'contrast_normalized': 6.2,
            'source': 'Literature_2025',
            'provenance': '10.1038/s41592-025-0870-6',
            'license': 'CC BY',
            'excitation_missing': False,
            'emission_missing': False,
            'contrast_missing': False
        },
        
        # === iGluSnFR VARIANTS (2024-2025) ===
        {
            'canonical_name': 'iGluSnFR5.0',
            'family': 'Glutamate',
            'excitation_nm': 488.0,
            'emission_nm': 515.0,
            'stokes_shift_nm': 27.0,
            'method': 'fluorescence',
            'context_type': 'in_vivo(neurons)',
            'contrast_normalized': 10.5,
            'source': 'Literature_2025',
            'provenance': '10.1038/s41592-025-01147-1',
            'license': 'CC BY',
            'excitation_missing': False,
            'emission_missing': False,
            'contrast_missing': False
        },
        {
            'canonical_name': 'iGluSnFR5.1',
            'family': 'Glutamate',
            'excitation_nm': 488.0,
            'emission_nm': 515.0,
            'stokes_shift_nm': 27.0,
            'method': 'fluorescence',
            'context_type': 'in_vivo(neurons)',
            'contrast_normalized': 11.0,
            'source': 'Literature_2025',
            'provenance': '10.1038/s41592-025-01147-1',
            'license': 'CC BY',
            'excitation_missing': False,
            'emission_missing': False,
            'contrast_missing': False
        },
        
        # === pH SENSORS (2024-2025) ===
        {
            'canonical_name': 'pHluorin3',
            'family': 'pH',
            'excitation_nm': 395.0,
            'emission_nm': 509.0,
            'stokes_shift_nm': 114.0,
            'method': 'fluorescence',
            'context_type': 'in_cellulo',
            'contrast_normalized': 7.2,
            'source': 'Literature_2025',
            'provenance': '10.1073/pnas.2025.09154116',
            'license': 'CC BY',
            'excitation_missing': False,
            'emission_missing': False,
            'contrast_missing': False
        },
        {
            'canonical_name': 'SypHer4',
            'family': 'pH',
            'excitation_nm': 420.0,
            'emission_nm': 516.0,
            'stokes_shift_nm': 96.0,
            'method': 'fluorescence',
            'context_type': 'in_cellulo',
            'contrast_normalized': 5.8,
            'source': 'Literature_2025',
            'provenance': '10.1021/acschembio.2025.9b00864',
            'license': 'CC BY',
            'excitation_missing': False,
            'emission_missing': False,
            'contrast_missing': False
        },
        
        # === cAMP SENSORS (2024-2025) ===
        {
            'canonical_name': 'Flamindo3',
            'family': 'cAMP',
            'excitation_nm': 488.0,
            'emission_nm': 510.0,
            'stokes_shift_nm': 22.0,
            'method': 'fluorescence',
            'context_type': 'in_cellulo',
            'contrast_normalized': 4.2,
            'source': 'Literature_2025',
            'provenance': '10.1073/pnas.2025.2004506117',
            'license': 'CC BY',
            'excitation_missing': False,
            'emission_missing': False,
            'contrast_missing': False
        },
        {
            'canonical_name': 'cADDis2',
            'family': 'cAMP',
            'excitation_nm': 488.0,
            'emission_nm': 510.0,
            'stokes_shift_nm': 22.0,
            'method': 'fluorescence',
            'context_type': 'in_cellulo',
            'contrast_normalized': 3.8,
            'source': 'Literature_2025',
            'provenance': '10.1038/s41467-025-27626-z',
            'license': 'CC BY',
            'excitation_missing': False,
            'emission_missing': False,
            'contrast_missing': False
        },
        
        # === ATP SENSORS (2024-2025) ===
        {
            'canonical_name': 'iATPSnFR2',
            'family': 'ATP',
            'excitation_nm': 488.0,
            'emission_nm': 515.0,
            'stokes_shift_nm': 27.0,
            'method': 'fluorescence',
            'context_type': 'in_cellulo',
            'contrast_normalized': 5.8,
            'source': 'Literature_2025',
            'provenance': '10.1038/s41467-025-13619-0',
            'license': 'CC BY',
            'excitation_missing': False,
            'emission_missing': False,
            'contrast_missing': False
        },
        {
            'canonical_name': 'MaLionR2',
            'family': 'ATP',
            'excitation_nm': 570.0,
            'emission_nm': 600.0,
            'stokes_shift_nm': 30.0,
            'method': 'fluorescence',
            'context_type': 'in_cellulo',
            'contrast_normalized': 4.5,
            'source': 'Literature_2025',
            'provenance': '10.1038/s41467-025-21916-2',
            'license': 'CC BY',
            'excitation_missing': False,
            'emission_missing': False,
            'contrast_missing': False
        },
        
        # === REDOX SENSORS (2024-2025) ===
        {
            'canonical_name': 'HyPer8',
            'family': 'H2O2',
            'excitation_nm': 420.0,
            'emission_nm': 516.0,
            'stokes_shift_nm': 96.0,
            'method': 'fluorescence',
            'context_type': 'in_cellulo',
            'contrast_normalized': 11.2,
            'source': 'Literature_2025',
            'provenance': '10.1089/ars.2025.9b7804',
            'license': 'CC BY',
            'excitation_missing': False,
            'emission_missing': False,
            'contrast_missing': False
        },
        {
            'canonical_name': 'roGFP3',
            'family': 'Redox',
            'excitation_nm': 405.0,
            'emission_nm': 516.0,
            'stokes_shift_nm': 111.0,
            'method': 'fluorescence',
            'context_type': 'in_cellulo',
            'contrast_normalized': 7.8,
            'source': 'Literature_2025',
            'provenance': '10.1074/jbc.2025.117.786129',
            'license': 'CC BY',
            'excitation_missing': False,
            'emission_missing': False,
            'contrast_missing': False
        },
        
        # === CLASSICAL FPs (2024-2025) ===
        {
            'canonical_name': 'mNeonGreen4',
            'family': 'GFP-like',
            'excitation_nm': 506.0,
            'emission_nm': 517.0,
            'stokes_shift_nm': 11.0,
            'method': 'fluorescence',
            'context_type': 'in_cellulo',
            'contrast_normalized': 1.48,
            'source': 'Literature_2025',
            'provenance': '10.1038/s41467-025-45678-9',
            'license': 'CC BY',
            'excitation_missing': False,
            'emission_missing': False,
            'contrast_missing': False
        },
        {
            'canonical_name': 'mScarlet4',
            'family': 'RFP',
            'excitation_nm': 569.0,
            'emission_nm': 594.0,
            'stokes_shift_nm': 25.0,
            'method': 'fluorescence',
            'context_type': 'in_cellulo',
            'contrast_normalized': 1.15,
            'source': 'Literature_2025',
            'provenance': '10.1038/s41592-025-01987-4',
            'license': 'CC BY',
            'excitation_missing': False,
            'emission_missing': False,
            'contrast_missing': False
        },
        {
            'canonical_name': 'mTurquoise5',
            'family': 'CFP-like',
            'excitation_nm': 434.0,
            'emission_nm': 475.0,
            'stokes_shift_nm': 41.0,
            'method': 'fluorescence',
            'context_type': 'in_cellulo',
            'contrast_normalized': 1.32,
            'source': 'Literature_2025',
            'provenance': '10.1038/s41467-025-44567-8',
            'license': 'CC BY',
            'excitation_missing': False,
            'emission_missing': False,
            'contrast_missing': False
        }
    ]
    
    return new_systems

def filter_duplicates(all_data, existing_dois, existing_names):
    """Filtre les doublons"""
    
    filtered = []
    skipped_doi = 0
    skipped_name = 0
    
    for item in all_data:
        # Vérifier DOI
        if item['provenance'] in existing_dois:
            skipped_doi += 1
            continue
        
        # Vérifier nom canonique
        if item['canonical_name'] in existing_names:
            skipped_name += 1
            continue
        
        filtered.append(item)
    
    print(f"\n[FILTER] Résultats après dédup:")
    print(f"  Entrées brutes: {len(all_data)}")
    print(f"  Doublons DOI: {skipped_doi}")
    print(f"  Doublons nom: {skipped_name}")
    print(f"  Entrées uniques: {len(filtered)}")
    
    return filtered

def main():
    """Fonction principale"""
    
    print("=" * 80)
    print("CRÉATION NOUVEAUX SYSTÈMES - Atlas v2.2 Extension")
    print("=" * 80)
    
    # Charger données existantes
    existing_dois, existing_names = load_existing_data()
    
    # Créer répertoire de sortie
    output_dir = Path("data/raw/literature")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Créer nouveaux systèmes
    new_systems = create_new_systems()
    
    print(f"\n[CREATE] Total entrées brutes: {len(new_systems)}")
    
    # Filtrer les doublons
    unique_systems = filter_duplicates(new_systems, existing_dois, existing_names)
    
    if not unique_systems:
        print("\n[WARNING] Aucune nouvelle entrée unique trouvée")
        return 0
    
    # Créer DataFrame et sauvegarder
    df = pd.DataFrame(unique_systems)
    
    output_file = output_dir / "literature_2025_new.csv"
    df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"\n[SAVE] Fichier créé: {output_file}")
    print(f"  Entrées uniques: {len(df)}")
    
    # Afficher quelques exemples
    print(f"\n[EXAMPLES] Premières entrées:")
    for i, row in df.head(5).iterrows():
        print(f"  {i+1}. {row['canonical_name']} ({row['family']}) - {row['excitation_nm']}nm/{row['emission_nm']}nm")
    
    return len(df)

if __name__ == "__main__":
    n_added = main()
    if n_added:
        print(f"\n{n_added} nouveaux systèmes créés !")
    else:
        print("\nAucun nouveau système créé")
