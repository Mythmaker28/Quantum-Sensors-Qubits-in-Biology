# 🎯 PROMPT D'ÉVALUATION - Biological Qubits Atlas

**Pour :** Agents IA Multi-Agents (GPT, Claude, Gemini, Llama, etc.)  
**Date :** 2025-11-15  
**Objectif :** Évaluer le repo et proposer des axes d'amélioration concrets

---

## 📋 MISSION : ÉVALUATION COMPLÈTE DU REPO

Vous êtes un **agent expert** rejoignant le projet **Biological Qubits & Quantum Sensors Atlas**. Votre mission est d'**évaluer la qualité du repo** et de proposer des **améliorations concrètes**.

---

## 🔍 CONTEXTE DU PROJET

### Vue d'ensemble

**Projet :** Atlas de 296 systèmes (180 curés) - Protéines fluorescentes, biosenseurs, qubits quantiques  
**Version :** v2.2.2 (active) + dataset qubits (34 systèmes)  
**Dashboard :** https://mythmaker28.github.io/Quantum-Sensors-Qubits-in-Biology/  
**DOI Zenodo :** 10.5281/zenodo.17420604  
**Licence :** CC BY 4.0 (data) + MIT (code)

### Travail Récent (Nov 2025)

✅ **Intégration complète effectuée par CLAUDE-BACKEND-ENGINEER :**
- 4 docs scientifiques excellents (2000+ lignes) : quantum_mechanisms, photosynthesis, magnetoreception, nv_centers
- 5 scripts d'analyse qubits : validation, stats, comparaisons
- Séparation dataset qubits (34) vs FP (180)
- Architecture bus robuste pour migration worktree
- Nettoyage 18 fichiers test

**Commit récent :** `7251d5b` (3141 lignes ajoutées, 13 fichiers)

---

## 📂 STRUCTURE DU REPO (À ÉVALUER)

```
tableau proteine fluo/
│
├── 🔬 PROJET PRINCIPAL (Atlas v2.2.2)
│   ├── data/processed/atlas_fp_optical_v2_2_curated.csv  (180 systèmes)
│   ├── data/processed/atlas_fp_optical_v2_2.csv          (296 systèmes)
│   ├── docs/                                              (Documentation)
│   │   ├── ATLAS_SPEC.md, DATA_TIERS.md, STAGING_GUIDE.md
│   │   ├── quantum_mechanisms.md                         ✨ NOUVEAU
│   │   ├── photosynthesis.md                             ✨ NOUVEAU
│   │   ├── magnetoreception.md                           ✨ NOUVEAU
│   │   └── nv_centers_qubits.md                          ✨ NOUVEAU
│   ├── scripts/
│   │   ├── qa/ (12 scripts validation/cleaning)
│   │   ├── etl/ (43 scripts extraction/transformation)
│   │   ├── web/ (2 scripts dashboard)
│   │   └── validate_atlas.py
│   ├── analysis/
│   │   ├── class_comparisons.py, descriptive_stats.py, simple_stats.py (FP)
│   │   ├── qubits_stats.py                               ✨ NOUVEAU
│   │   ├── qubits_class_comparisons.py                   ✨ NOUVEAU
│   │   └── qubits_descriptive_stats.py                   ✨ NOUVEAU
│   ├── README.md                                          (Excellente doc)
│   ├── DOCUMENTATION.md                                   (Complète)
│   └── docs/index.html                                    (Dashboard)
│
├── ⚛️ DATASET QUBITS (Distinct)
│   └── data/qubits/
│       ├── biological_qubits.csv                         ✨ NOUVEAU (34 systèmes)
│       └── README.md                                      ✨ NOUVEAU (Distinction claire)
│
├── 🚌 BUS DE CONVERSATION (Infrastructure)
│   ├── conversation-bus-module/
│   │   ├── conversation_bus.py                           (Module)
│   │   ├── BUS_ARCHITECTURE.md                           ✨ NOUVEAU (400 lignes)
│   │   ├── messages/
│   │   │   └── MESSAGE_NETTOYAGE_INTEGRATION_2025-11-15.md ✨ NOUVEAU
│   │   ├── tests/ (18 fichiers)
│   │   └── débats agents syntheses/ (Archive)
│   └── ~/.conversation_bus/biological-qubits-atlas/      (Bus global)
│
└── 📝 DOCS BUS (Potentiellement à nettoyer)
    ├── DEMARRAGE_RAPIDE_2_AGENTS.md
    ├── SYSTEME_2_AGENTS_COMPLET.md
    ├── EXEMPLE_SESSION_COMPLETE.md
    ├── COORDINATION_MANUELLE.md
    ├── RATTRAPAGE_ERREURS.md
    ├── README_WINDOWS.md
    ├── GROK_DOCS_STATUS.md
    └── TEST_BUS_README.md
```

---

## 🎯 VOTRE MISSION : NOTATION ET AMÉLIORATION

### 1️⃣ ÉVALUATION GLOBALE (Note sur 10)

Évaluez les aspects suivants et **donnez une note /10** pour chacun :

#### A. Organisation & Structure (/10)
- Clarté de la structure des dossiers
- Séparation logique des composants
- Nommage des fichiers/dossiers
- Présence de fichiers redondants ou mal placés

**Note : __/10**  
**Justification :**  
**Problèmes identifiés :**  
**Améliorations proposées :**

---

#### B. Documentation (/10)
- README.md (clarté, complétude)
- DOCUMENTATION.md (exhaustivité)
- Docs scientifiques (quantum_mechanisms, etc.)
- Cohérence entre docs
- Documentation code (docstrings, comments)

**Note : __/10**  
**Justification :**  
**Problèmes identifiés :**  
**Améliorations proposées :**

---

#### C. Qualité des Données (/10)
- Datasets (atlas_fp_optical_v2_2_curated.csv, biological_qubits.csv)
- Complétude des données
- Validation (scripts validate_*.py)
- Provenance (DOI, références)
- Séparation curated vs staging

**Note : __/10**  
**Justification :**  
**Problèmes identifiés :**  
**Améliorations proposées :**

---

#### D. Code & Scripts (/10)
- Qualité du code Python
- Scripts QA/ETL/Web
- Tests unitaires (manquants ?)
- Réutilisabilité
- Gestion erreurs

**Note : __/10**  
**Justification :**  
**Problèmes identifiés :**  
**Améliorations proposées :**

---

#### E. Reproductibilité & FAIR (/10)
- FAIR 12/12 compliance
- Provenance tracking (Source_T2, DOI)
- Métadonnées (zenodo.json, CITATION.cff)
- Requirements.txt / setup.py
- Instructions d'installation

**Note : __/10**  
**Justification :**  
**Problèmes identifiés :**  
**Améliorations proposées :**

---

#### F. Dashboard & Visualisations (/10)
- Dashboard interactif (docs/index.html)
- Graphiques (figures/)
- Accessibilité
- Performance
- Filtres et export

**Note : __/10**  
**Justification :**  
**Problèmes identifiés :**  
**Améliorations proposées :**

---

#### G. Infrastructure Multi-Agents (/10)
- Bus de conversation (architecture)
- Gestion worktree
- Messages bus (traçabilité)
- Documentation bus
- Scalabilité

**Note : __/10**  
**Justification :**  
**Problèmes identifiés :**  
**Améliorations proposées :**

---

#### H. Nettoyage & Maintenance (/10)
- Fichiers temporaires/test supprimés
- Dossiers bien organisés
- .gitignore complet
- Pas de duplication
- Archive des versions (archive/)

**Note : __/10**  
**Justification :**  
**Problèmes identifiés :**  
**Améliorations proposées :**

---

### 📊 NOTE GLOBALE : __/80 → __/10

**Moyenne pondérée :**
- Organisation (15%) : __/10
- Documentation (20%) : __/10
- Qualité données (20%) : __/10
- Code (15%) : __/10
- FAIR (10%) : __/10
- Dashboard (10%) : __/10
- Multi-agents (5%) : __/10
- Nettoyage (5%) : __/10

**Note finale : __/10**

---

## 🔧 2️⃣ AXES D'AMÉLIORATION PRIORITAIRES

### TOP 5 Améliorations Urgentes

Listez les **5 améliorations les plus urgentes** par ordre de priorité :

#### 1. [TITRE DE L'AMÉLIORATION] (Priorité : 🔴 Haute / 🟠 Moyenne / 🟢 Basse)

**Problème identifié :**  
**Impact :**  
**Solution proposée :**  
**Effort estimé :** (🕐 <1h / 🕑 1-3h / 🕒 >3h)  
**Fichiers concernés :**  
**Bénéfices attendus :**

---

#### 2. [TITRE]

...

---

#### 3. [TITRE]

...

---

#### 4. [TITRE]

...

---

#### 5. [TITRE]

...

---

## 🚀 3️⃣ PLAN D'ACTION CONCRET

### Phase 1 : Quick Wins (< 1 heure)

**Actions immédiates :**
1. [ ] Action 1
2. [ ] Action 2
3. [ ] Action 3

**Fichiers à modifier :**  
**Commandes à exécuter :**

---

### Phase 2 : Améliorations Moyennes (1-3 heures)

**Actions :**
1. [ ] Action 1
2. [ ] Action 2

**Fichiers à modifier :**  
**Dépendances :**

---

### Phase 3 : Refactoring Majeur (> 3 heures)

**Actions :**
1. [ ] Action 1
2. [ ] Action 2

**Fichiers à modifier :**  
**Risques :**  
**Tests requis :**

---

## 💡 4️⃣ SUGGESTIONS INNOVANTES

### Nouvelles Fonctionnalités

Proposez **3 fonctionnalités innovantes** qui amélioreraient significativement le projet :

#### Fonctionnalité 1 : [TITRE]

**Description :**  
**Valeur ajoutée :**  
**Complexité :** (🟢 Facile / 🟠 Moyenne / 🔴 Difficile)  
**Impact utilisateur :**  
**Technologies requises :**

---

#### Fonctionnalité 2 : [TITRE]

...

---

#### Fonctionnalité 3 : [TITRE]

...

---

## 🔍 5️⃣ ANALYSE DÉTAILLÉE (Optionnel)

### Fichiers à Examiner en Détail

Choisissez **3 fichiers critiques** à analyser en profondeur :

#### Fichier 1 : `[CHEMIN]`

**Analyse :**  
**Points forts :**  
**Points faibles :**  
**Refactoring suggéré :**  
**Code proposé :**

---

#### Fichier 2 : `[CHEMIN]`

...

---

#### Fichier 3 : `[CHEMIN]`

...

---

## 📝 6️⃣ RAPPORT FINAL

### Résumé Exécutif (3-5 lignes)

Résumez votre évaluation globale :

---

### Forces du Projet (TOP 3)

1. **Force 1 :**  
2. **Force 2 :**  
3. **Force 3 :**

---

### Faiblesses du Projet (TOP 3)

1. **Faiblesse 1 :**  
2. **Faiblesse 2 :**  
3. **Faiblesse 3 :**

---

### Opportunités (TOP 3)

1. **Opportunité 1 :**  
2. **Opportunité 2 :**  
3. **Opportunité 3 :**

---

### Risques (TOP 3)

1. **Risque 1 :**  
2. **Risque 2 :**  
3. **Risque 3 :**

---

## 🚌 7️⃣ MESSAGE POUR LE BUS

**Format pour poster au bus :**

```markdown
# 📊 ÉVALUATION REPO - [TON NOM AGENT]

**Date :** [DATE]  
**Note globale :** __/10  
**Durée évaluation :** [TEMPS]

## Résumé

[Résumé 2-3 lignes]

## Top 3 Améliorations Urgentes

1. [Amélioration 1] (Priorité : 🔴)
2. [Amélioration 2] (Priorité : 🟠)
3. [Amélioration 3] (Priorité : 🟢)

## Prochaines étapes proposées

1. [ ] Action 1
2. [ ] Action 2
3. [ ] Action 3

## Zones de travail disponibles

- Zone 1 (libre)
- Zone 2 (libre)
- Zone 3 (déjà prise par [AGENT])

**Je peux travailler sur :** [ZONE CHOISIE]
```

---

## 🎯 CHECKLIST AVANT DE POSTER

Avant de poster ton évaluation au bus, vérifie que tu as :

- [ ] Noté tous les 8 aspects (/10 chacun)
- [ ] Calculé la note globale (/10)
- [ ] Identifié TOP 5 améliorations prioritaires
- [ ] Proposé un plan d'action en 3 phases
- [ ] Suggéré 3 fonctionnalités innovantes
- [ ] Rédigé un rapport final (forces/faiblesses/opportunités/risques)
- [ ] Préparé ton message pour le bus

---

## 🔗 RESSOURCES À CONSULTER

### Documentation Projet

- `README.md` : Vue d'ensemble
- `DOCUMENTATION.md` : Documentation technique complète
- `docs/ATLAS_SPEC.md` : Spécifications dataset
- `docs/DATA_TIERS.md` : Tiers de qualité

### Documentation Bus

- `conversation-bus-module/BUS_ARCHITECTURE.md` : Architecture bus
- `conversation-bus-module/messages/MESSAGE_NETTOYAGE_INTEGRATION_2025-11-15.md` : Dernier travail

### Datasets

- `data/processed/atlas_fp_optical_v2_2_curated.csv` : 180 FP
- `data/qubits/biological_qubits.csv` : 34 qubits
- `data/qubits/README.md` : Distinction des datasets

### Scripts Clés

- `scripts/qa/validate_atlas.py` : Validation FP
- `scripts/qa/validate_qubits_data.py` : Validation qubits
- `analysis/qubits_stats.py` : Stats qubits

---

## 💬 INSTRUCTIONS FINALES

### Comment Répondre

1. **Lis attentivement** toute la structure du projet
2. **Examine les fichiers clés** (README, DOCUMENTATION, datasets)
3. **Exécute les scripts** de validation si possible
4. **Note chaque aspect** avec justification
5. **Propose des améliorations concrètes** (pas de généralités)
6. **Priorise** tes suggestions (urgent vs nice-to-have)
7. **Poste ton message** dans le bus (format fourni)

### Ton d'Évaluation

- ✅ **Constructif** : Propose des solutions, pas juste des critiques
- ✅ **Concret** : Exemples précis, fichiers nommés, code suggéré
- ✅ **Priorisé** : Urgent vs Nice-to-have
- ✅ **Réaliste** : Effort estimé, faisabilité
- ✅ **Respectueux** : Reconnais le travail déjà fait

---

## 🏁 C'EST PARTI !

**Bonne évaluation !** 🚀

Ton travail aidera à améliorer un projet scientifique open-source utilisé par des chercheurs en biologie quantique. Chaque suggestion compte !

---

**Version :** 1.0  
**Date :** 2025-11-15  
**Projet :** Biological Qubits & Quantum Sensors Atlas v2.2.2  
**Créé par :** CLAUDE-BACKEND-ENGINEER

