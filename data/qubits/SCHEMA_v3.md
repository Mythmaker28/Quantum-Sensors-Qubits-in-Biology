# biological_qubits_v3.csv — Schema

Canonical schema for the single-source-of-truth qubits table (v3.0).
UTF-8, comma-separated, header on row 1, decimal point.

Total: **35 columns**, in this exact order.

## Required fields (hard validation)

| Column | Type | Description |
| --- | --- | --- |
| `Systeme` | string | Human-readable system name (free text, must be non-empty). |
| `Classe` | enum `A`/`A_prime`/`B`/`C`/`D` | Taxonomic class. |
| `Hote_contexte` | string | Host / biological context (e.g. "Cellules HeLa (in_cellulo)", "bulk", "in_vivo"). |
| `Methode_lecture` | enum | Primary readout. Accepted: `ODMR`, `ESR`, `pulsed_ESR`, `NMR`, `pulsed_NMR`, `DNP_MRI`, `Optical-only`, `radical_pair_detection`, `dynamical_decoupling`, `Indirect`. |
| `Spin_type` | string | `Electron`, `Noyau; <isotope>`, `Electron; paires radicalaires`, or compound. |
| `Temperature_K` | float | Experimental temperature in kelvin (1-400 accepted). |
| `DOI` | string | DOI of the primary reference (canonical form, no URL prefix). |
| `Annee` | float | Year of the primary reference (1980-2027 accepted). |
| `Qualite` | `1`/`2`/`3` | Evidence tier: 1=exploratory, 2=published & replicable, 3=peer-reviewed high-impact / FDA-cleared. |
| `Verification_statut` | enum | `verifie`, `a_confirmer`, `deprecated`. |

## Quantum / measurement fields

| Column | Type | Description |
| --- | --- | --- |
| `Frequence` | string | Operating frequency (e.g. "2.87 GHz", "9.5 GHz (bande X)"). |
| `B0_Tesla` | float | Static magnetic field (T). |
| `Defaut` | string | Defect type when applicable (e.g. `NV`, `VSi`, `GeV`, `Radical-flavine`). |
| `Polytype_Site` | string | Crystallographic polytype / site (e.g. "4H-SiC; k-site"). |
| `T1_s` | float | Longitudinal relaxation time (s). Empty if not measured. |
| `T2_us` | float | Transverse coherence time (µs). |
| `Contraste_%` | float | ODMR / ESR contrast (%). |
| `Taille_objet_nm` | string | Size (nm) or descriptor ("Bulk (capteur µm)", "d:1-2nm; L:100-500nm"). |
| `Source_T2` | string | Figure / table / supplementary citation for T2. |
| `Source_T1` | string | Same for T1. |
| `Source_Contraste` | string | Same for contrast. |
| `T2_us_err` | float | 1-sigma uncertainty on T2 (µs). |
| `T1_s_err` | float | 1-sigma uncertainty on T1 (s). |
| `Contraste_err` | float | 1-sigma uncertainty on contrast (%). |

## Flags and qualitative fields

| Column | Type | Description |
| --- | --- | --- |
| `Hyperpol_flag` | 0/1 | 1 if the system relies on hyperpolarization (DNP, PHIP, SABRE, optical pumping). |
| `Cytotox_flag` | 0/1 | 1 if cytotoxicity is documented. |
| `Toxicity_note` | string | Free text. |
| `Temp_controlled` | 0/1 | 1 if active temperature control required during measurement. |
| `Photophysique` | string | Spectroscopic annotations (excitation / emission / ZPL / lifetime / QY / g-factor / linewidth). |
| `Conditions` | string | Buffer, laser power, microwave pulses, anesthesia, etc. |
| `Limitations` | string | Known limits (photobleaching, stability, clearance, etc.). |
| `In_vivo_flag` | 0/1 | 1 if in vivo measurement is demonstrated in the cited reference. |
| `Notes` | string | Narrative notes, key numbers, context. |

## Provenance

| Column | Type | Description |
| --- | --- | --- |
| `dataset_source` | string | Short provenance tag for the row (e.g. `biological_qubits_v1`, `nonoptical_merge_v2`, `enrichment_v3_A_prime`, `enrichment_v3_B`, ...). |
| `last_updated` | ISO-8601 | UTC timestamp of the last modification of that row. |

## Validation rules

Hard errors:
- Any required field empty or `NA`.
- `Temperature_K` outside `[1, 400]`.
- `Classe` not in `{A, A_prime, B, C, D}`.
- `Qualite` not in `{1, 2, 3}`.
- `Annee` outside `[1980, 2027]`.
- `DOI` without a dot or without `/`.

Warnings:
- `Temperature_K` outside physiological range `[273, 310]` when `Hote_contexte`
  contains `in_cellulo` or `in_vivo`.
- `Hyperpol_flag == 1` but `Classe != C`.
- Suspiciously long `T2_us` (> 1e9 µs i.e. 1000 s) without explicit bulk benchmark context.

## Backward-compatibility mapping (pre-v3 → v3)

| pre-v3 column | v3 column | Notes |
| --- | --- | --- |
| `system_name` | `Systeme` | Rename. |
| `class` | `Classe` | Uppercase enforced. |
| `temperature` | `Temperature_K` | Unit normalized to kelvin. |
| `readout_method` | `Methode_lecture` | Value set extended to include 2025 methods. |
| `T1_seconds` | `T1_s` | Unit explicit. |
| `T2_microseconds` | `T2_us` | Unit explicit. |

Downstream tooling (analysis, dashboard) must read v3 columns only.
