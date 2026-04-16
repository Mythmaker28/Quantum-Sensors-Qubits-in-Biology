#!/usr/bin/env python3
"""
Bootstrap CI pour facteur de réduction NV (T2_bulk / T2_bio)
Calcul après correction recatégorisation NV bulk
"""

import pandas as pd
import numpy as np
import json
import sys
from pathlib import Path
from datetime import datetime

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def load_v2_3():
    """Charge le dataset v2.3"""
    v23_path = Path("data/qubits/quantum_systems_unified_v2_3.csv")
    if not v23_path.exists():
        raise FileNotFoundError(f"Fichier {v23_path} non trouvé")
    
    df = pd.read_csv(v23_path)
    print(f"[LOAD] Dataset v2.3: {len(df)} systèmes")
    return df

def extract_nv_systems(df):
    """Extrait systèmes NV bulk et bio"""
    # Systèmes NV bulk (filtrer cryogéniques - garder seulement room temp)
    # Exclure aussi les spins nucléaires couplés (13C, 14N)
    nv_bulk = df[
        (df['Hote_contexte'] == 'bulk') & 
        (df['Systeme'].str.contains('NV', case=False, na=False)) &
        (~df['Systeme'].str.contains('13C|14N|15N|coupled', case=False, na=False)) &  # Exclure spins nucléaires
        (df['T2_us'].notna()) &
        (~df['Systeme'].str.contains('77K|4K|cryo', case=False, na=False)) &
        (df['Temperature_K'].fillna(298) >= 290) &  # Température ambiante ou supérieure
        (df['T2_us'] < 10000)  # T2 bulk room temp < 10 ms
    ].copy()
    
    # Systèmes NV bio (in_cellulo, in_vivo, ex_vivo)
    nv_bio = df[
        (df['Systeme'].str.contains('NV', case=False, na=False)) &
        (df['Hote_contexte'].str.contains('in_cellulo|in_vivo|ex_vivo', case=False, na=False)) &
        (df['T2_us'].notna())
    ].copy()
    
    print(f"\n[EXTRACT] Systèmes NV bulk: {len(nv_bulk)}")
    print(f"  T2_us: {nv_bulk['T2_us'].tolist()}")
    print(f"\n[EXTRACT] Systèmes NV bio: {len(nv_bio)}")
    print(f"  T2_us: {nv_bio['T2_us'].tolist()}")
    
    return nv_bulk, nv_bio

def calculate_reduction_factors(nv_bulk, nv_bio):
    """Calcule facteurs de réduction pour chaque paire bulk/bio"""
    factors = []
    
    if len(nv_bulk) == 0:
        print("[WARN] Aucun système NV bulk trouvé - impossible de calculer facteur")
        return factors
    
    if len(nv_bio) == 0:
        print("[WARN] Aucun système NV bio trouvé - impossible de calculer facteur")
        return factors
    
    # Utiliser T2 bulk moyen (ou unique si un seul)
    t2_bulk_mean = nv_bulk['T2_us'].mean()
    t2_bulk_values = nv_bulk['T2_us'].tolist()
    
    # Calculer facteur pour chaque système bio
    for idx, row in nv_bio.iterrows():
        t2_bio = row['T2_us']
        factor = t2_bulk_mean / t2_bio
        factors.append({
            'systeme': row['Systeme'],
            't2_bulk': t2_bulk_mean,
            't2_bio': t2_bio,
            'reduction_factor': factor,
            'hote_contexte': row['Hote_contexte']
        })
        print(f"  {row['Systeme'][:50]}: {t2_bulk_mean:.1f} / {t2_bio:.3f} = {factor:.1f}x")
    
    return factors, t2_bulk_values

def bootstrap_ci(factors, t2_bulk_values, n_iterations=10000, ci_level=0.95):
    """Calcule Bootstrap CI pour facteur de réduction"""
    
    if len(factors) == 0:
        return None
    
    reduction_factors = [f['reduction_factor'] for f in factors]
    
    # Bootstrap: rééchantillonner avec remise
    np.random.seed(42)  # Reproductibilité
    bootstrap_samples = []
    
    for _ in range(n_iterations):
        # Rééchantillonner les facteurs de réduction
        sample = np.random.choice(reduction_factors, size=len(reduction_factors), replace=True)
        bootstrap_samples.append(np.mean(sample))
    
    bootstrap_samples = np.array(bootstrap_samples)
    
    # Calculer CI
    alpha = 1 - ci_level
    lower = np.percentile(bootstrap_samples, 100 * alpha / 2)
    upper = np.percentile(bootstrap_samples, 100 * (1 - alpha / 2))
    mean_factor = np.mean(reduction_factors)
    median_factor = np.median(reduction_factors)
    
    results = {
        'mean_reduction_factor': float(mean_factor),
        'median_reduction_factor': float(median_factor),
        'ci_lower': float(lower),
        'ci_upper': float(upper),
        'ci_level': ci_level,
        'n_bootstrap': n_iterations,
        'n_bulk': len(t2_bulk_values),
        'n_bio': len(factors),
        't2_bulk_mean': float(np.mean(t2_bulk_values)),
        't2_bulk_std': float(np.std(t2_bulk_values)) if len(t2_bulk_values) > 1 else 0.0,
        't2_bio_mean': float(np.mean([f['t2_bio'] for f in factors])),
        't2_bio_std': float(np.std([f['t2_bio'] for f in factors]))
    }
    
    return results

def save_results(results, factors):
    """Sauvegarde résultats dans JSON"""
    output_path = Path("analysis/output/statistical_tests_results.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Charger résultats existants si disponibles
    existing_results = {}
    if output_path.exists():
        try:
            with open(output_path, 'r', encoding='utf-8') as f:
                existing_results = json.load(f)
        except:
            pass
    
    # Mettre à jour avec nouveaux résultats
    existing_results['nv_reduction_factor'] = results
    existing_results['nv_reduction_factors_individual'] = factors
    existing_results['last_updated'] = datetime.now().isoformat()
    existing_results['dataset_version'] = 'v2.3'
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(existing_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n[SAVE] Résultats sauvegardés: {output_path}")

def main():
    """Fonction principale"""
    print("=" * 80)
    print("BOOTSTRAP CI - Facteur Réduction NV")
    print("=" * 80)
    
    # Charger données
    df = load_v2_3()
    
    # Extraire systèmes NV
    nv_bulk, nv_bio = extract_nv_systems(df)
    
    if len(nv_bulk) == 0:
        print("\n[ERROR] Aucun système NV bulk trouvé - correction recatégorisation nécessaire")
        return 1
    
    if len(nv_bio) == 0:
        print("\n[ERROR] Aucun système NV bio trouvé")
        return 1
    
    # Calculer facteurs de réduction
    factors, t2_bulk_values = calculate_reduction_factors(nv_bulk, nv_bio)
    
    if len(factors) == 0:
        print("\n[ERROR] Aucun facteur de réduction calculable")
        return 1
    
    # Bootstrap CI
    print(f"\n[BOOTSTRAP] Calcul CI 95% avec 10,000 itérations...")
    results = bootstrap_ci(factors, t2_bulk_values, n_iterations=10000, ci_level=0.95)
    
    if results:
        print("\n" + "=" * 80)
        print("RÉSULTATS BOOTSTRAP CI")
        print("=" * 80)
        print(f"Facteur réduction moyen: {results['mean_reduction_factor']:.1f}x")
        print(f"Facteur réduction médian: {results['median_reduction_factor']:.1f}x")
        print(f"CI 95%: [{results['ci_lower']:.1f}, {results['ci_upper']:.1f}]x")
        print(f"\nT2 bulk moyen: {results['t2_bulk_mean']:.1f} ± {results['t2_bulk_std']:.1f} µs")
        print(f"T2 bio moyen: {results['t2_bio_mean']:.3f} ± {results['t2_bio_std']:.3f} µs")
        print(f"N_bulk: {results['n_bulk']}")
        print(f"N_bio: {results['n_bio']}")
        
        # Sauvegarder
        save_results(results, factors)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

