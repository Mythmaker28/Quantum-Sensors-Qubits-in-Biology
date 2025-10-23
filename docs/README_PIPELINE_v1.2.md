# Pipeline ETL v1.2.0 — Guide d'Utilisation

**Version**: 1.2.0  
**Date**: 2025-10-23  
**Type**: Extension FP Optical

---

## 🎯 Objectif

Ce pipeline automatise la construction d'un dataset extensif de **protéines fluorescentes (FP) et biosenseurs optiques** pour le Biological Qubits Atlas.

**Résultat**: 
- ≥50 entrées FP-like total
- ≥25 avec mesures de contraste (ΔF/F₀, on/off ratio)
- Provenance complète + licences tracées

---

## 🔧 Installation Rapide

```bash
# Cloner le repo
git clone https://github.com/Mythmaker28/biological-qubits-atlas.git
cd biological-qubits-atlas

# Basculer sur la branche release
git checkout release/v1.2-fp-optical

# Installer dépendances Python
pip install -r requirements.txt

# Vérifier installation
python run_pipeline.py --help
```

---

## 🚀 Exécution

### Mode Complet (Recommandé)

```bash
# Pipeline complet (harvest → build → contrast → tables → QA)
python run_pipeline.py --full
```

**Durée estimée**: 10-30 minutes (selon taille harvests et rate limiting APIs)

**Sorties**:
- `data/processed/atlas_fp_optical.csv`
- `data/processed/atlas_all_real.csv`
- `data/processed/TRAINING.METADATA.json`
- `reports/AUDIT_v1.2_fp_optical.md`
- `reports/MISSING_FP_WITH_CONTRAST.md`

### Mode Par Étapes

```bash
# 1. Harvest externe uniquement
python run_pipeline.py --harvest

# 2. Build candidats + classification
python run_pipeline.py --build

# 3. Extraction contraste PMC + proxies
python run_pipeline.py --contrast

# 4. Build tables finales
python run_pipeline.py --tables

# 5. QA audit (vérifie seuils)
python run_pipeline.py --qa
```

### Scripts Individuels

```bash
# Harvest
python scripts/etl/fetch_fpbase_candidates.py
python scripts/etl/fetch_uniprot_bulk.py
python scripts/etl/fetch_pdb_pdbe_bulk.py

# Build
python scripts/etl/build_external_candidates.py
python scripts/etl/classify_modality.py

# Contrast
python scripts/etl/fetch_pmc_contrast.py
python scripts/etl/compute_proxies.py

# Tables
python scripts/etl/build_atlas_tables_v1_2.py

# QA
python scripts/qa/audit_fp_optical_v1_2.py
```

---

## 📊 Architecture du Pipeline

```
┌─────────────────┐
│  HARVEST        │
│  (External APIs)│
└────────┬────────┘
         │
         ├─► FPbase API ──────► data/raw/external/fpbase/*.json
         ├─► UniProt API ─────► data/raw/external/uniprot/*.json
         └─► PDB/PDBe API ───► data/raw/external/pdb/*.json
         
         │
         ▼
┌─────────────────┐
│  BUILD          │
│  (Candidates)   │
└────────┬────────┘
         │
         ├─► Fusion sources
         ├─► Normalisation noms
         ├─► Déduplication
         └─► Classification modality (FP vs non-FP)
         
         │
         ▼
         data/interim/external_candidates.parquet
         
         │
         ▼
┌─────────────────┐
│  CONTRAST       │
│  (PMC + Proxies)│
└────────┬────────┘
         │
         ├─► PMC search (OA articles)
         ├─► Regex extraction (ΔF/F₀, on/off)
         └─► Brightness proxies (QY × ε)
         
         │
         ▼
         data/interim/pmc_contrast_measurements.parquet
         
         │
         ▼
┌─────────────────┐
│  TABLES         │
│  (Assembly)     │
└────────┬────────┘
         │
         ├─► atlas_all_real.csv (multi-modality)
         ├─► atlas_fp_optical.csv (FP-only)
         └─► TRAINING.METADATA.json
         
         │
         ▼
┌─────────────────┐
│  QA AUDIT       │
│  (Validation)   │
└────────┬────────┘
         │
         ├─► Check N_total ≥ 50
         ├─► Check N_measured ≥ 25
         ├─► Generate reports
         └─► Exit code (0=pass, ≠0=fail)
         
         │
         ▼
         ✅ RELEASE READY
```

---

## 📁 Structure de Données

### Input (Harvest)

```
data/raw/external/
  ├─ fpbase/
  │   └─ fpbase_proteins.json
  ├─ uniprot/
  │   └─ uniprot_fluorescent_proteins.json
  ├─ pdb/
  │   └─ pdb_fluorescent_proteins.json
  └─ pmc/
      └─ (articles OA, si applicable)
```

### Interim (Processing)

```
data/interim/
  ├─ external_candidates.parquet       # Candidats fusionnés + classifiés
  └─ pmc_contrast_measurements.parquet # Mesures de contraste extraites
```

### Output (Final)

```
data/processed/
  ├─ atlas_all_real.csv              # Multi-modality (FP + NV + NMR + ...)
  ├─ atlas_fp_optical.csv            # FP/biosensors uniquement ⭐
  └─ TRAINING.METADATA.json          # Schéma + licences + provenance

reports/
  ├─ EXTERNAL_HARVEST_LOG.md         # Traçabilité harvests (SHA256)
  ├─ MODALITY_SPLIT.md               # Stats classification
  ├─ AUDIT_v1.2_fp_optical.md        # Rapport QA complet ⭐
  └─ MISSING_FP_WITH_CONTRAST.md     # Action plan amélioration

patch/
  └─ SCHEMA_MAP.yaml                 # Mapping alias colonnes
```

---

## 🔍 Schéma `atlas_fp_optical.csv`

| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `SystemID` | string | ID unique | `FP_EXT_0001` |
| `protein_name` | string | Nom commun | `EGFP` |
| `variant` | string | Variant génétique | `A206K` |
| `family` | string | Famille | `GFP` |
| `is_biosensor` | int | 1=biosensor, 0=FP | `1` |
| `uniprot_id` | string | Accession UniProt | `P42212` |
| `pdb_id` | string | Structure PDB | `1EMA` |
| `excitation_nm` | float | Excitation (nm) | `488.0` |
| `emission_nm` | float | Émission (nm) | `509.0` |
| `temperature_K` | float | Température (K) | `298.15` |
| `pH` | float | pH | `7.4` |
| `contrast_ratio` | float | ΔF/F₀ ou on/off | `5.2` |
| `contrast_ci_low` | float | CI 95% low | `4.8` |
| `contrast_ci_high` | float | CI 95% high | `5.6` |
| `contrast_source` | string | `measured`, `computed`, `none` | `measured` |
| `condition_text` | string | Description conditions | `In HeLa cells, Ca²⁺ stimulus` |
| `source_refs` | string | DOI/PMCID/URL | `PMC1234567` |
| `license_source` | string | Licence source | `CC BY 4.0 (PMC)` |

---

## 🔐 Sources de Données & Licences

| Source | Type | Licence | Attribution |
|--------|------|---------|-------------|
| **FPbase** | API | CC BY-SA 4.0 | Pointer-only, https://www.fpbase.org |
| **UniProt** | API | CC BY 4.0 | https://www.uniprot.org |
| **PDB/PDBe** | API | CC0 | Domaine public |
| **PMC** | API | CC BY | Articles OA uniquement |

**Licence globale Atlas**: CC BY 4.0

---

## ⚙️ Configuration Avancée

### Rate Limiting

Scripts intègrent des `time.sleep()` pour respecter fair use des APIs:
- FPbase: 1s entre requêtes détaillées
- UniProt: 1s entre queries
- PMC: 0.5s entre articles, max 10 articles/protéine

### Customisation

Éditer directement les scripts pour:
- Changer queries de recherche (SEARCH_QUERIES dans `fetch_uniprot_bulk.py`)
- Modifier patterns regex contraste (CONTRAST_PATTERNS dans `fetch_pmc_contrast.py`)
- Ajuster seuils QA (MIN_TOTAL, MIN_MEASURED dans `audit_fp_optical_v1_2.py`)

---

## 🐛 Troubleshooting

### Erreur: `No proteins retrieved from FPbase`

**Cause**: API FPbase down ou rate limit

**Solution**:
```bash
# Vérifier connectivité
curl https://www.fpbase.org/api/proteins/

# Réessayer après 5 min
```

### Erreur: `QA audit failed - thresholds not met`

**Cause**: Pas assez de données récupérées

**Solution**:
1. Consulter `reports/MISSING_FP_WITH_CONTRAST.md`
2. Ajouter manuellement des sources supplémentaires
3. Ajuster seuils dans `scripts/qa/audit_fp_optical_v1_2.py` (déconseillé)

### Erreur: `ModuleNotFoundError: No module named 'pandas'`

**Cause**: Dépendances non installées

**Solution**:
```bash
pip install -r requirements.txt
```

---

## 📈 CI/CD Automatique

Le workflow `.github/workflows/atlas_external_fp.yml` s'exécute:

- **Manual trigger**: Actions → "Atlas External FP Pipeline" → Run workflow
- **Hebdomadaire**: Lundi 2am UTC (refresh automatique)

**Artifacts GitHub** (conservés 30-90 jours):
- `harvest-raw-data`
- `candidates-interim`
- `atlas-tables`
- `qa-reports`

---

## 🎯 Cas d'Usage

### 1. Chercheur ajoutant un nouveau biosenseur

```bash
# 1. Ajouter manuellement ligne dans biological_qubits.csv
# 2. Relancer pipeline pour fusion
python run_pipeline.py --full

# 3. Vérifier dans atlas_fp_optical.csv
head data/processed/atlas_fp_optical.csv
```

### 2. Data scientist entraînant modèle ML

```python
import pandas as pd

# Charger dataset stable
df = pd.read_csv("data/processed/atlas_fp_optical.csv")

# Filtrer données avec contraste mesuré
measured_df = df[df['contrast_source'] == 'measured']

# Features: excitation, emission, contraste
X = measured_df[['excitation_nm', 'emission_nm']].values
y = measured_df['contrast_ratio'].values
```

### 3. Mainteneur mettant à jour sources

```bash
# 1. Modifier queries dans fetch_uniprot_bulk.py
# 2. Relancer harvest
python scripts/etl/fetch_uniprot_bulk.py

# 3. Rebuild complet
python run_pipeline.py --build --tables --qa
```

---

## 📚 Documentation Complète

- **Contrat d'interface**: `docs/CONSUMERS.md`
- **Release notes**: `RELEASE_NOTES_v1.2.md`
- **Rapport livraison**: `README_v1.2.0_DELIVERY.md`
- **Citation**: `CITATION.cff`

---

## 🤝 Contribution

Voir `CONTRIBUTING.md` pour guidelines.

**Pull Requests** bienvenues pour:
- Nouveaux biosenseurs
- Amélioration parsers PMC
- Nouveaux proxies de contraste
- Corrections bugs

---

## 📞 Support

- **Issues**: https://github.com/Mythmaker28/biological-qubits-atlas/issues
- **Discussions**: https://github.com/Mythmaker28/biological-qubits-atlas/discussions

---

**Fin du Guide Pipeline v1.2.0**

