# 🔍 Rapport de Contrôle Qualité — Atlas des Qubits Biologiques v1.2

**Date** : 2025-10-23 02:57
**Fichier** : `biological_qubits.csv`

## 📊 Statistiques

- **Total systèmes analysés** : 32
- **❌ Erreurs bloquantes** : 0
- **⚠️ Warnings** : 4
- **ℹ️ Informations** : 0
- **✅ Systèmes sans erreur** : 32

### ✅ Aucune erreur bloquante détectée !

Le dataset est prêt pour publication.

## ⚠️ WARNINGS (4)

### Ligne 8 : Quantum dots CdSe avec lecture de spin

**Colonne** : `Source_T2`

**Problème** : T2 sans source de provenance

**Valeur actuelle** : `NA`

**Suggestion** : Ajouter DOI:xxx Fig.X ou estimation si calculé

---

### Ligne 8 : Quantum dots CdSe avec lecture de spin

**Colonne** : `Source_Contraste`

**Problème** : Contraste sans source

**Valeur actuelle** : `NA`

**Suggestion** : Ajouter référence publication

---

### Ligne 15 : Cryptochrome (Cry1) - paires radicalaires

**Colonne** : `Source_T2`

**Problème** : T2 sans source de provenance

**Valeur actuelle** : `NA`

**Suggestion** : Ajouter DOI:xxx Fig.X ou estimation si calculé

---

### Ligne 31 : Radicaux tyrosyl dans ribonucléotide réductase

**Colonne** : `Source_Contraste`

**Problème** : Contraste sans source

**Valeur actuelle** : `NA`

**Suggestion** : Ajouter référence publication

---

## 📝 Systèmes à confirmer (Verification_statut=a_confirmer)

**Total** : 9 systèmes

- **Nanotubes de carbone avec défauts sp3** (Classe B) — DOI: 10.1038/s41467-020-19390-3
- **Cryptochrome (Cry1) - paires radicalaires** (Classe D) — DOI: 10.1038/nature09324
- **Protéine LOV2 modifiée (flavine)** (Classe A) — DOI: 10.1021/jacs.0c12505
- **Centres GeV dans diamant (bioconjugué)** (Classe B) — DOI: 10.1021/acsphotonics.1c00935
- **Défauts divacancy VV dans SiC (nanoparticules)** (Classe B) — DOI: 10.1021/acs.nanolett.0c02342
- **Défauts Ti:C dans SiC (en développement)** (Classe B) — DOI: 10.1038/s41467-022-32717-8
- **Centres P1 dans nanodiamants (azote isolé)** (Classe B) — DOI: 10.1021/acsnano.8b07278
- **Radicaux tyrosyl dans ribonucléotide réductase** (Classe A) — DOI: 10.1021/bi00483a003
- **Quantum dots InP/ZnS biocompatibles** (Classe B) — DOI: 10.1021/acsnano.7b08724

---

*Rapport généré automatiquement par `qubits_linter.py`*
