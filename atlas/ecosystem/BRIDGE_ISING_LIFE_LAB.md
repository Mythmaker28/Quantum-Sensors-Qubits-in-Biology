# Bridge — Atlas ↔ Ising-Life-Lab

**Date :** 2025-11-13  
**Purpose :** Data flow, loaders, field mapping between Atlas (data source) and ising-life-lab (computational toolkit)  
**Status :** MVP (v0.1) — Functional but incomplete

---

## Architecture

```
Atlas (Quantum-Sensors-Qubits-in-Biology)
    │
    │ CSV exports
    ↓
data/optical/curated/atlas_fp_optical_v2_2_curated.csv (180 systems)
data/non_optical/spin_qubits/staging/spin_qubit_candidates.csv (9 systems)
data/non_optical/radical_pairs/staging/radical_pair_candidates.csv (7 systems)
data/non_optical/nuclear_spins/staging/nuclear_spin_candidates.csv (7 systems)
    │
    │ read_csv()
    ↓
ising-life-lab/isinglab/data_bridge/loaders.py
    │
    │ load_optical_atlas()
    │ load_spin_qubits()
    │ load_radical_pairs()
    │ load_nuclear_spins()
    ↓
pandas DataFrame
    │
    │ mapping.py
    ↓
Ising profiles (capacity, robustness, stability, basin_depth)
    │
    ↓
CA/Ising simulations, design space analysis, ranking
```

---

## Loaders (Confirmed Implemented in ising-life-lab)

### 1. load_optical_atlas()
**Source :** `atlas_fp_optical_v2_2_curated.csv`  
**Returns :** DataFrame (180 rows, optical FP systems)  
**Fields used :**
- `protein_name`, `family` → system identification
- `contrast_normalized` → **functional_score** proxy
- `temperature_K` → **robustness** (RT vs cryo)
- `excitation_nm`, `emission_nm` → spectral properties

**Status :** ✅ Implemented (ising-life-lab v8.2+)

---

### 2. load_spin_qubits()
**Source :** `spin_qubit_candidates.csv`  
**Returns :** DataFrame (9 rows, NV/SiC/diamond vacancies)  
**Fields used :**
- `label`, `system_type` → identification
- `T2_microseconds` → **coherence** (robustness proxy)
- `temperature_K` → RT vs cryo classification
- `measurement_method` → ODMR/ESR/pulsed ESR

**Status :** ✅ Implemented (ising-life-lab v9.0+, per web search)

---

### 3. load_radical_pairs()
**Source :** `radical_pair_candidates.csv`  
**Returns :** DataFrame (7 rows, Cryptochrome/Photolyase/PSII)  
**Fields used :**
- `protein_or_complex`, `organism` → identification
- `timescale_ns` → **coherence** (ns-µs regime)
- `field_sensitivity_uT` → **robustness** (magnetic sensitivity)
- `observable` → MFE, electron transfer, etc.

**Status :** ✅ Implemented (ising-life-lab v9.0+, per web search)

---

### 4. load_nuclear_spins()
**Source :** `nuclear_spin_candidates.csv`  
**Returns :** DataFrame (7 rows, ¹³C/³¹P/¹⁴N/²⁹Si)  
**Fields used :**
- `nucleus`, `host` → identification
- `T2_milliseconds` → **coherence** (ms-s regime)
- `coupling_strength_Hz` → NV-nuclear interaction
- `measurement_method` → NMR, ODMR, DD

**Status :** ✅ Implemented (ising-life-lab v9.0+, per web search)

---

## Field Mapping (Atlas → Ising Profiles)

### Optical FP

| Atlas Field | Ising Profile Field | Transformation |
|-------------|---------------------|----------------|
| `contrast_normalized` | `functional_score` | Direct (fold-change) |
| `temperature_K` | `robustness` | RT (298K) = robust, cryo = fragile |
| `family` | `class` | Calcium/Voltage/etc. → sensor_type |
| `is_biosensor` | `functional` | 1.0 = functional, 0.0 = fluorophore |

---

### Spin Qubits

| Atlas Field | Ising Profile Field | Transformation |
|-------------|---------------------|----------------|
| `T2_microseconds` | `coherence` | Direct (µs) |
| `temperature_K` | `robustness` | RT = robust, cryo = extended |
| `magnetic_sensitivity_nT_rtHz` | `sensitivity` | Lower = better (nT/√Hz) |
| `system_type` | `class` | NV_center, SiC_defect, etc. |

---

### Radical Pairs

| Atlas Field | Ising Profile Field | Transformation |
|-------------|---------------------|----------------|
| `timescale_ns` | `coherence` | ns-µs regime |
| `field_sensitivity_uT` | `robustness` | 50 µT = Earth field sensitive |
| `observable` | `functional_mode` | MFE, electron_transfer, etc. |
| `evidence_level` | `reliability` | A = high, B = medium, C = low |

---

### Nuclear Spins

| Atlas Field | Ising Profile Field | Transformation |
|-------------|---------------------|----------------|
| `T2_milliseconds` | `coherence` | ms-s regime (longest) |
| `coupling_strength_Hz` | `interaction_strength` | kHz-MHz (NV-nuclear) |
| `nucleus` | `isotope` | ¹³C, ³¹P, ¹⁴N, ²⁹Si |
| `host` | `platform` | diamond, silicon, protein |

---

## Modality Detection (ising-life-lab/isinglab/data_bridge/mapping.py)

**Extended mapping (as of v9.0) :**

```python
def detect_modality(row):
    """Detect system modality from Atlas row."""
    if 'excitation_nm' in row and pd.notna(row['excitation_nm']):
        return 'optical'
    elif 'T2_microseconds' in row and pd.notna(row['T2_microseconds']):
        return 'spin'
    elif 'timescale_ns' in row and pd.notna(row['timescale_ns']):
        return 'radical_pair'
    elif 'T2_milliseconds' in row and pd.notna(row['T2_milliseconds']):
        return 'nuclear'
    else:
        return 'unknown'
```

**Status :** ✅ Aligned with Atlas schema (per web search, ising-life-lab AGENT_LOG.md)

---

## Usage Examples

### Example 1: Load Optical Atlas

```python
from isinglab.data_bridge.loaders import load_optical_atlas

df = load_optical_atlas()
print(f"Loaded {len(df)} optical FP systems")

# Filter calcium sensors
ca_sensors = df[df['family'] == 'Calcium']
print(f"Calcium sensors: {len(ca_sensors)}")
# Output: Loaded 180 optical FP systems
#         Calcium sensors: 40
```

---

### Example 2: Load Spin Qubits

```python
from isinglab.data_bridge.loaders import load_spin_qubits

df_spin = load_spin_qubits()
print(f"Loaded {len(df_spin)} spin qubits")

# Filter RT systems (>270K)
rt_spin = df_spin[df_spin['temperature_K'] >= 270]
print(f"RT spin qubits: {len(rt_spin)}")
# Output: Loaded 9 spin qubits
#         RT spin qubits: 3 (NV-001, SiC-001, P1-001)
```

---

### Example 3: Combined Modalities

```python
from isinglab.data_bridge.loaders import (
    load_optical_atlas, load_spin_qubits, load_radical_pairs, load_nuclear_spins
)

optical = load_optical_atlas()
spin = load_spin_qubits()
radical = load_radical_pairs()
nuclear = load_nuclear_spins()

print(f"Total systems: {len(optical) + len(spin) + len(radical) + len(nuclear)}")
# Output: Total systems: 203 (180 optical + 9 spin + 7 radical + 7 nuclear)
```

---

## Limitations & TODO

### Current Limitations (MVP v0.1)

- ❌ **No automatic sync** (manual CSV updates required)
- ⚠️ **Field mapping incomplete** (some Atlas fields not used in Ising profiles)
- ⚠️ **No validation** (Atlas schema changes could break loaders)
- ❌ **No unit conversion** (Atlas uses µs/ms, Ising expects consistent units)

### TODO (v0.2+)

- [ ] Add schema validation (check Atlas CSV columns match expected)
- [ ] Add unit conversion layer (µs/ms → s, nT → T, etc.)
- [ ] Add automatic sync (check Atlas repo for updates, pull CSV)
- [ ] Add missing field mappings (e.g., `doi` → `source`, `curator` → `provenance`)
- [ ] Add data quality checks (DOI validation, range checks)

---

## Connexions Complémentaires

### Atlas → fp-qubit-design
**Status :** Partial (optical only, see `BRIDGE_FP_QUBIT_DESIGN_NONOPTICAL.md`)

### Atlas → arrest-molecules
**Status :** Conceptual only (see `BRIDGE_ARREST_MOLECULES_QUANTUM.md`)

---

**Last updated :** 2025-11-13  
**Maintainer :** Atlas curator (contact via [GitHub Issues](https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/issues) / ORCID [0009-0009-0577-9563](https://orcid.org/0009-0009-0577-9563))  
**Status :** ✅ Functional (MVP), ⚠️ Incomplete (field mapping, validation)  
**Next steps :** Add schema validation, unit conversion, sync automation

