# Atlas FP Optical — Consumer Documentation

**Version**: 1.2.0  
**Date**: 2025-10-23  
**Target Audience**: Downstream repositories (fp-qubit-design, machine learning pipelines)

---

## Overview

Ce document définit le contrat d'interface pour consommer les données de l'Atlas FP Optical.

L'Atlas FP Optical est un dataset curé de protéines fluorescentes (FP) et biosenseurs optiques, conçu pour alimenter des pipelines de design computationnel et d'apprentissage automatique.

---

## Stable Data Sources

### 1. atlas_fp_optical.csv

**URL stable (Release v1.2.0)**:
```
https://github.com/[OWNER]/[REPO]/releases/download/v1.2.0/atlas_fp_optical.csv
```

**Zenodo DOI** (versionné):
```
https://doi.org/10.5281/zenodo.XXXXXXX  # À compléter après dépôt
```

**Checksum (SHA256)**:
```
4924904F093A6A3D9C6ED15A5294E77AD31899CD689CF50A898F565BDAADE3DA
```

**Format**: CSV (UTF-8, comma-separated)

**Taille estimée**: ~50-200 entrées (v1.2.0)

---

## Schema Guarantees

L'`atlas_fp_optical.csv` garantit les colonnes suivantes dans cet ordre:

| Column Name | Type | Description | Nullable |
|-------------|------|-------------|----------|
| `SystemID` | string | Identifiant unique (format: `FP_EXT_XXXX`) | No |
| `protein_name` | string | Nom commun de la protéine | No |
| `variant` | string | Variant génétique (e.g., "wild-type", "A206K") | Yes |
| `family` | string | Famille de protéine (e.g., "GFP", "mCherry") | Yes |
| `is_biosensor` | int | `1` si biosenseur, `0` si FP classique | No |
| `uniprot_id` | string | Accession UniProt | Yes |
| `pdb_id` | string | Structure PDB ID | Yes |
| `excitation_nm` | float | Longueur d'onde d'excitation (nm) | Yes |
| `emission_nm` | float | Longueur d'onde d'émission (nm) | Yes |
| `temperature_K` | float | Température de mesure (Kelvin) | Yes |
| `pH` | float | pH de mesure | Yes |
| `contrast_ratio` | float | ΔF/F₀, on/off ratio, ou fold-change | Yes |
| `contrast_ci_low` | float | Borne inférieure IC 95% | Yes |
| `contrast_ci_high` | float | Borne supérieure IC 95% | Yes |
| `contrast_source` | string | `"measured"`, `"computed"`, ou `"none"` | No |
| `condition_text` | string | Description textuelle des conditions | Yes |
| `source_refs` | string | DOI, PMCID, ou référence base de données | Yes |
| `license_source` | string | Licence des données source | Yes |

---

## Data Quality Metrics (v1.2.0)

- **Total FP entries**: ≥ 50 (garanti par QA)
- **With measured contrast**: ≥ 25 (garanti par QA)
- **With computed contrast**: Variable (≥ 10 estimé)
- **With any contrast**: ≥ 35 (estimé)

---

## Versioning Policy

### Semantic Versioning

Le projet suit SemVer pour les releases de données:

- **MAJOR** (v2.0.0): Changements non rétrocompatibles du schéma (colonnes renommées, supprimées)
- **MINOR** (v1.2.0): Ajout de nouvelles colonnes, nouvelles entrées, améliorations compatibles
- **PATCH** (v1.2.1): Corrections de données, bugfixes, pas de changements de schéma

### DOI Policy

Chaque release MINOR ou MAJOR reçoit un **DOI versionné** via Zenodo.

Le **DOI concept** (toujours la dernière version):
```
https://doi.org/10.5281/zenodo.CONCEPT_ID
```

Les **DOIs versionnés** (figés):
```
v1.2.0: https://doi.org/10.5281/zenodo.VERSION_ID_1_2_0
v1.1.0: https://doi.org/10.5281/zenodo.VERSION_ID_1_1_0
```

---

## How to Consume

### Option 1: Direct Download (Recommended for Production)

```python
import pandas as pd

# Utiliser l'URL de release stable ou le DOI Zenodo
url = "https://github.com/[OWNER]/[REPO]/releases/download/v1.2.0/atlas_fp_optical.csv"

df = pd.read_csv(url)
print(f"Loaded {len(df)} FP entries")
```

### Option 2: Git Submodule (Pour Développement)

```bash
cd your-project/
git submodule add https://github.com/[OWNER]/[REPO].git data/atlas
git submodule update --init --recursive

# Pin à une version spécifique
cd data/atlas
git checkout v1.2.0
```

### Option 3: Package Manager (Future)

```bash
# Futur: pip install biological-qubits-atlas
```

---

## Metadata Access

Le fichier `TRAINING.METADATA.json` accompagne chaque release et contient:

- Schéma complet avec descriptions
- Licences par source
- Provenance (scripts ETL, dates de harvest)
- Quality metrics
- Parsing rules et aliases

**URL**:
```
https://github.com/[OWNER]/[REPO]/releases/download/v1.2.0/TRAINING.METADATA.json
```

---

## License & Attribution

### Data License

Les données de l'Atlas sont agrégées depuis plusieurs sources avec licences variées:

- **FPbase**: CC BY-SA 4.0 (pointer-only, attribution requise)
- **UniProt**: CC BY 4.0
- **PDB**: CC0 (domaine public)
- **PMC**: CC BY ou compatible (articles OA uniquement)

**Global License**: CC BY 4.0 (pour l'agrégation et métadonnées)

### Citation

```bibtex
@dataset{biological_qubits_atlas_2025,
  author       = {[Author Names]},
  title        = {Biological Qubits Atlas: Fluorescent Proteins \& Optical Biosensors},
  year         = 2025,
  version      = {1.2.0},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.XXXXXXX},
  url          = {https://github.com/[OWNER]/[REPO]}
}
```

---

## Support & Contributions

### Issues

Rapporter des problèmes de données via:
- **GitHub Issues**: [New Data Fix](https://github.com/[OWNER]/[REPO]/issues/new?template=data_fix.yml)
- **New Entry Request**: [New Entry](https://github.com/[OWNER]/[REPO]/issues/new?template=new_entry.yml)

### Pull Requests

Contributions bienvenues! Voir [CONTRIBUTING.md](../CONTRIBUTING.md).

### Contact

- **Maintainer**: [Contact info]
- **Email**: research@example.org
- **Discussions**: [GitHub Discussions](https://github.com/[OWNER]/[REPO]/discussions)

---

## Breaking Changes Policy

Les changements cassants (breaking changes) sont **toujours** signalés:

1. **Deprecation notice** dans la version MINOR précédente
2. **Migration guide** publié avant la version MAJOR
3. **Changelog détaillé** dans `RELEASE_NOTES_vX.Y.md`

---

## Example Integration (fp-qubit-design)

Fichier `config/data_sources.yaml`:

```yaml
atlas_fp_optical:
  source: "github_release"
  repository: "[OWNER]/[REPO]"
  version: "v1.2.0"
  file: "atlas_fp_optical.csv"
  checksum_sha256: "TBD"  # Verification
  license: "CC BY 4.0"
  update_policy: "manual"  # or "auto_minor"
```

Code Python:

```python
from pathlib import Path
import pandas as pd
import hashlib

def load_atlas(config: dict) -> pd.DataFrame:
    """Charge l'Atlas avec vérification d'intégrité."""
    version = config['version']
    url = f"https://github.com/{config['repository']}/releases/download/{version}/{config['file']}"
    
    df = pd.read_csv(url)
    
    # Vérifier checksum (optionnel)
    expected_checksum = config.get('checksum_sha256')
    if expected_checksum:
        actual_checksum = hashlib.sha256(df.to_csv(index=False).encode()).hexdigest()
        assert actual_checksum == expected_checksum, "Checksum mismatch!"
    
    return df

# Usage
atlas_df = load_atlas(config['atlas_fp_optical'])
```

---

## Changelog

### v1.2.0 (2025-10-23)

- ✨ **New**: External harvest pipeline (FPbase, UniProt, PDB, PMC)
- ✨ **New**: `atlas_fp_optical.csv` with ≥50 FP entries, ≥25 with measured contrast
- ✨ **New**: PMC contrast extraction (OA-only)
- ✨ **New**: Computed contrast proxies (QY × ε)
- 📝 **Docs**: Consumer documentation, versioning policy, DOI integration

### v1.1.0 (Earlier)

- 🐛 Legacy data (34 systems, mostly color centers)
- 📝 Initial schema

---

**End of Consumer Documentation**

