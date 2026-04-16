# ATLAS STATUS - Quantum Systems Biological Atlas

**Generated:** 2025-11-19 03:26:17  
**Repository:** QBitAtlas (Quantum-Sensors-Qubits-in-Biology)

---

## SUMMARY

### Total Systems

- **n_total_systems**: 117
- **n_high** (Data_Quality_Atlas = HIGH): 12
- **n_medium** (Data_Quality_Atlas = MEDIUM): 60
- **n_low** (Data_Quality_Atlas = LOW): 45
- **n_incomplete** (Data_Quality_Atlas = INCOMPLETE): 0

### Quality Breakdown

| Quality Level | Count | Percentage |
|---------------|-------|------------|
| HIGH | 12 | 10.3% |
| MEDIUM | 60 | 51.3% |
| LOW | 45 | 38.5% |
| INCOMPLETE | 0 | 0.0% |

### Data Completeness

- Systems with T1: 30 (25.6%)
- Systems with T2: 91 (77.8%)
- Systems with both T1 and T2: 18 (15.4%)
- Systems with DOI: 117 (100.0%)
- Systems with Classe: 85 (72.6%)

---

## BY CLASS

| Classe | HIGH | MEDIUM | LOW | INCOMPLETE | Total |
|--------|------|--------|-----|------------|-------|
| A | 0 | 3 | 0 | 0 | 3 |
| B | 1 | 20 | 2 | 0 | 23 |
| C | 11 | 8 | 0 | 0 | 19 |
| D | 0 | 9 | 4 | 0 | 13 |
| nuclear_spin | 0 | 4 | 3 | 0 | 7 |
| radical_pair | 0 | 9 | 1 | 0 | 10 |
| spin_qubit | 0 | 7 | 3 | 0 | 10 |


---

## DATA SOURCES

### CSV Files Discovered

- **quantum_systems_unified_v2.csv**
  - Category: qubits_unified
  - Columns: 35
- **quantum_systems_unified.csv**
  - Category: qubits_unified
  - Columns: 35
- **biological_qubits.csv**
  - Category: qubits_biological
  - Columns: 33
- **nonoptical_qubits_consolidated.csv**
  - Category: qubits_nonoptical
  - Columns: 12
- **spin_qubit_candidates.csv**
  - Category: non_optical_staging
  - Columns: 14
- **radical_pair_candidates.csv**
  - Category: non_optical_staging
  - Columns: 12
- **nuclear_spin_candidates.csv**
  - Category: non_optical_staging
  - Columns: 13
- **atlas_fp_optical_v2_2_curated.csv**
  - Category: optical_atlas
  - Columns: 43
- **atlas_fp_optical_v2_2.csv**
  - Category: optical_atlas
  - Columns: 43


---

## DATA GAPS

### Missing T2 by Class

- **Classe C**: 3/19 systems missing T2 (15.8%)
- **Classe nuclear_spin**: 3/7 systems missing T2 (42.9%)
- **Classe D**: 1/13 systems missing T2 (7.7%)
- **Classe B**: 3/23 systems missing T2 (13.0%)
- **Classe spin_qubit**: 3/10 systems missing T2 (30.0%)


### Missing T1 by Class

- **Classe C**: 3/19 systems missing T1 (15.8%)
- **Classe nuclear_spin**: 7/7 systems missing T1 (100.0%)
- **Classe D**: 13/13 systems missing T1 (100.0%)
- **Classe radical_pair**: 10/10 systems missing T1 (100.0%)
- **Classe B**: 17/23 systems missing T1 (73.9%)
- **Classe spin_qubit**: 10/10 systems missing T1 (100.0%)
- **Classe A**: 3/3 systems missing T1 (100.0%)


---

## SUSPICIOUS ENTRIES

**3 systems flagged as suspicious:**

- 29Si in silicon (bulk) (Classe: C): ; T2_out_of_range
- 29Si in silicon (bulk) (Classe: nuclear_spin): ; T2_out_of_range
- nan (Classe: nan): ; T1_out_of_range


---

## UNIFIED DATASET

**File:** `data/qubits/quantum_systems_unified_final.csv`

This file contains all systems from all discovered CSV files, deduplicated and cleaned.

**Key Features:**
- Deduplication by Systeme/Classe/DOI combination
- Decimal precision cleaned (T1_s: 3 decimals, T2_us: 2 decimals, etc.)
- Physical value validation (out-of-range values flagged)
- Quality scores assigned (HIGH/MEDIUM/LOW/INCOMPLETE)
- No invented values - all data from source CSVs only

---

**End of Report**
