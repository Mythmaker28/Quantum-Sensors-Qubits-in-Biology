# Data Directory Structure

## Current Layout (Dual Structure)

### Legacy (Maintained for Compatibility)
```
data/processed/   # Original location (still valid, used by existing scripts)
data/staging/     # Original staging (optical + non-optical mixed)
```

### New (Organized by Modality)
```
data/optical/
  ├── curated/
  │   ├── atlas_fp_optical_v2_2_curated.csv  # 180 Tier 1 systems
  │   └── atlas_fp_optical_v2_2.csv          # 296 mixed (all tiers)
  └── staging/
      ├── atlas_fp_optical_v2_2_candidates.csv  # 13 Tier 2
      └── atlas_fp_optical_v2_2_unknown.csv     # 103 Tier 3

data/non_optical/
  ├── spin_qubits/
  │   └── staging/
  │       └── spin_qubit_candidates.csv       # 13 systems
  ├── radical_pairs/
  │   └── staging/
  │       └── radical_pair_candidates.csv     # 11 systems
  └── nuclear_spins/
      └── staging/
          └── nuclear_spin_candidates.csv     # 11 systems
```

## Recommendation

**For new work :** Use `data/optical/` and `data/non_optical/`  
**For existing scripts :** `data/processed/` still functional (files copied, not moved)

## Synthesis Sheets

See `atlas/systems_by_modality/` for detailed documentation on each family.

