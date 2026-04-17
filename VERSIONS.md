# Version Policy — Biological Qubits Atlas

**Last updated**: 2026-04-17  
**Current stable**: v3.0.0 (Zenodo archived)  
**Current pre-release**: — (none)

---

## 📋 Semantic Versioning

This project follows [Semantic Versioning 2.0.0](https://semver.org/):

### Version Format: `MAJOR.MINOR.PATCH`

- **MAJOR (X.0.0)**: Breaking changes
  - Schema modifications (renamed/removed columns)
  - New class(es) in the qubits taxonomy (e.g., v3.0.0 introduced class `A'`)
  - Methodology changes that affect cross-version comparability
- **MINOR (1.X.0)**: Backward-compatible additions
  - New systems added to existing classes
  - New optional columns added
  - Enhanced provenance tracking (PMCIDs, licenses)
- **PATCH (1.2.X)**: Backward-compatible fixes
  - Corrected values (typos, unit errors)
  - Fixed DOI links
  - Documentation improvements

---

## 🏷️ Release Types

### Stable Releases
- **Badge**: 🟢 Stable
- **Naming**: `vX.Y.Z` (e.g., v3.0.0)
- **Quality**: Fully verified, QA passed, Zenodo DOI minted
- **Recommended for**: Citations in publications, reproducible analyses
- **Support**: Bug fixes via PATCH releases on the latest MAJOR line

### Pre-releases (Beta/Alpha)
- **Badge**: 🟡 Pre-release
- **Naming**: `vX.Y.Z-beta` or `vX.Y.Z-alpha`
- **Recommended for**: Early adopters, feedback
- **Support**: No long-term support; may be re-tagged before stable promotion

---

## 📊 Current Version Status

| Version | Release Date | Type | Qubits (v3) | FP biosensors | DOI | Status |
|---------|--------------|------|-------------|---------------|-----|--------|
| **v3.0.0** | 2026-04-17 | Stable | 82 (including 8 class A') | 195 | [10.5281/zenodo.19617435](https://doi.org/10.5281/zenodo.19617435) | 🟢 **Recommended** |
| v2.2.2 | 2025-11-15 | Stable (historical) | — | 187 | — (GitHub only) | Superseded |
| v2.2.0 | 2025-11 | Stable (historical) | — | ~180 | — | Superseded |
| v1.3.0-beta | 2025-10-24 | Pre-release | 80 | — | — | Archived |
| v1.2.1 | 2025-10-23 | Stable (frozen) | 66 | — | [10.5281/zenodo.17420604](https://doi.org/10.5281/zenodo.17420604) | Frozen (historical citation) |

**Concept DOI** (always resolves to the latest version):
[10.5281/zenodo.17420603](https://doi.org/10.5281/zenodo.17420603)

---

## 🔄 Deprecation Policy

### End-of-Life (EOL)
The **latest MAJOR line** is supported. Previous MAJOR lines are frozen and remain citable but receive no fixes.

- **v3.x** (current): Active
- **v2.x**: Frozen (available via Git tags, not Zenodo-archived)
- **v1.x**: Frozen (v1.2.1 Zenodo-archived at [10.5281/zenodo.17420604](https://doi.org/10.5281/zenodo.17420604))

### Migration Guide

When upgrading **v2 → v3**:
1. Expect a new qubit class `A'` (FP-qubits with direct ODMR readout)
2. The qubits dataset (`data/qubits/biological_qubits_v3.csv`, 82 rows) is now the canonical entry point
3. The FP optical atlas (`data/processed/atlas_fp_optical_v3_curated.csv`, 195 rows) is a distinct, complementary dataset
4. Read `CHANGELOG.md` for the full list of additions, deprecations, and corrections
5. Update citations to the new Zenodo DOI

---

## 🎯 Roadmap

### v3.1 (MINOR)
- Add more NV-based sensors from 2026 publications
- Cross-reference chemigenetic indicators (HaloTag-based) with the Atlas of chemigenetic probes
- Refresh license & PMCID coverage quarterly

### v3.2 / v3.x
- Integrate transportable HP-129Xe clinical protocols (class C)
- Extend class A' with additional FP+FMN SCRP variants (if confirmed in peer-reviewed publications)
- Tier-A uncertainty estimation (bootstrap CIs) for all measured quantities

### v4.0.0 (MAJOR, tentative)
- Schema overhaul: unified units, controlled vocabularies, JSON Schema validation
- Integration with [Bioschemas](https://bioschemas.org/) types for FAIR interoperability
- Cross-linking with [fp-qubit-design](https://github.com/Mythmaker28/fp-qubit-design) design space

---

## 🏷️ Git Tagging Convention

### Tag Format

```bash
# Stable releases
git tag -a v3.0.0 -m "Stable: 82 qubits (8 class A'), 195 FP biosensors, Zenodo-archived"

# Pre-releases
git tag -a v3.1.0-beta -m "Beta: new additions under review"

# Release candidates
git tag -a v3.1.0-rc.1 -m "Release candidate 1 for v3.1.0"
```

### Tag Naming Rules

- ✅ `v3.0.0` — Stable release
- ✅ `v3.1.0-beta` — Beta pre-release
- ✅ `v3.1.0-alpha` — Alpha pre-release
- ✅ `v3.1.0-rc.1` — Release candidate 1
- ❌ `3.0.0` — Missing "v" prefix (not allowed)
- ❌ `v3.0.0-stable` — Redundant suffix (stable is default)

---

## 📝 Citation Versioning

### Which version to cite?

**For publications (peer-reviewed journals)**:
- Cite the **latest stable** (currently v3.0.0)
- Use the Zenodo DOI for permanent reference
- Mention in methods: "Biological Qubits Atlas v3.0.0 (DOI: 10.5281/zenodo.19617435) was used."

**For long-term/meta-analysis studies**:
- Cite the **concept DOI** (10.5281/zenodo.17420603) to always resolve to the latest version.

**For reproducibility**:
- Pin the exact version in analysis scripts (e.g., download the tagged CSV via the Zenodo archive).
- Store a local copy of the CSV alongside your analysis code.

### Example citation

```bibtex
@dataset{biological_qubits_v3_0_0,
  author       = {Lepesteur, Tommy},
  title        = {Biological Qubits Atlas},
  version      = {3.0.0},
  year         = {2026},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.19617435},
  url          = {https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/releases/tag/v3.0.0}
}
```

See `CITATION.cff` and `VERSIONS_CITATION.md` for additional formats (BibTeX, APA, Chicago).

---

## 🔒 Version Immutability

**Once a version is tagged and released, it is immutable**:
- ✅ Released CSV files are never modified in-place
- ✅ Corrections are made in a new PATCH version (e.g., v3.0.0 → v3.0.1)
- ✅ Old versions remain accessible via Git tags and Zenodo deposits forever
- ⚠️ Pre-releases (beta/alpha/rc) *may* be re-tagged before stable promotion

---

## 🤝 Community Input

**Found a bug in a released version?**
- Open a [GitHub Issue](https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/issues) with label `bug`
- Provide: version number, affected systems, proposed correction
- Maintainer aims to cut a PATCH release within 7 days when warranted

**Want to suggest new systems?**
- Open a [GitHub Issue](https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/issues/new?template=new_entry.yml) with template `new_entry.yml`
- Provide: DOI, measured values, provenance, quality tier
- Accepted entries land in the next MINOR release

---

## Questions?

See `CONTRIBUTING.md` (coming soon), `DOCUMENTATION.md`, or open a GitHub Discussion.
