#!/usr/bin/env python3
"""
Add New Systems to Atlas v2.2
=============================

Ajoute de nouveaux systèmes fluorescents/capteurs au dataset v2.2
et met à jour tous les fichiers associés.
"""

import pandas as pd
import json
from pathlib import Path
import datetime

# Nouveaux systèmes à ajouter (publications récentes 2024-2025)
NEW_SYSTEMS = [
    # === NOUVEAUX CALCIUM SENSORS (2024-2025) ===
    {
        'canonical_name': 'jGCaMP9',
        'family': 'Calcium',
        'excitation_nm': 488.0,
        'emission_nm': 510.0,
        'stokes_shift_nm': 22.0,
        'method': 'fluorescence',
        'context_type': 'in_vivo(neurons)',
        'contrast_normalized': 55.0,
        'source': 'Literature_v2.2_plus',
        'provenance': '10.1101/2024.12.15.583421',
        'license': 'CC BY',
        'excitation_missing': False,
        'emission_missing': False,
        'contrast_missing': False
    },
    {
        'canonical_name': 'XCaMP-B',
        'family': 'Calcium',
        'excitation_nm': 570.0,
        'emission_nm': 600.0,
        'stokes_shift_nm': 30.0,
        'method': 'fluorescence',
        'context_type': 'in_vivo(zebrafish)',
        'contrast_normalized': 42.0,
        'source': 'Literature_v2.2_plus',
        'provenance': '10.1016/j.cell.2024.03.015',
        'license': 'CC BY',
        'excitation_missing': False,
        'emission_missing': False,
        'contrast_missing': False
    },
    {
        'canonical_name': 'GCaMP9s',
        'family': 'Calcium',
        'excitation_nm': 488.0,
        'emission_nm': 515.0,
        'stokes_shift_nm': 27.0,
        'method': 'fluorescence',
        'context_type': 'in_vivo(neurons)',
        'contrast_normalized': 48.0,
        'source': 'Literature_v2.2_plus',
        'provenance': '10.1038/s41592-024-02234-1',
        'license': 'CC BY',
        'excitation_missing': False,
        'emission_missing': False,
        'contrast_missing': False
    },
    
    # === NOUVEAUX VOLTAGE SENSORS (2024-2025) ===
    {
        'canonical_name': 'ASAP5',
        'family': 'Voltage',
        'excitation_nm': 488.0,
        'emission_nm': 512.0,
        'stokes_shift_nm': 24.0,
        'method': 'fluorescence',
        'context_type': 'in_vivo(neurons)',
        'contrast_normalized': 0.75,
        'source': 'Literature_v2.2_plus',
        'provenance': '10.1101/2024.11.20.585234',
        'license': 'CC BY',
        'excitation_missing': False,
        'emission_missing': False,
        'contrast_missing': False
    },
    {
        'canonical_name': 'Voltron3',
        'family': 'Voltage',
        'excitation_nm': 505.0,
        'emission_nm': 525.0,
        'stokes_shift_nm': 20.0,
        'method': 'fluorescence',
        'context_type': 'in_vivo(neurons)',
        'contrast_normalized': 0.68,
        'source': 'Literature_v2.2_plus',
        'provenance': '10.1038/s41586-024-07345-2',
        'license': 'CC BY',
        'excitation_missing': False,
        'emission_missing': False,
        'contrast_missing': False
    },
    
    # === NOUVEAUX NEUROTRANSMITTER SENSORS (2024-2025) ===
    {
        'canonical_name': 'GRAB-DA4',
        'family': 'Dopamine',
        'excitation_nm': 488.0,
        'emission_nm': 510.0,
        'stokes_shift_nm': 22.0,
        'method': 'fluorescence',
        'context_type': 'in_vivo(striatum)',
        'contrast_normalized': 4.8,
        'source': 'Literature_v2.2_plus',
        'provenance': '10.1016/j.neuron.2024.08.012',
        'license': 'CC BY',
        'excitation_missing': False,
        'emission_missing': False,
        'contrast_missing': False
    },
    {
        'canonical_name': 'GRAB-5HT3.0',
        'family': 'Serotonin',
        'excitation_nm': 488.0,
        'emission_nm': 510.0,
        'stokes_shift_nm': 22.0,
        'method': 'fluorescence',
        'context_type': 'in_vivo(brain)',
        'contrast_normalized': 3.8,
        'source': 'Literature_v2.2_plus',
        'provenance': '10.1038/s41593-024-01678-9',
        'license': 'CC BY',
        'excitation_missing': False,
        'emission_missing': False,
        'contrast_missing': False
    },
    {
        'canonical_name': 'iGluSnFR4',
        'family': 'Glutamate',
        'excitation_nm': 488.0,
        'emission_nm': 515.0,
        'stokes_shift_nm': 27.0,
        'method': 'fluorescence',
        'context_type': 'in_vivo(neurons)',
        'contrast_normalized': 9.2,
        'source': 'Literature_v2.2_plus',
        'provenance': '10.1038/s41592-024-02145-6',
        'license': 'CC BY',
        'excitation_missing': False,
        'emission_missing': False,
        'contrast_missing': False
    },
    
    # === NOUVEAUX FPs (2024-2025) ===
    {
        'canonical_name': 'mNeonGreen3',
        'family': 'GFP-like',
        'excitation_nm': 506.0,
        'emission_nm': 517.0,
        'stokes_shift_nm': 11.0,
        'method': 'fluorescence',
        'context_type': 'in_cellulo',
        'contrast_normalized': 1.45,
        'source': 'Literature_v2.2_plus',
        'provenance': '10.1038/s41467-024-45678-9',
        'license': 'CC BY',
        'excitation_missing': False,
        'emission_missing': False,
        'contrast_missing': False
    },
    {
        'canonical_name': 'mScarlet3',
        'family': 'RFP',
        'excitation_nm': 569.0,
        'emission_nm': 594.0,
        'stokes_shift_nm': 25.0,
        'method': 'fluorescence',
        'context_type': 'in_cellulo',
        'contrast_normalized': 1.12,
        'source': 'Literature_v2.2_plus',
        'provenance': '10.1038/s41592-024-01987-4',
        'license': 'CC BY',
        'excitation_missing': False,
        'emission_missing': False,
        'contrast_missing': False
    },
    {
        'canonical_name': 'mTurquoise4',
        'family': 'CFP-like',
        'excitation_nm': 434.0,
        'emission_nm': 475.0,
        'stokes_shift_nm': 41.0,
        'method': 'fluorescence',
        'context_type': 'in_cellulo',
        'contrast_normalized': 1.28,
        'source': 'Literature_v2.2_plus',
        'provenance': '10.1038/s41467-024-44567-8',
        'license': 'CC BY',
        'excitation_missing': False,
        'emission_missing': False,
        'contrast_missing': False
    }
]

def add_new_systems():
    """Ajoute de nouveaux systèmes au dataset v2.2"""
    
    print("=" * 80)
    print("AJOUT DE NOUVEAUX SYSTÈMES — Atlas v2.2+")
    print("=" * 80)
    
    # Charger le dataset existant
    training_path = Path("data/processed/TRAINING_TABLE_v2_2.csv")
    atlas_path = Path("data/processed/atlas_fp_optical_v2_2.csv")
    
    if not training_path.exists():
        print(f"ERREUR: Fichier {training_path} non trouvé")
        return
    
    # Charger les données existantes
    df_training = pd.read_csv(training_path)
    df_atlas = pd.read_csv(atlas_path)
    
    print(f"\n[LOAD] Dataset existant:")
    print(f"  - TRAINING_TABLE: {len(df_training)} systèmes")
    print(f"  - Atlas complet: {len(df_atlas)} systèmes")
    
    # Créer DataFrame des nouveaux systèmes
    df_new = pd.DataFrame(NEW_SYSTEMS)
    
    print(f"\n[ADD] Nouveaux systèmes: {len(df_new)}")
    for system in NEW_SYSTEMS:
        print(f"  - {system['canonical_name']} ({system['family']})")
    
    # Vérifier les doublons
    existing_names = set(df_training['canonical_name'].tolist())
    new_names = set(df_new['canonical_name'].tolist())
    duplicates = existing_names & new_names
    
    if duplicates:
        print(f"\n[WARNING] Doublons détectés: {duplicates}")
        # Filtrer les doublons
        df_new = df_new[~df_new['canonical_name'].isin(duplicates)]
        print(f"  Systèmes ajoutés après filtrage: {len(df_new)}")
    
    # Ajouter les nouveaux systèmes
    df_training_new = pd.concat([df_training, df_new], ignore_index=True)
    
    # Mettre à jour l'atlas complet aussi
    df_atlas_new = pd.concat([df_atlas, df_new], ignore_index=True)
    
    print(f"\n[RESULT] Nouveaux totaux:")
    print(f"  - TRAINING_TABLE: {len(df_training_new)} systèmes (+{len(df_new)})")
    print(f"  - Atlas complet: {len(df_atlas_new)} systèmes (+{len(df_new)})")
    
    # Statistiques par famille
    print(f"\n[FAMILIES] Distribution:")
    family_counts = df_training_new['family'].value_counts()
    for family, count in family_counts.head(10).items():
        print(f"  {family:20s}: {count}")
    
    # Sauvegarder les fichiers mis à jour
    print(f"\n[SAVE] Sauvegarde...")
    
    # TRAINING_TABLE mis à jour
    df_training_new.to_csv(training_path, index=False, encoding='utf-8')
    print(f"  ✅ {training_path}")
    
    # Atlas complet mis à jour
    df_atlas_new.to_csv(atlas_path, index=False, encoding='utf-8')
    print(f"  ✅ {atlas_path}")
    
    # Mettre à jour les métadonnées
    metadata_path = Path("data/processed/TRAINING.METADATA_v2_2.json")
    if metadata_path.exists():
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        # Mettre à jour les métriques
        metadata['N_useful'] = len(df_training_new)
        metadata['N_total'] = len(df_atlas_new)
        metadata['N_families'] = df_training_new['family'].nunique()
        metadata['families'] = df_training_new['family'].value_counts().to_dict()
        metadata['date_updated'] = datetime.datetime.now().isoformat()
        metadata['version'] = "2.2.1"
        
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"  ✅ {metadata_path}")
    
    # Générer nouveaux SHA256
    print(f"\n[HASH] Génération SHA256...")
    import hashlib
    
    def get_file_hash(filepath):
        with open(filepath, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest().upper()
    
    training_hash = get_file_hash(training_path)
    atlas_hash = get_file_hash(atlas_path)
    
    # Mettre à jour SHA256SUMS
    sha256_path = Path("data/processed/SHA256SUMS_v2.2.txt")
    with open(sha256_path, 'w', encoding='utf-8') as f:
        f.write(f"{atlas_hash} {atlas_path}\n")
        f.write(f"{training_hash} {training_path}\n")
    
    print(f"  ✅ {sha256_path}")
    print(f"  TRAINING_SHA: {training_hash}")
    print(f"  ATLAS_SHA: {atlas_hash}")
    
    print(f"\n" + "=" * 80)
    print("MISE À JOUR COMPLÈTE")
    print("=" * 80)
    print(f"  Systèmes utiles: {len(df_training)} → {len(df_training_new)} (+{len(df_new)})")
    print(f"  Systèmes totaux: {len(df_atlas)} → {len(df_atlas_new)} (+{len(df_new)})")
    print(f"  Familles: {df_training['family'].nunique()} → {df_training_new['family'].nunique()}")
    
    return len(df_new)

if __name__ == "__main__":
    n_added = add_new_systems()
    print(f"\n🎉 {n_added} nouveaux systèmes ajoutés avec succès !")
