# Versioning Roadmap — Biological Qubits Atlas

**Last updated**: 2025-10-26

---

## Version History

| Version | Date | Purpose | Systems | Status |
|---------|------|---------|---------|--------|
| **v2.2.2** | 2025-10-25 | Balanced dataset for ML | 250 | ✅ Current stable (dev/ML) |
| v2.2.0 | 2025-10-25 | Data boost | 191 total (170 usable) | Superseded |
| v2.1.0 | 2025-10-24 | FPbase integration | 120 | Superseded |
| v2.0.0 | 2025-10-24 | Dashboard & FP extension | 113 | Superseded |
| **v1.2.1** | 2025-10-23 | Frontiers submission | 66 | 🔒 Frozen (publication) |
| v1.3.0-beta | 2025-10-24 | Pre-release testing | 80 | Superseded |
| v1.2.0 | 2025-10-20 | Initial stable | 66 | Superseded |

---

## Current Stable Versions

### v2.2.2 (Latest stable for dev/ML)
- **Purpose**: Machine learning training, research, development
- **Systems**: 250 balanced dataset
- **Files**: `atlas_fp_optical_v2_2.csv`, `TRAINING_TABLE_v2_2_2_full.csv`
- **Citation**: Use [CITATION.cff](CITATION.cff)
- **DOI**: TBD (pending Zenodo deposit)
- **Status**: ✅ Active development

### v1.2.1 (Frontiers manuscript)
- **Purpose**: Publication submission (fixed dataset)
- **Systems**: 66
- **Citation**: Use [CITATION_v1.2.1.cff](CITATION_v1.2.1.cff)
- **DOI**: 10.5281/zenodo.17420604
- **Status**: 🔒 Frozen (do not modify)

---

## Dual Versioning Policy

### Why Two Versions?

- **v1.2.1**: Frozen for Frontiers publication (scientific reproducibility)
- **v2.2.2**: Active development for ML/research (adds 184 systems)

Both versions coexist:
- **Citations for manuscripts**: Use v1.2.1 (frozen, cited in Frontiers)
- **Citations for research/ML**: Use v2.2.2 (latest stable)

### How to Cite

See [README.md#citation](README.md#citation) for citation guidelines.

---

## Migration Guide

### Upgrading from v1.2.1 to v2.2.2

**Data compatibility**: ✅ Schema compatible, no breaking changes

**What's new**:
- +184 systems (66 → 250)
- Balanced family distribution (30 families)
- 100% optical coverage
- ML-optimized training splits

**Migration steps**:
1. Update file path: `atlas_fp_optical_v1_2_1.csv` → `atlas_fp_optical_v2_2.csv`
2. No schema changes (backward compatible)
3. Update citations if citing latest dataset

**Breaking changes**: None

---

## Future Roadmap

### Post-Nobel 2025 Context

Following the **2025 Nobel Prize in Physics** (Josephson junctions, superconducting circuits), this atlas positions itself as a complementary exploration of **room-temperature quantum platforms** for biological applications. Future versions will expand coverage of ambient-temperature systems, emphasizing biocompatibility and in vivo deployment.

**Strategic direction:**
- **Cryogenic platforms** (superconducting qubits) → **Ambient platforms** (NV centers, fluorescent proteins, hyperpolarized nuclei)
- **Isolated quantum systems** → **Quantum sensors in noisy biological environments**
- **Quantum computing** → **Quantum-enhanced sensing and imaging**

### v2.3.0 (Planned Q1 2026)
- **Goal**: 300+ systems (curated tier)
- **Focus**: 
  - Promote Tier 2 → Tier 1 (manual curation of 13 candidates)
  - Extend rare biosensor families (acetylcholine, serotonin, norepinephrine)
  - Add confidence intervals for contrast measurements
- **Non-optical extension**: Pilot integration of spin qubits (NV, SiC) in separate schema (see `data/staging/spin_qubit_candidates.csv`)
- **Timeline**: Q1 2026

### v2.4.0 (Planned Q2 2026)
- **Goal**: API REST endpoint for programmatic access
- **Features**:
  - JSON API with filtering (family, temperature range, contrast threshold)
  - Batch downloads via API keys
  - Real-time tier classification updates
- **Integration**: Enable fp-qubit-design and downstream tools to auto-sync with latest data
- **Timeline**: Q2 2026

### v3.0.0 (Long-term, Peer-Review Target)
- **Goal**: Peer-reviewed publication (Scientific Data or similar)
- **Breaking changes**: Schema v3.0 (major reorganization)
  - Add `confidence_interval` fields (CI_low, CI_high for all measurements)
  - Refactor `method` column (controlled vocabulary: ODMR, FRET, FLIM, etc.)
  - Add `biological_context` structured field (in_vitro, in_cellulo, ex_vivo, in_vivo)
- **Timeline**: Q3-Q4 2026
- **Milestone**: 500+ curated systems target

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
