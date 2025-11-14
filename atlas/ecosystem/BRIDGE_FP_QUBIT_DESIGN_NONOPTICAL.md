# Bridge — Atlas Non-Optical ↔ fp-qubit-design

**Date :** 2025-11-13  
**Purpose :** ML workflows for spin qubits, radical pairs, nuclear spins design  
**Status :** MVP (v0.1) — Conceptual, not yet implemented in fp-qubit-design

---

## Current State (fp-qubit-design)

**As of 2025-11** (per MODALITY_SPLIT.md) :
- ✅ 34 systems catalogued (62% non-optical)
- ✅ Classification NMR/ESR/ODMR implemented
- ✅ Optical FP ML pipeline (Atlas v2.2.2 curated → training data)
- ❌ Non-optical ML workflows **not yet implemented**

**Opportunity :** Extend fp-qubit-design to **predict** T2, field sensitivity, coupling strength for non-optical systems.

---

## Proposed Workflows

### Workflow 1: Spin Qubit T2 Prediction

**Goal :** Predict T2 coherence time given defect type, host material, temperature

**Training Data (Atlas) :**
- **Source :** `spin_qubit_candidates.csv` (9 systems → **insufficient**, need expansion to 25+)
- **Features :**
  - `system_type` (NV_center, SiC_defect, SiV_center, etc.) — categorical
  - `host_material` (diamond, silicon_carbide) — categorical
  - `temperature_K` (4K → 298K) — continuous
  - (Future: isotopic purity, defect density)
- **Target :** `T2_microseconds` — continuous

**Model :** Random Forest Regression (handles categorical + continuous features)

**Validation :** Leave-one-out cross-validation (LOOCV, n=9 insufficient for train/test split)

**Expected Performance :** R² ~0.6-0.8 (limited by small dataset)

---

### Workflow 2: Radical Pair Field Sensitivity Prediction

**Goal :** Predict magnetic field sensitivity given protein structure

**Training Data (Atlas) :**
- **Source :** `radical_pair_candidates.csv` (7 systems → **insufficient**, need 20+)
- **Features :**
  - `protein_or_complex` → derive structural features (FAD-Trp distance, if PDB available)
  - `organism` → phylogenetic embedding
  - `temperature_K` — continuous
- **Target :** `field_sensitivity_uT` — continuous (only 1 system has data: robin Cry4 = 50 µT)

**Model :** Linear regression (insufficient data for complex models)

**Limitation :** **Only 1 data point** (RP_CRY_001 has field_sensitivity). **Cannot train model** until ≥5 systems with field_sensitivity measured.

---

### Workflow 3: Nuclear Spin Coupling Strength Prediction

**Goal :** Predict hyperfine coupling strength (NV-¹³C, NV-¹⁴N) given nucleus distance

**Training Data (Atlas) :**
- **Source :** `nuclear_spin_candidates.csv` (7 systems, 4 have coupling_strength_Hz)
- **Features :**
  - `nucleus` (¹³C, ¹⁴N, ¹⁵N, ³¹P, ²⁹Si) — categorical
  - `host` (diamond_NV_coupled, silicon_bulk, etc.) — categorical
  - (Future: nucleus-NV distance from crystal structure)
- **Target :** `coupling_strength_Hz` — continuous

**Model :** K-Nearest Neighbors (n=4 data points, simple model only)

**Validation :** LOOCV (n=4, high variance expected)

---

## ML Pipeline Architecture (Proposed)

```
Atlas Non-Optical CSV
    ↓
Feature Engineering
    │
    ├─ Categorical encoding (one-hot, target encoding)
    ├─ Missing value imputation (mean/median/mode)
    └─ Feature scaling (StandardScaler)
    ↓
Train/Test Split (or LOOCV if n<20)
    ↓
Model Training
    │
    ├─ Spin Qubits: Random Forest
    ├─ Radical Pairs: Linear Regression (data insufficient)
    └─ Nuclear Spins: KNN (n=4, minimal model)
    ↓
Validation Metrics (R², MAE, RMSE)
    ↓
Prediction Service
    │
    └─ Input: system_type, temperature, host
        Output: T2_predicted ± uncertainty
```

---

## Implementation Checklist (fp-qubit-design)

### Phase 1: Data Preparation
- [ ] Import Atlas non-optical CSV (spin, radical, nuclear)
- [ ] Feature engineering (encode categorical, scale continuous)
- [ ] Handle missing values (T2, coupling_strength, field_sensitivity)

### Phase 2: Model Training
- [ ] Spin qubits: Train Random Forest (T2 prediction)
- [ ] Nuclear spins: Train KNN (coupling strength prediction)
- [ ] (Defer radical pairs until ≥5 field_sensitivity data points)

### Phase 3: Validation
- [ ] LOOCV for spin qubits (n=9)
- [ ] LOOCV for nuclear spins (n=4)
- [ ] Report R², MAE, confidence intervals

### Phase 4: Prediction Interface
- [ ] Create API: `predict_T2(system_type, temperature_K)`
- [ ] Create API: `predict_coupling_strength(nucleus, host)`
- [ ] Integrate with fp-qubit-design web interface

---

## Example Usage (Hypothetical)

```python
from fp_qubit_design.ml.predictors import predict_spin_T2

# Predict T2 for new SiC defect
system = {
    'system_type': 'SiC_defect',
    'host_material': 'silicon_carbide',
    'temperature_K': 298
}

T2_pred, T2_std = predict_spin_T2(system)
print(f"Predicted T2: {T2_pred:.1f} ± {T2_std:.1f} µs")
# Output: Predicted T2: 180.0 ± 50.0 µs (based on VSi @ 298K)
```

---

## Data Requirements

| Workflow | Current Data | Minimum Needed | Target (Ideal) |
|----------|--------------|----------------|----------------|
| **Spin T2 prediction** | 9 systems | 20 systems | 50+ systems |
| **Radical field sensitivity** | 1 system | 5 systems | 20+ systems |
| **Nuclear coupling strength** | 4 systems | 10 systems | 30+ systems |

**Action :** Atlas curation must expand non-optical datasets (see DW-NO1, DW-NO2, DW-NO3 in diagnostic).

---

## Design Choices

### Why Not Deep Learning?
**Reason :** Insufficient data (n=9, 7, 7 vs typical DL requirement n>1000)  
**Alternative :** Use **transfer learning** from related domains (materials science T2 databases) if available

### Why Random Forest for Spin Qubits?
**Reason :** Handles categorical features (system_type, host_material) + continuous (temperature) well. Robust to small datasets (n=9).

### Why Not Radical Pairs Yet?
**Reason :** Only 1 data point for field_sensitivity → **Cannot train**. Need ≥5 data points minimum (DW-NO1 will add 13 radical pairs).

---

## Connexions Complémentaires

### Atlas → fp-qubit-design → ising-life-lab
**Loop :** Atlas (data) → fp-qubit-design (ML predict) → ising-life-lab (simulate dynamics) → feedback to Atlas (validate predictions)

### Atlas → fp-qubit-design → experimental labs
**Loop :** Predict optimal SiC polytype (4H vs 6H) → lab synthesizes → measure T2 → update Atlas

---

## Limitations & TODO

### Current Limitations
- ❌ **Data insufficient** for robust ML (n=9, 7, 7)
- ❌ **No structural features** (PDB coordinates for radical pairs)
- ❌ **No uncertainty quantification** (confidence intervals not implemented)

### TODO (v0.2+)
- [ ] Expand Atlas non-optical to 20+ systems per modality (DW-NO1, DW-NO2, DW-NO3)
- [ ] Add PDB-derived features (FAD-Trp distance for radical pairs)
- [ ] Implement Bayesian models (uncertainty quantification)
- [ ] Add isotopic purity feature (¹²C vs ¹³C enrichment for diamond)
- [ ] Validate predictions experimentally (collaborate with labs)

---

**Last updated :** 2025-11-13  
**Status :** ⚠️ Conceptual (not yet implemented in fp-qubit-design)  
**Next steps :** Wait for Atlas expansion (20+ systems per modality), then implement ML pipelines

