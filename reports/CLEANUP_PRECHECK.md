# 🧹 CLEANUP PRE-CHECK v2.0

**Date** : 2025-10-24  
**Branche** : release/v2.0  
**Objectif** : Inventaire des fichiers à archiver avant consolidation v2.0

---

## 📋 Résumé Exécutif

| Catégorie | Fichiers à archiver | Action |
|-----------|---------------------|--------|
| **Doublons v1.3 (data/processed)** | 4 fichiers | → archive/ |
| **Pollution interim** | 5 fichiers | → archive/ |
| **Pollution submissions** | 22 fichiers (frontiers) | → archive/ |
| **Pollution dist/** | 4 fichiers | → archive/ |
| **Dashboards dupliqués** | 2 fichiers racine | Consolidation → docs/index.html |
| **Documentation obsolète** | 11 fichiers | → archive/ |
| **Scripts v1.2** | 3 fichiers | → archive/ |
| **TOTAL** | **51 fichiers** | |

---

## 🗂️ Section 1 : Doublons de Données (data/processed/)

### ❌ Fichiers v1.3 à archiver

```
data/processed/atlas_fp_optical_v1_3.csv
data/processed/atlas_fp_optical_v1_3.parquet
data/processed/SHA256SUMS_v1.3.txt
data/processed/TRAINING.METADATA.v1.3.json
```

### ❌ Fichiers sans version à archiver

```
data/processed/atlas_all_real.csv
data/processed/atlas_fp_optical.csv
data/processed/TRAINING.METADATA.json
```

**Note** : Ces fichiers sans suffixe de version sont probablement des liens symboliques ou copies de v1.3. Ils doivent être archivés pour éviter toute ambiguïté.

### ✅ Fichiers v2.0 à CONSERVER

```
data/processed/atlas_fp_optical_v2_0.csv
```

**⚠️ MANQUANTS (à vérifier/créer)** :
```
data/processed/atlas_fp_optical_v2_0.parquet
data/processed/TRAINING.METADATA.v2.0.json
data/processed/SHA256SUMS_v2.0.txt
```

---

## 🗂️ Section 2 : Pollution Interim (data/interim/)

### ❌ Tous les fichiers à archiver

```
data/interim/external_candidates_v1_3.parquet
data/interim/fulltext_contrasts.csv
data/interim/name_queries.parquet
data/interim/new_systems_batch1.csv
data/interim/pmc_contrasts.json
```

**Justification** : La pipeline v2.0 ne doit pas dépendre de fichiers intermédiaires. Ces fichiers doivent être régénérés si nécessaire via la pipeline, pas stockés dans le dépôt.

---

## 🗂️ Section 3 : Pollution Submissions

### ❌ submission/frontiers/ (22 fichiers à archiver)

**Tous les fichiers de ce dossier sont relatifs à v1.2.1 et doivent être archivés :**

```
submission/frontiers/atlas_all_real.csv
submission/frontiers/atlas_fp_optical.csv
submission/frontiers/Cover_Letter.txt
submission/frontiers/Figure_1_Publication_Timeline.png
submission/frontiers/Figure_1_Publication_Timeline.tiff
submission/frontiers/Figure_2_T2_vs_Temperature.png
submission/frontiers/Figure_2_T2_vs_Temperature.tiff
submission/frontiers/Frontiers_Submission_Atlas_v1_2_1.docx
submission/frontiers/Frontiers_Submission_Atlas_v1_2_1.pdf
submission/frontiers/INDEX.txt
submission/frontiers/manuscript.md
submission/frontiers/README_SUBMISSION.md
submission/frontiers/README_Supplementary.txt
submission/frontiers/SHA256SUMS.txt
submission/frontiers/SUBMISSION_CHECKLIST.md
submission/frontiers/Supplementary_A_Audit_Report.md
submission/frontiers/Supplementary_A_Audit_Report.txt
submission/frontiers/Supplementary_B_Evidence_Samples.md
submission/frontiers/Supplementary_B_Evidence_Samples.txt
submission/frontiers/Supplementary_C_Data_Schema.md
submission/frontiers/Supplementary_C_Data_Schema.txt
submission/frontiers/Supplementary_Data_v1_2_1.zip
submission/frontiers/TRAINING.METADATA.json
```

### ✅ submission/bioRxiv/ (à conserver)

Les fichiers bioRxiv semblent actifs et peuvent être conservés pour l'instant. À vérifier si une mise à jour v2.0 est prévue.

---

## 🗂️ Section 4 : Pollution dist/

### ❌ dist/ (4 fichiers à archiver)

```
dist/atlas_all_real.csv
dist/atlas_fp_optical.csv
dist/SHA256SUMS.txt
dist/TRAINING.METADATA.json
```

**Justification** : Le dossier `dist/` contient des copies sans version explicite. La source unique de vérité doit être `data/processed/atlas_fp_optical_v2_0.*`.

**Stratégie recommandée** : Archiver tout le dossier `dist/`. Si un dossier de distribution est nécessaire, il devra être régénéré avec des liens symboliques ou copies explicites vers v2.0.

---

## 🗂️ Section 5 : Dashboards Dupliqués

### ❌ Fichiers racine à traiter

```
index.html                   → À ARCHIVER (probablement v1.2 ou v1.3)
index_v2_interactive.html    → À DÉPLACER vers docs/index.html (et renommer)
```

**Action recommandée** :
1. Archiver l'ancien `index.html`
2. Exécuter `git mv index_v2_interactive.html docs/index.html`

### ✅ Dashboard actif

```
docs/index.html   (actuellement absent, doit être créé depuis index_v2_interactive.html)
```

---

## 🗂️ Section 6 : Documentation Obsolète

### ❌ Release Notes v1.2 (7 fichiers à archiver)

```
RELEASE_NOTES_v1.2.1.md
RELEASE_NOTES_v1.2.0.md
RELEASE_NOTES_v1.2.md
RELEASE_NOTES_v1.2.0.FULL.md
RELEASE_NOTES_v1.2.0-pre.md
README_v1.2.0_DELIVERY.md
docs/README_PIPELINE_v1.2.md
```

### ❌ Reports v1.2/v1.3 (1 fichier à archiver)

```
reports/AUDIT_v1.2_fp_optical.md
```

**Note** : Le fichier `reports/AUDIT_v1.3_fp_optical.md` peut être conservé si utile pour comparaison, mais devrait idéalement être archivé également.

---

## 🗂️ Section 7 : Scripts Obsolètes

### ❌ Scripts v1.2 (3 fichiers à archiver)

```
scripts/qa/audit_fp_optical_v1_2.py
scripts/qa/audit_atlas_v1_2_strict.py
scripts/etl/build_atlas_tables_v1_2.py
```

**⚠️ PALIER DE SÉCURITÉ** : Vérifier que ces scripts ne sont **pas** utilisés par la pipeline v2.0 avant archivage. Si des fonctionnalités sont toujours nécessaires, elles doivent être migrées vers des scripts v2.0.

---

## 🗂️ Section 8 : Liens Cassés (README.md)

### ❌ Badges et URLs à mettre à jour

**Lignes 12-13** : Références à v2.0.0 et v1.3.0-beta ✅ (OK)

**Ligne 48** : Mention de "Version 1.2.1 — Stable Release" 🟢
- **À CORRIGER** : Remplacer par "Version 2.0.0 — Stable Release"

**Ligne 77** : Structure du projet mentionne `biological_qubits.csv` (ancien nom)
- **À CORRIGER** : Mettre à jour vers `data/processed/atlas_fp_optical_v2_0.csv`

**Ligne 78** : Mention de `index.html` à la racine
- **À CORRIGER** : Doit pointer vers `docs/index.html`

### 🔍 URLs/DOIs à vérifier

- Ligne 3 : Zenodo DOI 10.5281/zenodo.17420604 (à vérifier si correspond à v2.0)
- Ligne 5 : GitHub Pages URL (doit pointer vers le nouveau dashboard docs/)

---

## ✅ Plan d'Archivage Recommandé

### Commandes Archivage (à exécuter à l'étape 3.3)

```powershell
# Créer le dossier d'archive avec timestamp
$archiveDate = Get-Date -Format "yyyy-MM-dd"
$archiveDir = "archive/$archiveDate-pre-v2-clean"
mkdir -p $archiveDir

# Archiver data/processed (v1.3 et sans version)
git mv data/processed/atlas_fp_optical_v1_3.csv $archiveDir/
git mv data/processed/atlas_fp_optical_v1_3.parquet $archiveDir/
git mv data/processed/SHA256SUMS_v1.3.txt $archiveDir/
git mv data/processed/TRAINING.METADATA.v1.3.json $archiveDir/
git mv data/processed/atlas_all_real.csv $archiveDir/
git mv data/processed/atlas_fp_optical.csv $archiveDir/
git mv data/processed/TRAINING.METADATA.json $archiveDir/

# Archiver data/interim (tout le contenu)
git mv data/interim/* $archiveDir/interim/

# Archiver submission/frontiers (tout le dossier)
git mv submission/frontiers $archiveDir/

# Archiver dist (tout le dossier)
git mv dist $archiveDir/

# Archiver dashboards dupliqués
git mv index.html $archiveDir/

# Archiver documentation obsolète
git mv RELEASE_NOTES_v1.2*.md $archiveDir/
git mv README_v1.2.0_DELIVERY.md $archiveDir/
git mv docs/README_PIPELINE_v1.2.md $archiveDir/
git mv reports/AUDIT_v1.2_fp_optical.md $archiveDir/

# Archiver scripts v1.2
git mv scripts/qa/audit_fp_optical_v1_2.py $archiveDir/scripts/qa/
git mv scripts/qa/audit_atlas_v1_2_strict.py $archiveDir/scripts/qa/
git mv scripts/etl/build_atlas_tables_v1_2.py $archiveDir/scripts/etl/
```

---

## 🎯 Artefacts v2.0 Canoniques (Checklist)

### ✅ Existants
- [ ] `data/processed/atlas_fp_optical_v2_0.csv` ✅

### ⚠️ Manquants (à créer/vérifier)
- [ ] `data/processed/atlas_fp_optical_v2_0.parquet`
- [ ] `data/processed/TRAINING.METADATA.v2.0.json`
- [ ] `data/processed/SHA256SUMS_v2.0.txt`
- [ ] `docs/index.html` (dashboard v2.0)

---

## 🚨 Questions pour le Maintainer (Paliers de Sécurité)

1. **data/processed/atlas_fp_optical_v2_0.parquet** : Ce fichier n'existe pas. Doit-il être généré par un script ?

2. **TRAINING.METADATA.v2.0.json** : Ce fichier n'existe pas. Doit-il être généré ou copié/renommé depuis un autre fichier ?

3. **SHA256SUMS_v2.0.txt** : Ce fichier n'existe pas. Le script `scripts/release/gen_checksums.py` doit-il être exécuté ?

4. **scripts/etl/build_atlas_tables_v1_2.py** : Ce script est-il toujours utilisé par la pipeline v2.0, ou existe-t-il un équivalent v2.0 ?

5. **Zenodo DOI** : Le DOI actuel (10.5281/zenodo.17420604) correspond-il à v2.0, ou doit-il être mis à jour ?

---

## 📊 Statistiques Finales

| Métrique | Valeur |
|----------|--------|
| **Fichiers à archiver** | 51 |
| **Dossiers à archiver** | 4 (interim/, frontiers/, dist/, scripts v1.2) |
| **Fichiers v2.0 manquants** | 3 |
| **Liens cassés (README.md)** | ~5 |
| **Taille estimée archive** | ~50-100 MB (à confirmer) |

---

**✅ PRÉ-CHECK TERMINÉ**

Prochaine étape : **3.3 Archivage Massif**


