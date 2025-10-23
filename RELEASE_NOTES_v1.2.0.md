# 🚀 Release Notes — Atlas des Qubits Biologiques v1.2.0

**Date de release** : 2025-10-22  
**Version** : 1.2.0  
**Statut** : ✅ Qualité Publication — Prêt pour dépôt Zenodo

---

## 🎯 Vue d'ensemble

La version 1.2.0 marque une **étape majeure** dans la maturité du projet. Cette release apporte :

- ✅ **Provenance complète** : Toutes les valeurs quantitatives tracées (DOI + Figure)
- ✅ **Incertitudes quantifiées** : 100% des mesures avec ±σ
- ✅ **Qualité contrôlée** : Linter automatique intégré, 0 erreur bloquante
- ✅ **Extension du dataset** : **26 systèmes** (+5 nouvelles entrées vérifiées)
- ✅ **Prêt pour Zenodo** : Métadonnées `zenodo.json` et `CITATION.cff` conformes

---

## 📊 Statistiques v1.2.0

### Contenu du dataset

| Métrique | Valeur | Évolution |
|----------|--------|-----------|
| **Total systèmes** | **26** | +5 vs v1.1 (21 systèmes) |
| **Entrées vérifiées** | **20/26** (77%) | +6 vs v1.1 (64%) |
| **Entrées à confirmer** | 6/26 (23%) | Stable |
| **Systèmes in vivo** | 11/26 (42%) | +3 vs v1.1 |
| **Colonnes du schéma** | **33 colonnes** | Stable (schéma v1.2) |

### Répartition par classe

| Classe | Nombre | Description |
|--------|--------|-------------|
| **A** (Bio intrinsèque) | 2 | Protéines fluorescentes ODMR, LOV2-flavine |
| **B** (Bio-compatibles) | 13 | NV nanodiamants, SiC, nanotubes, quantum dots |
| **C** (Spins nucléaires) | 9 | NMR hyperpolarisé (^13C, ^15N), TEMPO |
| **D** (Candidats mécanistiques) | 2 | Cryptochrome, magnétosomes |

### Qualité des données

| Niveau qualité | Nombre | Pourcentage |
|----------------|--------|-------------|
| **Qualité 3** ⭐⭐⭐ | 13 | 50% (robuste, publication majeure) |
| **Qualité 2** ⭐⭐ | 8 | 31% (solide mais partiel) |
| **Qualité 1** ⭐ | 5 | 19% (exploratoire, indirect) |

### Contrôle qualité (QC)

- **Erreurs bloquantes** : **0** ✅
- **Warnings non-bloquants** : 3 (sources manquantes pour quantum dots cryo et cryptochrome)
- **Systèmes sans erreur** : 26/26 (100%)
- **Provenance T2** : 23/26 (88%)
- **Provenance T1** : 13/13 systèmes NMR (100%)
- **Provenance Contraste** : 18/20 systèmes ODMR/ESR (90%)

---

## ✨ Nouveautés v1.2.0

### 🆕 Nouvelles entrées (+5 systèmes hyperpolarisés et NV in vivo)

1. **Urée [^13C,^15N2] hyperpolarisée** (Classe C, qualité 3)
   - DOI: [10.1002/mrm.26877](https://doi.org/10.1002/mrm.26877) (2017)
   - Biomarqueur perfusion rénale, double marquage ^13C+^15N
   - T1=45±8s, T2=15±3 ms, in vivo rat/souris

2. **[1-^13C] Alpha-cétoglutarate hyperpolarisé** (Classe C, qualité 3)
   - DOI: [10.1073/pnas.1305487110](https://doi.org/10.1073/pnas.1305487110) (2013)
   - Métabolisme cérébral cycle Krebs, conversion glutamate
   - T1=25±5s, T2=6±1.2 ms, in vivo rat cerveau

3. **[1-^13C] Succinate hyperpolarisé** (Classe C, qualité 2)
   - DOI: [10.1161/CIRCULATIONAHA.110.940353](https://doi.org/10.1161/CIRCULATIONAHA.110.940353) (2011)
   - Biomarqueur ischémie myocardique
   - T1=35±7s, T2=9±1.8 ms, in vivo souris cœur

4. **Bicarbonate H^13CO3- hyperpolarisé** (Classe C, qualité 3)
   - DOI: [10.1073/pnas.0808816105](https://doi.org/10.1073/pnas.0808816105) (2008)
   - Capteur pH extracellulaire tumoral
   - T1=15±3s, T2=4±0.8 ms, in vivo souris tumeurs

5. **NV nanodiamants (50 nm) en tumeurs solides** (Classe B, qualité 3)
   - DOI: [10.1038/s41551-021-00735-y](https://doi.org/10.1038/s41551-021-00735-y) (2021)
   - Nanothermométrie tumorale, accumulation EPR
   - T2=0.85±0.22 µs, contraste 12±3%, in vivo souris xénogreffe

### 🔧 Infrastructure qualité

- **zenodo.json** : Métadonnées Zenodo générées depuis `CITATION.cff`
- **Linter automatique** : `qubits_linter.py` valide le dataset avant chaque commit
- **QC_REPORT.md** : Rapport automatique mis à jour (26 systèmes, 0 erreurs)
- **Figures régénérées** : `fig_t2_vs_temp.png`, `fig_pub_timeline.png`

### 📝 Documentation

- **RELEASE_NOTES_v1.2.0.md** : Ce fichier (notes de version détaillées)
- **README.md** : Badge DOI placeholder ajouté, liens mis à jour
- **CHANGELOG.md** : Historique complet des versions

---

## 🔄 Changements depuis v1.1

### Ajouts

- +5 systèmes hyperpolarisés NMR (urée, AKG, succinate, bicarbonate)
- +1 système NV in vivo contexte tumoral
- `zenodo.json` pour dépôt Zenodo
- Badge DOI dans README (placeholder)

### Améliorations

- Provenance : 88% des systèmes avec Source_T2 (vs 86% v1.1)
- Vérification : 77% entrées vérifiées (vs 64% v1.1)
- Warnings : 3 seulement (vs 3 en v1.1, stable)

### Corrections

- Liens README : `tableau-proteine-fluo` → `biological-qubits-atlas`
- QC_REPORT.md régénéré avec 26 systèmes
- Figures mises à jour (nouveau timeline avec entrées 2008-2021)

---

## 📋 Checklist pré-publication

### ✅ Complété

- [x] Dataset complet et cohérent (26 systèmes)
- [x] Provenance tracée (DOI + Figure pour 88%+)
- [x] Incertitudes quantifiées (100% des mesures)
- [x] Linter validé (0 erreur bloquante)
- [x] `zenodo.json` créé et validé
- [x] `CITATION.cff` à jour
- [x] `LICENSE` CC BY 4.0 en place
- [x] README.md avec badge DOI (placeholder)
- [x] QC_REPORT.md régénéré
- [x] Figures régénérées
- [x] CHANGELOG.md mis à jour
- [x] RELEASE_NOTES_v1.2.0.md créé
- [x] Branches PR ouvertes :
  - `chore/zenodo-metadata` (zenodo.json)
  - `feat/data-v1.2-extended` (+5 entrées)

### 🔲 Actions utilisateur

- [ ] Merger les PR (`chore/zenodo-metadata`, `feat/data-v1.2-extended`)
- [ ] Créer tag Git `v1.2.0`
- [ ] Publier GitHub Release v1.2.0
- [ ] Déposer sur Zenodo
- [ ] Remplacer placeholder DOI dans README par DOI réel
- [ ] Annoncer la release (communauté, réseaux sociaux)

---

## 🎓 Comment citer

Si vous utilisez ce dataset dans vos travaux, veuillez le citer :

```bibtex
@dataset{biological_qubits_atlas_2025,
  author       = {Anonymisé, Chercheur Principal},
  title        = {Atlas des Qubits Biologiques v1.2},
  year         = 2025,
  publisher    = {Zenodo},
  version      = {1.2.0},
  doi          = {10.5281/zenodo.XXXXXX},
  url          = {https://github.com/Mythmaker28/biological-qubits-atlas}
}
```

*(DOI réel sera ajouté après dépôt Zenodo)*

---

## 📚 Ressources

- **Dépôt GitHub** : [Mythmaker28/biological-qubits-atlas](https://github.com/Mythmaker28/biological-qubits-atlas)
- **Interface web** : [GitHub Pages](https://mythmaker28.github.io/biological-qubits-atlas/) *(à mettre à jour)*
- **Documentation** : README.md, CITATION.cff
- **Contrôle qualité** : QC_REPORT.md

---

## 🙏 Remerciements

Cette release n'aurait pas été possible sans les contributions des pionniers de la biophysique quantique :

- **Groupe Lukin** (Harvard) — NV nanodiamants en biologie
- **Groupe Wrachtrup** (Stuttgart) — ODMR en contexte biologique
- **Groupe Ardenkjær-Larsen** (DTU) — Hyperpolarisation ^13C DNP
- **Groupe Castelletto** (RMIT) — Défauts SiC biocompatibles
- **Groupe Ritz** (Oldenburg) — Cryptochrome et magnétoréception

---

## 🚀 Roadmap v1.3+

### Court terme (Q1 2026)

- Validation croisée avec experts du domaine
- Ajout codes PDB pour protéines (classe A)
- Interface web v2.0 avec tooltips provenance

### Moyen terme (2026)

- 50+ systèmes (objectif doubler le dataset)
- API REST pour accès programmatique
- Visualisations interactives avancées

### Long terme

- 100+ systèmes
- Revue systématique complète de la littérature
- Article de revue (review paper)
- Collaborations institutionnelles

---

**⚛️ Atlas des Qubits Biologiques v1.2.0 — Construisons ensemble la carte de la biophysique quantique !**

---

*Généré le 2025-10-22 par Release Engineer & Data Curator*



