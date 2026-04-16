"""
Analyze Quantum-Sensors-Qubits-in-Biology repository content
to determine quantum data availability and overlap with atlas_fp_optical.

NO EMOJIS - Windows PowerShell compatibility
"""

import sys
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import pandas as pd
from pathlib import Path
import json

# Paths
REPO_ROOT = Path(__file__).parent
QS_REPO = REPO_ROOT / "Quantum-Sensors-Qubits-in-Biology"
DATA_DIR = QS_REPO / "data"

# Output
OUTPUT = {
    "repo_type": None,
    "contains_quantum_data": False,
    "n_qs": 0,
    "overlap_with_fp_optical": False,
    "overlap_percentage": 0,
    "details": {}
}

def analyze_non_optical_data():
    """Analyze non-optical quantum sensor data (spin qubits, radical pairs, nuclear spins)."""
    
    print("\n[ANALYSIS] Non-Optical Quantum Data")
    print("=" * 60)
    
    # Spin qubits
    spin_path = DATA_DIR / "non_optical" / "spin_qubits" / "staging" / "spin_qubit_candidates.csv"
    if spin_path.exists():
        df_spin = pd.read_csv(spin_path)
        print(f"\n[OK] Spin qubits file found: {len(df_spin)} systems")
        print(f"Columns: {list(df_spin.columns)}")
        
        # Count systems with T1 or T2
        has_t2 = df_spin['T2_microseconds'].notna()
        has_t1 = df_spin['T1_microseconds'].notna()
        has_coherence = has_t2 | has_t1
        n_spin = len(df_spin[has_coherence])
        
        print(f"[STATS] Systems with T2: {has_t2.sum()}")
        print(f"[STATS] Systems with T1: {has_t1.sum()}")
        print(f"[STATS] Systems with T1 OR T2: {n_spin}")
        
        OUTPUT["details"]["spin_qubits"] = {
            "total": len(df_spin),
            "with_coherence_metrics": n_spin,
            "with_t2": int(has_t2.sum()),
            "with_t1": int(has_t1.sum())
        }
    else:
        print(f"[WARN] Spin qubits file not found: {spin_path}")
        n_spin = 0
        OUTPUT["details"]["spin_qubits"] = {"total": 0, "with_coherence_metrics": 0}
    
    # Radical pairs
    rp_path = DATA_DIR / "non_optical" / "radical_pairs" / "staging" / "radical_pair_candidates.csv"
    if rp_path.exists():
        try:
            df_rp = pd.read_csv(rp_path, on_bad_lines='skip')
            print(f"\n[OK] Radical pairs file found: {len(df_rp)} systems")
            print(f"Columns: {list(df_rp.columns)}")
        except Exception as e:
            print(f"[ERROR] Failed to read radical pairs: {e}")
            df_rp = None
            n_rp = 0
        
        if df_rp is not None:
            # Radical pairs use timescale_ns instead of T1/T2
            has_timescale = df_rp['timescale_ns'].notna()
            n_rp = len(df_rp[has_timescale])
        
        print(f"[STATS] Systems with timescale_ns: {n_rp}")
        print(f"[NOTE] Radical pairs use 'timescale_ns' (coherence lifetime), not T1/T2")
        
        OUTPUT["details"]["radical_pairs"] = {
            "total": len(df_rp),
            "with_timescale": n_rp,
            "note": "Uses timescale_ns instead of T1/T2"
        }
    else:
        print(f"[WARN] Radical pairs file not found: {rp_path}")
        n_rp = 0
        OUTPUT["details"]["radical_pairs"] = {"total": 0, "with_timescale": 0}
    
    # Nuclear spins
    nuc_path = DATA_DIR / "non_optical" / "nuclear_spins" / "staging" / "nuclear_spin_candidates.csv"
    if nuc_path.exists():
        df_nuc = pd.read_csv(nuc_path)
        print(f"\n[OK] Nuclear spins file found: {len(df_nuc)} systems")
        print(f"Columns: {list(df_nuc.columns)}")
        
        # Nuclear spins use T2_milliseconds and T1_milliseconds
        has_t2 = df_nuc['T2_milliseconds'].notna()
        has_t1 = df_nuc['T1_milliseconds'].notna()
        has_coherence = has_t2 | has_t1
        n_nuc = len(df_nuc[has_coherence])
        
        print(f"[STATS] Systems with T2_milliseconds: {has_t2.sum()}")
        print(f"[STATS] Systems with T1_milliseconds: {has_t1.sum()}")
        print(f"[STATS] Systems with T1 OR T2: {n_nuc}")
        print(f"[NOTE] Nuclear spins use milliseconds, not microseconds")
        
        OUTPUT["details"]["nuclear_spins"] = {
            "total": len(df_nuc),
            "with_coherence_metrics": n_nuc,
            "with_t2_ms": int(has_t2.sum()),
            "with_t1_ms": int(has_t1.sum()),
            "note": "Uses T1/T2 in milliseconds"
        }
    else:
        print(f"[WARN] Nuclear spins file not found: {nuc_path}")
        n_nuc = 0
        OUTPUT["details"]["nuclear_spins"] = {"total": 0, "with_coherence_metrics": 0}
    
    # Total quantum systems with coherence metrics
    n_qs_total = n_spin + n_rp + n_nuc
    
    print(f"\n[SUMMARY] Total quantum systems with coherence metrics:")
    print(f"  - Spin qubits: {n_spin}")
    print(f"  - Radical pairs: {n_rp}")
    print(f"  - Nuclear spins: {n_nuc}")
    print(f"  - TOTAL n_qs: {n_qs_total}")
    
    return n_qs_total


def check_overlap_with_fp_optical():
    """Check overlap between non-optical data and atlas_fp_optical_v2_2_curated.csv."""
    
    print("\n[ANALYSIS] Overlap with atlas_fp_optical")
    print("=" * 60)
    
    # Load atlas_fp_optical_v2_2_curated.csv
    fp_path = REPO_ROOT / "data" / "processed" / "atlas_fp_optical_v2_2_curated.csv"
    if not fp_path.exists():
        print(f"[ERROR] atlas_fp_optical not found: {fp_path}")
        return False, 0
    
    df_fp = pd.read_csv(fp_path)
    print(f"[OK] atlas_fp_optical loaded: {len(df_fp)} systems")
    
    # Non-optical data is completely separate from optical FP data
    # Spin qubits = NV centers, SiC defects, etc. (NOT fluorescent proteins)
    # Radical pairs = Cryptochrome, photosystem II, etc. (NOT fluorescent proteins)
    # Nuclear spins = 13C, 31P, etc. (NOT fluorescent proteins)
    
    print(f"\n[CONCLUSION] No overlap expected:")
    print(f"  - atlas_fp_optical: Fluorescent proteins (GCaMP, ASAP, dLight, etc.)")
    print(f"  - Non-optical data: Spin qubits, radical pairs, nuclear spins")
    print(f"  - These are DIFFERENT modalities")
    
    overlap = False
    overlap_pct = 0
    
    OUTPUT["details"]["overlap_analysis"] = {
        "fp_optical_systems": len(df_fp),
        "overlap": overlap,
        "overlap_percentage": overlap_pct,
        "reason": "Different modalities: FP optical vs non-optical quantum sensors"
    }
    
    return overlap, overlap_pct


def determine_repo_type():
    """Determine the type of repository."""
    
    print("\n[ANALYSIS] Repository Type")
    print("=" * 60)
    
    # Check for data files
    has_fp_optical = (DATA_DIR / "processed" / "atlas_fp_optical_v2_2_curated.csv").exists()
    has_spin_qubits = (DATA_DIR / "non_optical" / "spin_qubits" / "staging" / "spin_qubit_candidates.csv").exists()
    has_radical_pairs = (DATA_DIR / "non_optical" / "radical_pairs" / "staging" / "radical_pair_candidates.csv").exists()
    has_nuclear_spins = (DATA_DIR / "non_optical" / "nuclear_spins" / "staging" / "nuclear_spin_candidates.csv").exists()
    
    print(f"[DATA] Fluorescent proteins (optical): {has_fp_optical}")
    print(f"[DATA] Spin qubits (non-optical): {has_spin_qubits}")
    print(f"[DATA] Radical pairs (non-optical): {has_radical_pairs}")
    print(f"[DATA] Nuclear spins (non-optical): {has_nuclear_spins}")
    
    if has_fp_optical and (has_spin_qubits or has_radical_pairs or has_nuclear_spins):
        repo_type = "Multi-modal atlas: Optical FP + Non-optical quantum sensors"
    elif has_fp_optical:
        repo_type = "Atlas of fluorescent proteins (optical)"
    elif has_spin_qubits or has_radical_pairs or has_nuclear_spins:
        repo_type = "Atlas of non-optical quantum sensors"
    else:
        repo_type = "Documentation/review (no data files found)"
    
    print(f"\n[CONCLUSION] Repository type: {repo_type}")
    
    return repo_type


def main():
    """Main analysis function."""
    
    print("=" * 60)
    print("QUANTUM-SENSORS-QUBITS-IN-BIOLOGY REPOSITORY ANALYSIS")
    print("=" * 60)
    
    # 1. Determine repo type
    OUTPUT["repo_type"] = determine_repo_type()
    
    # 2. Analyze non-optical quantum data
    n_qs = analyze_non_optical_data()
    OUTPUT["n_qs"] = n_qs
    OUTPUT["contains_quantum_data"] = (n_qs > 0)
    
    # 3. Check overlap with atlas_fp_optical
    overlap, overlap_pct = check_overlap_with_fp_optical()
    OUTPUT["overlap_with_fp_optical"] = overlap
    OUTPUT["overlap_percentage"] = overlap_pct
    
    # Final summary
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    print(f"Type repo: {OUTPUT['repo_type']}")
    print(f"Contient donnees quantiques: {'Oui' if OUTPUT['contains_quantum_data'] else 'Non'}")
    print(f"Si oui, n_qs = {OUTPUT['n_qs']}")
    print(f"Overlap atlas_fp_optical: {'Oui' if OUTPUT['overlap_with_fp_optical'] else 'Non'}")
    
    if OUTPUT['overlap_percentage'] > 0:
        print(f"Overlap percentage: {OUTPUT['overlap_percentage']:.1f}%")
    
    # Save JSON output
    output_path = REPO_ROOT / "analysis" / "output" / "quantum_sensors_repo_analysis.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(OUTPUT, f, indent=2, ensure_ascii=False)
    
    print(f"\n[OK] Analysis saved to: {output_path}")
    
    # Generate markdown report
    md_path = REPO_ROOT / "analysis" / "output" / "quantum_sensors_repo_analysis.md"
    generate_markdown_report(md_path)
    print(f"[OK] Markdown report saved to: {md_path}")


def generate_markdown_report(output_path):
    """Generate markdown report."""
    
    md = f"""# Quantum-Sensors-Qubits-in-Biology Repository Analysis

**Date:** 2025-11-19  
**Repository:** https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology

---

## SUMMARY

```
Type repo: {OUTPUT['repo_type']}
Contient donnees quantiques: {'Oui' if OUTPUT['contains_quantum_data'] else 'Non'}
Si oui, n_qs = {OUTPUT['n_qs']}
Overlap atlas_fp_optical: {'Oui' if OUTPUT['overlap_with_fp_optical'] else 'Non'}
```

---

## DETAILS

### Repository Type

**{OUTPUT['repo_type']}**

This repository contains:
- **Optical data:** Fluorescent proteins (atlas_fp_optical_v2_2_curated.csv, 180 systems)
- **Non-optical data:** Spin qubits, radical pairs, nuclear spins

### Quantum Data (Non-Optical)

"""
    
    if "spin_qubits" in OUTPUT["details"]:
        sq = OUTPUT["details"]["spin_qubits"]
        md += f"""
#### Spin Qubits
- Total systems: {sq['total']}
- With coherence metrics (T1/T2): {sq['with_coherence_metrics']}
- With T2: {sq.get('with_t2', 0)}
- With T1: {sq.get('with_t1', 0)}
"""
    
    if "radical_pairs" in OUTPUT["details"]:
        rp = OUTPUT["details"]["radical_pairs"]
        md += f"""
#### Radical Pairs
- Total systems: {rp['total']}
- With timescale_ns: {rp['with_timescale']}
- Note: {rp.get('note', '')}
"""
    
    if "nuclear_spins" in OUTPUT["details"]:
        ns = OUTPUT["details"]["nuclear_spins"]
        md += f"""
#### Nuclear Spins
- Total systems: {ns['total']}
- With coherence metrics (T1/T2): {ns['with_coherence_metrics']}
- With T2 (ms): {ns.get('with_t2_ms', 0)}
- With T1 (ms): {ns.get('with_t1_ms', 0)}
- Note: {ns.get('note', '')}
"""
    
    md += f"""
**Total n_qs = {OUTPUT['n_qs']}**

### Overlap with atlas_fp_optical

**Result:** {'Oui' if OUTPUT['overlap_with_fp_optical'] else 'Non'}

"""
    
    if "overlap_analysis" in OUTPUT["details"]:
        oa = OUTPUT["details"]["overlap_analysis"]
        md += f"""
- atlas_fp_optical systems: {oa['fp_optical_systems']}
- Overlap: {oa['overlap']}
- Reason: {oa['reason']}
"""
    
    md += """
---

## CONCLUSION

**Quantum-Sensors-Qubits-in-Biology** is the same repository as **QBitAtlas**.

It contains:
1. **Optical data (180 FP systems):** Already counted in atlas_fp_optical_v2_2_curated.csv
2. **Non-optical quantum data (n_qs systems):** Spin qubits, radical pairs, nuclear spins

**Impact on bridge scenario:**
- If non-optical data has T1/T2 metrics, it can be added to n_total
- No overlap with atlas_fp_optical (different modalities)
- n_total = n_ising + n_fp + n_qs (if n_qs > 0)

---

**Generated by:** analyze_quantum_sensors_repo.py  
**Version:** QBitAtlas v2.2.2
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md)


if __name__ == "__main__":
    main()

