# Curation Methodology — Biological Qubits Catalog

**Version**: 1.3.0-beta  
**Last updated**: 2025-10-24  
**Status**: Active development (hybrid curated strategy)  
**Document type**: Living methodology (updated with each major release)

---

## 🎯 Objective

Provide a **comprehensive, traceable, and reproducible** catalog of quantum systems demonstrated or hypothesized in biological contexts (in vitro, in cellulo, in vivo).

**Scope**:
- Quantum coherent systems (T2 > 1 ns)
- Bio-compatible or bio-intrinsic
- Peer-reviewed evidence (primary literature)
- Temperature ≤ 310K preferred (exceptions documented)

**Non-scope**:
- Purely theoretical proposals (no experimental data)
- Cryogenic-only systems (T < 77K) without biological pathway
- Non-peer-reviewed claims (preprints accepted if highly cited >20)

---

## 🔬 Inclusion Criteria

### Mandatory Requirements

1. **Bio-compatibility OR bio-intrinsic**
   - System must interface with biological matter
   - Examples: NV nanodiamonds in cells, proteins with ODMR-active cofactors, hyperpolarized metabolites

2. **Quantum coherence evidence**
   - **Direct**: T2 measured via ODMR/ESR/NMR/optical readout
   - **Indirect**: Mechanistic evidence with peer-reviewed support (Class D only, max 10% of dataset)

3. **Peer-reviewed publication**
   - Primary research article with DOI
   - Published in indexed journal (PubMed, Web of Science, Scopus)
   - Preprints accepted if: highly cited (>20 citations) OR replicated by independent group

4. **Temperature feasibility**
   - ≤310K (37°C) preferred for in vivo relevance
   - Exceptions allowed if biological pathway demonstrated (e.g., cryoprotectant-based, extremophile organisms)

### Exclusionary Criteria

❌ **Theoretical proposals only** (no experimental demonstration)  
❌ **Cryogenic-locked systems** (T < 77K) without demonstrated bio-interface  
❌ **Blog posts, patents, popular science** (non-peer-reviewed)  
❌ **Duplicate entries** (same system, same measurement conditions)  
❌ **Mutants/variants without canonical parent** (must include WT reference)

---

## 📊 Hybrid Curated Strategy (v1.3+)

### Overview

Starting with v1.3.0-beta, the catalog uses a **3-tier hybrid approach**:

1. **Tier 1: Manual Curation** (Gold Standard)
   - Human-verified extraction from primary literature
   - Every value cross-checked against original Figure/Table
   - Uncertainties extracted or estimated with transparent methodology
   - **Coverage**: 65/80 systems (81% in v1.3.0-beta)

2. **Tier 2: Conservative Automated Extraction**
   - Structured data only (XML tables, HTML tables, CSV supplements)
   - No OCR, no figure scraping
   - Ambiguous entries flagged for manual review
   - **Coverage**: 8/80 systems (10% in v1.3.0-beta)

3. **Tier 3: Specialist Database Cross-Reference**
   - Secondary extraction from trusted databases (FPbase, UniProt, PDB)
   - Original DOI traced and validated
   - Marked explicitly in `source` column
   - **Coverage**: 43/80 systems (54% in v1.3.0-beta, metadata only)

---

## 🛠️ Data Extraction Protocol

### Step 1: Literature Search

**Databases**:
- PubMed (biomedical primary literature)
- Web of Science (citation tracking)
- arXiv (q-bio.QM, cond-mat.mes-hall, quant-ph)
- Google Scholar (gray literature, highly cited preprints)

**Keywords** (Boolean queries):
```
("quantum biology" OR "NV diamond" OR "quantum coherence") 
AND ("in vivo" OR "in vitro" OR "cells" OR "biological")

("ODMR" OR "ESR" OR "EPR") AND ("protein" OR "cells" OR "tissue")

("hyperpolarization" OR "DNP") AND ("MRI" OR "metabolic imaging")

"GCaMP" OR "fluorescent biosensor" OR "FRET sensor"
```

**Time range**: 1990–2025 (focus on 2010+)

**Language filter**: English only (limitation noted in `KNOWN_ISSUES.md`)

---

### Step 2: Screening

**Level 1: Title/Abstract Review**
- Screened: ~500 papers (for v1.2.1)
- Inclusion rate: ~25% (120 full-text reviewed)
- Automated tools: None (manual review only)

**Level 2: Full-Text Review**
- Read: ~120 papers
- Extraction criteria:
  - T2 value explicitly reported (not inferred)
  - Biological context described (in vitro/cellulo/vivo)
  - Temperature and other conditions documented
- Inclusion rate: ~55% (66 systems included in v1.2.1)

**Exclusion reasons** (tracked in `reports/EXCLUDED.md`):
- 20% : No T2 value (only T1 or optical properties)
- 15% : Cryogenic only (T < 77K, no bio pathway)
- 10% : Insufficient documentation (conference abstract, no full paper)
- 5% : License restrictions (paywalled, no OA access)

---

### Step 3: Data Entry

**Template**: 33 columns (see `schema/schema_v1.3.json`)

**Mandatory fields**:
- `Systeme` (system name)
- `Classe` (A/B/C/D)
- `T2_us` (coherence time, microseconds)
- `Source_T2` (provenance: DOI + Figure/Table)
- `DOI` (primary reference)
- `Verification_statut` (Verified/To confirm)

**Optional fields** (but encouraged):
- `T1_s`, `Contraste`, uncertainties, biological flags, notes

**Entry process**:
1. Fill CSV row using template
2. Run `qubits_linter.py` (validate format, units, DOI format)
3. If errors: fix before commit
4. If warnings: document in commit message

---

### Step 4: Verification

**Verification levels**:

- **Verified**: Curator read original paper + validated all values + cross-checked provenance
  - Requirement: 100% for stable releases
  - Current: 77% in v1.2.1 (50/66 verified)

- **To confirm**: Preliminary entry, needs re-check
  - Acceptable: <25% in stable, <40% in beta
  - Current: 23% in v1.2.1 (16/66 to confirm)

**Verification process** (for "To confirm" → "Verified"):
1. Re-open original paper (via DOI)
2. Locate exact Figure/Table mentioned in Source_T2
3. Verify value matches (within rounding error)
4. Check units (µs vs ns vs ms)
5. Update `Verification_statut` to "Verified"

**Inter-curator validation** (v1.4+ planned):
- 10% random sample reviewed by second curator
- Discrepancies resolved via discussion
- Logged in `VERIFICATION_LOG.md`

---

## 📏 Quality Tiers

### Quantum Systems (T2-based)

| Tier | Criteria | Example | % in v1.2.1 |
|------|----------|---------|-------------|
| **★★★ (Robust)** | T2 >1µs + Major journal (Nature/Science/PNAS) + Reproduced | Pyruvate ^13C (FDA-approved), NV in HeLa (PNAS) | 50% |
| **★★ (Solid)** | T2 >0.1µs + In vitro/cellulo + Peer-reviewed | SiC defects in buffer (Sci. Adv.) | 31% |
| **★ (Exploratory)** | Indirect evidence OR T2 <0.1µs OR Hypothetical | Cryptochrome (behavioral only) | 19% |

### Optical Systems (Contrast-based, v1.3+)

| Tier | Criteria | Example | % in v1.3.0-beta |
|------|----------|---------|------------------|
| **A** | Measured + CI/n + Table/Figure | GCaMP6s (Nature 2013, Table 1, n=8, SD=3.2) | 0% (target: 20% in v1.3.0 stable) |
| **B** | Measured + Precise value | dLight1.1 (text: "ΔF/F0 = 2.3") | 100% |
| **C** | Computed/Estimated | Brightness from QY × ε | 0% |

---

## 🔍 Provenance Tracking

### Format Standards

**Source_T2, Source_T1, Source_Contraste**:
```
Format: DOI:10.xxxx/xxxxx Fig.X
        DOI:10.xxxx/xxxxx Table Y
        PMCID:PMCxxxxxxx Supp Fig.Z
```

**Coverage targets**:
- Stable release: >90% (all measured values must have provenance)
- Beta release: >85%
- Current v1.3.0-beta: 88% (70/80 systems)

**Missing provenance**:
- Flagged in `QC_REPORT.md` as warnings (non-blocking in beta)
- Blocking error in stable releases (linter exits with code 1)

**Example provenance chain**:
```csv
Systeme,T2_us,Source_T2,DOI
NV 50nm in HeLa,1.2,DOI:10.1073/pnas.0912814107 Fig.3,10.1073/pnas.0912814107
```

---

## 🧪 Uncertainty Quantification

### Extracted Uncertainties (Preferred)

When error bars, CIs, or SDs are reported in original paper:
- **Extract directly** from Figure caption or Table
- **Format**: Store in `_err` columns (e.g., `T2_us_err = 0.3` for T2 = 1.2 ± 0.3 µs)
- **Note provenance**: Same Figure/Table as measurement itself

**Current coverage**:
- v1.2.1: 42% have extracted uncertainties (28/66 systems)
- v1.3.0-beta target: 60%

---

### Estimated Uncertainties (Conservative)

When error bars NOT reported in original paper:
- **Estimate conservatively** based on measurement method
- **Flag explicitly** in `Notes` column: "(uncertainty estimated ±X% based on typical [method] noise)"

**Estimation rules**:

| Method | Typical Error | Rationale |
|--------|---------------|-----------|
| ODMR (diamond) | ±20% | Laser power drift, magnetic field inhomogeneity |
| ESR (nitroxide) | ±25% | Temperature fluctuations, sample heterogeneity |
| NMR T1 | ±15% | RF field inhomogeneity, relaxation pathways |
| Optical contrast (GCaMP) | ±25% | Photon shot noise, photobleaching, cell-to-cell variability |
| Lifetime (ns) | ±10% | Instrument response function, fitting uncertainty |

**Example**:
```csv
Systeme,T2_us,T2_us_err,Notes
NV 10nm,0.8,0.16,"T2 from ODMR spectrum. Uncertainty estimated ±20% (typical ODMR noise, not reported in paper)"
```

**Goal**: Replace ALL estimates with extracted values by v2.0 (requires re-reading ~30 papers)

---

## 🔄 Update Cycle & Versioning

### Release Schedule

- **Stable releases**: Quarterly (January, April, July, October)
  - Full QA audit
  - Peer-review-ready quality
  - Zenodo DOI minted
  
- **Beta releases**: Ad-hoc (when +10 systems OR major schema change)
  - Community testing
  - Feature preview
  - May have known limitations (documented)
  
- **Hotfixes**: Immediate (critical errors only)
  - Wrong T2 value (order of magnitude error)
  - Broken DOI link
  - License compliance issue

### Version Numbering (Semantic Versioning)

```
vMAJOR.MINOR.PATCH[-beta|-alpha]

Examples:
- v1.2.1       : Stable patch (bug fix over v1.2.0)
- v1.3.0-beta  : Beta pre-release for v1.3.0
- v2.0.0       : Major version (breaking schema changes)
```

See `VERSIONS.md` for full policy.

---

## 🚨 Known Limitations & Biases

### Documented Limitations (v1.3.0-beta)

1. **License audit incomplete**
   - 8 systems from specialist databases lack explicit license verification
   - Status: "varies (see DOI)" → requires manual check
   - Target: 100% verified by v1.3.0 stable

2. **No confidence intervals for 15 systems**
   - Affected: Pre-2015 papers (older methodology, error bars not reported)
   - Mitigation: Conservative estimates (±20-25%) with explicit flagging
   - Target: Re-extract from supplementary materials by v1.4.0

3. **Class D controversial**
   - Cryptochrome magnetoreception: Debated mechanism (quantum vs classical)
   - Magnetosomes: Coherence not directly measured
   - Inclusion rationale: High-impact publications (Nature), active research area
   - Marked explicitly: Tier ★ (Exploratory)

4. **Temporal bias**
   - 70% of systems from 2015-2025 (modern techniques: ODMR, optogenetics, super-res)
   - Older literature (1990-2010): Under-represented (~15%)
   - Mitigation: Systematic review planned (v2.0, target: 200+ systems, balanced timeline)

5. **Geographic bias**
   - Likely over-representation of US/EU research groups
   - Reason: Language barrier (English-only search), database access (Web of Science)
   - Mitigation: Collaborate with non-English-speaking groups (v1.4+ planned)

6. **Measurement heterogeneity**
   - T2 measured under different conditions (temp, field strength, pulse sequence)
   - Optical contrast: Different stimuli, concentrations, time windows
   - Normalization attempt: Document all conditions in `condition_text` column
   - Future: Add normalized_T2 column with standard conditions (v2.0)

---

## 📖 Data Extraction Workflow (Detailed)

### Phase 1: Search & Screening

**Week 1-2: Systematic search**
```python
# PubMed query example
search_query = '("quantum biology"[Title/Abstract] OR "NV diamond"[Title/Abstract]) 
                AND ("in vivo"[All Fields] OR "cells"[All Fields])'

# Results: ~500 papers (for v1.2.1 expansion)
```

**Week 3: Title/Abstract screening**
- Inclusion: Quantum coherence mentioned + Biological context
- Exclusion: Purely theoretical, no coherence measurement
- Output: ~120 papers for full-text review

---

### Phase 2: Data Extraction

**Per paper** (15-30 min/paper):
1. Open DOI in browser
2. Search for keywords: "T2", "coherence time", "ΔF/F", "fold change", "dynamic range"
3. Locate Figure/Table with measurement
4. Extract:
   - Value (with units!)
   - Error bars (if present)
   - Conditions (T, pH, host, context)
   - Provenance (Figure number)
5. Fill CSV row

**Tools used**:
- PDF reader with text selection (Adobe Acrobat, Foxit, Okular)
- Europe PMC API (for full-text XML when available)
- Spreadsheet editor (Excel, LibreOffice, Python pandas)

**Quality checks during extraction**:
- ✅ Value matches Figure (not off by 10× due to unit confusion)
- ✅ WT/canonical identified (not a mutant/control)
- ✅ License checked (paper is OA: CC-BY/CC0, or fair use applies)

---

### Phase 3: Verification

**Initial entry**: `Verification_statut = "To confirm"`

**Verification process** (second pass):
1. Re-open paper
2. Re-locate Figure/Table
3. Confirm value exact match
4. Check units again (common errors: ns vs µs, mM vs µM)
5. Update: `Verification_statut = "Verified"`

**Verification target**:
- Stable: 100% verified
- Beta: >75% verified
- Current v1.3.0-beta: ~80% verified

**Who verifies?**
- v1.1-v1.2.1: Single curator (Tommy Lepesteur)
- v1.3+: Planned inter-curator validation (10% sample)
- v1.4+: Community contributions with maintainer review

---

## 🎨 Classification System

### Class A: Bio-Intrinsic (Native Biological)

**Definition**: Natural biological molecules/proteins with quantum properties

**Examples**:
- Cryptochrome (proposed magnetoreceptor)
- Aromatic amino acids (tryptophan ODMR)
- FMO complex (photosynthesis, debated quantum coherence)

**Criteria**:
- Found naturally in organisms
- No synthetic engineering required
- Quantum property demonstrated or strongly hypothesized

**Count**: 4/80 systems (5% in v1.3.0-beta)

---

### Class B: Bio-Compatible Internalized

**Definition**: Synthetic quantum systems introduced into biological environments

**Examples**:
- NV nanodiamonds in HeLa cells
- SiC nanoparticles in neurons
- Quantum dots conjugated to antibodies

**Criteria**:
- Not naturally occurring
- Internalized/attached to biological matter
- Quantum readout demonstrated in bio context

**Count**: 28/80 systems (35% in v1.3.0-beta)

---

### Class C: Hyperpolarized Nuclei (NMR)

**Definition**: Nuclear spins (^13C, ^15N, ^31P) with enhanced polarization

**Examples**:
- Pyruvate ^13C (FDA-approved MRI contrast agent)
- Fumarate ^13C (metabolic imaging)
- Glucose ^13C (brain metabolism)

**Criteria**:
- Hyperpolarization required (DNP, PHIP, or parahydrogen)
- T1 > 10s (long-lived for imaging)
- In vivo application demonstrated or feasible

**Count**: 12/80 systems (15% in v1.3.0-beta)

---

### Class D: Mechanistic Candidates (Hypotheses)

**Definition**: Systems with proposed quantum function, indirect evidence

**Examples**:
- Cryptochrome (radical pair mechanism, no direct T2 measurement in vivo)
- Magnetosomes (magnetite crystals, coherence hypothesized)
- Microtubules (Penrose-Hameroff Orch OR, highly controversial)

**Criteria**:
- High-impact publication (Nature, Science, PNAS, PRL)
- Active research area (>10 citations/year)
- Mechanistic model proposed with quantum coherence role
- **Explicit caveat**: Marked Tier ★ (Exploratory), not used for ML training without flagging

**Count**: 2/80 systems (2.5% in v1.3.0-beta, max 10% allowed)

---

## 🧮 Unit Standardization

### T2 (Coherence Time)

**Standard unit**: Microseconds (µs)

**Conversions**:
```
1 ms = 1000 µs
1 ns = 0.001 µs
1 s = 1,000,000 µs
```

**Validation**: Linter checks T2 >0.001 µs (lower bound: 1 ns, realistic for room-temp bio systems)

---

### T1 (Relaxation Time)

**Standard unit**: Seconds (s)

**Conversions**:
```
1 min = 60 s
1 ms = 0.001 s
```

**Validation**: Linter checks T1 >0.1 s (lower bound for hyperpolarized systems)

---

### Optical Contrast

**Standard units** (multiple accepted):
- `fold` (fold-change: 1.0 = no change, 2.0 = doubling)
- `deltaF/F0` (fractional change: 0.5 = 50% increase)
- `percent` (percentage: 50 = 50% increase)

**Normalization** (v1.3+):
- All converted to `contrast_normalized` (fold-change basis)
- Formula:
  - `fold` → as-is (e.g., 26 → 26.0)
  - `deltaF/F0` → 1 + value (e.g., 0.35 → 1.35)
  - `percent` → 1 + value/100 (e.g., 18% → 1.18)

---

## 🔐 License Compliance

### Allowed Licenses (for direct inclusion)

- ✅ **CC-BY** (Creative Commons Attribution)
- ✅ **CC0** (Public Domain)
- ✅ **CC-BY-SA** (Share-Alike, pointer-only in FPbase case)
- ✅ **OA with author permission** (email confirmation documented)

### Restricted Licenses (excluded or pointer-only)

- ⚠️ **Paywalled journals** (no OA version):
  - Excluded from dataset unless fair use applies (single value extraction)
  - Logged in `reports/EXCLUDED_FOR_LICENSE.md`
  
- ⚠️ **Non-commercial licenses** (CC-BY-NC):
  - Excluded by default (conflicts with commercial use downstream)
  - Exception: If explicitly relevant and no OA alternative exists

### Verification Process

For each entry:
1. Check journal policy (via Sherpa Romeo or journal website)
2. Confirm OA status (green icon on journal page or PMC listing)
3. Record license in `license` column
4. If uncertain: Contact publisher or exclude

**Current compliance**:
- v1.2.1: 100% OA (all entries CC-BY or CC0)
- v1.3.0-beta: 10% verified (curated entries), 90% "varies (see DOI)" (specialist DBs, pending verification)

---

## 🤝 Community Contributions (Planned v1.4+)

### How to Contribute

**Current (v1.3)**: Closed curation (maintainer only)

**Planned (v1.4+)**: Open to community via GitHub PRs

**Contribution workflow** (coming soon):
1. Fork repository
2. Add new system to CSV (use template in `CONTRIBUTING.md`)
3. Run `qubits_linter.py` (must pass with 0 errors)
4. Create PR with:
   - System name in title
   - DOI link in description
   - Screenshot of Figure/Table (provenance proof)
5. Maintainer review (within 7 days)
6. If approved: Merged into next beta release

**Credit system**:
- Contributors listed in `CONTRIBUTORS.md`
- Curator field tracks who added each entry
- Top contributors may be invited as co-authors on Data Descriptor

---

## 📊 Data Quality Metrics (Automated)

### Linter Checks (`qubits_linter.py`)

**Blocking errors** (exit code 1):
- Missing mandatory fields (Systeme, Classe, T2_us for Class A/B/C)
- Invalid DOI format (must start with "10.")
- Out-of-range values (T2 <0.001 µs or >1,000,000 µs)
- Duplicate SystemIDs

**Warnings** (exit code 0 in beta, 1 in stable):
- Missing provenance (Source_T2 empty but T2 measured)
- Missing uncertainties (T2_us_err empty)
- Verification status "To confirm" (>25% in stable)

**Usage**:
```bash
# Beta mode (warnings OK)
QA_MODE=beta python qubits_linter.py

# Stable mode (warnings = errors)
QA_MODE=stable python qubits_linter.py
```

---

### QA Report Generation

**Automated reports**:
- `QC_REPORT.md` — Full quality control audit
- `reports/AUDIT_v1.3_fp_optical.md` — Release-specific audit
- `reports/METRICS_v1.3.json` — Machine-readable metrics

**Metrics tracked**:
- N_total, N_measured, N_verified
- Provenance coverage (%)
- License compliance (%)
- Quality tier distribution
- Family/Class distribution

---

## 🔬 Methodological Inspirations

This catalog's curation methodology is inspired by:

1. **UniProt** (tiered curation, provenance tracking)
   - DOI: [10.1093/nar/gkaa1100](https://doi.org/10.1093/nar/gkaa1100)
   - Adapted: Verification levels, evidence codes

2. **Materials Project** (hybrid database approach)
   - DOI: [10.1063/1.4812323](https://doi.org/10.1063/1.4812323)
   - Adapted: Computational + experimental integration

3. **FAIR Data Principles** (findable, accessible, interoperable, reusable)
   - DOI: [10.1038/sdata.2016.18](https://doi.org/10.1038/sdata.2016.18)
   - Implemented: Metadata, provenance, open licenses, versioning

4. **FPbase** (fluorescent protein database)
   - URL: [https://fpbase.org](https://fpbase.org)
   - Adapted: GraphQL API integration, cross-referencing

---

## 🎯 Future Improvements

### Short-term (v1.3.0 stable → v1.4.0)
- [ ] Complete license audit (100% verified)
- [ ] Add Tier A measurements (with CIs)
- [ ] Inter-curator validation (10% sample)
- [ ] Automated evidence extraction (PMC XML parser)

### Medium-term (v1.4.0 → v2.0.0)
- [ ] Systematic review (200+ systems)
- [ ] Community contribution workflow
- [ ] REST API endpoint
- [ ] Multi-language metadata

### Long-term (v2.0+)
- [ ] Schema v2.0 (breaking changes: unified measurement standards)
- [ ] Integration with other databases (Materials Project, PubChem)
- [ ] Automated weekly pre-releases (CI/CD pipeline)
- [ ] Machine learning models trained on catalog (fp-qubit-design v2.0)

---

## 📚 References & Further Reading

**Key papers cited in methodology**:
- Gruber et al. 1997 (first NV center ODMR): DOI:10.1126/science.276.5321.2012
- Chen et al. 2013 (GCaMP6 suite): DOI:10.1038/nature12354
- Hanson & Awschalom 2008 (quantum sensing review): DOI:10.1038/nphys1075

**Methodological standards**:
- PRISMA guidelines (systematic reviews): [https://prisma-statement.org](https://prisma-statement.org)
- FAIR principles: [https://www.go-fair.org](https://www.go-fair.org)
- Semantic Versioning: [https://semver.org](https://semver.org)

---

## 📧 Questions or Feedback?

**Methodology-related questions**:
- Open GitHub Issue with label `methodology`
- Email maintainer: [via GitHub profile]

**Suggestions for improvement**:
- Open GitHub Discussion: "Curation Methodology Feedback"
- Pull requests welcome (for documentation improvements)

---

**Last updated**: 2025-10-24  
**Maintainer**: Tommy Lepesteur  
**License**: This methodology document is CC-BY-4.0  
**Version**: 1.3 (aligned with catalog v1.3.0-beta)

