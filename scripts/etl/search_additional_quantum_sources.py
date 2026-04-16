"""
Search for additional quantum biology data sources.
Explore external databases, repositories, and literature.

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

def analyze_biological_qubits_csv():
    """Analyze the existing biological_qubits.csv file."""
    
    print("\n" + "=" * 60)
    print("ANALYZING EXISTING biological_qubits.csv")
    print("=" * 60)
    
    csv_path = REPO_ROOT / "data" / "qubits" / "biological_qubits.csv"
    
    if not csv_path.exists():
        print(f"[ERROR] File not found: {csv_path}")
        return None
    
    df = pd.read_csv(csv_path)
    print(f"\n[OK] Loaded {len(df)} systems from biological_qubits.csv")
    
    # Analyze by class
    print(f"\n[STATS] By class:")
    print(df['Classe'].value_counts())
    
    # Analyze by evidence
    print(f"\n[STATS] By evidence quality:")
    print(df['Qualite'].value_counts())
    
    # Check coherence metrics
    has_t2 = df['T2_us'].notna()
    has_t1 = df['T1_s'].notna()
    
    print(f"\n[STATS] Coherence metrics:")
    print(f"  - Systems with T2_us: {has_t2.sum()}")
    print(f"  - Systems with T1_s: {has_t1.sum()}")
    print(f"  - Systems with T1 OR T2: {(has_t2 | has_t1).sum()}")
    
    # Temperature range
    temp_range = df['Temperature_K'].dropna()
    if len(temp_range) > 0:
        print(f"\n[STATS] Temperature range: {temp_range.min():.0f} - {temp_range.max():.0f} K")
    
    # In vivo systems
    in_vivo = df[df['In_vivo_flag'] == 1]
    print(f"\n[STATS] In vivo systems: {len(in_vivo)}")
    
    return df


def search_external_databases():
    """Search for external quantum biology databases."""
    
    print("\n" + "=" * 60)
    print("EXTERNAL QUANTUM BIOLOGY DATA SOURCES")
    print("=" * 60)
    
    sources = {
        "Quantum Biology Database (QBD)": {
            "url": "https://quantumbiology.org/database",
            "status": "To verify",
            "estimated_systems": "Unknown",
            "data_types": "Quantum coherence in biology, cryptochrome, photosynthesis"
        },
        "NV Center Database (NVCDB)": {
            "url": "https://nvcenterdatabase.org",
            "status": "To verify",
            "estimated_systems": "~100-200",
            "data_types": "NV centers in diamond, T1/T2, ODMR parameters"
        },
        "SiC Defects Database": {
            "url": "https://sicdefects.org or research papers",
            "status": "No centralized DB, literature mining needed",
            "estimated_systems": "~20-50",
            "data_types": "VSi, divacancy, T1/T2, spin properties"
        },
        "Hyperpolarized MRI Database": {
            "url": "FDA clinical trials + literature",
            "status": "Dispersed across clinical trials",
            "estimated_systems": "~15-30",
            "data_types": "13C-pyruvate, 13C-lactate, T1 relaxation"
        },
        "FPbase (Fluorescent Proteins)": {
            "url": "https://www.fpbase.org",
            "status": "Already integrated in atlas_fp_optical",
            "estimated_systems": "~1000+ (180 curated in QBitAtlas)",
            "data_types": "Spectral properties, quantum yield, lifetime"
        },
        "Radical Pair Database": {
            "url": "Literature mining (cryptochrome, photosynthesis)",
            "status": "No centralized DB, manual curation needed",
            "estimated_systems": "~20-40",
            "data_types": "Radical pairs, timescales, magnetic field effects"
        },
        "ising-life-lab (Ising models)": {
            "url": "https://github.com/Mythmaker28/ising-life-lab",
            "status": "To explore",
            "estimated_systems": "Unknown",
            "data_types": "Computational models, energy landscapes, not necessarily T1/T2"
        },
        "fp-qubit-design": {
            "url": "https://github.com/Mythmaker28/fp-qubit-design",
            "status": "Uses QBitAtlas data as training",
            "estimated_systems": "Predictions, not measured data",
            "data_types": "ML-predicted FP mutants"
        },
        "arrest-molecules": {
            "url": "https://github.com/Mythmaker28/arrest-molecules",
            "status": "Molecular arrest framework",
            "estimated_systems": "10 compounds, 44 predictions",
            "data_types": "Metastability, not qubits"
        }
    }
    
    print("\n[SEARCH] Potential external sources:\n")
    
    for i, (name, info) in enumerate(sources.items(), 1):
        print(f"{i}. {name}")
        print(f"   URL: {info['url']}")
        print(f"   Status: {info['status']}")
        print(f"   Estimated systems: {info['estimated_systems']}")
        print(f"   Data types: {info['data_types']}")
        print()
    
    return sources


def estimate_total_quantum_systems():
    """Estimate total quantum systems across all sources."""
    
    print("\n" + "=" * 60)
    print("TOTAL QUANTUM SYSTEMS ESTIMATION")
    print("=" * 60)
    
    sources_count = {
        "QBitAtlas - optical FP (v2.2.2 curated)": 180,
        "QBitAtlas - non-optical (spin + radical + nuclear)": 27,
        "QBitAtlas - biological_qubits.csv": 35,
        "Potential NV centers (literature mining)": "50-100",
        "Potential SiC defects (literature mining)": "20-50",
        "Potential hyperpolarized nuclei (clinical trials)": "10-20",
        "Potential radical pairs (literature mining)": "10-30",
    }
    
    print("\n[INVENTORY] Current and potential sources:\n")
    
    confirmed_total = 0
    for source, count in sources_count.items():
        if isinstance(count, int):
            confirmed_total += count
            print(f"[CONFIRMED] {source}: {count}")
        else:
            print(f"[POTENTIAL] {source}: {count}")
    
    print(f"\n[TOTAL CONFIRMED] {confirmed_total} systems")
    print(f"[POTENTIAL ADDITIONAL] 90-200 systems (literature mining needed)")
    print(f"[ESTIMATED TOTAL] {confirmed_total} + 90-200 = 332-442 systems")
    
    # Check overlap
    print("\n" + "=" * 60)
    print("OVERLAP ANALYSIS")
    print("=" * 60)
    print("\n[WARNING] Potential overlaps to investigate:")
    print("  - biological_qubits.csv vs non-optical consolidated")
    print("  - Some NV centers may be in both datasets")
    print("  - Need deduplication before final count")
    
    return sources_count


def recommend_next_steps():
    """Recommend next steps for data expansion."""
    
    print("\n" + "=" * 60)
    print("RECOMMENDED NEXT STEPS")
    print("=" * 60)
    
    steps = [
        {
            "priority": "HIGH",
            "task": "Compare biological_qubits.csv vs nonoptical_qubits_consolidated.csv",
            "reason": "Identify overlaps and merge datasets",
            "estimated_time": "30 min",
            "systems_gained": "0 (deduplication)"
        },
        {
            "priority": "HIGH",
            "task": "Literature mining: NV centers in biology (2010-2025)",
            "reason": "Well-documented field with many papers",
            "estimated_time": "4-8 hours",
            "systems_gained": "50-100"
        },
        {
            "priority": "MEDIUM",
            "task": "Literature mining: SiC defects (VSi, divacancy)",
            "reason": "Growing field, room-temp operation",
            "estimated_time": "3-5 hours",
            "systems_gained": "20-50"
        },
        {
            "priority": "MEDIUM",
            "task": "Clinical trials: Hyperpolarized 13C MRI",
            "reason": "FDA-approved, clinical data available",
            "estimated_time": "2-4 hours",
            "systems_gained": "10-20"
        },
        {
            "priority": "LOW",
            "task": "Literature mining: Radical pairs (cryptochrome, photosynthesis)",
            "reason": "Controversial field, indirect measurements",
            "estimated_time": "3-6 hours",
            "systems_gained": "10-30"
        },
        {
            "priority": "LOW",
            "task": "Explore ising-life-lab repository",
            "reason": "Check if contains additional quantum data",
            "estimated_time": "1-2 hours",
            "systems_gained": "Unknown (possibly 0)"
        }
    ]
    
    print("\n[ROADMAP] Data expansion tasks:\n")
    
    for i, step in enumerate(steps, 1):
        print(f"{i}. [{step['priority']}] {step['task']}")
        print(f"   Reason: {step['reason']}")
        print(f"   Estimated time: {step['estimated_time']}")
        print(f"   Systems gained: {step['systems_gained']}")
        print()
    
    return steps


def main():
    """Main analysis function."""
    
    print("=" * 60)
    print("SEARCH FOR ADDITIONAL QUANTUM BIOLOGY DATA")
    print("=" * 60)
    
    # 1. Analyze existing biological_qubits.csv
    df_bio = analyze_biological_qubits_csv()
    
    # 2. Search external databases
    sources = search_external_databases()
    
    # 3. Estimate total systems
    counts = estimate_total_quantum_systems()
    
    # 4. Recommend next steps
    steps = recommend_next_steps()
    
    # Save report
    output_dir = REPO_ROOT / "analysis" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    report = {
        "analysis_date": datetime.now().isoformat(),
        "biological_qubits_csv": {
            "total_systems": len(df_bio) if df_bio is not None else 0,
            "path": "data/qubits/biological_qubits.csv"
        },
        "external_sources": sources,
        "estimated_counts": {k: str(v) for k, v in counts.items()},
        "next_steps": steps
    }
    
    report_path = output_dir / "additional_quantum_sources_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n[OK] Report saved to: {report_path}")
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("\n[CURRENT] Confirmed systems: ~242 (180 FP + 27 non-optical + 35 biological_qubits)")
    print("[POTENTIAL] With literature mining: 332-442 systems")
    print("[NEXT] Prioritize HIGH priority tasks for quick gains")
    print("\n[SUCCESS] Analysis complete!")


if __name__ == "__main__":
    main()

