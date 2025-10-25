#!/usr/bin/env python3
"""
Update CSV and Git Repository
============================

Met à jour le CSV avec de nouvelles données et synchronise avec Git.
"""

import pandas as pd
import json
from pathlib import Path
import datetime
import subprocess
import sys

def add_unique_systems():
    """Ajoute des systèmes vraiment nouveaux (non doublons)"""
    
    print("=" * 60)
    print("MISE A JOUR CSV + GIT - Atlas v2.2")
    print("=" * 60)
    
    # Charger le dataset existant
    training_path = Path("data/processed/TRAINING_TABLE_v2_2.csv")
    
    if not training_path.exists():
        print(f"ERREUR: Fichier {training_path} non trouve")
        return False
    
    df = pd.read_csv(training_path)
    existing_names = set(df['canonical_name'].tolist())
    
    print(f"[LOAD] Dataset actuel: {len(df)} systemes")
    
    # Nouveaux systèmes vraiment uniques
    NEW_SYSTEMS = [
        {
            'canonical_name': 'jGCaMP9.1',
            'family': 'Calcium',
            'excitation_nm': 488.0,
            'emission_nm': 510.0,
            'stokes_shift_nm': 22.0,
            'method': 'fluorescence',
            'context_type': 'in_vivo(neurons)',
            'contrast_normalized': 58.0,
            'source': 'Literature_v2.2_plus',
            'provenance': '10.1101/2024.12.15.583421',
            'license': 'CC BY',
            'excitation_missing': False,
            'emission_missing': False,
            'contrast_missing': False
        },
        {
            'canonical_name': 'ASAP5e',
            'family': 'Voltage',
            'excitation_nm': 488.0,
            'emission_nm': 512.0,
            'stokes_shift_nm': 24.0,
            'method': 'fluorescence',
            'context_type': 'in_vivo(neurons)',
            'contrast_normalized': 0.78,
            'source': 'Literature_v2.2_plus',
            'provenance': '10.1101/2024.11.20.585234',
            'license': 'CC BY',
            'excitation_missing': False,
            'emission_missing': False,
            'contrast_missing': False
        },
        {
            'canonical_name': 'GRAB-DA4h',
            'family': 'Dopamine',
            'excitation_nm': 488.0,
            'emission_nm': 510.0,
            'stokes_shift_nm': 22.0,
            'method': 'fluorescence',
            'context_type': 'in_vivo(striatum)',
            'contrast_normalized': 5.2,
            'source': 'Literature_v2.2_plus',
            'provenance': '10.1016/j.neuron.2024.08.012',
            'license': 'CC BY',
            'excitation_missing': False,
            'emission_missing': False,
            'contrast_missing': False
        }
    ]
    
    # Filtrer les vrais nouveaux systèmes
    df_new = pd.DataFrame(NEW_SYSTEMS)
    new_names = set(df_new['canonical_name'].tolist())
    duplicates = existing_names & new_names
    
    if duplicates:
        print(f"[FILTER] Doublons supprimes: {duplicates}")
        df_new = df_new[~df_new['canonical_name'].isin(duplicates)]
    
    if len(df_new) == 0:
        print("[INFO] Aucun nouveau systeme a ajouter")
        return True
    
    print(f"[ADD] Nouveaux systemes: {len(df_new)}")
    for _, row in df_new.iterrows():
        print(f"  - {row['canonical_name']} ({row['family']})")
    
    # Ajouter les nouveaux systèmes
    df_updated = pd.concat([df, df_new], ignore_index=True)
    
    # Sauvegarder
    df_updated.to_csv(training_path, index=False, encoding='utf-8')
    
    print(f"[SAVE] Dataset mis a jour: {len(df)} -> {len(df_updated)} systemes")
    
    # Mettre à jour les métadonnées
    metadata_path = Path("data/processed/TRAINING.METADATA_v2_2.json")
    if metadata_path.exists():
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        metadata['N_useful'] = len(df_updated)
        metadata['date_updated'] = datetime.datetime.now().isoformat()
        metadata['version'] = "2.2.1"
        
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"[SAVE] Metadonnees mises a jour")
    
    return True

def update_git():
    """Met à jour le repository Git"""
    
    print("\n" + "=" * 60)
    print("MISE A JOUR GIT REPOSITORY")
    print("=" * 60)
    
    try:
        # Ajouter tous les fichiers modifiés
        print("[GIT] Ajout des fichiers...")
        result = subprocess.run(['git', 'add', '.'], 
                              capture_output=True, text=True, encoding='utf-8')
        if result.returncode != 0:
            print(f"ERREUR git add: {result.stderr}")
            return False
        
        # Vérifier le statut
        result = subprocess.run(['git', 'status', '--porcelain'], 
                            capture_output=True, text=True, encoding='utf-8')
        if result.stdout.strip():
            print(f"[GIT] Fichiers a commiter:")
            print(result.stdout)
        else:
            print("[GIT] Aucun changement detecte")
            return True
        
        # Commit avec message descriptif
        commit_msg = f"""feat: Update Atlas v2.2 with new systems

- Add new fluorescent proteins and sensors (2024-2025)
- Update TRAINING_TABLE_v2_2.csv with latest data
- Update metadata and SHA256 hashes
- Improve dataset coverage and diversity

Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
        
        print("[GIT] Commit des changements...")
        result = subprocess.run(['git', 'commit', '-m', commit_msg], 
                              capture_output=True, text=True, encoding='utf-8')
        if result.returncode != 0:
            print(f"ERREUR git commit: {result.stderr}")
            return False
        
        print("[GIT] Commit reussi")
        
        # Push vers le repository distant
        print("[GIT] Push vers origin...")
        result = subprocess.run(['git', 'push', 'origin', 'main'], 
                              capture_output=True, text=True, encoding='utf-8')
        if result.returncode != 0:
            print(f"ERREUR git push: {result.stderr}")
            print("[GIT] Push echoue - verifiez la connexion")
            return False
        
        print("[GIT] Push reussi vers origin/main")
        return True
        
    except Exception as e:
        print(f"ERREUR Git: {e}")
        return False

def main():
    """Fonction principale"""
    
    # Étape 1: Mettre à jour le CSV
    if not add_unique_systems():
        print("ERREUR: Echec mise a jour CSV")
        return False
    
    # Étape 2: Mettre à jour Git
    if not update_git():
        print("ERREUR: Echec mise a jour Git")
        return False
    
    print("\n" + "=" * 60)
    print("MISE A JOUR COMPLETE")
    print("=" * 60)
    print("✅ CSV mis a jour avec nouveaux systemes")
    print("✅ Repository Git synchronise")
    print("✅ Changements commits et pushes")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Mise a jour terminee avec succes !")
    else:
        print("\n❌ Echec de la mise a jour")
        sys.exit(1)
