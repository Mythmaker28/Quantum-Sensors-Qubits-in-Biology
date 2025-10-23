# Backlog — Atlas v1.3 Roadmap

**Date**: 2025-10-23  
**Current Version**: v1.2.1  
**Next Version**: v1.3 (target: Q1 2026)

---

## 🎯 Objectifs v1.3

**Quantitatifs**:
- N_fp_like_total: 150-200 (vs 66 actuel)
- N_fp_like_with_contrast_measured: 75-100 (vs 54 actuel)
- Familles: 12-15 avec ≥3 mesures (vs 7 actuel)

**Qualitatifs**:
- Tier A (with CI/n): ≥20 entrées
- Spectral data: ex/em pour 80%+ entrées
- Temperature & pH: 50%+ entrées

---

## 📋 Features Prioritaires

### 1. FPbase GraphQL Full Integration

**Description**: Intégrer l'API GraphQL de FPbase (https://www.fpbase.org/graphql/) pour récupérer toutes les FPs avec propriétés complètes.

**Impact**: 🔥 **TRÈS ÉLEVÉ**  
**Effort**: MOYEN (2-3 jours)  
**Risque**: BAS (API stable depuis 2019)

**Deliverables**:
- `scripts/providers/fpbase_graphql.py`
- Requêtes pour: name, ex/em, QY, ε, brightness, DOI/PMID
- Cache local (SQLite) pour éviter re-fetches
- +150 FPs potentiels

**Estimations**:
- Entries: +100-150
- Measured contrasts: +20-40 (via DOIs récupérés)
- Spectral data: 90%+

**Dependencies**: Aucune (API publique)

**Notes**: License FPbase = CC BY-SA (pointer-only pour textes, OK pour chiffres).

---

### 2. Supplementary Data Extraction

**Description**: Télécharger et parser les fichiers supplémentaires (Excel, CSV, PDF tables) des publications clés.

**Impact**: 🔥 **ÉLEVÉ**  
**Effort**: ÉLEVÉ (5-7 jours)  
**Risque**: MOYEN (formats hétérogènes)

**Deliverables**:
- `scripts/etl/fetch_supplements.py` (Nature, Science, Cell APIs)
- `scripts/etl/extract_contrast_spreadsheets.py` (openpyxl, pandas)
- `scripts/etl/extract_contrast_pdf_tables.py` (pdfplumber, camelot)
- `reports/SUPP_FETCH_LOG.md`

**Cibles prioritaires**:
- Chen 2013 (GCaMP6): Extended Data probablement avec TOUTES les variantes
- Dana 2019 (jGCaMP7): Supplementary tables
- Zhang 2021 (jGCaMP8): Source Data
- Shaner 2013/2017 (mNeonGreen, mScarlet): Photophysics tables

**Estimations**:
- Measured contrasts: +15-30
- Temperature/pH data: +20-40 entrées
- Tier A (with n/SD): +10-20

---

### 3. OCR Figure Captions & Tables

**Description**: OCR sur figures/tables des PDFs OA pour extraire valeurs numériques.

**Impact**: MOYEN  
**Effort**: MOYEN (3-4 jours)  
**Risque**: ÉLEVÉ (OCR quality variable)

**Deliverables**:
- `scripts/etl/extract_contrast_captions.py` (pytesseract)
- `scripts/etl/extract_contrast_pdf_images.py` (pdf2image + OCR)
- Post-processing (validate numbers in plausible range)

**Estimations**:
- Measured contrasts: +5-15
- Quality: Variable (manual validation required)

**Dependencies**: tesseract-ocr install

---

### 4. Photoswitchable FPs Addition

**Description**: Ajouter les FPs photoswitchables (Dronpa, Padron, mEos, Kaede, etc.)

**Impact**: MOYEN  
**Effort**: BAS (1-2 jours)  
**Risque**: BAS

**Deliverables**:
- Colonne `is_photoswitchable` (0/1)
- Colonne `switch_contrast` (ratio état on/off)
- ~20-30 nouvelles entrées

**Estimations**:
- Entries: +20-30
- Switch contrasts: +15-25 (très élevés, >100x possible)

**Notes**: Pertinent pour fp-qubit-design si photoswitching = mécanisme de contrôle optique.

---

### 5. Fuzzy Name Matching & Deduplication

**Description**: Améliorer le matching avec Levenshtein distance pour récupérer les 3 ratés (TagRFP, Clover, jGCaMP7c).

**Impact**: BAS  
**Effort**: BAS (0.5 jour)  
**Risque**: BAS

**Deliverables**:
- `scripts/etl/fuzzy_matcher.py` (fuzzywuzzy ou rapidfuzz)
- Seuil: Levenshtein ≤ 2 + validation sémantique

**Estimations**:
- Entries recovered: +3-5
- Quality improvement: HAUTE (évite doublons)

---

### 6. NLP-Based Extraction (BioBERT/SciBERT)

**Description**: Extraction avancée avec transformers pour mieux capturer les mesures dans texte narratif.

**Impact**: 🔥 **TRÈS ÉLEVÉ** (long-term)  
**Effort**: TRÈS ÉLEVÉ (10-15 jours)  
**Risque**: ÉLEVÉ (complexité ML)

**Deliverables**:
- Fine-tuned model sur corpus biosenseurs
- Entity recognition: (protein, measurement, unit, condition)
- Relation extraction: protein ↔ measurement

**Estimations**:
- Measured contrasts: +50-100
- Precision/Recall: 80-90% (avec validation)

**Dependencies**: transformers, torch, labeled training set

**Notes**: Projet v1.3 ou v2.0 (ambitieux).

---

### 7. Community Contribution Workflow

**Description**: Système de crowdsourcing pour soumettre nouveaux biosenseurs.

**Impact**: ÉLEVÉ (scalability)  
**Effort**: MOYEN (3-4 jours)  
**Risque**: BAS

**Deliverables**:
- GitHub Issue template "Submit Biosensor"
- GitHub Action pour valider format
- Auto-PR si validation passe
- Community review process

**Estimations**:
- Contributions: 5-20/an (estimé)
- Quality: Variable (need moderation)

---

### 8. Specialist Databases Cross-Referencing

**Description**: Intégrer GECI DB, Biosensor DB, FluoroFinder (pointer-only pour DOIs).

**Impact**: ÉLEVÉ  
**Effort**: MOYEN (2-3 jours)  
**Risque**: MOYEN (APIs/scraping)

**Deliverables**:
- `scripts/providers/geci_db.py`
- `scripts/providers/biosensor_db.py`
- DOI extraction → PMC fetch pour mesures

**Estimations**:
- Entries: +30-50
- Measured contrasts: +20-40

---

## 📊 Priorisation (MoSCoW)

### Must Have (v1.3.0)

1. ✅ FPbase GraphQL integration
2. ✅ Supplementary data extraction
3. ✅ Fuzzy matching

### Should Have (v1.3.0 or v1.3.1)

4. ✅ OCR captions
5. ✅ Photoswitchable FPs
6. ✅ Specialist DBs

### Could Have (v1.3.x)

7. ✅ Community workflow
8. ✅ Spectral arrays (HDF5)

### Won't Have (defer to v2.0)

9. ⏸ NLP/BioBERT (too ambitious for v1.3)
10. ⏸ API REST public (need infrastructure)

---

## 🗓 Timeline Estimée

**Q4 2025** (Nov-Dec):
- FPbase GraphQL (2 semaines)
- Supplements extraction (3 semaines)
- Fuzzy matching (1 semaine)
- **Release v1.3.0-alpha** (150+ entries, 70+ measured)

**Q1 2026** (Jan-Mar):
- OCR implementation (2 semaines)
- Photoswitchable FPs (1 semaine)
- Specialist DBs (2 semaines)
- **Release v1.3.0** (180+ entries, 85+ measured)

**Q2 2026** (Apr-Jun):
- Community workflow (3 semaines)
- Incremental improvements
- **Release v1.3.1** (stable)

---

## 💰 Resource Estimations

| Feature | Dev Time | Compute | Storage |
|---------|----------|---------|---------|
| FPbase GraphQL | 2-3 days | Minimal | +5 MB |
| Supplements | 5-7 days | Moderate | +50-100 MB |
| OCR | 3-4 days | High | +200-500 MB |
| NLP (v2.0) | 10-15 days | Very High | +1-2 GB |

---

## 🎓 Lessons for v1.3

### What Worked in v1.2.1

1. **Literature curation** = Highest yield/effort ratio
2. **Seed-based fallback** = Robust when APIs down
3. **Strict data integrity** = Zero regrets, high trust
4. **Family diversification** = Prevents bias

### What to Improve

1. **Automate more** (less manual curation)
2. **Better name resolution** (fuzzy matching earlier)
3. **Spectral data** (not just ex_max/em_max)
4. **Temperature & pH** (critical for biosensors)

---

## 🔮 Vision v2.0 (2026-2027)

**Transformations majeures**:
- Public API REST (queries programmatiques)
- Interactive dashboard (Streamlit/Plotly)
- Multi-modality fusion (FP + NV centers + NMR)
- Quantum-enhanced biosensors (hybrid class A+B)
- Machine learning models (predict contrast from sequence)

---

## 📞 Feedback Loop

Cette backlog est **vivante**. Contributions bienvenues via:
- GitHub Issues (feature requests)
- Discussions (brainstorming)
- Pull Requests (implementations)

---

**End of Backlog v1.3**

