#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ETL Script: Build Atlas Tables v1.2
====================================
Construit les tables finales:
- atlas_all_real.csv (legacy complet, multi-modalité)
- atlas_fp_optical.csv (FP-like uniquement, colonnes minimales)
- TRAINING.METADATA.json (schéma + licences + provenance)

Input: data/interim/external_candidates.parquet
       biological_qubits.csv (legacy data if exists)
Output: data/processed/atlas_all_real.csv
        data/processed/atlas_fp_optical.csv
        data/processed/TRAINING.METADATA.json
"""

import sys
from pathlib import Path
import pandas as pd
import json
from datetime import datetime

# Paths
CANDIDATES_FILE = Path("data/interim/external_candidates.parquet")
LEGACY_FILE = Path("biological_qubits.csv")
OUTPUT_ALL = Path("data/processed/atlas_all_real.csv")
OUTPUT_FP = Path("data/processed/atlas_fp_optical.csv")
METADATA_FILE = Path("data/processed/TRAINING.METADATA.json")

# Colonnes minimales pour atlas_fp_optical
FP_OPTICAL_COLUMNS = [
    'SystemID', 'protein_name', 'variant', 'family', 'is_biosensor',
    'uniprot_id', 'pdb_id', 'excitation_nm', 'emission_nm', 
    'temperature_K', 'pH', 'contrast_ratio', 'contrast_ci_low', 
    'contrast_ci_high', 'contrast_source', 'condition_text', 
    'source_refs', 'license_source'
]

def load_legacy() -> pd.DataFrame:
    """Charge les données legacy si elles existent."""
    if not LEGACY_FILE.exists():
        print("No legacy data found")
        return pd.DataFrame()
    
    try:
        df = pd.read_csv(LEGACY_FILE)
        print(f"Loaded {len(df)} legacy entries")
        return df
    except Exception as e:
        print(f"WARNING: Could not load legacy data: {e}", file=sys.stderr)
        return pd.DataFrame()

def normalize_candidates(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise les candidats vers le schéma standard."""
    
    # Créer les colonnes manquantes avec valeurs par défaut
    normalized = df.copy()
    
    # Ensure all required columns exist
    for col in FP_OPTICAL_COLUMNS:
        if col not in normalized.columns:
            normalized[col] = None
    
    # Map existing columns
    if 'protein_name' not in normalized.columns and 'name' in normalized.columns:
        normalized['protein_name'] = normalized['name']
    
    # Set defaults
    if 'variant' not in normalized.columns:
        normalized['variant'] = 'wild-type'
    
    if 'temperature_K' not in normalized.columns:
        normalized['temperature_K'] = 298.15  # Room temp default
    
    if 'pH' not in normalized.columns:
        normalized['pH'] = 7.4  # Physiological default
    
    # Ensure is_biosensor is int
    if 'is_biosensor' in normalized.columns:
        normalized['is_biosensor'] = normalized['is_biosensor'].fillna(0).astype(int)
    else:
        normalized['is_biosensor'] = 0
    
    # Source refs from pmcid/doi
    if 'doi' in normalized.columns:
        normalized['source_refs'] = normalized['doi']
    elif 'pmcid' in normalized.columns:
        normalized['source_refs'] = 'PMC:' + normalized['pmcid'].astype(str)
    else:
        normalized['source_refs'] = normalized['source'].apply(
            lambda x: f"source:{x}" if pd.notna(x) else None
        )
    
    # Use contrast_final if exists
    if 'contrast_final' in normalized.columns:
        normalized['contrast_ratio'] = normalized['contrast_final']
    
    # CI placeholders (would need actual extraction from papers)
    normalized['contrast_ci_low'] = None
    normalized['contrast_ci_high'] = None
    
    return normalized

def build_atlas_all(legacy_df: pd.DataFrame, candidates_df: pd.DataFrame) -> pd.DataFrame:
    """Construit atlas_all_real en combinant legacy + nouveaux."""
    
    # Combine
    all_df = pd.concat([legacy_df, candidates_df], ignore_index=True)
    
    # Deduplicate on SystemID
    all_df = all_df.drop_duplicates(subset=['SystemID'], keep='first')
    
    print(f"Built atlas_all_real with {len(all_df)} entries")
    
    return all_df

def build_atlas_fp_optical(all_df: pd.DataFrame) -> pd.DataFrame:
    """Filtre et formate atlas_fp_optical."""
    
    # Filter FP-like only
    fp_df = all_df[all_df.get('is_fp_like', 0) == 1].copy()
    
    # Select and reorder columns
    fp_df = fp_df[FP_OPTICAL_COLUMNS]
    
    print(f"Built atlas_fp_optical with {len(fp_df)} FP entries")
    
    return fp_df

def build_metadata(all_df: pd.DataFrame, fp_df: pd.DataFrame) -> dict:
    """Construit le fichier TRAINING.METADATA.json."""
    
    metadata = {
        "version": "1.2.0",
        "date": datetime.now().isoformat(),
        "description": "Biological Qubits Atlas - Fluorescent Proteins & Optical Biosensors",
        "datasets": {
            "atlas_all_real": {
                "file": "atlas_all_real.csv",
                "rows": len(all_df),
                "description": "Multi-modality dataset (FP, color centers, NMR, ESR, etc.)",
                "columns": list(all_df.columns)
            },
            "atlas_fp_optical": {
                "file": "atlas_fp_optical.csv",
                "rows": len(fp_df),
                "description": "FP and optical biosensors only",
                "columns": FP_OPTICAL_COLUMNS
            }
        },
        "schema": {
            "SystemID": "Unique identifier (FP_EXT_XXXX for external harvest)",
            "protein_name": "Common name of the protein",
            "variant": "Genetic variant (e.g., wild-type, A206K)",
            "family": "Protein family (e.g., GFP, mCherry)",
            "is_biosensor": "1 if biosensor, 0 if regular FP",
            "uniprot_id": "UniProt accession",
            "pdb_id": "PDB structure ID",
            "excitation_nm": "Excitation wavelength (nm)",
            "emission_nm": "Emission wavelength (nm)",
            "temperature_K": "Measurement temperature (Kelvin)",
            "pH": "pH condition",
            "contrast_ratio": "ΔF/F₀, on/off ratio, or fold-change",
            "contrast_ci_low": "Lower bound of 95% CI",
            "contrast_ci_high": "Upper bound of 95% CI",
            "contrast_source": "measured | computed | none",
            "condition_text": "Textual description of measurement conditions",
            "source_refs": "DOI, PMCID, or database reference",
            "license_source": "License of source data"
        },
        "licenses": {
            "FPbase": "CC BY-SA 4.0 (pointer-only, attribution required)",
            "UniProt": "CC BY 4.0",
            "PDB": "CC0 (public domain)",
            "PMC": "CC BY or compatible (OA articles only)"
        },
        "provenance": {
            "sources": ["FPbase", "UniProt", "PDB", "PubMed Central"],
            "harvest_scripts": [
                "scripts/etl/fetch_fpbase_candidates.py",
                "scripts/etl/fetch_uniprot_bulk.py",
                "scripts/etl/fetch_pdb_pdbe_bulk.py",
                "scripts/etl/fetch_pmc_contrast.py"
            ],
            "processing_pipeline": [
                "build_external_candidates.py",
                "classify_modality.py",
                "compute_proxies.py",
                "build_atlas_tables_v1_2.py"
            ]
        },
        "quality_metrics": {
            "total_entries": len(all_df),
            "fp_like_entries": len(fp_df),
            "with_measured_contrast": int((fp_df['contrast_source'] == 'measured').sum()),
            "with_computed_contrast": int((fp_df['contrast_source'] == 'computed').sum()),
            "with_any_contrast": int((fp_df['contrast_source'] != 'none').sum())
        }
    }
    
    return metadata

def save_outputs(all_df: pd.DataFrame, fp_df: pd.DataFrame, metadata: dict):
    """Sauvegarde les fichiers de sortie."""
    OUTPUT_ALL.parent.mkdir(parents=True, exist_ok=True)
    
    # Save CSVs
    all_df.to_csv(OUTPUT_ALL, index=False)
    print(f"Saved {OUTPUT_ALL}")
    
    fp_df.to_csv(OUTPUT_FP, index=False)
    print(f"Saved {OUTPUT_FP}")
    
    # Save metadata
    with open(METADATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"Saved {METADATA_FILE}")

def main():
    """Point d'entrée."""
    print("=" * 70)
    print("Build Atlas Tables v1.2 Pipeline")
    print("=" * 70)
    
    if not CANDIDATES_FILE.exists():
        print(f"ERROR: {CANDIDATES_FILE} not found!", file=sys.stderr)
        sys.exit(1)
    
    # Load data
    legacy_df = load_legacy()
    candidates_df = pd.read_parquet(CANDIDATES_FILE)
    
    # Normalize candidates
    candidates_df = normalize_candidates(candidates_df)
    
    # Build tables
    all_df = build_atlas_all(legacy_df, candidates_df)
    fp_df = build_atlas_fp_optical(all_df)
    
    # Build metadata
    metadata = build_metadata(all_df, fp_df)
    
    # Save
    save_outputs(all_df, fp_df, metadata)
    
    print("\nOK Atlas tables v1.2 built successfully!")
    print(f"  atlas_all_real: {len(all_df)} entries")
    print(f"  atlas_fp_optical: {len(fp_df)} entries")
    print(f"  Measured contrast: {metadata['quality_metrics']['with_measured_contrast']}")
    print(f"  Computed contrast: {metadata['quality_metrics']['with_computed_contrast']}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

