# 🔧 Release Notes — Biological Qubits Atlas v1.2.1

**Date de release** : 2025-10-23  
**Type** : Patch (Metadata Fix)  
**Tag** : v1.2.1

---

## 🎯 Objectif de cette Release

Cette release **v1.2.1** corrige les métadonnées de citation pour :
- ✅ Résoudre l'erreur "Citation metadata load failed"
- ✅ Forcer la génération du DOI Zenodo avec auteur valide
- ✅ Mettre à jour les créateurs dans zenodo.json

**Aucune modification des données** : Le dataset reste identique à v1.2.0 (26 systèmes).

---

## 🔧 Changements v1.2.1

### Métadonnées Corrigées

**CITATION.cff** :
- ✅ Format CFF 1.2.0 strictement conforme
- ✅ Auteur : Tommy Lepesteur (ORCID: 0009-0009-0577-9563)
- ✅ Version mise à jour : 1.2.1
- ✅ Date de release : 2025-10-23
- ✅ Abstract complet ajouté

**zenodo.json** :
- ✅ Créateurs mis à jour : Lepesteur, Tommy
- ✅ ORCID : 0009-0009-0577-9563
- ✅ Cohérence avec CITATION.cff

---

## 📊 Dataset Inchangé (v1.2.0 → v1.2.1)

Le contenu scientifique est **identique à v1.2.0** :

- **26 systèmes** quantiques biologiques
- **20 entrées vérifiées** (77%)
- **11 systèmes in vivo** (42%)
- **0 erreurs bloquantes** (linter validé)
- **Provenance complète** (88% T2, 100% T1, 90% Contraste)

### Répartition par Classe
- Classe A (Bio intrinsèque) : 2
- Classe B (Bio-compatibles) : 13
- Classe C (Spins nucléaires) : 9
- Classe D (Candidats mécanistiques) : 2

---

## 🆚 Différences v1.2.0 vs v1.2.1

| Aspect | v1.2.0 | v1.2.1 |
|--------|--------|--------|
| **Dataset** | 26 systèmes | 26 systèmes (inchangé) |
| **CITATION.cff** | Auteur anonymisé | Tommy Lepesteur + ORCID ✅ |
| **zenodo.json** | Créateur anonymisé | Tommy Lepesteur + ORCID ✅ |
| **Format CFF** | 1.2.0 (erreurs) | 1.2.0 (conforme) ✅ |
| **Zenodo DOI** | Pending | Sera généré automatiquement |

---

## ⚡ Actions Déclenchées par v1.2.1

1. **Tag Git** : v1.2.1 créé et poussé
2. **GitHub Release** : À créer manuellement (voir instructions)
3. **Zenodo** : Détection automatique de la release + génération DOI
4. **GitHub Pages** : Redéploiement automatique

---

## 📋 Instructions Publication

### 1. Créer la Release GitHub (REQUIS)

**URL** : https://github.com/Mythmaker28/biological-qubits-atlas/releases/new?tag=v1.2.1

**Formulaire** :
- Tag : `v1.2.1` (sélectionner)
- Title : `Biological Qubits Atlas v1.2.1`
- Description : Copier ce fichier (RELEASE_NOTES_v1.2.1.md)
- Assets : biological_qubits.csv, QC_REPORT.md, LICENSE, CITATION.cff
- Publier (pas de draft)

### 2. Vérifier Zenodo (2-10 minutes après)

**URL** : https://zenodo.org/account/settings/github/

Actions :
1. Vérifier que `biological-qubits-atlas` apparaît
2. Si absent : "Sync now" + activer toggle
3. Récupérer le **Concept DOI** (permanent)
4. Noter aussi le **Version DOI** (spécifique v1.2.1)

### 3. Mettre à Jour le Badge DOI

Éditer `README.md` et `CITATION.cff` avec le DOI réel (voir rapport final).

---

## 🔗 Liens Utiles

- **Tag v1.2.1** : https://github.com/Mythmaker28/biological-qubits-atlas/tree/v1.2.1
- **Créer Release** : https://github.com/Mythmaker28/biological-qubits-atlas/releases/new?tag=v1.2.1
- **Zenodo** : https://zenodo.org/account/settings/github/
- **Site Live** : https://mythmaker28.github.io/biological-qubits-atlas/

---

## 📧 Citation

Après génération du DOI Zenodo :

```bibtex
@dataset{biological_qubits_atlas_2025,
  author       = {Lepesteur, Tommy},
  title        = {Biological Qubits Atlas},
  year         = 2025,
  publisher    = {Zenodo},
  version      = {1.2.1},
  doi          = {10.5281/zenodo.XXXXXXX},
  url          = {https://github.com/Mythmaker28/biological-qubits-atlas}
}
```

---

**🎉 Cette release corrige les métadonnées et déclenche la génération du DOI Zenodo !**





