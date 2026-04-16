# Release Notes - v3.0.0 (Zenodo)

**Release date:** 2026-04-17  
**Scope:** Biological Qubits and Quantum Sensors Atlas, full dataset + documentation refresh.  
**Zenodo DOI (v3.0.0):** [10.5281/zenodo.19617435](https://doi.org/10.5281/zenodo.19617435).  
**Concept DOI (all versions):** [10.5281/zenodo.17420603](https://doi.org/10.5281/zenodo.17420603).  
**Citation:** see `CITATION.cff` (root) for the v3.0.0 block and `CITATION_v1.2.1.cff` for the frozen Frontiers release.

---

## Summary

Version 3.0.0 is a major consolidation release. It:

- introduces the new class **A' (A-prime)** of fluorescent-protein (FP) qubits with direct ODMR readout;
- merges every historical qubit CSV into a single source of truth (`data/qubits/biological_qubits_v3.csv`, 82 systems);
- refreshes classes B, C, D with 2024 to 2026 literature (non-optical qubits, hyperpolarised nuclei, radical-pair mechanisms);
- extends the FP biosensor atlas with seven 2024 to 2026 biosensors and completes missing licences / PMCIDs via Unpaywall and the NCBI ID Converter;
- ships updated validators, analysis scripts, and a curated 35-column schema.

## Headline numbers

| Metric | v2.2.2 | v3.0.0 | Delta |
|--------|--------|--------|-------|
| Qubits total | 34 | 82 | +48 |
| Class A | 3 | 3 | 0 |
| Class A' (new) | 0 | 8 | +8 |
| Class B | 15 | 31 | +16 |
| Class C | 12 | 23 | +11 |
| Class D | 4 | 17 | +13 |
| FP biosensors (curated) | 180 | 187 | +7 |
| Missing FP licences | 113 | 50 | -63 |
| Missing FP PMCIDs | 148 | 88 | -60 |

## Class A' (A-prime): FP-qubits with direct ODMR

The 2024 to 2025 literature established that fluorescent proteins and engineered flavin systems support room-temperature ODMR:

- **EYFP** - Singh et al., Nature 2025 (DOI `10.1038/s41586-025-09417-w`): coherent control at 80 K and 293 K, OADF readout, AC sensitivity upper bound 183 fT·mol^{1/2}·Hz^{-1/2} at 80 K, 93 pT·mol^{1/2}·Hz^{-1/2} at room temperature.
- **MagLOV / MagLOV 2** - Nature 2025 (DOI `10.1038/s41586-025-09971-3`): LOV2-derived FMN SCRP with engineered singlet-to-triplet mixing, RYDMR readout.
- **mScarlet + FMN, mCherry + FMN, mScarlet-I + FMN** - bioRxiv 2025.02.27.640669: flavin-mediated SCRPs reporting through red-shifted FP fluorescence.
- **DmCry (purified)** - Nature 2025 (DOI `10.1038/s41586-025-09971-3`): Drosophila cryptochrome controlled with microwaves.

Class A' systems inherit the genetic targetability of FPs and the physical accessibility of spin qubits, which closes a long-standing gap between classes A (FP optical reporters) and B (solid-state colour centres).

See [`docs/FP_QUBITS_ODMR_2025.md`](docs/FP_QUBITS_ODMR_2025.md) for the full narrative.

## Class B (solid-state colour centres, 2024 to 2026)

Added or updated:
- SiC divacancy defects (Wolfowicz et al. 2024 Nat Commun; Anderson et al. 2024 Nat Mater).
- Alkene-functionalised NV nanodiamonds for bio-conjugation (2024).
- BNNT spin defects (ACS Nano 2025).
- SnV and GeV nanodiamonds for in vivo thermometry (Nano Lett 2024).
- FND thermometry in vivo (Nat Commun 2025).
- hBN colour centres for quantum sensing at 300 K (Nat Photon 2025).

## Class C (hyperpolarised nuclei and clinical translation)

Added or updated:
- First-in-human HP 13C,15N2-urea renal perfusion MRI (Nat Biomed Eng 2025).
- FDA-cleared 129Xe pulmonary MRI (Xenoview, clinical workflow updates).
- HP 13C pyruvate clinical trials (Oncology 2024 to 2025).
- 31P-in-silicon donor benchmark (new cryogenic calibration reference).

## Class D (radical-pair mechanisms)

Added:
- Flavin-Guanine radical pair in DNA with MFE 65 % (Comm Chem 2025, `10.1038/s42004-025-01596-x`).
- Photolyase oxetane intermediate radical pair (Comm Chem 2025).
- Room-temperature FMO coherence with resolved lineshapes (Sci Adv 2025).
- GgCry4a (chicken cryptochrome 4a, JACS 2025).

Deprecated / annotated:
- ErCry1-type rows marked `deprecated` in `Verification_statut` based on 2025 evidence that ErCry1 is circadian rather than magnetoreceptive.
- Cryptochrome 1a assignment superseded by ErCry4a-centred evidence; kept in the dataset for traceability.

## Fluorescent biosensor atlas

Added:
- CaBLAM (Nat Methods 2026, `10.1038/s41592-025-02972-0`): bioluminescent Ca2+ with ~83x in vitro contrast.
- HaloDA1.0 (Science 2025, `10.1126/science.adt7705`): far-red chemigenetic dopamine sensor.
- iGluSnFR4f and iGluSnFR4s (Nat Methods 2026, `10.1038/s41592-025-02965-z`): 4th-generation glutamate indicators.
- ASAP4.4-Kv (Nat Commun 2025, `10.1038/s41467-025-61774-2`): positively-tuned soma-targeted voltage GEVI.
- PinkyCaMP (bioRxiv 2024, `10.1101/2024.12.16.628673`): mScarlet-based red calcium indicator.
- OCaMP / O-GECO2 (bioRxiv 2025, `10.1101/2025.07.28.667269`): orange calcium indicator optimised for 1030 nm 2P.

Licences and PMCIDs for 63 + 60 rows respectively were filled via Unpaywall and the NCBI ID Converter (see `reports/FP_LICENSE_PMCID_log.md`).

## Data infrastructure

- Single canonical qubits CSV: `data/qubits/biological_qubits_v3.csv`.
- Canonical schema documented in `data/qubits/SCHEMA_v3.md` (35 columns).
- Legacy qubit CSVs archived under `data/qubits/archive/pre_v3/` with a dedicated `README_ARCHIVE.md`.
- FP atlas shipped at `data/optical/curated/atlas_fp_optical_v3_curated.csv` (mirrored in `data/processed/`).
- `scripts/qa/validate_qubits_data.py` updated: temperature range widened to 1-400 K, year range 1980-2027, class `A_prime` accepted.
- `analysis/qubits_stats.py` now accepts `--input` and `--version`.

## Validation status

- `python scripts/qa/validate_qubits_data.py --input data/qubits/biological_qubits_v3.csv` returns **0 critical errors** and 2 warnings (legitimate cryogenic contexts at 77 K and 80 K).
- FP atlas row count: 187, no duplicate `protein_name`.
- Qubit dataset: no duplicate `(Classe, Systeme)`; DOI co-occurrences only for shared-paper entries (EYFP 80 K vs 295 K; DmCry / MagLOV / MagLOV2; mScarlet / mCherry / mScarlet-I; NV vs P1).

## Reproducibility

All enrichment steps are captured in scripts and logs:

- `scripts/etl/build_qubits_v3.py` -> `reports/BUILD_QUBITS_V3_LOG.md`
- `scripts/etl/add_class_A_prime.py`
- `scripts/etl/enrich_v3_literature_2024_2026.py` -> `reports/ENRICHMENT_v3_log.md`
- `scripts/etl/deprecate_invalidated_cryptochromes.py`
- `scripts/etl/enrich_fp_atlas_v3_2024_2026.py` -> `reports/FP_ENRICHMENT_v3_log.md`
- `scripts/etl/complete_fp_licenses_pmcids.py` -> `reports/FP_LICENSE_PMCID_log.md`

## Compatibility notes

- v3.0 intentionally breaks the `data/qubits/biological_qubits.csv` contract. The legacy path is preserved via the archive but will no longer be updated.
- v1.2.1 remains frozen for the Frontiers manuscript. Its DOI (`10.5281/zenodo.17420604`) and citation file are unchanged.
- v3.0.0 is archived on Zenodo: DOI `10.5281/zenodo.19617435` (concept DOI `10.5281/zenodo.17420603`).
- Dashboard (`docs/index.html`) has been regenerated for v3.0 to expose class A' and the refreshed numbers.

## Known limitations

- Some Tier 2 (candidates) and Tier 3 (unknown) FP rows still lack licences or PMCIDs after automated enrichment.
- Two qubit rows trigger temperature warnings (77 K FMO and 80 K FND) that are physically legitimate; the validator reports them as `WARN`, not `ERROR`.

## Acknowledgements

The v3.0 release was produced from the `release/v3.0` branch with a full safety commit on `main`. The plan `atlas_qubits_v3.0_zenodo_c73fc676.plan.md` (not versioned) served as the internal checklist.
