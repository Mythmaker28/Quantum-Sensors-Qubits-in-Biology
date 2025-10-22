# 🔍 Rapport de Contrôle Qualité — Atlas des Qubits Biologiques v1.2

**Date** : 2025-10-22 21:55
**Fichier** : `biological_qubits.csv`

## 📊 Statistiques

- **Total systèmes analysés** : 21
- **❌ Erreurs bloquantes** : 0
- **⚠️ Warnings** : 3
- **ℹ️ Informations** : 0
- **✅ Systèmes sans erreur** : 21

### ✅ Aucune erreur bloquante détectée !

Le dataset est prêt pour publication.

## ⚠️ WARNINGS (3)

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

## 📝 Systèmes à confirmer (Verification_statut=a_confirmer)

**Total** : 6 systèmes

- **Nanotubes de carbone avec défauts sp3** (Classe B) — DOI: 10.1038/s41467-020-19390-3
- **Cryptochrome (Cry1) - paires radicalaires** (Classe D) — DOI: 10.1038/nature09324
- **Protéine LOV2 modifiée (flavine)** (Classe A) — DOI: 10.1021/jacs.0c12505
- **Centres GeV dans diamant (bioconjugué)** (Classe B) — DOI: 10.1021/acsphotonics.1c00935
- **Défauts divacancy VV dans SiC (nanoparticules)** (Classe B) — DOI: 10.1021/acs.nanolett.0c02342
- **Défauts Ti:C dans SiC (en développement)** (Classe B) — DOI: 10.1038/s41467-022-32717-8

---

*Rapport généré automatiquement par `qubits_linter.py`*
