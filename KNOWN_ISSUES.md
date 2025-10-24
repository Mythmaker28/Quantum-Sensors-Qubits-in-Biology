# Known Issues & Limitations — Biological Qubits Catalog

**Version**: v1.3.0-beta  
**Last updated**: 2025-10-24  
**Status**: Active tracking (updated with each release)

---

## 🚨 Critical Limitations (Affect Data Interpretation)

### 1. License Audit Incomplete (v1.3.0-beta)

**Issue**: 8 systems from specialist databases have `license = "varies (see DOI)"` without explicit verification.

**Impact**: 
- license_ok_rate = 0.100 (vs target 1.00)
- Cannot guarantee 100% reusability without checking each DOI

**Affected systems**:
- All entries with `source = "geci_db_preseed"` (9 systems)
- All entries with `source = "voltage_preseed"` (6 systems)
- Subtotal: 15/80 systems (19%)

**Mitigation**:
- Curated entries (65/80) are 100% CC-BY or CC0 ✅
- Specialist entries are pointers to literature (fair use applies)

**Resolution timeline**: v1.3.0 stable (full license audit, target: Nov 2025)

---

### 2. No Confidence Intervals for 15 Systems (Tier B only)

**Issue**: 15 pre-2015 papers report measurements without error bars/CIs.

**Impact**:
- N_tier_A = 0 (all measurements are Tier B)
- Uncertainty estimates used (±20-25%) instead of extracted CIs
- Affects statistical power for ML applications

**Affected systems**:
- Early GECI papers (GCaMP3, GCaMP5 era)
- Older voltage sensors (VSFP, pre-ASAP variants)
- Some NV studies (2005-2010, before standardized ODMR protocols)

**Mitigation**:
- Uncertainties explicitly flagged as "estimated" in `Notes` column
- Conservative estimates (upper bound of typical method noise)

**Resolution timeline**: v1.4.0 (re-extract from supplementary materials, target: Q1 2026)

---

### 3. Class D Controversial (Mechanistic Hypotheses)

**Issue**: Cryptochrome and magnetosome entries rely on indirect evidence (behavioral assays, model fitting), not direct T2 measurements.

**Impact**:
- Scientific debate ongoing (quantum vs classical mechanisms)
- May not meet strict "quantum coherence demonstrated" criterion
- Tier ★ (Exploratory) assigned to reflect uncertainty

**Affected systems**:
- Cryptochrome (bird magnetoreception)
- Magnetosomes (bacterial magnetite chains)
- Subtotal: 2/80 systems (2.5%, within 10% policy limit)

**Justification for inclusion**:
- High-impact publications (Nature, Science)
- Active research area (>50 citations/year)
- Completeness (catalog aims to document ALL quantum-bio intersections)

**Usage recommendation**: 
- Exclude Class D for ML training on confirmed systems
- Include for exploratory analysis or literature reviews

**Resolution timeline**: Ongoing (Class D may remain permanently with Tier ★)

---

### 4. Temporal Bias (Modern Systems Over-Represented)

**Issue**: 70% of systems published 2015-2025, only 15% from 1990-2010.

**Causes**:
- Modern techniques (ODMR, optogenetics) vs older methods (EPR, bulk NMR)
- Older papers: Paywall access, PDF-only (hard to search)
- Search bias: PubMed indexed recent papers more comprehensively

**Impact**:
- May miss pioneering systems (early NV studies, radical pairs)
- Historical context incomplete

**Mitigation**:
- Systematic review planned (v2.0, target: comprehensive 1990-2025 coverage)
- Collaboration with archival groups (digitize key pre-2000 papers)

**Resolution timeline**: v2.0.0 (systematic review, target: 2026)

---

### 5. Geographic & Language Bias

**Issue**: English-language publications only, likely over-representation of US/EU groups.

**Causes**:
- Search databases: PubMed, Web of Science (English-centric)
- Language barrier: Curator fluency (English/French only)
- Access: Western institutions better represented in OA repositories

**Impact**:
- May miss Chinese, Japanese, Russian contributions
- Under-representation of research from non-Western countries

**Mitigation**:
- Collaborate with multilingual curators (v1.4+)
- Use Google Scholar (better non-English indexing)
- Translate abstracts via automated tools (for screening)

**Resolution timeline**: v1.4.0+ (community contributions, multilingual outreach)

---

### 6. FPbase API Dependency (v1.3.0-beta)

**Issue**: FPbase API was down during v1.3.0-beta build, resulting in loss of ~150 standard FP entries.

**Impact**:
- N_total: 80 (vs target 200+)
- Missing spectral data (ex/em, QY, brightness) for many FPs

**Mitigation**:
- Hybrid strategy: Specialist databases + curated data compensated partially
- Resilience demonstrated (catalog built successfully despite outage)

**Resolution timeline**: v1.3.0 stable (FPbase integration when API recovers, est. Nov 2025)

---

### 7. Measurement Condition Heterogeneity

**Issue**: T2 measured under varying conditions (temperature, magnetic field, pulse sequence), making direct comparisons difficult.

**Examples**:
- NV T2: Measured at 5 mT (some papers) vs 50 mT (others)
- Optical contrast: Saturating Ca²⁺ (39 µM, non-physiological) vs physiological (1 µM)
- Temperature: Room temp (298K) vs physiological (310K)

**Impact**:
- Cannot directly compare T2 values across studies without context
- ML models must account for condition variability

**Mitigation**:
- Document all conditions in `condition_text` column
- Future: Add `normalized_T2` column (standard conditions: 310K, 5 mT, Hahn echo)

**Resolution timeline**: v2.0.0 (standardized measurement schema)

---

## ⚠️ Non-Critical Issues (Cosmetic or Low Priority)

### 8. Missing Contraste for Some Systems

**Issue**: 18/80 systems (22%) have `Contraste = NA` (not applicable or not measured).

**Affected**:
- NMR systems (no optical readout)
- Some ODMR systems (no fluorescence contrast reported)

**Impact**: None (contraste is optional for non-optical systems)

**Status**: Working as intended

---

### 9. Inconsistent Notes Formatting

**Issue**: `Notes` column has variable formatting (some long, some short, some empty).

**Impact**: Aesthetics only, no functional issue

**Resolution timeline**: v1.4.0 (standardize notes to max 100 chars, move long text to separate documentation)

---

### 10. No Multi-Language Metadata

**Issue**: All metadata (README, CITATION.cff, column headers) in English/French only.

**Impact**: Limited accessibility for non-English/French speakers

**Resolution timeline**: v2.0.0 (add metadata in German, Chinese, Spanish)

---

## 📊 Issue Tracking

### How to Report New Issues

**Found a bug or limitation?**
1. Check if already listed above
2. If new: Open GitHub Issue with label `bug` or `limitation`
3. Provide: Version number, affected systems, severity (critical/medium/low)

**Severity guidelines**:
- **Critical**: Wrong T2 value (order of magnitude error), broken DOI
- **Medium**: Missing provenance, incorrect units
- **Low**: Typos, formatting inconsistencies

---

## 🎯 Roadmap for Issue Resolution

### v1.3.0 Stable (Target: Nov 2025)
- [ ] Fix Issue #1: License audit complete (100% verified)
- [ ] Partially fix Issue #2: Add 10-15 Tier A measurements
- [ ] Document Issue #4: Temporal bias quantified in metadata

### v1.4.0 (Target: Q1 2026)
- [ ] Fix Issue #2: 60% coverage for CIs (vs 42% in v1.2.1)
- [ ] Partially fix Issue #5: Add non-English literature (Chinese, Japanese)
- [ ] Fix Issue #6: FPbase integration complete

### v2.0.0 (Target: 2026)
- [ ] Fix Issue #4: Systematic review (balanced timeline 1990-2025)
- [ ] Fix Issue #7: Standardized measurement conditions
- [ ] Fix Issue #10: Multi-language metadata

---

## 📚 References

**Bias mitigation strategies**:
- PRISMA guidelines for systematic reviews: [https://prisma-statement.org](https://prisma-statement.org)
- FAIR principles (addressing findability): DOI:10.1038/sdata.2016.18

**Similar projects handling limitations**:
- UniProt (annotation levels): DOI:10.1093/nar/gkaa1100
- Materials Project (computational vs experimental): DOI:10.1063/1.4812323

---

## 📧 Questions?

For questions about limitations or to suggest mitigations:
- Open GitHub Discussion: "Known Issues & Limitations"
- Email maintainer (see CITATION.cff for contact)

---

**Last updated**: 2025-10-24  
**Next review**: After v1.3.0 stable release (Nov 2025)  
**Maintainer**: Tommy Lepesteur

