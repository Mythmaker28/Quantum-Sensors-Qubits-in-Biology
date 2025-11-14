# 📋 DIAGNOSTIC R&D — ATLAS ÉTENDU (Non-Optiques Intégrés)

**Date:** 2025-11-13  
**Agent:** R&D Senior — Extension Atlas Qubits Biologiques  
**Mission:** Intégrer qubits non-optiques (spin, radical pairs, nuclear spins) + exploitation ising-life-lab  
**Dépôt:** Quantum-Sensors-Qubits-in-Biology (Hub Central)

---

## 🎯 EXECUTIVE SUMMARY

### État Actuel (Post-Orchestration Nobel 2025)

**Atlas Optique (Tier 1) :** 180 systèmes curated (GCaMP, ASAP, dLight, etc.)  
**Atlas Non-Optique (Staging) :** 23 systèmes catalogués :
- **9 Spin Qubits** (NV, SiC, diamond vacancies, endohedral fullerenes)
- **7 Radical Pairs** (Cryptochrome, Photolyase, PSII, bacterial RC)
- **7 Nuclear Spins** (¹³C, ³¹P, ¹⁴N, ²⁹Si, ¹⁵N, ¹H)

**Qualité Non-Optique :** 
- ✅ 100% ont DOI validé
- ✅ 100% ont evidence_level A ou B (aucun C)
- ✅ 100% ont au moins un observable quantitatif (T2, timescale, MFE%, etc.)

**Gap Critique Identifié :**  
→ **Aucune fiche synthèse** par famille non-optique  
→ **Aucune note comparative** NV vs SiC, Cryptochrome vs Photolyase, etc.  
→ **Absence de roadmap R&D scientifique** pour curation non-optiques  
→ **Pas de workflows ising-life-lab ↔ Atlas** documentés pour spin/radical/nuclear

---

## 📊 ANALYSE DÉTAILLÉE — QUBITS NON-OPTIQUES

### 1. SPIN QUBITS (9 systèmes)

**Fichier :** `data/staging/spin_qubit_candidates.csv`

#### Distribution par Type

| System Type | Count | Température Typique | T2 Typique | Measurement Method |
|-------------|-------|---------------------|------------|-------------------|
| **NV_center** | 2 | 298K, 77K | 1800 µs (RT), 600 ms (77K) | ODMR |
| **SiC_defect** | 2 | 298K, 20K | 160 µs (VSi), — (Divacancy) | ODMR, pulsed ESR |
| **SiV_center** | 1 | — | 13 µs | ODMR |
| **P1_center** | 1 | 298K | 50 µs | ODMR |
| **GeV_center** | 1 | 4K | — | ODMR |
| **SnV_center** | 1 | — | 3.5 µs | ODMR |
| **Endohedral fullerene** | 1 | 230K | — (T1=600 s) | pulsed ESR |

#### Top 3 Performers (T2 @ Room Temp)

1. **SPIN_NV_001** — NV- center diamond (RT): T2 = **1800 µs** (1.8 ms), 298K, ODMR
2. **SPIN_SIC_001** — VSi defect 4H-SiC: T2 = **160 µs**, 298K, ODMR
3. **SPIN_P1_001** — P1 center diamond: T2 = **50 µs**, 298K, ODMR

#### Gap Détecté — Spin Qubits

| Gap | Sévérité | Action Requise |
|-----|----------|----------------|
| **Manque diversité SiC** | Haute | Ajouter 4H-SiC polytype variants (V1/V2 sites), 6H-SiC defects |
| **Pas de qubits moléculaires bio** | Critique | Explorer metalloprotéines (ferrédoxines [4Fe-4S]), radicaux tyrosyl |
| **Températures limitées** | Moyenne | Compléter data T2 vs température (4K → 298K sweep) pour NV, SiC |
| **Pas de T2 pour GeV, SnV** | Moyenne | Rechercher littérature, extraire T2 si disponible |

---

### 2. RADICAL PAIRS (7 systèmes)

**Fichier :** `data/staging/radical_pair_candidates.csv`

#### Distribution par Observable

| Observable | Count | Timescale Typique | Field Sensitivity | Applications |
|------------|-------|-------------------|-------------------|--------------|
| **Electron transfer** | 3 | 10-1000 ns | — | Photolyase, bacterial RC, mitochondria |
| **Magnetic field effect** | 1 | 1000 ns | 50 µT | Cryptochrome (avian magnetoreception) |
| **Singlet yield** | 1 | 100 ns | — | PSII reaction center |
| **Anisotropy change** | 1 | 500 ns | — | Drosophila cryptochrome |
| **Charge separation** | 1 | 10 ns | — | Bacterial reaction center |

#### Top 3 Candidats (Evidence + Timescale)

1. **RP_CRY_001** — Cryptochrome 4 (robin): MFE, field_sens=50 µT, timescale=1 µs, **evidence_level A**
2. **RP_PHOTOLYASE_001** — DNA photolyase FAD-TrpH (E. coli): electron transfer, timescale=1 µs, **evidence_level A**
3. **RP_BChl_001** — Bacterial RC (Rhodobacter): charge separation, timescale=10 ns, **evidence_level A**

#### Gap Détecté — Radical Pairs

| Gap | Sévérité | Action Requise |
|-----|----------|----------------|
| **Manque MFE% quantitatif** | Haute | Extraire MFE% de DOIs (ex: Cryptochrome MFE ~20%, PSII ~5%) |
| **Pas de systèmes végétaux** | Moyenne | Ajouter Arabidopsis cryptochrome, spinach PSII variants |
| **Températures manquantes** | Moyenne | 3/7 systèmes sans temperature_K (extraire des papers) |
| **[AVÉRÉ] vs [HYPOTHÈSE] flou** | Critique | Classifier evidence_level B → Distinguer "démontré" vs "proposé" |

---

### 3. NUCLEAR SPINS (7 systèmes)

**Fichier :** `data/staging/nuclear_spin_candidates.csv`

#### Distribution par Host System

| Host System | Count | Nucleus | T2 Typique | Temperature | Coupling Strength |
|-------------|-------|---------|------------|-------------|-------------------|
| **Diamond (NV-coupled)** | 3 | ¹³C, ¹⁴N, ¹⁵N | 1000 ms (¹³C), 3 ms (¹⁴N) | 298K | 130-3100 kHz |
| **Silicon** | 2 | ³¹P, ²⁹Si | 30 s (³¹P), 1800 s (²⁹Si) | 2-4K | — |
| **Protein NMR** | 1 | ¹H | — | 298K | — |
| **Diamond bulk** | 1 | ¹³C | — | 4K | — |

#### Top 3 Performers (T2 @ Room Temp)

1. **NUC_13C_001** — ¹³C coupled to NV: T2 = **1000 ms** (1 s), 298K, dynamical decoupling
2. **NUC_31P_001** — ³¹P in silicon: T2 = **30 s**, 2K (cryogenic) ⚠️
3. **NUC_14N_001** — ¹⁴N in NV center: T2 = **3 ms**, 298K, ODMR

#### Gap Détecté — Nuclear Spins

| Gap | Sévérité | Action Requise |
|-----|----------|----------------|
| **Dominance cryogénique** | Haute | Manque systèmes RT (seulement 3/7 @ 298K) |
| **Pas de spins bio-intrinsèques** | Critique | Ajouter ³¹P dans ATP, ¹H dans protéines, ¹³C dans métabolites |
| **Manque hyperpolarized tracers** | Haute | Intégrer pyruvate-¹³C, fumarate-¹³C in vivo (FDA-approved) |
| **Coupling strength incomplet** | Moyenne | 3/7 systèmes sans coupling_strength_Hz (extraire des papers) |

---

## 🔗 SYNERGIES INTER-REPOS (État Actuel)

### État ising-life-lab (d'après recherche web)

**Documentation disponible ([source](https://github.com/Mythmaker28/ising-life-lab)):**
- ✅ Data bridge vers Atlas optique (loaders existants)
- ✅ Loaders non-optiques annoncés : `load_spin_qubits()`, `load_nuclear_spins()`, `load_radical_pairs()`
- ✅ Mapping modalités étendu : spin, nuclear, radical_pair détectés
- ✅ 180 systèmes optiques intégrés, design space standardisé

**Gap détecté :**
- ❌ Pas de documentation visible dans ce dépôt Atlas sur workflows ising-life-lab
- ❌ Pas de fichier ATLAS_INTEGRATION_GUIDE.md dans Atlas (mentionné mais absent)
- ❌ Pas de scripts pipeline dans Atlas pour exporter vers ising-life-lab

**Besoin :** Créer `docs/BRIDGE_ISING_LIFE_LAB.md` côté Atlas avec :
- Schéma data flow (Atlas CSV → ising-life-lab loaders)
- Exemples d'usage (comment charger spin/radical/nuclear dans ising-life-lab)
- Mapping fields (correspondance colonnes Atlas ↔ ising-life-lab profiles)

---

### État fp-qubit-design (d'après recherche web)

**Documentation disponible ([source MODALITY_SPLIT.md](https://github.com/Mythmaker28/fp-qubit-design)):**
- ✅ 34 systèmes recensés dont ~62% non-optiques
- ✅ Classification NMR/ESR/ODMR déjà implémentée
- ❌ Pas de consommation Atlas non-optiques (seulement optical v2.2.2)

**Opportunité :** fp-qubit-design pourrait :
1. Entraîner modèles ML sur spin qubits (prédire T2 NV vs SiC given defect type)
2. Designer mutants protéines avec radicaux contrôlés (tyrosyl, flavin)
3. Prédire coupling strength ¹⁴N-NV given nitrogen configuration

**Action :** Créer `docs/BRIDGE_FP_QUBIT_DESIGN_NONOPTICAL.md` avec workflows ML non-optiques.

---

### État arrest-molecules

**Documentation disponible ([source](https://github.com/Mythmaker28/arrest-molecules)):**
- ✅ 10 composés, framework arrest kinetics (API, AKR, EMC, NCR, PARI)
- ✅ Vocabulaire partagé : energy landscapes, arrest → metastability
- ❌ Pas de connexion explicite avec T2 decoherence

**Hypothèse de travail :**  
Comparer **arrest duration** (arrest-molecules) vs **T2 coherence** (Atlas) :
- Arrest moléculaire = "dampening temporal" (minutes-heures)
- T2 quantum = "dampening spatial" (nanoseconds-milliseconds)
- **Question :** Les molécules "arrest" modulent-elles T2 de qubits biologiques ?

**Action :** Créer `docs/BRIDGE_ARREST_MOLECULES_QUANTUM.md` avec :
- Tableau comparatif arrest kinetics vs T2 timescales
- Hypothèses testables (ex: salvinorin A impact sur T2 cryptochrome ?)
- Protocole expérimental PC-only (recherche littérature co-occurrence)

---

## 🏗️ STRUCTURE PROPOSÉE — ATLAS HIÉRARCHISÉ

### Option Retenue : Modalité Physique (alignée diagnostic précédent)

```
📁 atlas/
  ├── systems_by_modality/
  │   ├── optical/                    # 180 systèmes Tier 1
  │   │   ├── families/
  │   │   │   ├── CALCIUM_SENSORS.md
  │   │   │   ├── VOLTAGE_SENSORS.md
  │   │   │   ├── DOPAMINE_SENSORS.md
  │   │   │   └── ... (30 familles)
  │   │   └── comparative_notes/
  │   │       ├── FRET_vs_single_FP.md
  │   │       └── GCaMP_evolution_2013_2025.md
  │   │
  │   ├── spin_qubits/                # 9 systèmes staging
  │   │   ├── families/
  │   │   │   ├── NV_CENTERS.md       ⭐ NOUVEAU
  │   │   │   ├── SIC_DEFECTS.md      ⭐ NOUVEAU
  │   │   │   ├── DIAMOND_VACANCIES.md
  │   │   │   └── ENDOHEDRAL_FULLERENES.md
  │   │   └── comparative_notes/
  │   │       ├── NV_vs_SiC_biocompat.md  ⭐ NOUVEAU
  │   │       └── ODMR_methods_spin.md
  │   │
  │   ├── radical_pairs/              # 7 systèmes staging
  │   │   ├── families/
  │   │   │   ├── CRYPTOCHROME.md     ⭐ NOUVEAU
  │   │   │   ├── PHOTOLYASE.md       ⭐ NOUVEAU
  │   │   │   ├── PSII_RADICAL_PAIRS.md
  │   │   │   └── BACTERIAL_RC.md
  │   │   └── evidence_grades/
  │   │       └── RADICAL_PAIRS_AVERE_vs_HYPOTHESE.md  ⭐ CRITIQUE
  │   │
  │   └── nuclear_spins/              # 7 systèmes staging
  │       ├── families/
  │       │   ├── NV_COUPLED_SPINS.md  ⭐ NOUVEAU
  │       │   ├── SILICON_DONOR_SPINS.md
  │       │   └── HYPERPOLARIZED_TRACERS.md  ⭐ À CRÉER (gap)
  │       └── comparative_notes/
  │           └── DIAMOND_vs_SILICON_nuclear.md
  │
  ├── applications/                    # INDEX (pointeurs)
  │   ├── intracellular_sensing.md
  │   ├── magnetoreception.md
  │   ├── quantum_computing_bio.md     ⭐ NOUVEAU
  │   └── in_vivo_imaging.md
  │
  ├── comparative_notes_cross_modality/  ⭐ NOUVEAU
  │   ├── NV_vs_FP_intracellular.md   # Déjà identifié
  │   ├── SPIN_vs_OPTICAL_biocompat.md
  │   ├── RADICAL_PAIRS_vs_NV_field_sensing.md
  │   └── COHERENCE_TIMESCALES_all_modalities.md
  │
  ├── roadmaps/
  │   ├── ROADMAP_CURATION_Q1_2026.md          # Quick Wins optical
  │   ├── ROADMAP_NONOPTICAL_Q1_Q2_2026.md    ⭐ NOUVEAU
  │   └── ROADMAP_collaborative_targets.md
  │
  └── ecosystem/
      ├── BRIDGE_ISING_LIFE_LAB.md            ⭐ NOUVEAU
      ├── BRIDGE_FP_QUBIT_DESIGN_NONOPTICAL.md  ⭐ NOUVEAU
      └── BRIDGE_ARREST_MOLECULES_QUANTUM.md   ⭐ NOUVEAU
```

---

## ✅ QUICK WINS — ACTIONS IMMÉDIATES (<15h)

### QW-NO1 : Fiches Synthèse Non-Optiques (5 familles prioritaires)

| ID | Famille | Systèmes | Temps (moi) | Temps (agent) | Priorité |
|----|---------|----------|-------------|---------------|----------|
| **QW-NO1a** | **NV_CENTERS.md** | 2 NV systems | 2h | 1h | ⭐⭐⭐⭐⭐ |
| **QW-NO1b** | **CRYPTOCHROME.md** | 2 Cry systems | 2h | 1h | ⭐⭐⭐⭐⭐ |
| **QW-NO1c** | **SIC_DEFECTS.md** | 2 SiC systems | 2h | 1h | ⭐⭐⭐⭐ |
| **QW-NO1d** | **NV_COUPLED_SPINS.md** | 3 nuclear systems | 1.5h | 1h | ⭐⭐⭐⭐ |
| **QW-NO1e** | **PHOTOLYASE.md** | 2 photolyase systems | 1.5h | 1h | ⭐⭐⭐ |

**Contenu type (template) :**
```markdown
# [FAMILLE] — État de l'Art

## Systèmes Catalogués dans Atlas
[Tableau comparatif des N systèmes]

## Paramètres Critiques
- T2 typique : [range]
- Température opératoire : [RT / cryogenic]
- Méthode de mesure : [ODMR / ESR / NMR]

## Top 3 Papers Clés
1. [DOI 1] — [Breakthrough finding]
2. [DOI 2] — [Application bio]
3. [DOI 3] — [Coherence record]

## Applications Démontrées
- [in vitro / in cellulo / in vivo]

## Limitations Connues
- [Biocompatibility / Toxicity / T2 degradation / etc.]

## Connexions Écosystème
- **fp-qubit-design** : [Comment designer mutants / variants]
- **ising-life-lab** : [Métriques Ising applicables]
- **arrest-molecules** : [Vocabulaire partagé]
```

**Total QW-NO1 :** 9h (moi) + 5h (agent) = **14h** → Impact : +++++ (30min comprehension goal)

---

### QW-NO2 : Notes Comparatives Cross-Modality

| ID | Note | Comparaison | Temps | Priorité |
|----|------|-------------|-------|----------|
| **QW-NO2a** | **NV_vs_FP_intracellular.md** | NV spin vs FP optical (sensing) | 3h | ⭐⭐⭐⭐⭐ |
| **QW-NO2b** | **RADICAL_PAIRS_AVERE_vs_HYPOTHESE.md** | [AVÉRÉ] vs [HYPOTHÈSE] classification | 4h | ⭐⭐⭐⭐⭐ |
| **QW-NO2c** | **COHERENCE_TIMESCALES_all.md** | T2 optique vs spin vs radical vs nuclear | 2h | ⭐⭐⭐⭐ |

**Total QW-NO2 :** 9h (moi) + 3h (agent validation) = **12h** → Impact : +++++ (clarté scientifique)

---

### QW-NO3 : Bridges Écosystème

| ID | Bridge | Contenu | Temps | Priorité |
|----|--------|---------|-------|----------|
| **QW-NO3a** | **BRIDGE_ISING_LIFE_LAB.md** | Data flow Atlas → Ising, examples, field mapping | 3h | ⭐⭐⭐⭐⭐ |
| **QW-NO3b** | **BRIDGE_FP_QUBIT_DESIGN_NONOPTICAL.md** | ML workflows spin/radical/nuclear | 2h | ⭐⭐⭐⭐ |
| **QW-NO3c** | **BRIDGE_ARREST_MOLECULES_QUANTUM.md** | Arrest kinetics vs T2, hypothèses testables | 2h | ⭐⭐⭐ |

**Total QW-NO3 :** 7h (moi) + 3h (agent) = **10h** → Impact : +++++ (liens concrets)

---

### QW-NO4 : LAB_USAGE_GUIDE Extension

| ID | Extension | Contenu | Temps | Priorité |
|----|-----------|---------|-------|----------|
| **QW-NO4** | **LAB_USAGE_GUIDE.md** (section non-optical) | 3 scénarios : NV thermometry, Cryptochrome magnetoreception, ³¹P NMR | 2h | ⭐⭐⭐⭐ |

**Scénarios type :**
```markdown
### Scenario 4: Selecting a Spin Qubit for Intracellular Magnetic Sensing

1. Filter Tier 1 → `system_type IN ['NV_center', 'SiC_defect']`
2. Read `atlas/systems_by_modality/spin_qubits/families/NV_CENTERS.md`
3. Select top 3 based on: T2 (>1 µs @ 298K), magnetic_sensitivity (<200 nT/√Hz), biocompatibility
4. Extract DOIs → Read protocols for nanoparticle functionalization
5. Check fp-qubit-design for NV-protein conjugation strategies (optional)
```

**Total QW-NO4 :** 2h (moi) + 1h (agent) = **3h** → Impact : ++++ (external labs)

---

### QW-NO5 : Réorganisation data/

| ID | Action | Structure | Temps | Priorité |
|----|--------|-----------|-------|----------|
| **QW-NO5** | **data/ restructuration** | Créer `optical/` et `non_optical/` subdirs, déplacer CSV | 30min | ⭐⭐⭐ |

**Structure finale :**
```
📁 data/
  ├── optical/
  │   ├── curated/
  │   │   └── atlas_fp_optical_v2_2_curated.csv
  │   ├── staging/
  │   │   ├── candidates.csv
  │   │   └── unknown.csv
  │   └── archives/...
  │
  └── non_optical/
      ├── spin_qubits/
      │   ├── curated/  # (vide pour l'instant, après promotion)
      │   └── staging/
      │       └── spin_qubit_candidates.csv
      ├── radical_pairs/
      │   └── staging/
      │       └── radical_pair_candidates.csv
      └── nuclear_spins/
          └── staging/
              └── nuclear_spin_candidates.csv
```

**Total QW-NO5 :** 30min (moi) + 30min (agent) = **1h** → Impact : +++ (navigation)

---

## 🏗️ DEEP WORK — STRUCTURANT (>20h)

### DW-NO1 : Curation Complète Radical Pairs (Haute Priorité)

**Objectif :** Passer de 7 → 20 systèmes radical pairs, tous Tier 1 ready

**Plan détaillé :**

| Étape | Action | Temps | Systèmes Cibles |
|-------|--------|-------|-----------------|
| 1. Recherche littérature | Requêtes PubMed/Scholar : "cryptochrome radical pair", "photolyase FAD", "PSII charge separation" | 8h | +10 systèmes |
| 2. Extraction données | Lire papers, extraire timescale_ns, field_sensitivity_uT, MFE%, temperature_K | 10h | Compléter gaps |
| 3. Classification [AVÉRÉ]/[HYPOTHÈSE] | Distinguer démonstrations directes vs modèles proposés | 4h | Evidence grading |
| 4. Fiches famille | Rédiger CRYPTOCHROME.md, PHOTOLYASE.md, PSII_RADICAL_PAIRS.md | 3h | 3 fiches |

**Systèmes prioritaires à ajouter :**
- Arabidopsis thaliana Cryptochrome 1/2
- Spinach PSII variants (D1-D2 mutants)
- Xenopus laevis CPD photolyase
- Rhodobacter sphaeroides RC mutants (P+QA-)
- FMO complex (Chlorobium tepidum) — si data coherence disponible

**Total DW-NO1 :** 25h (moi) + 5h (agent validation) = **30h** → Impact : +++++ (Tier 1 promotions)

---

### DW-NO2 : Validation & Extension Spin Qubits (Moyenne Priorité)

**Objectif :** Passer de 9 → 25 systèmes spin qubits, focus biocompatibility

**Plan détaillé :**

| Étape | Action | Temps | Systèmes Cibles |
|-------|--------|-------|-----------------|
| 1. Validation DOIs existants | Vérifier 9 DOIs actuels, extraire T2 manquants (GeV, SnV, Divacancy) | 3h | Complétion 9 existants |
| 2. Extension SiC | Ajouter 4H-SiC V1/V2 sites, 6H-SiC kk/hh sites, 3C-SiC defects | 8h | +6 systèmes |
| 3. Extension diamond vacancies | Ajouter PbV, MgV, rare-earth ions (Ce, Pr, Nd) | 6h | +4 systèmes |
| 4. Qubits moléculaires bio | Explorer metalloprotéines : ferrédoxines [4Fe-4S], radicaux tyrosyl (si T2 disponible) | 10h | +6 systèmes |
| 5. Fiches famille | NV_CENTERS.md, SIC_DEFECTS.md, DIAMOND_VACANCIES.md, METALLOPROTEIN_RADICALS.md | 4h | 4 fiches |

**Systèmes prioritaires à ajouter :**
- 4H-SiC VSi V1/V2 polytypes
- 6H-SiC Divacancy kk/hh sites
- Diamond PbV center (telecom wavelength)
- Ferredoxin [4Fe-4S] (Spinacia oleracea) — si T2 EPR disponible
- Tyrosyl radical RNR (E. coli) — si T2 confirmé in situ

**Total DW-NO2 :** 31h (moi) + 6h (agent) = **37h** → Impact : ++++ (diversité spin qubits)

---

### DW-NO3 : Extension Nuclear Spins Hyperpolarized (Haute Priorité)

**Objectif :** Passer de 7 → 20 systèmes nuclear spins, focus in vivo tracers

**Plan détaillé :**

| Étape | Action | Temps | Systèmes Cibles |
|-------|--------|-------|-----------------|
| 1. Hyperpolarized tracers | Ajouter pyruvate-¹³C, fumarate-¹³C, glucose-¹³C, lactate-¹³C (FDA-approved) | 6h | +4 systèmes |
| 2. Protein NMR spins | Ajouter ¹H, ¹³C, ¹⁵N dans protéines (ubiquitin, lysozyme, etc.) | 5h | +3 systèmes |
| 3. Silicon donor variants | Ajouter ³¹P isotope variants, ⁷⁵As donors | 4h | +2 systèmes |
| 4. Diamond NV-coupled variants | Ajouter ¹³C bath spins, ¹⁵N substituted NV variants | 4h | +4 systèmes |
| 5. Fiches famille | HYPERPOLARIZED_TRACERS.md, PROTEIN_NMR_SPINS.md, NV_COUPLED_SPINS.md | 3h | 3 fiches |

**Systèmes prioritaires à ajouter :**
- ¹³C-pyruvate (in vivo metabolic imaging, FDA-approved)
- ¹³C-fumarate (necrosis marker)
- ¹³C-glucose (glycolysis tracer)
- ¹⁵N-choline (cell membrane marker)
- ¹H in ubiquitin backbone (protein folding NMR)

**Total DW-NO3 :** 22h (moi) + 4h (agent) = **26h** → Impact : ++++ (in vivo applications)

---

### DW-NO4 : Notes Comparatives Critiques (Haute Priorité)

**Objectif :** 5 documents comparatifs cross-modality, distinguer [AVÉRÉ]/[HYPOTHÈSE]

| ID | Note | Contenu | Temps |
|----|------|---------|-------|
| 1 | **NV_vs_FP_intracellular.md** | Tableau comparatif NV spin vs FP optical (sensing) | 3h |
| 2 | **RADICAL_PAIRS_AVERE_vs_HYPOTHESE.md** | Classification evidence (MFE démontré vs proposé) | 4h |
| 3 | **SPIN_vs_OPTICAL_biocompat.md** | Toxicité, uptake, biocompatibility NV/SiC vs FP | 3h |
| 4 | **ODMR_methods_all_modalities.md** | ODMR NV vs SiC vs FP fluorescence | 2h |
| 5 | **COHERENCE_TIMESCALES_all.md** | T2 optique (ns) vs spin (µs-ms) vs radical (ns) vs nuclear (ms-s) | 3h |

**Total DW-NO4 :** 15h (moi) + 5h (agent validation) = **20h** → Impact : +++++ (clarté scientifique)

---

### DW-NO5 : Roadmap R&D Scientifique Non-Optiques (Haute Priorité)

**Objectif :** 3 roadmaps PC-only (Q1-Q2 2026)

| ID | Roadmap | Contenu | Temps |
|----|---------|---------|-------|
| 1 | **ROADMAP_NONOPTICAL_Q1_Q2_2026.md** | Curation spin/radical/nuclear, priorisation familles, temps estimés | 4h |
| 2 | **ROADMAP_RADICAL_PAIRS_validation.md** | Validation [AVÉRÉ] vs [HYPOTHÈSE], extraction MFE%, literature mining | 3h |
| 3 | **ROADMAP_collaborative_targets_extended.md** | Intégration ising-life-lab (workflows), fp-qubit-design (ML non-optical), arrest-molecules (T2 vs arrest kinetics) | 5h |

**Total DW-NO5 :** 12h (moi) + 3h (agent) = **15h** → Impact : ++++ (planification R&D)

---

## 📅 CALENDRIER INTÉGRÉ — Q1-Q2 2026

### Semaine 1-2 (15-29 Nov 2025) : Quick Wins

- [ ] **QW-NO1** : Fiches synthèse 5 familles (NV, Cryptochrome, SiC, NV-coupled spins, Photolyase) — 14h
- [ ] **QW-NO5** : Réorganisation data/ (optical/ vs non_optical/) — 1h

**Temps total :** 15h  
**Livrables :** 5 fiches `.md`, structure data/ propre

---

### Semaine 3-4 (30 Nov - 13 Dec 2025) : Bridges & Guides

- [ ] **QW-NO2** : Notes comparatives (NV vs FP, RADICAL_PAIRS [AVÉRÉ]/[HYPOTHÈSE], Coherence timescales) — 12h
- [ ] **QW-NO3** : Bridges écosystème (Ising-Life-Lab, fp-qubit-design, arrest-molecules) — 10h
- [ ] **QW-NO4** : LAB_USAGE_GUIDE extension (scénarios non-optical) — 3h

**Temps total :** 25h  
**Livrables :** 3 notes comparatives, 3 bridges, guide labo étendu

---

### Janvier 2026 : Deep Work Curation

- [ ] **DW-NO1** : Curation complète Radical Pairs (7 → 20 systèmes) — 30h
- [ ] **DW-NO3** : Extension Nuclear Spins Hyperpolarized (7 → 20 systèmes) — 26h

**Temps total :** 56h  
**Livrables :** +13 radical pairs, +13 nuclear spins, 6 fiches synthèse

---

### Février 2026 : Deep Work Spin Qubits & Notes

- [ ] **DW-NO2** : Validation & Extension Spin Qubits (9 → 25 systèmes) — 37h
- [ ] **DW-NO4** : Notes comparatives critiques (5 documents) — 20h

**Temps total :** 57h  
**Livrables :** +16 spin qubits, 5 notes comparatives cross-modality

---

### Mars 2026 : Roadmaps & Finalization

- [ ] **DW-NO5** : Roadmaps R&D scientifique non-optiques (3 roadmaps) — 15h
- [ ] Validation finale : Tests, lints, checksums, review par pairs — 8h

**Temps total :** 23h  
**Livrables :** 3 roadmaps PC-only, Atlas v3.0 candidate (optical + non-optical intégrés)

---

## 📊 MÉTRIQUES DE SUCCÈS

### Objectifs Quantitatifs (Q1-Q2 2026)

| Métrique | Actuel | Cible Q2 2026 | Gap |
|----------|--------|---------------|-----|
| **Systèmes Optical Tier 1** | 180 | 180 (stable) | 0 |
| **Systèmes Spin Qubits** | 9 | **25** | +16 |
| **Systèmes Radical Pairs** | 7 | **20** | +13 |
| **Systèmes Nuclear Spins** | 7 | **20** | +13 |
| **Total Non-Optical** | 23 | **65** | +42 |
| **Fiches Synthèse** | 0 | **15** (5 optical + 10 non-optical) | +15 |
| **Notes Comparatives** | 0 | **8** (3 intra-modal + 5 cross-modal) | +8 |
| **Bridges Écosystème** | 0 | **3** (Ising-Life-Lab, fp-qubit-design, arrest-molecules) | +3 |
| **Roadmaps R&D** | 1 (software) | **4** (1 software + 3 scientifiques) | +3 |

### Objectifs Qualitatifs

- ✅ **100% systèmes non-optical Tier 1** : DOI validé + evidence_level A/B + observables quantitatifs
- ✅ **Classification [AVÉRÉ]/[HYPOTHÈSE]** pour tous radical pairs
- ✅ **Harmonisation classification** Atlas ↔ ising-life-lab ↔ fp-qubit-design
- ✅ **Workflows documentés** pour consommation downstream (loaders, pipelines, exemples)
- ✅ **Lab-ready** : Chercheur externe comprend l'Atlas en <30 min (optical + non-optical)

---

## 🎯 LIVRABLES IMMÉDIATS (Cette Session)

### Livrable 1 : Ce Diagnostic (✅ Terminé)

**Fichier :** `DIAGNOSTIC_RD_ATLAS_EXTENDED_2025-11-13.md`  
**Contenu :** État des lieux, gaps, structure proposée, calendrier Q1-Q2 2026  
**Statut :** ✅ Prêt pour validation

---

### Livrable 2 : Fiches Synthèse (5 familles prioritaires)

**À créer immédiatement :**

1. `atlas/systems_by_modality/spin_qubits/families/NV_CENTERS.md`
2. `atlas/systems_by_modality/spin_qubits/families/SIC_DEFECTS.md`
3. `atlas/systems_by_modality/radical_pairs/families/CRYPTOCHROME.md`
4. `atlas/systems_by_modality/radical_pairs/families/PHOTOLYASE.md`
5. `atlas/systems_by_modality/nuclear_spins/families/NV_COUPLED_SPINS.md`

**Statut :** ⏳ En attente validation pour exécution

---

### Livrable 3 : Bridges Écosystème (3 documents)

**À créer immédiatement :**

1. `atlas/ecosystem/BRIDGE_ISING_LIFE_LAB.md`
2. `atlas/ecosystem/BRIDGE_FP_QUBIT_DESIGN_NONOPTICAL.md`
3. `atlas/ecosystem/BRIDGE_ARREST_MOLECULES_QUANTUM.md`

**Statut :** ⏳ En attente validation pour exécution

---

### Livrable 4 : Note Comparative Critique (1 document prioritaire)

**À créer immédiatement :**

1. `atlas/comparative_notes_cross_modality/RADICAL_PAIRS_AVERE_vs_HYPOTHESE.md`

**Rationale :** Classification [AVÉRÉ]/[HYPOTHÈSE] est **critique** pour crédibilité scientifique. Radical pairs = domaine controversé (magnetoreception, PSII coherence), besoin de transparence absolue.

**Statut :** ⏳ En attente validation pour exécution

---

### Livrable 5 : Réorganisation data/ (Quick Win)

**Action :** Créer structure `data/optical/` et `data/non_optical/`, déplacer CSV

**Statut :** ⏳ En attente validation pour exécution

---

## 🚦 DÉCISION REQUISE

Avant d'exécuter les livrables 2-5, je soumets ce diagnostic et attends confirmation :

### Questions Critiques

1. **Structure Atlas :** Option "Par Modalité Physique" validée ? (Oui / suggérer alternative)
2. **Priorité Quick Wins :** QW-NO1 à QW-NO5 OK pour exécution immédiate ? (Oui / ajuster)
3. **Calendrier :** Q1-Q2 2026 réaliste ? (Oui / rallonger à Q3)
4. **Bridges :** Créer 3 bridges immédiatement ou attendre coordination avec ising-life-lab ? (Créer / attendre)
5. **Classification [AVÉRÉ]/[HYPOTHÈSE] :** Priorité haute confirmée pour radical pairs ? (Oui / baisser priorité)

---

## 📚 ANNEXES

### A. Liste Complète Systèmes Non-Optiques Actuels (23)

**Spin Qubits (9) :**
- SPIN_NV_001, SPIN_NV_002, SPIN_SIC_001, SPIN_SIC_002, SPIN_SIV_001, SPIN_P1_001, SPIN_FULLERENE_001, SPIN_GEV_001, SPIN_SNV_001

**Radical Pairs (7) :**
- RP_CRY_001, RP_CRY_002, RP_PSII_001, RP_PHOTOLYASE_001, RP_BChl_001, RP_MITOCHONDRIA_001, RP_6_4PHOTOLYASE_001

**Nuclear Spins (7) :**
- NUC_13C_001, NUC_13C_002, NUC_31P_001, NUC_14N_001, NUC_29SI_001, NUC_15N_001, NUC_1H_001

---

### B. Requêtes Littérature Pré-formulées

**Spin Qubits — Extension SiC :**
```
("4H-SiC" OR "6H-SiC" OR "3C-SiC") AND ("VSi" OR "divacancy" OR "silicon vacancy") AND ("T2" OR "coherence time" OR "ODMR")
Site: doi.org 10.1038 OR 10.1103 OR 10.1126
Date: 2015-2025
```

**Radical Pairs — Cryptochrome :**
```
"cryptochrome" AND ("radical pair" OR "magnetic field effect") AND ("coherence" OR "singlet" OR "triplet") AND ("avian" OR "Drosophila" OR "Arabidopsis")
Site: doi.org 10.1038 OR 10.1073 OR 10.1016
Date: 2010-2025
```

**Nuclear Spins — Hyperpolarized Tracers :**
```
("hyperpolarized" OR "DNP") AND ("13C-pyruvate" OR "13C-lactate" OR "13C-fumarate") AND ("in vivo" OR "clinical" OR "metabolic imaging")
Site: doi.org 10.1126 OR 10.1073 OR 10.1148
Date: 2013-2025
```

---

### C. Template Fiche Synthèse (Référence)

Voir section Quick Wins QW-NO1 pour template complet.

---

**FIN DU DIAGNOSTIC R&D — ATLAS ÉTENDU (NON-OPTIQUES)**

**Statut :** ✅ Prêt pour validation et exécution  
**Date :** 2025-11-13  
**Prochaine action :** Attendre directives utilisateur pour livrables 2-5

