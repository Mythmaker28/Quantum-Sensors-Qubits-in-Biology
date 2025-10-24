# Version Policy — Biological Qubits Catalog

**Last updated**: 2025-10-24  
**Current stable**: v1.2.1  
**Current pre-release**: v1.3.0-beta

---

## 📋 Semantic Versioning

This project follows [Semantic Versioning 2.0.0](https://semver.org/):

### Version Format: `MAJOR.MINOR.PATCH`

- **MAJOR (X.0.0)**: Breaking changes
  - Schema modifications (renamed/removed columns)
  - Methodology changes affecting comparability
  - Incompatible API changes (if REST API implemented)
  
- **MINOR (1.X.0)**: Backward-compatible additions
  - New systems added
  - New columns added (optional, non-breaking)
  - Enhanced provenance tracking
  - Quality improvements (e.g., uncertainties added)
  
- **PATCH (1.2.X)**: Backward-compatible fixes
  - Corrected values (typos, unit errors)
  - Fixed DOI links
  - Metadata corrections
  - Documentation improvements

---

## 🏷️ Release Types

### Stable Releases

- **Badge**: 🟢 Stable
- **Naming**: `vX.Y.Z` (e.g., v1.2.1)
- **Quality**: Fully verified, QA passed (0 blocking errors)
- **Recommended for**: Citations in publications, production use
- **Frequency**: Quarterly (Jan, Apr, Jul, Oct)
- **Support**: Bug fixes for latest stable only

**Criteria for stable release**:
- ✅ 0 blocking errors in `qubits_linter.py` (strict mode)
- ✅ >90% provenance coverage (Source_T2/T1/Contraste)
- ✅ >75% verification rate (Verification_statut = "Verified")
- ✅ All assets published (CSV, metadata, evidence samples)
- ✅ DOI minted (Zenodo)

---

### Pre-releases (Beta/Alpha)

- **Badge**: 🟡 Pre-release
- **Naming**: `vX.Y.Z-beta` or `vX.Y.Z-alpha`
- **Quality**: Feature-complete but under community review
- **Recommended for**: Early adopters, testing, feedback
- **Frequency**: Ad-hoc (when +10 systems or major feature)
- **Support**: No bug fixes (use at own risk)

**Beta criteria**:
- ✅ 0-5 warnings in linter (beta mode)
- ✅ >85% provenance coverage
- ✅ >60% verification rate
- ✅ New features documented

**Alpha criteria**:
- ⚠️ Experimental features, API may change
- ⚠️ <85% provenance coverage acceptable
- ⚠️ Not recommended for citations

---

## 📊 Current Version Status

| Version | Release Date | Type | Systems | Measured | Status |
|---------|--------------|------|---------|----------|--------|
| **v1.3.0-beta** | 2025-10-24 | Pre-release | 80 | 65 | 🟡 Beta testing |
| **v1.2.1** | 2025-10-23 | Stable | 66 | 54 | 🟢 **Recommended** |
| v1.2.0 | 2025-10-20 | Stable | 66 | 54 | Superseded by v1.2.1 |
| v1.1.0 | 2025-10-15 | Stable | 21 | 18 | Archived |

---

## 🔄 Deprecation Policy

### End-of-Life (EOL)

Stable versions are supported for **6 months** after a newer stable release:

- **v1.2.1** (current): Supported until v1.4.0 stable release
- **v1.2.0**: EOL when v1.3.0 stable is released
- **v1.1.0**: Already EOL (superseded by v1.2.x)

**EOL definition**: No bug fixes, security patches, or data corrections.

### Migration Guide

When upgrading between MAJOR versions:
1. Read `CHANGELOG.md` for breaking changes
2. Update import scripts if column names changed
3. Re-validate analysis pipelines
4. Update citations to new DOI

When upgrading between MINOR versions:
- No breaking changes, safe to upgrade
- New columns may appear (check schema documentation)

---

## 🎯 Roadmap

### v1.3.0 (Stable) — Target: Q4 2025
- Expand to 120+ measured systems
- Achieve >90% provenance coverage
- License audit complete (all sources verified)
- Add Tier A measurements (with confidence intervals)

### v1.4.0 — Target: Q1 2026
- Peer-reviewed publication (Data Descriptor)
- API REST endpoint (JSON access)
- Community contributions accepted (GitHub PRs)
- Geographic/temporal bias mitigation

### v2.0.0 — Target: 2026
- Schema v2.0 (breaking changes: unified units, new classes)
- Expand to 200+ systems
- Multi-language metadata (EN/FR/DE/ZH)
- Integration with Materials Project

---

## 🏷️ Git Tagging Convention

### Tag Format

```bash
# Stable releases
git tag -a v1.2.1 -m "Stable: 66 systems, 54 measured, QA passed"

# Pre-releases
git tag -a v1.3.0-beta -m "Beta: 80 systems, hybrid curated expansion"

# Release candidates (if used)
git tag -a v1.3.0-rc.1 -m "Release candidate 1 for v1.3.0"
```

### Tag Naming Rules

- ✅ `v1.2.1` — Stable release
- ✅ `v1.3.0-beta` — Beta pre-release
- ✅ `v1.3.0-alpha` — Alpha pre-release
- ✅ `v1.3.0-rc.1` — Release candidate 1
- ❌ `1.2.1` — Missing "v" prefix (not allowed)
- ❌ `v1.2.1-stable` — Redundant suffix (stable is default)

---

## 📝 Citation Versioning

### Which version to cite?

**For publications (peer-reviewed journals)**:
- Always cite **latest stable** (currently v1.2.1)
- Use Zenodo DOI for permanent reference
- Mention in methods: "Version X.Y.Z was used (stable release as of YYYY-MM-DD)"

**For preprints/conference papers**:
- You may cite beta releases if explicitly stated
- Mention: "Version X.Y.Z-beta (pre-release, not peer-reviewed)"

**For reproducibility**:
- Pin exact version in analysis scripts
- Store local copy of CSV (in case EOL version is removed from GitHub)

### Example citations

```bibtex
@dataset{biological_qubits_v1_2_1,
  author = {[Your Name]},
  title = {Biological Qubits Catalog},
  version = {1.2.1},
  year = {2025},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.17420604},
  url = {https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/releases/tag/v1.2.1}
}
```

---

## 🔒 Version Immutability

**Once a version is tagged and released, it is immutable**:

- ✅ We **do not** modify released CSV files
- ✅ Corrections are made in new PATCH versions (e.g., v1.2.1 → v1.2.2)
- ✅ Old versions remain accessible via Git tags forever

**Exception**: Pre-releases (beta/alpha) may be re-tagged if critical errors found before stable promotion.

---

## 🤝 Community Input

**Found a bug in a released version?**
- Open GitHub Issue with label `bug`
- Provide: Version number, affected systems, proposed correction
- Maintainer will release PATCH version (e.g., v1.2.2) within 7 days

**Want to suggest new systems?**
- Open GitHub Issue with label `enhancement`
- Provide: DOI, T2/T1 values, provenance
- Will be included in next MINOR release (e.g., v1.3.0)

---

## 📧 Questions?

See `CONTRIBUTING.md` (coming soon) or open a GitHub Discussion.

