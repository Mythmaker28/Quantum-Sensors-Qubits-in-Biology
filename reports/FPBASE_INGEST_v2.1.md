# FPbase Ingestion Report — v2.1

**Date**: 2025-10-24  
**Status**: ⚠️ **PARTIEL — FPbase API indisponible**  
**Phase**: A1 — Intégration FPbase

---

## ⚠️ STATUT DE L'INGESTION

### Problème Rencontré

**FPbase GraphQL API** : **INDISPONIBLE**

**Erreur** :
```
Connection aborted: ConnectionResetError(10054) 
'Une connexion existante a dû être fermée par l'hôte distant'
```

**Tentatives effectuées** :
1. ✗ GraphQL API (https://fpbase.org/api/graphql/) — 3 tentatives
2. ✗ CSV Fallback (https://fpbase.org/api/proteins/?format=csv) — Échec
3. ✓ Outage loggé dans `reports/OUTAGE_LOG_v1.3.md`

### Historique des Pannes

**Outages récents** (depuis `OUTAGE_LOG_v1.3.md`) :
- **2025-10-24 02:16:19** : Connexion refusée
- **2025-10-24 03:43:26** : Connexion refusée
- **2025-10-24 21:42:52** : Connexion refusée
- **2025-10-25 00:56:05** : Connexion refusée ← **Dernière tentative**

**Durée de l'outage** : >22 heures (probablement problème réseau local ou pare-feu)

---

## 🔄 STRATÉGIE ALTERNATIVE

### Sources Utilisées (Fallback)

Vu l'indisponibilité de FPbase, nous utilisons :

1. **Specialist Databases** (PRIORITÉ 1)
   - ✅ `data/raw/specialist/specialist_all.json`
   - Contient : GCaMP, GRAB, dLight, iGluSnFR, etc.
   - **Systèmes disponibles** : ~60+ biosensors

2. **Europe PMC Fulltext** (PRIORITÉ 2)
   - ✅ `data/raw/oa/PMC11613326/fulltext.xml`
   - ✅ `data/raw/oa/PMC5771076/fulltext.xml`
   - Extraction de tableaux et mesures de contraste

3. **Literature Manual Mining** (PRIORITÉ 3)
   - Liste prioritaire de protéines à rechercher manuellement
   - Focus : Calcium, Voltage, pH, Neurotransmitters

4. **UniProt & PDB** (MÉTADONNÉES)
   - ✅ `data/raw/external/uniprot/uniprot_from_seed.json`
   - ✅ `data/raw/external/pdb/pdb_from_seed.json`
   - Pour enrichir les métadonnées structurales

---

## 📊 DONNÉES DISPONIBLES

### Specialist DB (Analyse Rapide)

**Source** : `specialist_all.json`

**Biosensors identifiés** (extrait) :
- **Calcium** : GCaMP6s/f/m, jGCaMP7s/f, jGCaMP8s/f/m, XCaMP, etc.
- **Voltage** : ASAP, Archon, QuasAr, etc.
- **Neurotransmitters** : GRAB-DA, GRAB-ACh, dLight, etc.
- **Glutamate** : iGluSnFR, SF-iGluSnFR, etc.
- **pH, ATP, cAMP, H2O2** : Divers senseurs

**Format** :
```json
{
  "name": "GCaMP6s",
  "doi": "10.1038/nature12354",
  "family": "Calcium",
  "type": "GCaMP",
  "year": 2013
}
```

**Nombre estimé** : 60-80 systèmes potentiels

---

## 🎯 OBJECTIF v2.1 ADAPTÉ

### Cible Initiale (avec FPbase)

| Source | Systèmes Attendus |
|--------|-------------------|
| FPbase GraphQL | +20-30 |
| Specialist DB | +10-15 |
| Littérature | +5-10 |
| **Total gain attendu** | **+35-55** |

### Cible Révisée (sans FPbase)

| Source | Systèmes Attendus |
|--------|-------------------|
| ~~FPbase GraphQL~~ | ~~+20-30~~ ❌ |
| Specialist DB | +15-25 ✅ (augmenté) |
| PMC Fulltext | +5-10 ✅ |
| Littérature prioritaire | +10-15 ✅ (augmenté) |
| **Total gain attendu** | **+30-50** |

**Gap à combler** : +26 systèmes (baseline 94 → objectif 120)

**Faisabilité** : ✅ **POSSIBLE** avec sources alternatives

---

## 📝 PLAN D'ACTION RÉVISÉ

### Étape A1bis : Exploitation Specialist DB

1. ✅ Vérifier `specialist_all.json` (fait)
2. ⏳ Parser et mapper vers schéma Atlas
3. ⏳ Enrichir avec DOI, excitation_nm, emission_nm
4. ⏳ Créer `data/processed/specialist_mapped.csv`

**Script à utiliser** : `scripts/etl/integrate_specialist_v2.py` (existe)

### Étape A2 : PMC Fulltext Mining

1. ⏳ Parser PMC XML (2 fichiers disponibles)
2. ⏳ Extraire tableaux et mesures
3. ⏳ Créer `data/processed/pmc_extracted.csv`

**Script à créer/adapter** : `scripts/etl/mine_fulltext_contrasts.py`

### Étape A3 : Littérature Prioritaire

**Requêtes ciblées** (PubMed, Google Scholar) :
```
1. "calcium indicator" AND "deltaF/F0" AND ("GCaMP" OR "XCaMP" OR "R-GECO")
2. "voltage sensor" AND "deltaF/F0" AND ("ASAP" OR "Archon" OR "QuasAr")
3. "pH sensor" AND "dynamic range" AND ("pHluorin" OR "SypHer")
4. "neurotransmitter sensor" AND "contrast" AND ("GRAB" OR "dLight" OR "iGluSnFR")
```

**Extraction manuelle** :
- Nom protéine
- Famille
- DOI
- Contrast (deltaF/F0 ou fold)
- Excitation / Emission (si disponible)
- Contexte (in vitro / cellulo / vivo)

**Output** : `data/processed/lit_extracted_v2_1.csv`

---

## 🔍 CHAMPS À EXTRAIRE (Schema Mapping)

### Champs Prioritaires (SCHÉMA v2.1)

| Champ Atlas | Source Specialist | Notes |
|-------------|-------------------|-------|
| `canonical_name` | `name` | Nom principal |
| `family` | `family` | Calcium, Voltage, etc. |
| `doi` | `doi` | Provenance |
| `year` | `year` | Année publication |
| `method` | `type` | GECI, GEVI, ratiometric, etc. |
| `excitation_nm` | ❌ Manquant | **À enrichir depuis littérature** |
| `emission_nm` | ❌ Manquant | **À enrichir depuis littérature** |
| `contrast_normalized` | ❌ Manquant | **À enrichir depuis littérature** |
| `source` | Constant: "specialist_db" | - |
| `license` | "varies (see DOI)" | **À vérifier DOI par DOI** |

### Champs Optionnels (enrichissement secondaire)

- `quantum_yield` : Depuis littérature (FPbase unavailable)
- `extinction_coeff` : Depuis littérature
- `brightness` : Calculé = `QY × EC`
- `stokes_shift_nm` : Calculé = `emission_nm - excitation_nm`
- `uniprot_id` : Depuis `uniprot_from_seed.json`
- `pdb_id` : Depuis `pdb_from_seed.json`

---

## ⚙️ SCRIPTS DISPONIBLES

### Scripts Existants (à réutiliser)

1. **`scripts/etl/integrate_specialist_v2.py`**
   - Parse `specialist_all.json`
   - Mappe vers schéma Atlas
   - Output : `data/interim/specialist_mapped.csv`

2. **`scripts/etl/mine_fulltext_contrasts.py`**
   - Parse PMC XML
   - Extrait tableaux + mesures
   - Output : `data/interim/pmc_contrasts.csv`

3. **`scripts/etl/fetch_uniprot_bulk.py`**
   - Enrichit avec UniProt IDs
   - Utilise `uniprot_from_seed.json`

### Scripts à Créer

1. **`scripts/etl/enrich_optical_from_literature_v2_1.py`**
   - Entrée manuelle (CSV template)
   - Champs : name, family, doi, excitation_nm, emission_nm, contrast, context
   - Output : `data/processed/lit_extracted_v2_1.csv`

---

## 📄 OUTPUTS ATTENDUS

### Fichiers Générés (Phase A1 révisée)

- ✅ `reports/FPBASE_INGEST_v2.1.md` : Ce rapport
- ⏳ `data/raw/fpbase/` : **VIDE** (API unavailable)
- ⏳ `data/processed/specialist_mapped.csv` : Specialist DB mappé
- ⏳ `data/processed/pmc_extracted.csv` : PMC extractions
- ⏳ `data/processed/lit_extracted_v2_1.csv` : Littérature manuelle
- ⏳ `reports/SOURCES_v2_1.md` : Liste des DOIs utilisés

---

## 🚧 LIMITATIONS

### Impacts de l'Absence de FPbase

**Champs manquants** (non disponibles dans Specialist DB) :
- ✗ `quantum_yield` (QY)
- ✗ `extinction_coefficient` (EC)
- ✗ `brightness` (calculé depuis QY × EC)
- ✗ `excitation_nm` / `emission_nm` (partiellement)
- ✗ `photostability`
- ✗ `maturation_time`

**Mitigation** :
1. Extraction manuelle depuis publications originales (DOI → PDF → Table)
2. Prioriser les champs **minimaux requis** :
   - `canonical_name`, `family`, `doi`
   - `excitation_nm`, `emission_nm` (pour ML)
   - `contrast_normalized` (cible principale)
3. Marquer champs optionnels comme `NULL` si indisponibles

**Qualité** :
- Systèmes issus de Specialist DB : **Tier B** (mesurés, sans CI)
- Systèmes enrichis manuellement : **Tier A** (si CI extraits) ou **Tier B**

---

## ✅ PROCHAINES ÉTAPES

### Actions Immédiates

1. ⏳ Exécuter `scripts/etl/integrate_specialist_v2.py`
2. ⏳ Parser PMC XML avec `mine_fulltext_contrasts.py`
3. ⏳ Créer template CSV pour extraction littérature
4. ⏳ Rechercher publications prioritaires (PubMed/Scholar)
5. ⏳ Merger sources → `atlas_fp_optical_v2_1_interim.csv`

### Validation

- Vérifier schéma conforme
- Déduplication canonique (name + doi)
- Outliers (z-score > 5)
- Licences (au moins 90% CC BY ou vérifiées)

---

## 🔒 CONCLUSION

### Statut Phase A1

⚠️ **PARTIEL — FPbase indisponible, stratégie alternative déployée**

**Réalisé** :
- ✅ Tentative FPbase GraphQL (3× échecs loggés)
- ✅ Identification sources alternatives (Specialist DB + PMC + Littérature)
- ✅ Rapport d'ingestion rédigé

**Prochaines phases** :
- ⏳ **A1bis** : Exploitation Specialist DB
- ⏳ **A2** : PMC Fulltext Mining
- ⏳ **A2bis** : Littérature manuelle prioritaire
- ⏳ **A3** : Fusion & QA

**Impact sur objectif v2.1** :
- Gap : +26 systèmes requis
- Sources alternatives : +30-50 systèmes estimés
- **Faisabilité** : ✅ **MAINTENUE** (avec plus d'effort manuel)

---

**Fin du Rapport FPBASE_INGEST_v2.1**  
**Prochaine Étape** : A1bis — Intégration Specialist DB + A2 — PMC Mining

