#!/usr/bin/env python3
"""
Build Atlas v2.1 - Fusion des sources et création du schéma final
==================================================================

Sources:
- atlas_fp_optical_v2_0.csv (baseline)
- lit_extracted_v2_1_template.csv (enrichissements + nouveaux systèmes)

Output:
- atlas_fp_optical_v2_1.csv (table finale enrichie)
- TRAINING_TABLE_v2_1.csv (contrat interface pour fp-qubit-design)
"""

import pandas as pd
import numpy as np
from pathlib import Path
import hashlib
import json

def load_sources():
    """Charge les sources de données"""
    
    # Atlas v2.0 baseline
    v2_0_path = Path("data/processed/atlas_fp_optical_v2_0.csv")
    df_v2_0 = pd.read_csv(v2_0_path)
    
    # Extractions littérature v2.1
    lit_path = Path("data/processed/lit_extracted_v2_1_template.csv")
    
    # Skip comment lines and read
    with open(lit_path, 'r', encoding='utf-8') as f:
        lines = [l for l in f if not l.strip().startswith('#')]
    
    import io
    df_lit = pd.read_csv(io.StringIO(''.join(lines)))
    
    return df_v2_0, df_lit

def normalize_contrast(value, unit):
    """Normalise contraste vers fold-change"""
    if pd.isna(value) or pd.isna(unit):
        return np.nan
    
    unit_lower = str(unit).lower()
    
    if 'fold' in unit_lower:
        return float(value)
    elif 'deltaf' in unit_lower or 'df/f' in unit_lower:
        return 1.0 + float(value)
    elif 'percent' in unit_lower or '%' in unit_lower:
        return 1.0 + float(value) / 100.0
    else:
        return float(value)  # Assume fold

def merge_sources(df_v2_0, df_lit):
    """Fusionne les sources avec déduplication"""
    
    print("\n[MERGE] Fusion des sources...")
    
    # Normaliser les noms pour matching
    df_v2_0['name_lower'] = df_v2_0['protein_name'].str.lower().str.strip()
    df_lit['name_lower'] = df_lit['protein_name'].str.lower().str.strip()
    
    # Séparer nouveaux vs enrichissements
    existing_names = set(df_v2_0['name_lower'])
    df_lit_new = df_lit[~df_lit['name_lower'].isin(existing_names)].copy()
    df_lit_enrich = df_lit[df_lit['name_lower'].isin(existing_names)].copy()
    
    print(f"  - Systèmes à enrichir: {len(df_lit_enrich)}")
    print(f"  - Nouveaux systèmes: {len(df_lit_new)}")
    
    # Enrichir systèmes existants
    for idx, row_lit in df_lit_enrich.iterrows():
        name_lower = row_lit['name_lower']
        
        # Trouver dans v2.0
        mask = df_v2_0['name_lower'] == name_lower
        v2_idx = df_v2_0[mask].index
        
        if len(v2_idx) > 0:
            v2_idx = v2_idx[0]
            
            # Mettre à jour contrast si manquant
            if pd.isna(df_v2_0.at[v2_idx, 'contrast_value']):
                df_v2_0.at[v2_idx, 'contrast_value'] = row_lit['contrast_value']
                df_v2_0.at[v2_idx, 'contrast_unit'] = row_lit['contrast_unit']
                
                # Normaliser
                norm = normalize_contrast(row_lit['contrast_value'], row_lit['contrast_unit'])
                df_v2_0.at[v2_idx, 'contrast_normalized'] = norm
            
            # Mettre à jour DOI si manquant
            if pd.isna(df_v2_0.at[v2_idx, 'doi']) and pd.notna(row_lit['doi']):
                df_v2_0.at[v2_idx, 'doi'] = row_lit['doi']
            
            # Ajouter source_note
            if pd.notna(row_lit.get('source_note')):
                df_v2_0.at[v2_idx, 'source_note'] = row_lit['source_note']
    
    # Préparer nouveaux systèmes au format v2.0
    df_new_mapped = []
    
    for idx, row_lit in df_lit_new.iterrows():
        # Générer SystemID
        system_id = f"FP_{len(df_v2_0) + len(df_new_mapped) + 1:04d}"
        
        # Normaliser contrast
        norm = normalize_contrast(row_lit['contrast_value'], row_lit['contrast_unit'])
        
        new_row = {
            'SystemID': system_id,
            'protein_name': row_lit['protein_name'],
            'family': row_lit['family'],
            'is_biosensor': row_lit.get('is_biosensor', 1.0),
            'contrast_value': row_lit['contrast_value'],
            'contrast_unit': row_lit['contrast_unit'],
            'contrast_normalized': norm,
            'quality_tier': row_lit.get('quality_tier', 'B'),
            'context': row_lit.get('context', ''),
            'temperature_K': row_lit.get('temperature_K'),
            'pH': row_lit.get('pH'),
            'doi': row_lit.get('doi'),
            'license': 'CC BY',  # Assumption (verifier DOI)
            'source_note': row_lit.get('source_note', ''),
            'method': row_lit.get('method', 'fluorescence'),
            'assay': 'imaging',
            'curator': 'v2.1_lit_extraction'
        }
        
        df_new_mapped.append(new_row)
    
    # Concaténer
    if df_new_mapped:
        df_new_full = pd.DataFrame(df_new_mapped)
        
        # Aligner colonnes avec v2.0
        for col in df_v2_0.columns:
            if col not in df_new_full.columns:
                df_new_full[col] = np.nan
        
        df_merged = pd.concat([df_v2_0, df_new_full[df_v2_0.columns]], ignore_index=True)
    else:
        df_merged = df_v2_0.copy()
    
    # Cleanup
    df_merged.drop('name_lower', axis=1, inplace=True, errors='ignore')
    
    return df_merged

def add_optical_fields(df):
    """Ajoute les champs optiques manquants pour v2.1"""
    
    print("\n[OPTICAL] Ajout des champs optiques...")
    
    # Template avec les valeurs connues (depuis littérature)
    optical_data = {
        # GCaMPs
        'gcamp6s': {'excitation_nm': 488, 'emission_nm': 515},
        'gcamp6f': {'excitation_nm': 488, 'emission_nm': 515},
        'gcamp6m': {'excitation_nm': 488, 'emission_nm': 515},
        'jgcamp7s': {'excitation_nm': 488, 'emission_nm': 510},
        'jgcamp7f': {'excitation_nm': 488, 'emission_nm': 510},
        'jgcamp7c': {'excitation_nm': 488, 'emission_nm': 510},
        'jgcamp7b': {'excitation_nm': 488, 'emission_nm': 510},
        'jgcamp8s': {'excitation_nm': 488, 'emission_nm': 510},
        'jgcamp8f': {'excitation_nm': 488, 'emission_nm': 510},
        'jgcamp8m': {'excitation_nm': 488, 'emission_nm': 510},
        
        # RGECOs
        'r-geco1': {'excitation_nm': 570, 'emission_nm': 600},
        'jrgeco1a': {'excitation_nm': 570, 'emission_nm': 600},
        'jrgeco1b': {'excitation_nm': 570, 'emission_nm': 600},
        'rcamp1h': {'excitation_nm': 570, 'emission_nm': 600},
        'rcamp2': {'excitation_nm': 570, 'emission_nm': 600},
        'nir-geco2': {'excitation_nm': 625, 'emission_nm': 655},
        
        # GRABs & dLights (dopamine)
        'dlight1.1': {'excitation_nm': 488, 'emission_nm': 510},
        'dlight1.2': {'excitation_nm': 488, 'emission_nm': 510},
        'dlight1.3': {'excitation_nm': 488, 'emission_nm': 510},
        'grab-da2m': {'excitation_nm': 490, 'emission_nm': 515},
        'grab-da2h': {'excitation_nm': 490, 'emission_nm': 515},
        'grab-da1h': {'excitation_nm': 490, 'emission_nm': 515},
        
        # Neurotransmitters
        'grab-ach3.0': {'excitation_nm': 488, 'emission_nm': 510},
        'iachsnfr': {'excitation_nm': 488, 'emission_nm': 515},
        'grab-5ht1.0': {'excitation_nm': 488, 'emission_nm': 510},
        'grab-ne1m': {'excitation_nm': 488, 'emission_nm': 510},
        
        # Glutamate
        'iglusnfr': {'excitation_nm': 488, 'emission_nm': 515},
        'sf-iglusnfr': {'excitation_nm': 488, 'emission_nm': 515},
        'sf-iglusnfr.a184s': {'excitation_nm': 488, 'emission_nm': 515},
        
        # Voltage
        'asap2s': {'excitation_nm': 488, 'emission_nm': 510},
        'asap3': {'excitation_nm': 488, 'emission_nm': 512},
        'ace-mneon': {'excitation_nm': 488, 'emission_nm': 516},
        'arclight': {'excitation_nm': 485, 'emission_nm': 510},
        'archon1': {'excitation_nm': 560, 'emission_nm': 590},
        'quasar2': {'excitation_nm': 640, 'emission_nm': 680},
        'vsfp-butterfly': {'excitation_nm': 440, 'emission_nm': 535},
        
        # Metabolic
        'epac-sh187': {'excitation_nm': 440, 'emission_nm': 535},
        'pinkflamindo': {'excitation_nm': 560, 'emission_nm': 580},
        'pink flamindo': {'excitation_nm': 560, 'emission_nm': 580},
        'percevalhr': {'excitation_nm': 488, 'emission_nm': 515},
        'perceval': {'excitation_nm': 488, 'emission_nm': 515},
        'caddis': {'excitation_nm': 488, 'emission_nm': 510},
        
        # H2O2/Redox
        'hyper': {'excitation_nm': 420, 'emission_nm': 516},
        'hyper3': {'excitation_nm': 420, 'emission_nm': 516},
        'hyper-7': {'excitation_nm': 420, 'emission_nm': 516},
        'rogfp2': {'excitation_nm': 488, 'emission_nm': 510},
        
        # pH
        'phluorin': {'excitation_nm': 395, 'emission_nm': 509},
        'sypher3s': {'excitation_nm': 420, 'emission_nm': 516},
        
        # FPs classiques
        'egfp': {'excitation_nm': 488, 'emission_nm': 509},
        'gfp': {'excitation_nm': 488, 'emission_nm': 509},
        'mcherry': {'excitation_nm': 587, 'emission_nm': 610},
        'mscarlet': {'excitation_nm': 569, 'emission_nm': 594},
        'morange2': {'excitation_nm': 549, 'emission_nm': 565},
        'fusionred': {'excitation_nm': 580, 'emission_nm': 608},
        'mneongreen': {'excitation_nm': 506, 'emission_nm': 517},
        'clover': {'excitation_nm': 505, 'emission_nm': 515},
        'dsred2': {'excitation_nm': 558, 'emission_nm': 583},
        'ecfp': {'excitation_nm': 433, 'emission_nm': 475},
        'tagbfp2': {'excitation_nm': 402, 'emission_nm': 457},
        'tagrfp': {'excitation_nm': 555, 'emission_nm': 584},
    }
    
    # Ajouter les colonnes si elles n'existent pas
    if 'excitation_nm' not in df.columns:
        df['excitation_nm'] = np.nan
    if 'emission_nm' not in df.columns:
        df['emission_nm'] = np.nan
    if 'stokes_shift_nm' not in df.columns:
        df['stokes_shift_nm'] = np.nan
    
    # Remplir les valeurs
    for idx, row in df.iterrows():
        name_key = str(row['protein_name']).lower().strip()
        
        if name_key in optical_data:
            df.at[idx, 'excitation_nm'] = optical_data[name_key]['excitation_nm']
            df.at[idx, 'emission_nm'] = optical_data[name_key]['emission_nm']
    
    # Calculer Stokes shift
    df['stokes_shift_nm'] = df['emission_nm'] - df['excitation_nm']
    
    # Ajouter flags de manquance
    df['excitation_missing'] = df['excitation_nm'].isna()
    df['emission_missing'] = df['emission_nm'].isna()
    df['contrast_missing'] = df['contrast_normalized'].isna()
    
    return df

def build_training_table(df):
    """Construit la table d'entraînement pour fp-qubit-design"""
    
    print("\n[TRAINING] Construction TRAINING_TABLE_v2_1.csv...")
    
    # Schéma du contrat d'interface
    training_cols = [
        'canonical_name',
        'family',
        'excitation_nm',
        'emission_nm',
        'stokes_shift_nm',
        'method',
        'context_type',
        'contrast_normalized',
        'source',
        'provenance',
        'license',
        'excitation_missing',
        'emission_missing',
        'contrast_missing'
    ]
    
    # Mapper colonnes
    df_train = pd.DataFrame()
    df_train['canonical_name'] = df['protein_name']
    df_train['family'] = df['family']
    df_train['excitation_nm'] = df['excitation_nm']
    df_train['emission_nm'] = df['emission_nm']
    df_train['stokes_shift_nm'] = df['stokes_shift_nm']
    df_train['method'] = df.get('method', 'fluorescence')
    df_train['context_type'] = df.get('context', '')
    df_train['contrast_normalized'] = df['contrast_normalized']
    df_train['source'] = 'Atlas_v2.1'
    df_train['provenance'] = df.get('doi', '')
    df_train['license'] = df.get('license', 'CC BY')
    df_train['excitation_missing'] = df['excitation_missing']
    df_train['emission_missing'] = df['emission_missing']
    df_train['contrast_missing'] = df['contrast_missing']
    
    # Filtrer systèmes utiles (mesurés)
    df_useful = df_train[df_train['contrast_normalized'].notna()].copy()
    
    return df_useful

def generate_metadata(df_full, df_training):
    """Génère les fichiers de métadonnées"""
    
    print("\n[METADATA] Génération des métadonnées...")
    
    n_total = len(df_full)
    n_measured = df_full['contrast_normalized'].notna().sum()
    n_useful = len(df_training)
    
    families = df_training['family'].value_counts()
    
    metadata = {
        "version": "2.1.0",
        "date_created": pd.Timestamp.now().isoformat(),
        "schema_version": "2.1",
        "N_total": int(n_total),
        "N_measured": int(n_measured),
        "N_useful": int(n_useful),
        "N_families": int(df_training['family'].nunique()),
        "families": families.to_dict(),
        "sources": ["Atlas_v2.0", "Literature_v2.1"],
        "license": "CC BY 4.0",
        "citation": "Biological Qubits Atlas v2.1 (2025)",
        "contract_interface": {
            "consumer": "fp-qubit-design",
            "guaranteed_columns": [
                "canonical_name", "family", "excitation_nm", "emission_nm",
                "stokes_shift_nm", "method", "context_type", "contrast_normalized",
                "source", "provenance", "license", "excitation_missing",
                "emission_missing", "contrast_missing"
            ],
            "stability": "Stable - No breaking changes without major version bump"
        }
    }
    
    return metadata

def main():
    """Main pipeline"""
    
    print("=" * 80)
    print("BUILD ATLAS v2.1 - Pipeline d'enrichissement")
    print("=" * 80)
    
    # Load
    print("\n[LOAD] Chargement des sources...")
    df_v2_0, df_lit = load_sources()
    print(f"  - Atlas v2.0: {len(df_v2_0)} systèmes")
    print(f"  - Littérature v2.1: {len(df_lit)} systèmes")
    
    # Merge
    df_merged = merge_sources(df_v2_0, df_lit)
    print(f"\n[RESULT] Total après fusion: {len(df_merged)} systèmes")
    
    # Add optical fields
    df_merged = add_optical_fields(df_merged)
    
    # Build training table
    df_training = build_training_table(df_merged)
    
    # Generate metadata
    metadata = generate_metadata(df_merged, df_training)
    
    # Stats
    print("\n" + "=" * 80)
    print("STATISTIQUES v2.1")
    print("=" * 80)
    print(f"  Total systèmes: {metadata['N_total']}")
    print(f"  Systèmes mesurés: {metadata['N_measured']}")
    print(f"  Systèmes utiles: {metadata['N_useful']}")
    print(f"  Familles: {metadata['N_families']}")
    print(f"\n  Top families:")
    for family, count in list(metadata['families'].items())[:10]:
        print(f"    {family:20s}: {count}")
    
    # Save
    print("\n[SAVE] Sauvegarde des fichiers...")
    
    output_full = Path("data/processed/atlas_fp_optical_v2_1.csv")
    df_merged.to_csv(output_full, index=False)
    print(f"  - {output_full}")
    
    output_training = Path("data/processed/TRAINING_TABLE_v2_1.csv")
    df_training.to_csv(output_training, index=False)
    print(f"  - {output_training}")
    
    output_metadata = Path("data/processed/TRAINING.METADATA_v2_1.json")
    with open(output_metadata, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"  - {output_metadata}")
    
    # Measured metadata
    measured_meta = {
        "version": "2.1.0",
        "N_measured": int(metadata['N_measured']),
        "coverage_excitation": float((~df_training['excitation_missing']).sum() / len(df_training)),
        "coverage_emission": float((~df_training['emission_missing']).sum() / len(df_training)),
        "coverage_contrast": float((~df_training['contrast_missing']).sum() / len(df_training))
    }
    
    output_measured = Path("data/processed/TRAIN_MEASURED.METADATA_v2_1.json")
    with open(output_measured, 'w', encoding='utf-8') as f:
        json.dump(measured_meta, f, indent=2)
    print(f"  - {output_measured}")
    
    print("\n" + "=" * 80)
    print("BUILD COMPLETE")
    print("=" * 80)
    
    return metadata

if __name__ == "__main__":
    result = main()

