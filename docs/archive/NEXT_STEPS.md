# 🗺️ Roadmap — Atlas des Qubits Biologiques

## ✅ v1.2 - COMPLÉTÉ (22 Oct 2025)

### Infrastructure ✅
- [x] Dataset v1.2 (22 systèmes, 33 colonnes)
- [x] 0 erreur bloquante (QC validé)
- [x] Provenance tracée (86% T2, 100% T1, 89% Contraste)
- [x] Incertitudes quantifiées (100%)
- [x] Linter automatique (`qubits_linter.py`)
- [x] LICENSE CC BY 4.0 + CITATION.cff
- [x] CI/CD GitHub Actions
- [x] GitHub Pages configuré
- [x] Templates issues/PR

---

## 🚀 v1.3 - EN COURS (Nov-Déc 2025)

### 🎯 Objectifs prioritaires

#### 1. Enrichissement dataset (+15 entrées)
**Objectif** : Passer de 22 à 37 systèmes

**Priorités** :
- [ ] **5 NV nanodiamants in vivo** (nouveaux papiers 2023-2025)
  - NV dans neurones de souris (2024)
  - NV dans Drosophila (2023)
  - NV dans tissu tumoral (2024)
  - NV microcristaux dans moelle épinière (2023)
  - NV dans embryons zebrafish (2025)

- [ ] **4 SiC variants** (3C-SiC, 6H-SiC)
  - VSi dans 3C-SiC (fréquence différente)
  - VV dans 6H-SiC (polytypes alternatifs)
  - NCVSi complex dans 4H-SiC
  - CSiVC complex dans 4H-SiC

- [ ] **3 qubits protéiques** (classe A expansion)
  - Variants GFP ODMR (mutations optimisées)
  - Cytochrome c avec lecture ESR
  - Ferritine avec spin électronique

- [ ] **2 hyperpolarisés** (classe C)
  - Lactate ^13C (métabolisme anaérobie)
  - Bicarbonate ^13C (équilibre acide-base)

- [ ] **1 quantum dot biocompatible** (classe B)
  - InP quantum dots (non toxique, alternative CdSe)

#### 2. Provenance 100%
- [ ] Compléter Source_T2 pour 3 systèmes (86% → 100%)
- [ ] Compléter Source_Contraste pour 2 systèmes (89% → 100%)
- [ ] Ajouter Source_T1 pour classe B (si T1 mesuré)

#### 3. Toxicité enrichie
- [ ] Compléter Toxicity_note pour 11 systèmes classe B
- [ ] Ajouter études cytotoxicité long terme (>7 jours)
- [ ] Préciser LC50/IC50 quand disponible
- [ ] Ajouter notes biocompatibilité in vivo

#### 4. Figures & visualisations
- [ ] **T2 vs Température** (scatter plot, coloré par classe)
- [ ] **Timeline publications** (2006-2025, barres empilées par classe)
- [ ] **Distribution méthodes** (pie chart ODMR/ESR/NMR/Indirect)
- [ ] **In vivo vs in vitro** (bar chart, pourcentage par classe)
- [ ] Intégrer dans `index.html` avec Plotly.js

#### 5. Zenodo DOI
- [ ] Connecter repo GitHub à Zenodo via webhook
- [ ] Déposer release v1.2.0 sur Zenodo
- [ ] Obtenir DOI permanent
- [ ] Mettre à jour CITATION.cff avec DOI Zenodo
- [ ] Ajouter badge DOI dans README

---

## 📅 v1.4 - PLANIFIÉ (Jan-Fév 2026)

### Objectifs

#### 1. Dataset enrichi (+20 entrées, total 57)
- [ ] 10 systèmes classe B (autres défauts: SnV, VB, DV0)
- [ ] 5 systèmes classe C (autres isotopes: ^15N, ^31P, ^129Xe)
- [ ] 3 systèmes classe A (protéines photo-activables)
- [ ] 2 systèmes classe D (autres hypothèses magnétoréception)

#### 2. Métadonnées étendues
- [ ] Ajouter colonne `PDB_code` (pour protéines classe A)
- [ ] Ajouter colonne `Material_database_ID` (Materials Project, ICSD)
- [ ] Ajouter colonne `Applications` (liste applications démontrées)
- [ ] Ajouter colonne `Funding_agency` (provenance financement)

#### 3. API REST
- [ ] Créer API Flask/FastAPI pour accès programmatique
- [ ] Endpoints : `/systems`, `/search`, `/stats`, `/export`
- [ ] Déployer sur Heroku/Railway (gratuit)
- [ ] Documentation OpenAPI/Swagger

#### 4. Intégrations externes
- [ ] Lien automatique vers PubMed (afficher abstracts)
- [ ] Lien vers Materials Project (structures cristallines)
- [ ] Lien vers PDB (structures protéiques)
- [ ] Lien vers Zenodo (datasets connexes)

---

## 🔮 v2.0 - VISION (2026-2027)

### Objectifs ambitieux

#### 1. Dataset complet (100+ systèmes)
- [ ] Couvrir tous les défauts diamant connus (20+)
- [ ] Couvrir tous les polytypes SiC (3C, 4H, 6H, 15R)
- [ ] Couvrir tous les isotopes hyperpolarisés cliniques
- [ ] Couvrir tous les candidats magnétoréception

#### 2. Multi-langue
- [ ] Interface anglais/français
- [ ] Documentation bilingue
- [ ] Contributions internationales

#### 3. Visualisations avancées
- [ ] Dashboard interactif (Dash/Streamlit)
- [ ] Graphiques 3D (T2 vs T vs Contraste)
- [ ] Heatmaps corrélations
- [ ] Animations timeline
- [ ] Comparateur systèmes (side-by-side)

#### 4. Machine Learning
- [ ] Prédiction T2 à partir de structure (ML model)
- [ ] Clustering systèmes (similarité)
- [ ] Recommandation systèmes pour applications
- [ ] Détection anomalies (outliers)

#### 5. Communauté
- [ ] 10+ contributeurs externes
- [ ] 50+ citations (Google Scholar)
- [ ] Partenariats institutionnels (Harvard, Stuttgart, Chicago)
- [ ] Workshops annuels

---

## 📊 Métriques de succès

### Données
| Métrique | v1.2 (Oct 2025) | v1.3 (Déc 2025) | v1.4 (Fév 2026) | v2.0 (2027) |
|----------|-----------------|-----------------|-----------------|-------------|
| **Systèmes** | 22 | 37 | 57 | 100+ |
| **Colonnes** | 33 | 35 | 40 | 50+ |
| **Provenance** | 86% | 100% | 100% | 100% |
| **Vérifiés** | 64% | 75% | 85% | 90% |

### Qualité
| Métrique | v1.2 | v1.3 | v1.4 | v2.0 |
|----------|------|------|------|------|
| **Erreurs lint** | 0 | 0 | 0 | 0 |
| **DOI valides** | 100% | 100% | 100% | 100% |
| **Incertitudes** | 100% | 100% | 100% | 100% |

### Impact
| Métrique | v1.2 | v1.3 | v1.4 | v2.0 |
|----------|------|------|------|------|
| **Citations** | 0 | 5 | 15 | 50+ |
| **Contributeurs** | 1 | 3 | 7 | 10+ |
| **Stars GitHub** | 0 | 25 | 75 | 200+ |
| **Downloads** | 0 | 100 | 500 | 2000+ |

---

## 🎯 Prochaines actions immédiates

### Cette semaine (22-29 Oct 2025)
1. [ ] **Créer repo GitHub** `biological-qubits-atlas` (voir GITHUB_SETUP.md)
2. [ ] **Activer GitHub Pages** (Settings → Pages → GitHub Actions)
3. [ ] **Créer PR v1.2** (develop → main)
4. [ ] **Merger PR** (après review)
5. [ ] **Release v1.2.0** + tag
6. [ ] **Déposer sur Zenodo** (obtenir DOI)
7. [ ] **Créer 4 issues initiales**
8. [ ] **Activer Discussions**

### Semaine prochaine (29 Oct - 5 Nov 2025)
1. [ ] **Ajouter badge DOI** dans README
2. [ ] **Mettre à jour CITATION.cff** avec DOI Zenodo
3. [ ] **Commencer dataset v1.3** (+5 entrées NV in vivo)
4. [ ] **Compléter provenance** (86% → 95%)
5. [ ] **Créer première figure** (T2 vs Temp)

### Mois prochain (Nov 2025)
1. [ ] **Terminer dataset v1.3** (+15 entrées)
2. [ ] **Enrichir toxicité** (11 systèmes classe B)
3. [ ] **Créer 4 figures** (timeline, méthodes, in vivo%, T2 vs Temp)
4. [ ] **Article Data Descriptor** (Scientific Data) — draft
5. [ ] **Outreach** : Twitter thread, blog post, email équipes

---

## 🌐 Outreach & Communication

### Équipes à contacter
1. **Groupe Lukin (Harvard)** — NV nanodiamants in vivo
2. **Groupe Wrachtrup (Stuttgart)** — ODMR biologique, SiC
3. **Groupe Chicago (Univ. of Chicago)** — Qubit protéique classe A

### Canaux de diffusion
- [ ] **Twitter/X** : Thread v1.2 release + visuels
- [ ] **Reddit** : r/QuantumComputing, r/biophysics
- [ ] **ResearchGate** : Publication dataset
- [ ] **LinkedIn** : Post professionnel
- [ ] **Mailing lists** : quantum-bio, biophysics-announce

### Conférences cibles (2026)
- [ ] **APS March Meeting** (Mars 2026) — Poster
- [ ] **Biophysical Society Annual Meeting** (Fév 2026)
- [ ] **Quantum Tech Conference** (Avril 2026)
- [ ] **Gordon Research Conference - Quantum Sensing** (Juin 2026)

---

## 💰 Financement potentiel

### Agences
- [ ] **NSF** (USA) — Data infrastructure grant
- [ ] **ANR** (France) — Projet jeune chercheur
- [ ] **ERC** (Europe) — Starting Grant
- [ ] **Chan Zuckerberg Initiative** — Open Science

### Montant cible
- **Phase 1** (2026) : $50k — Maintenance + 1 postdoc 6 mois
- **Phase 2** (2027) : $150k — Expansion + 1 postdoc 1 an + 2 étudiants

---

## 📈 KPIs (Key Performance Indicators)

### Croissance dataset
- **Q4 2025** : 37 systèmes (+68% vs v1.2)
- **Q1 2026** : 57 systèmes (+159% vs v1.2)
- **Q4 2026** : 100 systèmes (+355% vs v1.2)

### Qualité
- **Provenance 100%** : Déc 2025
- **Vérification 90%** : Juin 2026
- **0 erreur lint** : Toujours ✅

### Impact
- **Premier article citant** : Fév 2026
- **10 citations** : Juin 2026
- **50 citations** : Déc 2026

---

**Mise à jour** : 22 Octobre 2025  
**Prochaine révision** : 1er Novembre 2025

---

*Roadmap vivant — mise à jour trimestrielle*

