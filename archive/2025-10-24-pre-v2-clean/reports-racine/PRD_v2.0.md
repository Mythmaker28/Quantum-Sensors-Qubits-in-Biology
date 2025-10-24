# Product Requirements Document — Biological Qubits Atlas v2.0

**Version** : 2.0.0  
**Date** : 24 octobre 2025  
**Équipe** : Tommy Lepesteur (Lead), Community Contributors  
**Status** : 🟢 APPROVED — Ready for Implementation

---

## 1. INTRODUCTION

### 1.1 Vision

Le **Biological Qubits Atlas** a pour ambition de devenir la **référence internationale** en biologie quantique et biosenseurs optiques, offrant :

- Le catalogue le plus exhaustif de systèmes quantiques biologiques (capteurs calcium, voltage, neurotransmetteurs, métabolites)
- Une plateforme FAIR (Findable, Accessible, Interoperable, Reusable) de niveau gold standard
- Des outils prédictifs ML pour design rationnel de nouveaux biosenseurs
- Une interface interactive facilitant l'adoption par la communauté scientifique

### 1.2 Contexte Actuel (v1.3.0-beta)

**Acquis** :
- ✅ 80 systèmes quantiques documentés
- ✅ 65 mesures de contraste (Tier B)
- ✅ Pipeline ETL reproductible
- ✅ Provenance complète (DOI + source notes)
- ✅ Linter automatique + QA
- ✅ Licence CC BY 4.0

**Limitations** :
- ⚠️ Couverture partielle (80/500+ systèmes publiés)
- ⚠️ Interface statique (CSV/HTML basique)
- ⚠️ Pas de modèles prédictifs
- ⚠️ Validation in vivo non systématisée
- ⚠️ Score FAIR incomplet (8/12)

---

## 2. OBJECTIFS v2.0

### 2.1 Objectifs Quantitatifs

| Métrique | v1.3 | v2.0 Target | Croissance |
|----------|------|-------------|------------|
| **Systèmes totaux** | 80 | 200+ | **+150%** |
| **Avec contraste mesuré** | 65 | 150+ | **+130%** |
| **Familles (≥5 systèmes)** | 5 | 12+ | **+140%** |
| **Score FAIR** | 8/12 | 12/12 | **100%** |
| **Citations/an (estimé)** | 50 | 200+ | **+300%** |
| **Visiteurs/an** | 500 | 10K+ | **+1900%** |

### 2.2 Objectifs Qualitatifs

1. **Exhaustivité** : Couvrir 90%+ des biosensors publiés dans Nature/Science/Neuron (2015-2025)
2. **Reproductibilité** : Pipeline 100% automatisé, déterministe, versionné
3. **Utilisabilité** : Interface interactive permettant exploration visuelle (non-experts)
4. **Innovation** : Premier atlas avec prédiction ML (T2, contraste) avant synthèse
5. **Standard** : Seul atlas biologie quantique conforme FAIR 12/12

---

## 3. FONCTIONNALITÉS REQUISES

### 3.1 Amélioration #1 : Expansion Automatisée (200+ systèmes)

**Description** : Pipeline automatisé d'extraction multi-sources vers 200+ systèmes.

**Specs Techniques** :
- **Sources** :
  - PubMed E-utilities API (clé NCBI fournie)
  - PMC full-text (XML parsing, Open Access uniquement)
  - FPbase GraphQL (protéines fluorescentes)
  - Specialist databases (preseeded CSVs)
  
- **Contraintes** :
  - ❌ Aucune donnée synthétique
  - ✅ DOI obligatoire pour toute valeur mesurée
  - ✅ Licence CC BY/CC0 vérifiée par source
  - ✅ Validation manuelle 20% échantillon (flag `curator_validated`)

- **Deliverables** :
  - `scripts/automation/auto_harvest_v2.py` (existant, à tester)
  - `data/interim/auto_harvest_v2_output.csv` (candidates)
  - `reports/HARVEST_LOG_v2.0.md` (metrics + manual validation checklist)

**Success Criteria** :
- ✅ 200+ systèmes uniques (après dedup)
- ✅ 150+ avec contraste mesuré (Tier B minimum)
- ✅ 100% sources tracées (DOI + source_note)

---

### 3.2 Amélioration #2 : Prédiction ML via GNN

**Description** : Modèle Graph Neural Network pour prédire T2/contraste depuis structure moléculaire.

**Specs Techniques** :
- **Architecture** :
  - PyTorch Geometric (GCNConv × 3 layers)
  - Input : Graphe moléculaire (SMILES → PyG Data)
  - Features : Atomes (type, charge, hybridation), Liaisons (ordre)
  - Output : [log(T2_us), contrast_normalized]

- **Dataset** :
  - Training : 150+ systèmes avec SMILES/PDB
  - Validation : 20% hold-out
  - Test : Systèmes 2024-2025 (external validation)

- **Contraintes** :
  - ✅ R² ≥ 0.75 (T2 prediction)
  - ✅ R² ≥ 0.70 (Contrast prediction)
  - ✅ Open-source (MIT license)
  - ✅ Reproductible (fixed seeds, version PyTorch)

- **Deliverables** :
  - `scripts/ml/predict_quantum_proxies.py` (existant, à entraîner)
  - `models/quantum_proxy_gnn_v2.0.pth` (trained weights)
  - `reports/ML_TRAINING_REPORT_v2.0.md` (R², loss curves, validation)

**Success Criteria** :
- ✅ R² T2 ≥ 0.75
- ✅ MAE < 0.5 log(µs)
- ✅ Inference < 1s pour 100 molécules

---

### 3.3 Amélioration #3 : Dashboard Interactif D3.js

**Description** : Interface web moderne avec visualisations interactives.

**Specs Techniques** :
- **Visualisations** :
  - Scatter plot T2 vs Température (zoom, tooltip, filtres)
  - Barplot familles (trié par médiane T2)
  - Timeline publications (évolution temporelle)
  - Network graph (relations famille-méthode)

- **Technologies** :
  - D3.js v7 (via CDN, pas de build npm)
  - Responsive design (mobile/tablette)
  - Export SVG/PNG haute résolution

- **Contraintes** :
  - ✅ Standalone HTML (pas de serveur backend requis)
  - ✅ Chargement CSV local (fetch API)
  - ✅ Accessible (WCAG 2.1 niveau AA)

- **Deliverables** :
  - `scripts/web/generate_interactive_dashboard.py` (existant, à tester)
  - `index_v2.html` (dashboard généré)
  - `docs/DASHBOARD_USER_GUIDE.md`

**Success Criteria** :
- ✅ Temps chargement < 2s (80 systèmes)
- ✅ Responsive sur mobile
- ✅ Graphiques exportables en SVG 300 dpi

---

### 3.4 Amélioration #4 : Validation In Vivo Systématique

**Description** : Système automatisé de validation contexte in vivo.

**Specs Techniques** :
- **Scoring (0-100)** :
  - Organisme détecté (mouse, rat, zebrafish): +30
  - Context "in_vivo" explicite: +20
  - Méthode quantitative (ODMR, imaging): +20
  - Publication high-impact (Nature, Science): +20
  - Contraste mesuré: +10

- **Outputs** :
  - Flag `in_vivo_validated` (Boolean)
  - Score `in_vivo_score` (0-100)
  - Field `organism` (mouse|rat|zebrafish|c.elegans|human|NA)

- **Deliverables** :
  - `scripts/qa/in_vivo_validator.py` (existant, à tester)
  - `reports/IN_VIVO_VALIDATION_v2.0.md` (top 10 + gaps)

**Success Criteria** :
- ✅ 60%+ systèmes validés in vivo (score ≥50)
- ✅ 100% systèmes avec flag (Boolean, jamais NULL)

---

### 3.5 Amélioration #5 : Conformité FAIR Avancée

**Description** : Score FAIR 12/12 avec métadonnées complètes.

**Specs Techniques** :
- **Formats générés** :
  - Schema.org JSON-LD (Google Dataset Search)
  - DataCite XML (DOI minting Zenodo)
  - DCAT JSON-LD (EU Open Data Portal)
  - CODEMETA JSON (software metadata)

- **Checklist FAIR** :
  - F1: DOI persistant ✅
  - F2: Métadonnées riches ✅
  - F3: DOI dans metadata ✅
  - F4: Indexable ✅
  - A1: Protocole ouvert (HTTPS) ✅
  - A2: Métadonnées persistantes ✅
  - I1: Format standard (CSV/Parquet) ✅
  - I2: Vocabulaire contrôlé ✅
  - I3: Références qualifiées ✅
  - R1: Licence explicite ✅
  - R1.1: Provenance ✅
  - R1.2: Standards communautaires ✅

- **Deliverables** :
  - `scripts/fair/generate_fair_metadata.py` (existant, à tester)
  - `metadata/fair/schema_org_v2.0.json`
  - `metadata/fair/datacite_v2.0.xml`
  - `metadata/fair/codemeta.json` (NEW)

**Success Criteria** :
- ✅ Score FAIR : 12/12 (100%)
- ✅ Indexé Google Dataset Search dans 7 jours

---

## 4. EXIGENCES TECHNIQUES

### 4.1 Stack Technologique

**Langages** :
- Python 3.8+ (core pipeline)
- JavaScript (D3.js dashboard, vanilla ES6+)
- Markdown (documentation)

**Dépendances Python** :
- **Core** : pandas ≥2.0, numpy ≥1.24, requests ≥2.31
- **ML** : torch ≥2.0, torch-geometric ≥2.3, rdkit ≥2022.9, scikit-learn ≥1.3
- **Automation** : biopython ≥1.80, beautifulsoup4 ≥4.12
- **Web** : Aucune (D3.js via CDN)

**Dépendances Externes** :
- NCBI E-utilities API (clé fournie: a0b0aa017e8720528fb9f89dc68088ce8208)
- FPbase GraphQL (API publique)
- Zenodo API (pour DOI)

### 4.2 Standards & Licences

**Code** :
- Licence : Apache-2.0 (permissive, compatible OSI)
- Style : PEP 8 (Python), ESLint (JavaScript)
- Tests : pytest ≥7.4, coverage ≥90%

**Données** :
- Licence : CC BY 4.0 (attribution requise)
- Format : CSV (UTF-8), Parquet (Arrow)
- Versioning : Git tags (v2.0.0, v2.0.1, etc.)

### 4.3 Tests & QA

**Tests Unitaires** :
- `tests/test_v2_installation.py` (existant)
- `tests/test_harvest_pipeline.py` (NEW)
- `tests/test_ml_predictions.py` (NEW)
- `tests/test_dashboard_generation.py` (NEW)

**QA Automatique** :
- Linter : `qubits_linter.py` (existant, 0 erreurs bloquantes)
- Coverage : pytest-cov (≥90% code coverage)
- CI/CD : GitHub Actions (lint + tests sur PR)

---

## 5. ROADMAP

### 5.1 Timeline Global (6 mois)

```
┌────────────────────────────────────────────────────────────────┐
│  Phase 1: Quick Wins (Semaines 1-4)                           │
│  - Dashboard D3.js                                             │
│  - FAIR metadata avancée                                       │
│  - Validation in vivo                                          │
│  Livrable : Dashboard déployé + Score FAIR 12/12              │
└────────────────────────────────────────────────────────────────┘
                              ▼
┌────────────────────────────────────────────────────────────────┐
│  Phase 2: Expansion (Semaines 5-12)                           │
│  - Pipeline auto-harvest (PubMed/FPbase)                       │
│  - Curation manuelle (150 → 200 systèmes)                     │
│  Livrable : 200+ systèmes validés                             │
└────────────────────────────────────────────────────────────────┘
                              ▼
┌────────────────────────────────────────────────────────────────┐
│  Phase 3: Innovation ML (Semaines 13-24)                      │
│  - Collecte features (SMILES/PDB)                              │
│  - Entraînement GNN (R² >0.75)                                │
│  Livrable : Modèle prédictif + API publique                   │
└────────────────────────────────────────────────────────────────┘
```

### 5.2 Détail Phase 1 (Prioritaire)

| Semaine | Tâche | Deliverable | Owner |
|---------|-------|-------------|-------|
| **1** | FAIR metadata | `metadata/fair/*.json` | Auto |
| **2-3** | Dashboard D3.js | `index_v2.html` | Auto |
| **4** | Validation in vivo | `reports/IN_VIVO_v2.0.md` | Auto |

**Checkpoint Phase 1** : Dashboard déployé, FAIR 12/12, rapport validation ✅

---

## 6. MESURES DE SUCCÈS

### 6.1 KPIs Principaux

| KPI | Baseline (v1.3) | Target (v2.0) | Méthode Mesure |
|-----|-----------------|---------------|----------------|
| **Total systèmes** | 80 | 200+ | `wc -l atlas_v2.csv` |
| **Contraste mesuré** | 65 | 150+ | `grep -v "NA" | wc -l` |
| **Score FAIR** | 8/12 | 12/12 | Checklist manuelle |
| **R² ML (T2)** | N/A | ≥0.75 | `sklearn.metrics.r2_score` |
| **Visiteurs/an** | 500 | 10K+ | Google Analytics |
| **Citations/an** | 50 | 200+ | Google Scholar |

### 6.2 Acceptance Criteria (Release Gate)

**Critères Bloquants** (must pass avant release v2.0) :

- ✅ N_total ≥ 200
- ✅ N_measured ≥ 150
- ✅ families_with_≥5 ≥ 12
- ✅ Score FAIR = 12/12
- ✅ Linter : 0 erreurs bloquantes
- ✅ Tests : 100% pass
- ✅ Dashboard : chargement < 2s
- ✅ ML model : R² ≥ 0.75 (si Phase 3 complétée)

**Critères Non-Bloquants** (nice-to-have) :

- ⚠️ Code coverage ≥ 90%
- ⚠️ Documentation complète (100% fonctions documentées)
- ⚠️ Peer-review externe (2+ reviewers GitHub)

---

## 7. RISQUES & MITIGATION

### 7.1 Risques Techniques

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| **FPbase API down** | Moyen | Élevé | Fallback : specialist DBs + PMC mining |
| **ML R² < 0.75** | Faible | Moyen | Feature engineering + hyperparameter tuning |
| **Licence ambiguë** | Faible | Élevé | Unpaywall API + manual check 100% entries |
| **Clé NCBI révoquée** | Très faible | Élevé | Backup key + rate limiting |

### 7.2 Risques Non-Techniques

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| **Manque contributeurs** | Moyen | Moyen | Documentation claire + exemples |
| **Faible adoption** | Faible | Élevé | Marketing : Twitter, bioRxiv, conférences |

---

## 8. DÉPENDANCES & ASSUMPTIONS

### 8.1 Dépendances Externes

- ✅ Clé NCBI fournie (a0b0aa017e8720528fb9f89dc68088ce8208)
- ✅ FPbase API accessible
- ✅ PMC Open Access stable
- ✅ Zenodo API fonctionnel

### 8.2 Assumptions

- Dataset actuel (v1.3.0-beta) est valide et propre
- Infrastructure GitHub Actions disponible pour CI/CD
- Communauté scientifique réceptive (bioRxiv preprint soumis)

---

## 9. WORKFLOW DÉVELOPPEMENT

### 9.1 Branching Strategy

```
main
  ├─ release/v2.0 (feature branch pour v2.0)
  │   ├─ feature/dashboard-d3js
  │   ├─ feature/fair-metadata
  │   └─ feature/ml-gnn
  └─ hotfix/* (si bugs critiques v1.3)
```

### 9.2 Commit Messages

Format : `<type>(<scope>): <description>`

**Types** :
- `feat`: Nouvelle fonctionnalité
- `fix`: Correction bug
- `docs`: Documentation
- `test`: Tests
- `refactor`: Refactoring
- `chore`: Maintenance

**Exemples** :
```
feat(dashboard): add D3.js interactive scatter plot
fix(harvest): handle FPbase API timeout gracefully
docs(readme): update installation instructions for v2.0
test(ml): add unit tests for GNN predictions
```

### 9.3 Pull Request Template

```markdown
## Description
Brief summary of changes

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation
- [ ] Breaking change

## Checklist
- [ ] Tests pass (`pytest tests/`)
- [ ] Linter passes (`python qubits_linter.py`)
- [ ] Documentation updated
- [ ] CHANGELOG.md updated

## Related Issues
Fixes #123
```

---

## 10. DOCUMENTATION REQUISE

### 10.1 User Documentation

- [ ] `README_v2.0.md` (quick start, features, examples)
- [ ] `CHANGELOG_v2.0.md` (what's new, breaking changes)
- [ ] `docs/DASHBOARD_USER_GUIDE.md` (dashboard usage)
- [ ] `docs/ML_API_REFERENCE.md` (model usage, API)

### 10.2 Developer Documentation

- [ ] `CONTRIBUTING_v2.0.md` (how to contribute)
- [ ] `docs/ARCHITECTURE_v2.0.md` (system design)
- [ ] `docs/TESTING_GUIDE.md` (test strategy)
- [ ] Inline docstrings (100% coverage)

---

## 11. APPROBATIONS

| Rôle | Nom | Status | Date |
|------|-----|--------|------|
| **Product Owner** | Tommy Lepesteur | ✅ APPROVED | 2025-10-24 |
| **Tech Lead** | Tommy Lepesteur | ✅ APPROVED | 2025-10-24 |
| **QA Lead** | Tommy Lepesteur | ✅ APPROVED | 2025-10-24 |

---

## 12. ANNEXES

### A. Références

- FAIR Principles: Wilkinson et al. 2016, Sci Data (DOI: 10.1038/sdata.2016.18)
- GNN Architecture: Gilmer et al. 2017, ICML
- D3.js Best Practices: Bostock 2011, IEEE TVCG

### B. Glossaire

- **GNN** : Graph Neural Network
- **FAIR** : Findable, Accessible, Interoperable, Reusable
- **PMC** : PubMed Central
- **DOI** : Digital Object Identifier
- **Tier B** : Quality tier (measured, no CI/n)

---

**END OF PRD v2.0**

📅 Dernière mise à jour : 2025-10-24  
✍️ Auteur : Tommy Lepesteur  
📜 Statut : APPROVED — Ready for Implementation  
🔗 GitHub : https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology


