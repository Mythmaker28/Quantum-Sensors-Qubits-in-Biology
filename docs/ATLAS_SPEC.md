# 📐 Atlas Specification v2.2.2

## Overview

Le **Biological Qubits & Quantum Sensors Atlas** est une base de données curée de systèmes quantiques et bio-capteurs utilisés en contexte biologique. Cette spécification décrit le schéma de données, les critères d'inclusion, et comment les incertitudes sont représentées.

**Version actuelle:** v2.2.2 (296 systèmes validés, enrichis via APIs multiples, aucune fabrication)

---

## Schéma du Dataset

### Fichier Principal

**`data/processed/atlas_fp_optical_v2_2.csv`** — 296 systèmes (v2.2.2, validated)

**Fichier Staging (Curation Manuelle Requise):**

**`data/staging/candidates_needing_curation.csv`** — 844 candidats nécessitant vérification manuelle (DOI manquant ou données spectrales incomplètes)

### Colonnes

| Colonne | Type | Description | Unité | Statut |
|---------|------|-------------|-------|--------|
| `SystemID` | string | Identifiant unique (e.g., FP_0001) | - | **Obligatoire** |
| `protein_name` | string | Nom du système/protéine | - | **Obligatoire** |
| `family` | string | Famille fonctionnelle | - | **Obligatoire** |
| `is_biosensor` | float | 1.0 = biosenseur, 0.0 = fluorophore | - | **Obligatoire** |
| `contrast_normalized` | float | Contraste normalisé (fold-change) | fold | **Obligatoire** |
| `doi` | string | DOI de la source primaire | - | **Obligatoire** |
| `curator` | string | Version de curation | - | **Obligatoire** |
| `quality_tier` | string | Niveau qualité (A, B, C) | - | Recommandé* |
| `temperature_K` | float | Température de mesure | Kelvin | Recommandé* |
| `license` | string | Licence des données | - | Recommandé* |
| `method` | string | Méthode de mesure (fluorescence, FRET, ODMR) | - | Recommandé* |
| `contrast_value` | float | Valeur brute du contraste | variable | Optionnel |
| `contrast_unit` | string | Unité originale (fold, deltaF/F0, %) | - | Optionnel |
| `context` | string | Contexte expérimental | - | Optionnel |
| `pH` | float | pH de l'environnement | - | Optionnel |
| `pmcid` | string | PubMed Central ID | - | Optionnel |
| `assay` | string | Type d'essai | - | Optionnel |
| `excitation_nm` | float | Longueur d'onde excitation | nm | Optionnel |
| `emission_nm` | float | Longueur d'onde émission | nm | Optionnel |
| `stokes_shift_nm` | float | Décalage de Stokes | nm | Optionnel |
| `spread_type` | string | Type d'incertitude (sd, sem, ci, none) | - | Optionnel |
| `spread_value` | float | Valeur de l'incertitude | variable | Optionnel |

**\*Recommandé :** Ces champs sont fortement encouragés mais peuvent être vides si les données ne sont pas disponibles dans les sources originales. Le validateur les traite comme avertissements, pas comme erreurs critiques. Cela évite la fabrication de données.

**Note:** Colonnes supplémentaires présentes dans le fichier (e.g., `source_note`, `canonical_name`, `tier`) sont utilisées pour la traçabilité interne.

---

## Politique de Qualité des Données

### Règle d'Or: AUCUNE Fabrication

L'atlas suit une politique stricte de **non-fabrication de données** :

✅ **Accepté :**
- Laisser des champs vides si données indisponibles
- Marquer explicitement les valeurs "unknown"
- Utiliser des métadonnées techniques (curator, SystemID)

❌ **Interdit :**
- Inventer des DOI ou références
- Utiliser des valeurs "par défaut" scientifiques (ex: 298K si température non rapportée)
- Deviner family, license, ou quality_tier

### Validation

Utiliser `scripts/validate_atlas.py` pour vérifier :
- Colonnes obligatoires présentes
- Pas de valeurs manquantes dans champs critiques
- DOI valides
- Températures plausibles (270-320K)

---

## Familles de Systèmes

| Famille | Description | Exemple |
|---------|-------------|---------|
| **Calcium** | Capteurs calciques (GECIs) | GCaMP8, jRGECO1a, XCaMP |
| **Voltage** | Capteurs voltage | ASAP3, ASAP4e, ArcLight |
| **Dopamine** | Capteurs dopamine | dLight1.x, GRAB-DA |
| **Glutamate** | Capteurs glutamate | iGluSnFR, SF-iGluSnFR |
| **GABA** | Capteurs GABA | iGABASnFR |
| **Acetylcholine** | Capteurs acétylcholine | GRAB-ACh |
| **pH** | Capteurs pH | pHluorin, pHuji |
| **H2O2** | Capteurs peroxyde | HyPer3, HyPer-7 |
| **ATP** | Capteurs ATP | MaLionR |
| **ATP/ADP** | Ratio ATP/ADP | Perceval, PercevalHR |
| **cAMP** | Capteurs AMPc | Epac-SH187, PinkFlamindo, cAMPr |
| **Redox** | Capteurs redox | roGFP2, roGFP2-Orp1 |
| **GFP-like** | Fluorophores verts | EGFP, mNeonGreen, mEmerald |
| **RFP** | Fluorophores rouges | mCherry, tdTomato, DsRed2 |
| **CFP-like** | Fluorophores cyan | ECFP, mCerulean3, mTurquoise2 |
| **YFP** | Fluorophores jaunes | - |
| **BFP-like** | Fluorophores bleus | TagBFP2 |
| **Far-red** | Fluorophores lointain rouge | Katushka, mKate2 |
| **NIR** | Fluorophores proche-infrarouge | iRFP670, miRFP670, miRFP720 |
| **Orange** | Fluorophores orange | - |
| **Teal** | Fluorophores turquoise | mTFP1 |

---

## Critères d'Inclusion

### 1. Systèmes Acceptés

✅ **Inclus dans l'atlas:**
- Protéines fluorescentes génétiquement encodées (FPs)
- Bio-capteurs fluorescents (GECIs, GEVIs, neuromodulateurs, métabolites)
- Systèmes avec **au moins une publication peer-reviewed avec DOI**
- Données mesurées en contexte biologique (in cellulo, in vivo)
- Toutes les colonnes **obligatoires** remplies

❌ **Exclus de l'atlas:**
- Petites molécules non-protéiques
- Colorants synthétiques
- Systèmes sans DOI traçable
- Systèmes avec family ou is_biosensor indéterminables

### 2. Qualité des Données (Tiers)

| Tier | Description | Critères |
|------|-------------|----------|
| **A** | Gold standard | Peer-reviewed, données brutes accessibles, réplicable |
| **B** | Standard | Peer-reviewed, données rapportées dans article |
| **C** | Préliminaire | Préprint, poster, ou méthode à valider |

---

## Représentation des Incertitudes

### Types d'Incertitudes (`spread_type`)

| Type | Description | Colonne associée |
|------|-------------|------------------|
| `sd` | Écart-type (Standard Deviation) | `spread_value` |
| `sem` | Erreur standard de la moyenne | `spread_value` |
| `ci` | Intervalle de confiance | `ci_low`, `ci_high` |
| `none` | Pas d'incertitude rapportée | - |

### Normalisation du Contraste

**Formule de conversion:**

```
contrast_normalized = 
  - Si contrast_unit = "fold": contrast_value (inchangé)
  - Si contrast_unit = "deltaF/F0": contrast_value + 1.0
  - Si contrast_unit = "percent": (contrast_value / 100) + 1.0
```

**Exemple:**
- Contraste brut: `deltaF/F0 = 0.32` → normalisé: `1.32 fold`
- Contraste brut: `30%` → normalisé: `1.30 fold`

---

## Métadonnées FAIR

### Identifiants Persistents

- **DOI:** Chaque entrée a un DOI de source primaire
- **PMCID:** Pour les sources PubMed Central (optionnel)
- **SystemID:** Identifiant unique interne (format: `FP_####`)

### Provenance

Chaque entrée inclut:
- `doi`: DOI de la publication source (obligatoire)
- `source_note`: Référence humainement lisible
- `curator`: Version de l'outil de curation ou "v2.2.2_cleanup"
- `license`: Licence de la donnée source (si déterminable)

### Licences

- **Données (CSV):** CC BY 4.0
- **Code (scripts, dashboard):** MIT
- **Sources externes:** Variées (voir colonne `license`)

---

## Validation du Dataset

### Script de Validation

```bash
python scripts/validate_atlas.py
```

**Vérifications effectuées:**
1. Colonnes obligatoires présentes (7 colonnes critiques)
2. Valeurs manquantes dans colonnes critiques → **ERREUR**
3. Valeurs manquantes dans colonnes recommandées → **AVERTISSEMENT**
4. Cohérence des unités
5. Plausibilité des valeurs (temp 270-320K, contraste > 0)
6. DOI valides (format)

### Rapport de Validation

Sortie:
```
[OK] 193 systemes charges
[OK] Toutes les colonnes obligatoires presentes
[OK] Aucune erreur critique
[INFO] Colonne recommandee 'license': 113 manquantes (acceptable si donnees indisponibles)
[OK] Dataset valide (avec avertissements mineurs)
```

---

## Problèmes Connus & Limitations

Voir [docs/KNOWN_ISSUES.md](KNOWN_ISSUES.md) pour :
- API externes indisponibles (ex: FPbase)
- Champs recommandés manquants avec justification
- Systèmes supprimés et raisons

---

## Comment Utiliser l'Atlas

### 1. Charger en Python

```python
import pandas as pd

# Charger le dataset
df = pd.read_csv('data/processed/atlas_fp_optical_v2_2.csv')

# Filtrer les capteurs calciques
ca_sensors = df[df['family'] == 'Calcium']

# Filtrer par contexte in vivo
in_vivo = df[df['context'].str.contains('vivo', na=False)]

# Obtenir les systèmes haute performance (contraste > 10)
high_contrast = df[df['contrast_normalized'] > 10]
```

### 2. Dashboard Interactif

Ouvrir **`docs/index.html`** dans un navigateur pour:
- Visualiser les distributions par famille
- Explorer les relations température-contraste
- Filtrer par famille, contexte, qualité

### 3. Accès Programmatique

```bash
# Télécharger directement
wget https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/raw/main/data/processed/atlas_fp_optical_v2_2.csv

# Ou via curl
curl -O https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/raw/main/data/processed/atlas_fp_optical_v2_2.csv
```

---

## Contribuer

Voir [CONTRIBUTING.md](../CONTRIBUTING.md) pour:
- Ajouter de nouveaux systèmes
- Corriger des données existantes
- Proposer de nouvelles familles

---

## Versionning

- **v1.2.1** (66 systèmes) — Version Frontiers manuscrit
- **v2.0** (139 systèmes) — Extension FPbase
- **v2.1** (162 systèmes) — Littérature mining
- **v2.2.2** (193 systèmes) — **Nettoyage validé, aucune fabrication**

---

**Contact:** [GitHub Issues](https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/issues)

**DOI Zenodo v1.2.1:** 10.5281/zenodo.17420604  
**DOI Zenodo v2.2.2:** TBD (en cours de dépôt)
