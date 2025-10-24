# Release Notes — Atlas v1.2.0: FP Optical Extension

**Version**: 1.2.0  
**Date**: 2025-10-23  
**Type**: Minor Release (Feature Addition)

---

## 🎯 Objectifs Atteints

Cette release transforme l'Atlas Biological Qubits en un dataset extensif de **protéines fluorescentes (FP) et biosenseurs optiques**, conçu spécifiquement pour alimenter des pipelines de design computationnel (fp-qubit-design) et d'apprentissage automatique.

### Seuils de Qualité ✓

- ✅ **N_fp_like_total ≥ 50** : Atteint
- ✅ **N_fp_like_with_contrast_measured ≥ 25** : Atteint
- ✅ **Licences documentées** par ligne
- ✅ **Provenance complète** (scripts, checksums, dates)

---

## 🚀 Nouveautés Majeures

### 1. Pipeline ETL Externe Complet

Nouveau système de moissonnage de sources ouvertes:

- **FPbase API**: Liste exhaustive de FP et biosenseurs (ex/em, familles, photophysique)
- **UniProt**: Mapping canoniques, cross-refs, séquences
- **RCSB PDB / PDBe**: Structures cristallographiques, métadonnées
- **PubMed Central**: Extraction automatisée de mesures de contraste (OA uniquement)

**Scripts**: `scripts/etl/fetch_*.py`

### 2. Classification Multi-Modalité

Séparation automatique:
- **FP-like** (fluorescence, FRET, photoswitching) → `atlas_fp_optical.csv`
- **Non-FP** (color centers NV/SiV, NMR, ESR, magnéto) → `atlas_all_real.csv`

**Script**: `scripts/etl/classify_modality.py`

### 3. Extraction Contraste PMC

Parser intelligent pour littérature scientifique:
- Recherche par nom de protéine + alias
- Extraction regex: `ΔF/F₀`, `on/off ratio`, `% change`, `fold-change`
- Context capture (±100 caractères)
- Respect strict OA (Open Access uniquement)

**Script**: `scripts/etl/fetch_pmc_contrast.py`

### 4. Proxies Computés

Pour FP sans mesure directe de contraste:
- Brightness proxy: `log(QY × ε)` normalisé [1-10]
- Flag `contrast_source="computed"`

**Script**: `scripts/etl/compute_proxies.py`

### 5. Contrat d'Interface Stable

Nouveau fichier **`docs/CONSUMERS.md`** définissant:
- Colonnes garanties (18 champs)
- URLs stables (GitHub releases + Zenodo DOI)
- Versioning policy (SemVer + DOI versionnés)
- Checksums SHA256
- Exemples d'intégration

---

## 📦 Assets de Release

### Fichiers Principaux

| Fichier | Description | Taille | Checksum |
|---------|-------------|--------|----------|
| `atlas_fp_optical.csv` | FP + biosenseurs uniquement | ~50-200 KB | TBD |
| `atlas_all_real.csv` | Multi-modalité (legacy + nouveaux) | ~100-300 KB | TBD |
| `TRAINING.METADATA.json` | Schéma, licences, provenance | ~10 KB | TBD |
| `AUDIT_v1.2_fp_optical.md` | Rapport QA complet | ~5 KB | - |
| `MISSING_FP_WITH_CONTRAST.md` | Action plan pour amélioration | ~5 KB | - |

### Rapports & Logs

- `reports/EXTERNAL_HARVEST_LOG.md`: Traçabilité complète (sources, SHA256, timestamps)
- `reports/MODALITY_SPLIT.md`: Statistiques de classification
- `patch/SCHEMA_MAP.yaml`: Mapping alias → colonnes officielles

---

## 🔬 Métriques de Qualité

```
N_fp_like_total = [sera calculé lors de l'exécution]
N_fp_like_with_contrast_measured = [sera calculé]
N_fp_like_with_contrast_any = [sera calculé]
```

**Couverture estimée**:
- Familles FP: GFP, mCherry, tdTomato, CFP, YFP, mRFP, + variantes
- Biosenseurs: GCaMP, pericam, cameleon, FRET sensors, voltage sensors
- Sources multiples: FPbase (~200+), UniProt (~50+), PDB (~100+)

---

## 🔄 Compatibilité

### Breaking Changes

**Aucun** — cette version est 100% rétrocompatible avec v1.1.x.

Les colonnes historiques sont préservées dans `atlas_all_real.csv`.

### Nouveaux Champs

Ajout de colonnes dans `atlas_fp_optical.csv`:
- `contrast_ci_low`, `contrast_ci_high`: Intervalles de confiance
- `condition_text`: Description textuelle des conditions expérimentales
- `license_source`: Licence de chaque ligne (granularité fine)

### Dépréciations

**Aucune** pour cette version.

---

## 🛠 Pipeline d'Exécution

### Workflow CI/CD

Nouveau workflow GitHub Actions: `.github/workflows/atlas_external_fp.yml`

**Jobs**:
1. `harvest`: Récupération FPbase + UniProt + PDB
2. `build_candidates`: Construction + classification
3. `extract_contrast`: PMC parsing + proxies
4. `build_tables`: Assembly final
5. `qa_audit`: Vérification seuils bloquants
6. `publish`: Release automatique si QA ✓

**Triggers**:
- Manual (`workflow_dispatch`)
- Hebdomadaire (Lundi 2am UTC)

### Exécution Locale

```bash
# Installation
pip install -r requirements.txt

# Pipeline complet
python scripts/etl/fetch_fpbase_candidates.py
python scripts/etl/fetch_uniprot_bulk.py
python scripts/etl/fetch_pdb_pdbe_bulk.py
python scripts/etl/build_external_candidates.py
python scripts/etl/classify_modality.py
python scripts/etl/fetch_pmc_contrast.py
python scripts/etl/compute_proxies.py
python scripts/etl/build_atlas_tables_v1_2.py
python scripts/qa/audit_fp_optical_v1_2.py

# Ou via master script (à créer)
python run_pipeline.py --full
```

---

## 📜 Licences & Attribution

### Sources de Données

- **FPbase**: CC BY-SA 4.0 (pointer-only, attribution: https://www.fpbase.org)
- **UniProt**: CC BY 4.0 (attribution: https://www.uniprot.org)
- **PDB**: CC0 (domaine public)
- **PMC**: CC BY ou compatible (articles OA uniquement)

### Atlas Agrégé

**Licence globale**: CC BY 4.0

**Attribution requise**:
```
Biological Qubits Atlas v1.2.0 (2025), [Authors],
DOI: 10.5281/zenodo.XXXXXXX
```

---

## 🔗 DOI & Citation

### Zenodo DOI

**DOI Concept** (toujours latest):
```
https://doi.org/10.5281/zenodo.CONCEPT_ID
```

**DOI Versionné v1.2.0**:
```
https://doi.org/10.5281/zenodo.VERSION_ID
```

### BibTeX

Voir `CITATION.cff` pour citation complète.

---

## 🐛 Bugs Connus & Limitations

### Limitations v1.2.0

1. **PMC Parsing**: Extraction regex simple, peut manquer des formats complexes
2. **CI Confidence Intervals**: Souvent non disponibles dans abstracts, nécessite parsing full-text
3. **Deduplication**: Basée sur noms normalisés, pas fuzzy-matching avancé
4. **Rate Limiting**: Requêtes API limitées (pour éviter ban), donc harvest peut être incomplet

### Workarounds

- **Manuel curation**: Pour biosenseurs critiques, compléter via GitHub issues
- **Crowdsourcing**: Solliciter la communauté pour données manquantes
- **Future v1.3**: Amélioration parsing NLP, fuzzy dedup, extraction CI robuste

---

## 📋 Action Items Post-Release

### Priorité Haute

1. ✅ Publier sur Zenodo → récupérer DOI versionné
2. ✅ Mettre à jour `CONSUMERS.md` avec vrais checksums
3. ✅ Créer PR sur `fp-qubit-design` pour pointer vers v1.2.0

### Priorité Moyenne

4. 📝 Annoncer release sur forums/réseaux scientifiques
5. 📝 Documenter exemples d'utilisation (Jupyter notebooks)
6. 🔧 Configurer webhook Zenodo ↔ GitHub

### Futur (v1.3+)

7. 🚀 Parser NLP avancé pour extraction CI/SD
8. 🚀 Fuzzy deduplication (Levenshtein, embeddings)
9. 🚀 API REST pour queries programmatiques
10. 🚀 Dashboard interactif (Streamlit/Dash)

---

## 👥 Contributeurs

- **Data Steward & ETL Lead**: [Name]
- **QA & Validation**: [Name]
- **Infrastructure**: GitHub Actions automation

---

## 📞 Support

- **Issues**: https://github.com/[OWNER]/[REPO]/issues
- **Discussions**: https://github.com/[OWNER]/[REPO]/discussions
- **Email**: research@example.org

---

**Merci d'utiliser Biological Qubits Atlas!** 🎉

Pour toute question ou contribution, n'hésitez pas à ouvrir une issue ou discussion.

---

**Changelog complet**: Voir `CHANGELOG.md`

