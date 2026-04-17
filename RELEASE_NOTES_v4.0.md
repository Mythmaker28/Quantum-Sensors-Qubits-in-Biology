# Release Notes - v4.0.0 (Zenodo)

**Release date:** 2026-04-17  
**Scope:** Clean re-release of the v3.0.0 scientific content on a pruned repository.  
**Concept DOI (all versions):** [10.5281/zenodo.17420603](https://doi.org/10.5281/zenodo.17420603).  
**Supersedes:** v3.0.0 (DOI [10.5281/zenodo.19617435](https://doi.org/10.5281/zenodo.19617435)), now **restricted** on Zenodo.  
**Citation:** see `CITATION.cff`.

---

## Why v4.0.0 and not v3.0.1?

The v3.0.0 Zenodo bundle was restricted because it shipped:

1. historical release artefacts (`docs/archive/`, `reports/`, `archive/`, `conversation-bus-module/`, `logs/`) that bloated the public zip with internal logs;
2. a binary `bioRxiv` submission bundle (docx + pdf) whose document metadata embedded the maintainer's personal email address;
3. an NCBI API key that had been committed to history in `config/env_template.txt`.

Because the v3 slot was already occupied on Zenodo by an October 2025 pre-release, and because the v3.0.0 DOI is permanently associated with the flawed bundle, the clean re-release is published as **v4.0.0** with identical scientific content.

All sensitive data has been redacted on the active branch; the NCBI API key must be rotated by the maintainer outside this repository.

---

## What changed versus v3.0.0 (repository only)

No data or schema change. Only repository hygiene:

- Removed `archive/` (all pre-v3 historical snapshots, ~56 MB).
- Removed `docs/archive/` (old release reports: `DEPLOYMENT_SUMMARY.md`, `DIAGNOSTIC_*.md`, `LIVRAISON_v2.*.md`, `REPORT.md`, etc.).
- Removed `reports/` (per-version QA logs such as `CLEANUP_LOG_v2.1.md`, `AUDIT_v2.2.md`, `CLEANUP_PRECHECK.md`).
- Removed `conversation-bus-module/` (internal agent-debate module, not scientific content).
- Removed `logs/`, `.atlas_sync/`, `.n_sys`, `CITATION_v1.2.1.cff` (obsolete artefacts).
- Removed the `submission/bioRxiv/` bundle (moved to archive in the final v3 audit; not tracked in v4).
- Redacted the maintainer's email address from `atlas/ecosystem/BRIDGE_ISING_LIFE_LAB.md`, `docs/LAB_USAGE_GUIDE.md`, `metadata/fair/codemeta.json`, and any remaining archived text files.
- Redacted the NCBI API key from `config/env_template.txt` and from the archived git-command log; the key must be rotated.
- Added 8 biosensors that were missed at the v3 data cut-off (FR-GECO1a/1c, NEMOf/c, LifeCamp, ASAP6.1/6b, GRAB-NE2h) to the FP atlas (187 → 195 rows).

Net effect: the public zip shrinks dramatically, no binary with embedded metadata, no internal logs.

---

## Scientific content (unchanged vs v3.0.0)

Version 4.0.0 preserves every v3.0.0 contribution:

- New class **A' (A-prime)** of fluorescent-protein (FP) qubits with direct ODMR readout.
- Single source of truth for qubits: `data/qubits/biological_qubits_v3.csv` (82 systems).
- Refresh of classes B, C, D with 2024 to 2026 literature.
- FP biosensor atlas at 195 rows (`data/processed/atlas_fp_optical_v3_curated.csv`).
- Updated validators, analysis scripts, and a curated schema.

### Headline numbers

| Metric | v2.2.2 | v4.0.0 | Delta |
|--------|--------|--------|-------|
| Qubits total | 34 | 82 | +48 |
| Class A | 3 | 3 | 0 |
| Class A' (new) | 0 | 8 | +8 |
| Class B | 15 | 31 | +16 |
| Class C | 12 | 23 | +11 |
| Class D | 4 | 17 | +13 |
| FP biosensors (curated) | 180 | 195 | +15 |
| Missing FP licences | 113 | 50 | -63 |
| Missing FP PMCIDs | 148 | 88 | -60 |

### Class A' (A-prime): FP-qubits with direct ODMR

The 2024 to 2025 literature established that fluorescent proteins and engineered flavin systems support room-temperature ODMR:

- **EYFP** - Singh et al., Nature 2025 (DOI `10.1038/s41586-025-09417-w`): coherent control at 80 K and 293 K.
- **MagLOV / MagLOV 2** - Nature 2025 (DOI `10.1038/s41586-025-09971-3`): LOV2-derived FMN SCRP with engineered singlet-to-triplet mixing.
- **mScarlet + FMN, mCherry + FMN, mScarlet-I + FMN** - bioRxiv 2025.02.27.640669: flavin-mediated SCRPs reporting through red-shifted FP fluorescence.
- **DmCry (purified)** - Nature 2025 (DOI `10.1038/s41586-025-09971-3`): Drosophila cryptochrome controlled with microwaves.

See [`docs/FP_QUBITS_ODMR_2025.md`](docs/FP_QUBITS_ODMR_2025.md) for the full narrative.

### Fluorescent biosensor atlas

Added in v3.0.0 and kept in v4.0.0:

- CaBLAM, HaloDA1.0, iGluSnFR4f/s, ASAP4.4-Kv, PinkyCaMP, OCaMP / O-GECO2.

Added in the final v3 audit and shipped in v4.0.0:

- FR-GECO1a / FR-GECO1c (far-red GECIs, Nat Commun 2025).
- NEMOf / NEMOc (Nat Methods 2023).
- LifeCamp (bioRxiv 2025, FLIM calcium sensor).
- ASAP6.1 / ASAP6b (bioRxiv 2024, voltage GEVIs).
- GRAB-NE2h (Neuron 2024).

---

## Validation status

- `python scripts/qa/validate_qubits_data.py --input data/qubits/biological_qubits_v3.csv` returns **0 critical errors** and 2 physically legitimate warnings (77 K and 80 K).
- FP atlas row count: 195, no duplicate `protein_name`.
- Qubit dataset: no duplicate `(Classe, Systeme)`.

## Compatibility notes

- No schema change vs v3.0.0; any analysis code built against v3 works unmodified.
- v1.2.1 remains frozen for the Frontiers manuscript. Its DOI (`10.5281/zenodo.17420604`) is unchanged.
- v3.0.0 is restricted on Zenodo; cite v4.0.0 or the concept DOI (`10.5281/zenodo.17420603`) instead.

## Known limitations

- Some Tier 2 (candidates) and Tier 3 (unknown) FP rows still lack licences or PMCIDs after automated enrichment.
- Two qubit rows trigger temperature warnings (77 K FMO and 80 K FND) that are physically legitimate; the validator reports them as `WARN`, not `ERROR`.

## Security note

The NCBI API key that appeared in an earlier commit of `config/env_template.txt` is redacted on the current tree but remains visible in git history. The maintainer should revoke and regenerate the key in the NCBI account dashboard.
