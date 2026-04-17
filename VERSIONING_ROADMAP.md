# Versioning Roadmap - Biological Qubits Atlas

**Last updated:** 2026-04-17

---

## Version history

| Version | Date | Purpose | Systems | Status |
|---------|------|---------|---------|--------|
| **v4.0.0** | 2026-04-17 | Clean re-release of v3.0.0 content on a pruned repository | 82 qubits + 195 FP biosensors | Current stable |
| v3.0.0 | 2026-04-17 | Consolidated release (bundle issues) | 82 qubits + 195 FP biosensors | Restricted on Zenodo |
| v2.2.2 | 2025-10-25 | Balanced dataset for ML (pre-consolidation) | 180 curated FP + 34 qubits | Superseded |
| v2.2.0 | 2025-10-25 | Data boost | 191 total (170 usable) | Superseded |
| v2.1.0 | 2025-10-24 | FPbase integration | 120 | Superseded |
| v2.0.0 | 2025-10-24 | Dashboard & FP extension | 113 | Superseded |
| **v1.2.1** | 2025-10-23 | Frontiers submission | 66 | Frozen (publication) |
| v1.3.0-beta | 2025-10-24 | Pre-release testing | 80 | Superseded |
| v1.2.0 | 2025-10-20 | Initial stable | 66 | Superseded |

---

## Current stable versions

### v4.0.0 (latest stable, research and ML)
- Purpose: research, ML, clinical context, 2024-2026 literature. Clean re-release of v3.0.0 content.
- Qubits: 82 (classes A, A', B, C, D).
- FP biosensors: 195 (Tier 1 curated).
- Files: `data/qubits/biological_qubits_v3.csv`, `data/processed/atlas_fp_optical_v3_curated.csv`.
- Citation: [`CITATION.cff`](CITATION.cff).
- DOI: concept DOI [10.5281/zenodo.17420603](https://doi.org/10.5281/zenodo.17420603) (always resolves to latest).
- Status: active.

### v1.2.1 (Frontiers manuscript)
- Purpose: publication submission (fixed dataset).
- Systems: 66.
- Citation: `CITATION.cff` references section.
- DOI: `10.5281/zenodo.17420604`.
- Status: frozen (do not modify).

---

## Versioning policy

### Why multiple versions coexist

- v1.2.1 is frozen for the Frontiers publication (scientific reproducibility).
- v4.0.0 is the active research and ML release (clean re-release of v3.0.0 content, refreshed with 2024-2026 literature).
- v3.0.0 is restricted on Zenodo (bundle issues); do not cite.
- v2.x references remain reachable via the git history.

Both live versions are citable:
- For Frontiers manuscript references: use v1.2.1 (DOI `10.5281/zenodo.17420604`).
- For research, ML, or clinical-context work: use v4.0.0 (concept DOI `10.5281/zenodo.17420603`).

### How to cite

See [`README.md#citation`](README.md#citation) and [`VERSIONS_CITATION.md`](VERSIONS_CITATION.md).

---

## Migration guide

### Upgrading from v3.0.0 to v4.0.0

No migration is needed. v4.0.0 ships identical scientific content and the same file names. Only the public release bundle differs (internal archives, QA logs, and binary submission files are no longer shipped). If your code references `data/qubits/biological_qubits_v3.csv` or `data/processed/atlas_fp_optical_v3_curated.csv`, it continues to work unchanged.

Update only your citation:
- Replace the version-specific DOI `10.5281/zenodo.19617435` (v3.0.0, restricted) with the concept DOI `10.5281/zenodo.17420603` or the v4.0.0 version-specific DOI once Zenodo assigns it.

### Upgrading from v2.2.2 to v4.0.0

Breaking changes vs v2.2.2:
- Canonical qubit CSV moves from `data/qubits/biological_qubits.csv` (34 rows) to `data/qubits/biological_qubits_v3.csv` (82 rows).
- `Classe` now accepts the new value `A_prime` (FP-qubits with direct ODMR).
- FP atlas canonical path becomes `data/processed/atlas_fp_optical_v3_curated.csv` (195 rows).
- Temperature validator widened to 1-400 K, year validator widened to 1980-2027.

Migration steps:
1. Point pipelines at `biological_qubits_v3.csv` and `atlas_fp_optical_v3_curated.csv`.
2. If you filter by `Classe`, include `A_prime` (or use `Classe IN (A, A_prime, B)` for strict controllable qubits).
3. Re-run validators: `python scripts/qa/validate_qubits_data.py --input data/qubits/biological_qubits_v3.csv` and FP linters.
4. Update citations using `CITATION.cff` (v4.0.0).

---

## Future roadmap

### Post-Nobel 2025 context

Following the 2025 Nobel Prize in Physics (Josephson junctions, superconducting circuits), this atlas positions itself as a complementary exploration of room-temperature quantum platforms for biological applications. Future releases will continue to expand coverage of ambient-temperature systems with an emphasis on biocompatibility and in vivo deployment.

Strategic direction:
- Cryogenic platforms (superconducting qubits) -> ambient platforms (NV centres, FP qubits, hyperpolarised nuclei).
- Isolated quantum systems -> quantum sensors in noisy biological environments.
- Quantum computing -> quantum-enhanced sensing and imaging.

### v4.1.0 (planned Q3 2026)
- Integrate Tier 2 promotions (manual curation of the candidates queue).
- Extend class A' with next-generation FP-qubits reported in 2026.
- Add bootstrap-based confidence intervals for class B coherence times.

### v4.2.0 (planned Q4 2026)
- REST API for programmatic access to qubits and FP biosensors.
- Integration of SciCrunch / RRID identifiers for reagents.

### v5.0.0 (long-term, peer-review target)
- Goal: peer-reviewed Data Descriptor submission (Scientific Data or equivalent).
- Breaking changes: possibly split `Classe` into `Classe_primary` and `Classe_secondary`.
- Milestone: 150+ qubits and 300+ curated FP biosensors with CI-bounded measurements.

### Long-Term Vision (2027+)

**Exploration of biological quantum platforms beyond fluorescence:**
- **Radical pairs** (cryptochrome, photolyase) — hypothesized magnetoreception
- **Nuclear spins** (hyperpolarized ¹³C, ¹⁵N) — metabolic imaging at clinical scale
- **Engineered quantum sensors** — protein-based ODMR systems (experimental, follow-up to Nature 2025)

**Cross-repository integration:**
- **fp-qubit-design** uses atlas as ML training source → feedback loop for validation
- **arrest-molecules** provides energy landscape vocabulary → apply to quantum metastability
- **ising-life-lab** tests emergent quantum-inspired principles → biological network dynamics

**Community-driven curation:**
- Establish curator network (5-10 domain experts)
- Quarterly data releases with community input
- Integration with FPbase, UniProt, PDB via automated API pipelines

---

## Semantic Versioning

This project follows [Semantic Versioning 2.0.0](https://semver.org/):

- **MAJOR** (X.0.0): Breaking schema changes
- **MINOR** (1.X.0): New systems, backward-compatible additions
- **PATCH** (1.2.X): Fixes, corrections

---

## Questions?

- GitHub Issues: [Issues](https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/issues)
- Documentation: [DOCUMENTATION.md](DOCUMENTATION.md)
- Version policy: See [VERSIONS.md](VERSIONS.md)
