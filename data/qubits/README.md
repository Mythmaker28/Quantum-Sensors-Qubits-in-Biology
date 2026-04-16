# Biological Qubits Dataset (v3.0)

Single source of truth for genuine quantum systems (qubits and spin sensors)
documented in biological contexts. This dataset is distinct from the
fluorescent-protein optical atlas (`data/processed/atlas_fp_optical_*.csv`).

## Primary file

`biological_qubits_v3.csv` — **58 curated systems** after consolidation of the
legacy v2.3 dataset and pre-v3 cross-checks. Each row describes one quantum
system with coherence metrics (T1, T2), readout method, host context, and
provenance (DOI, year, quality tier).

**Schema**: see `SCHEMA_v3.md` (35 columns).

## Classes

| Class | Description | Count (v3.0 initial) |
| --- | --- | --- |
| A | Bio-intrinsic electron-spin qubits (protein radicals, FP ODMR) | 3 |
| A' (planned) | FP-qubits with direct ODMR readout (EYFP, MagLOV, mScarlet+FMN, 2025+) | 0 → to be added in Phase 2 |
| B | Engineered solid-state spin defects in biological hosts (NV, VSi, SnV, GeV, SiC, hBN, BNNT) | 23 |
| C | Hyperpolarized nuclear spins (13C, 15N, 129Xe) | 19 |
| D | Radical-pair candidates and controversial bio-quantum mechanisms | 13 |

After Phase 2 and 3 enrichment the target is **~85-100 systems**.

## Archive

Legacy CSV/JSON files from v1.2.1 through v2.3 have been moved to
`archive/pre_v3/`. See `archive/pre_v3/README_ARCHIVE.md`.

The following files are superseded and must not be edited:
- `biological_qubits.csv` (v1.2.1, 34 systems)
- `quantum_systems_unified.csv`, `_v2.csv`, `_v2_3.csv`, `_final.csv`
- `nonoptical_qubits_consolidated.csv`
- `environment_recategorization_log.csv`

Any updates go into `biological_qubits_v3.csv` through
`scripts/etl/build_qubits_v3.py` or the Phase 2/3 enrichment scripts.

## Relationship to the FP optical atlas

| Aspect | `biological_qubits_v3.csv` | `atlas_fp_optical_v*.csv` |
| --- | --- | --- |
| Domain | Quantum systems (spin coherence) | Fluorescent-protein biosensors |
| Key observable | T2 coherence time, ODMR contrast | Fluorescence fold-change (dF/F) |
| Readout | ODMR, ESR, NMR | Fluorescence microscopy |
| Quantum addressing | Required (class A-C) or candidate (D) | Not required |
| Typical size | ~60-100 entries | ~180-210 entries |

The two datasets overlap only for class A/A' systems (proteins with both
optical and quantum readout). In that overlap the protein appears with
distinct semantics in each file; downstream joins must use DOI as the key.

## Quick usage

```python
import pandas as pd

qubits = pd.read_csv("data/qubits/biological_qubits_v3.csv")
print(qubits["Classe"].value_counts())

class_b = qubits[qubits["Classe"] == "B"]
print(f"Class B mean T2: {class_b['T2_us'].mean():.2f} us")
```

## Validation

```bash
python scripts/qa/validate_qubits_data.py --input data/qubits/biological_qubits_v3.csv
```

Expected result for the initial v3.0 build: 0 critical errors, 1 documented
warning (FMO complex at 77 K is intentional, see entry notes).

## Provenance

Each row is traceable via the `DOI`, `Source_T1`, `Source_T2`, and
`Source_Contraste` fields. Dataset-level provenance is recorded in the
`dataset_source` column (`biological_qubits_v1`, `nonoptical_merge_v2`,
and future `enrichment_v3_*` markers).

Last regeneration: see `reports/BUILD_QUBITS_V3_LOG.md`.
