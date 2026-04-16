"""
Consolidate non-optical quantum systems into a single dataset.
Includes spin qubits, radical pairs, and nuclear spins.

NO EMOJIS - Windows PowerShell compatibility
"""

import sys
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import pandas as pd
from pathlib import Path
import json
from datetime import datetime

# Paths
REPO_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = REPO_ROOT / "data"
OUTPUT_DIR = REPO_ROOT / "data" / "qubits"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_spin_qubits():
    """Load spin qubit data."""
    path = DATA_DIR / "non_optical" / "spin_qubits" / "staging" / "spin_qubit_candidates.csv"
    if not path.exists():
        print(f"[WARN] Spin qubits not found: {path}")
        return pd.DataFrame()
    
    df = pd.read_csv(path)
    print(f"[OK] Loaded {len(df)} spin qubits")
    
    # Standardize columns
    df['modality'] = 'spin_qubit'
    df['system_name'] = df['label']
    df['T1_us'] = df['T1_microseconds']
    df['T2_us'] = df['T2_microseconds']
    df['temperature_K'] = df['temperature_K']
    df['method'] = df['measurement_method']
    df['source_doi'] = df['doi']
    df['evidence'] = df['evidence_level']
    df['notes'] = df['notes']
    
    # Select relevant columns
    cols = ['id', 'modality', 'system_name', 'system_type', 'host_material', 
            'T1_us', 'T2_us', 'temperature_K', 'method', 'source_doi', 'evidence', 'notes']
    
    return df[cols]

def load_radical_pairs():
    """Load radical pair data."""
    path = DATA_DIR / "non_optical" / "radical_pairs" / "staging" / "radical_pair_candidates.csv"
    if not path.exists():
        print(f"[WARN] Radical pairs not found: {path}")
        return pd.DataFrame()
    
    # Skip bad lines due to CSV formatting issues
    df = pd.read_csv(path, on_bad_lines='skip')
    print(f"[OK] Loaded {len(df)} radical pairs")
    
    # Standardize columns
    df['modality'] = 'radical_pair'
    df['system_name'] = df['protein_or_complex']
    df['system_type'] = df['observable']
    df['host_material'] = df['organism']
    
    # Convert timescale_ns to microseconds for consistency
    df['T2_us'] = df['timescale_ns'] / 1000.0  # ns to us
    df['T1_us'] = None  # Not measured for radical pairs
    
    df['temperature_K'] = df['temperature_K']
    df['method'] = 'radical_pair_detection'
    df['source_doi'] = df['doi']
    df['evidence'] = df['evidence_level']
    df['notes'] = df['notes']
    
    # Select relevant columns
    cols = ['id', 'modality', 'system_name', 'system_type', 'host_material', 
            'T1_us', 'T2_us', 'temperature_K', 'method', 'source_doi', 'evidence', 'notes']
    
    return df[cols]

def load_nuclear_spins():
    """Load nuclear spin data."""
    path = DATA_DIR / "non_optical" / "nuclear_spins" / "staging" / "nuclear_spin_candidates.csv"
    if not path.exists():
        print(f"[WARN] Nuclear spins not found: {path}")
        return pd.DataFrame()
    
    df = pd.read_csv(path)
    print(f"[OK] Loaded {len(df)} nuclear spins")
    
    # Standardize columns
    df['modality'] = 'nuclear_spin'
    df['system_name'] = df['nucleus'] + ' in ' + df['host']
    df['system_type'] = df['system_type']
    df['host_material'] = df['host']
    
    # Convert milliseconds to microseconds for consistency
    df['T1_us'] = df['T1_milliseconds'] * 1000.0  # ms to us
    df['T2_us'] = df['T2_milliseconds'] * 1000.0  # ms to us
    
    df['temperature_K'] = df['temperature_K']
    df['method'] = df['measurement_method']
    df['source_doi'] = df['doi']
    df['evidence'] = df['evidence_level']
    df['notes'] = df['notes']
    
    # Select relevant columns
    cols = ['id', 'modality', 'system_name', 'system_type', 'host_material', 
            'T1_us', 'T2_us', 'temperature_K', 'method', 'source_doi', 'evidence', 'notes']
    
    return df[cols]

def consolidate_all():
    """Consolidate all non-optical quantum systems."""
    
    print("\n" + "=" * 60)
    print("CONSOLIDATING NON-OPTICAL QUANTUM SYSTEMS")
    print("=" * 60)
    
    # Load all datasets
    df_spin = load_spin_qubits()
    df_rp = load_radical_pairs()
    df_nuc = load_nuclear_spins()
    
    # Concatenate
    df_all = pd.concat([df_spin, df_rp, df_nuc], ignore_index=True)
    
    print(f"\n[SUMMARY] Total systems: {len(df_all)}")
    print(f"  - Spin qubits: {len(df_spin)}")
    print(f"  - Radical pairs: {len(df_rp)}")
    print(f"  - Nuclear spins: {len(df_nuc)}")
    
    # Filter systems with coherence metrics
    has_coherence = df_all['T1_us'].notna() | df_all['T2_us'].notna()
    df_with_metrics = df_all[has_coherence].copy()
    
    print(f"\n[FILTER] Systems with T1/T2 metrics: {len(df_with_metrics)}")
    
    # Save consolidated dataset
    output_path = OUTPUT_DIR / "nonoptical_qubits_consolidated.csv"
    df_with_metrics.to_csv(output_path, index=False)
    print(f"\n[OK] Saved to: {output_path}")
    
    # Generate statistics
    stats = {
        "dataset": "nonoptical_qubits_consolidated",
        "version": "v1.0",
        "generated_at": datetime.now().isoformat(),
        "total_systems": len(df_with_metrics),
        "by_modality": {
            "spin_qubits": len(df_with_metrics[df_with_metrics['modality'] == 'spin_qubit']),
            "radical_pairs": len(df_with_metrics[df_with_metrics['modality'] == 'radical_pair']),
            "nuclear_spins": len(df_with_metrics[df_with_metrics['modality'] == 'nuclear_spin'])
        },
        "by_evidence": df_with_metrics['evidence'].value_counts().to_dict(),
        "temperature_range_K": {
            "min": float(df_with_metrics['temperature_K'].min()) if df_with_metrics['temperature_K'].notna().any() else None,
            "max": float(df_with_metrics['temperature_K'].max()) if df_with_metrics['temperature_K'].notna().any() else None
        },
        "coherence_times_us": {
            "T1_min": float(df_with_metrics['T1_us'].min()) if df_with_metrics['T1_us'].notna().any() else None,
            "T1_max": float(df_with_metrics['T1_us'].max()) if df_with_metrics['T1_us'].notna().any() else None,
            "T2_min": float(df_with_metrics['T2_us'].min()) if df_with_metrics['T2_us'].notna().any() else None,
            "T2_max": float(df_with_metrics['T2_us'].max()) if df_with_metrics['T2_us'].notna().any() else None
        }
    }
    
    stats_path = OUTPUT_DIR / "nonoptical_qubits_stats.json"
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print(f"[OK] Stats saved to: {stats_path}")
    
    # Display summary table
    print("\n" + "=" * 60)
    print("SUMMARY BY MODALITY")
    print("=" * 60)
    print(df_with_metrics.groupby('modality').agg({
        'id': 'count',
        'T1_us': lambda x: x.notna().sum(),
        'T2_us': lambda x: x.notna().sum(),
        'temperature_K': lambda x: x.notna().sum()
    }).rename(columns={
        'id': 'count',
        'T1_us': 'has_T1',
        'T2_us': 'has_T2',
        'temperature_K': 'has_temp'
    }))
    
    return df_with_metrics

if __name__ == "__main__":
    df = consolidate_all()
    print("\n[SUCCESS] Consolidation complete!")

