#!/usr/bin/env python3
"""
Tests de validation du schéma Atlas v2.1 et de la TRAINING_TABLE
================================================================
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path

# Paths
ATLAS_FILE = Path("data/processed/atlas_fp_optical_v2_1.csv")
TRAINING_FILE = Path("data/processed/TRAINING_TABLE_v2_1.csv")
METADATA_FILE = Path("data/processed/TRAINING.METADATA_v2_1.json")

def test_files_exist():
    """Test que tous les fichiers requis existent"""
    assert ATLAS_FILE.exists(), f"Atlas v2.1 non trouvé: {ATLAS_FILE}"
    assert TRAINING_FILE.exists(), f"Training table non trouvée: {TRAINING_FILE}"
    assert METADATA_FILE.exists(), f"Metadata non trouvée: {METADATA_FILE}"

def test_atlas_schema():
    """Test que le schéma de l'atlas est conforme"""
    df = pd.read_csv(ATLAS_FILE)
    
    # Colonnes requises
    required_cols = [
        'protein_name', 'family', 'contrast_normalized',
        'excitation_nm', 'emission_nm', 'stokes_shift_nm',
        'excitation_missing', 'emission_missing', 'contrast_missing'
    ]
    
    for col in required_cols:
        assert col in df.columns, f"Colonne manquante: {col}"

def test_training_table_schema():
    """Test du schéma TRAINING_TABLE (contrat interface)"""
    df = pd.read_csv(TRAINING_FILE)
    
    # Colonnes garanties par le contrat
    required_cols = [
        'canonical_name', 'family', 'excitation_nm', 'emission_nm',
        'stokes_shift_nm', 'method', 'context_type', 'contrast_normalized',
        'source', 'provenance', 'license',
        'excitation_missing', 'emission_missing', 'contrast_missing'
    ]
    
    for col in required_cols:
        assert col in df.columns, f"Contrat violé: colonne {col} manquante"

def test_data_types():
    """Test que les types de données sont corrects"""
    df = pd.read_csv(TRAINING_FILE)
    
    # Float columns
    float_cols = ['excitation_nm', 'emission_nm', 'stokes_shift_nm', 'contrast_normalized']
    for col in float_cols:
        assert df[col].dtype in [float, np.float64, np.float32] or df[col].dtype == object, \
            f"{col} devrait être float, trouvé: {df[col].dtype}"
    
    # Boolean columns
    bool_cols = ['excitation_missing', 'emission_missing', 'contrast_missing']
    for col in bool_cols:
        unique_vals = df[col].dropna().unique()
        assert all(v in [True, False, 0, 1] for v in unique_vals), \
            f"{col} devrait être booléen"

def test_wavelength_ranges():
    """Test que les longueurs d'onde sont dans des plages plausibles"""
    df = pd.read_csv(TRAINING_FILE)
    
    # Excitation: 350-700 nm (visible + UV proche)
    ex_valid = df['excitation_nm'].dropna()
    assert (ex_valid >= 350).all() and (ex_valid <= 700).all(), \
        f"Excitation hors plage: {ex_valid.min()}-{ex_valid.max()} nm"
    
    # Emission: 400-750 nm
    em_valid = df['emission_nm'].dropna()
    assert (em_valid >= 400).all() and (em_valid <= 750).all(), \
        f"Emission hors plage: {em_valid.min()}-{em_valid.max()} nm"
    
    # Stokes shift positif (sauf cas rares)
    stokes = df['stokes_shift_nm'].dropna()
    neg_stokes = (stokes < 0).sum()
    assert neg_stokes / len(stokes) < 0.05, \
        f"Trop de Stokes shifts négatifs: {neg_stokes}/{len(stokes)}"

def test_contrast_normalization():
    """Test que les contrastes normalisés sont plausibles"""
    df = pd.read_csv(TRAINING_FILE)
    
    contrast = df['contrast_normalized'].dropna()
    
    # Plage plausible: 0.1 à 100 (fold-change)
    assert (contrast >= 0.1).all(), \
        f"Contraste trop faible: min={contrast.min()}"
    assert (contrast <= 100).all(), \
        f"Contraste trop élevé: max={contrast.max()}"

def test_canonical_name_uniqueness():
    """Test que les noms canoniques sont uniques (pas de doublons)"""
    df = pd.read_csv(TRAINING_FILE)
    
    # Grouper par source si nécessaire
    duplicates = df['canonical_name'].duplicated()
    assert duplicates.sum() == 0, \
        f"Doublons détectés: {df[duplicates]['canonical_name'].tolist()}"

def test_target_n_useful():
    """Test que nous avons >=120 systèmes utiles"""
    df = pd.read_csv(TRAINING_FILE)
    
    n_useful = len(df)
    TARGET = 120
    
    assert n_useful >= TARGET, \
        f"Objectif non atteint: {n_useful} systèmes utiles (cible: {TARGET})"

def test_coverage_minimal():
    """Test que la couverture des champs minimaux est >=90%"""
    df = pd.read_csv(TRAINING_FILE)
    
    # Champs critiques
    critical_fields = {
        'excitation_nm': 'excitation_missing',
        'emission_nm': 'emission_missing',
        'contrast_normalized': 'contrast_missing'
    }
    
    TARGET_COVERAGE = 0.90
    
    for field, missing_flag in critical_fields.items():
        coverage = (~df[missing_flag]).sum() / len(df)
        assert coverage >= TARGET_COVERAGE, \
            f"Couverture insuffisante pour {field}: {coverage:.1%} (cible: {TARGET_COVERAGE:.0%})"

def test_family_distribution():
    """Test que les familles sont bien distribuées"""
    df = pd.read_csv(TRAINING_FILE)
    
    family_counts = df['family'].value_counts()
    
    # Au moins 10 familles avec >=5 systèmes
    families_ge_5 = (family_counts >= 5).sum()
    assert families_ge_5 >= 10, \
        f"Pas assez de familles bien représentées: {families_ge_5} (cible: 10)"

def test_license_compliance():
    """Test que les licences sont renseignées"""
    df = pd.read_csv(TRAINING_FILE)
    
    missing_license = df['license'].isna().sum()
    missing_rate = missing_license / len(df)
    
    assert missing_rate < 0.1, \
        f"Trop de licences manquantes: {missing_rate:.1%}"

def test_provenance_doi():
    """Test que les provenances (DOI) sont renseignées"""
    df = pd.read_csv(TRAINING_FILE)
    
    missing_prov = df['provenance'].isna().sum()
    missing_rate = missing_prov / len(df)
    
    assert missing_rate < 0.15, \
        f"Trop de provenances manquantes: {missing_rate:.1%}"

def test_metadata_consistency():
    """Test que les métadonnées sont cohérentes avec les données"""
    import json
    
    df = pd.read_csv(TRAINING_FILE)
    
    with open(METADATA_FILE, 'r') as f:
        metadata = json.load(f)
    
    # Vérifier cohérence
    assert metadata['N_useful'] == len(df), \
        f"N_useful incohérent: metadata={metadata['N_useful']}, actual={len(df)}"
    
    assert metadata['N_families'] == df['family'].nunique(), \
        f"N_families incohérent: metadata={metadata['N_families']}, actual={df['family'].nunique()}"

def test_no_extreme_outliers():
    """Test qu'il n'y a pas d'outliers extrêmes (z-score > 5)"""
    df = pd.read_csv(TRAINING_FILE)
    
    # Log transform pour contraste
    contrast_log = np.log1p(df['contrast_normalized'].dropna())
    
    # Z-score
    z_scores = np.abs((contrast_log - contrast_log.mean()) / contrast_log.std())
    
    outliers = (z_scores > 5).sum()
    outlier_rate = outliers / len(z_scores)
    
    assert outlier_rate < 0.01, \
        f"Trop d'outliers extrêmes: {outliers} ({outlier_rate:.1%})"

# Summary test
def test_v2_1_summary():
    """Test récapitulatif pour affichage"""
    df_atlas = pd.read_csv(ATLAS_FILE)
    df_train = pd.read_csv(TRAINING_FILE)
    
    print("\n" + "=" * 60)
    print("RÉSUMÉ DES TESTS — ATLAS v2.1")
    print("=" * 60)
    print(f"Total systèmes (Atlas): {len(df_atlas)}")
    print(f"Systèmes utiles (Training): {len(df_train)}")
    print(f"Familles: {df_train['family'].nunique()}")
    print(f"Couverture excitation: {(~df_train['excitation_missing']).sum() / len(df_train):.1%}")
    print(f"Couverture emission: {(~df_train['emission_missing']).sum() / len(df_train):.1%}")
    print(f"Couverture contrast: {(~df_train['contrast_missing']).sum() / len(df_train):.1%}")
    print("=" * 60)
    
    # Always pass (just for info)
    assert True

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])

