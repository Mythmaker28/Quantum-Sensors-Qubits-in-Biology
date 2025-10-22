# 📊 Atlas des Qubits Biologiques — État du Projet v1.2

## ✅ CE QUI EST FAIT (100%)

### 🎯 Dataset v1.2 — Qualité Publication
- [x] **22 systèmes** recensés (4 classes: A/B/C/D)
- [x] **33 colonnes** (vs 23 en v1.1) — +10 colonnes v1.2
- [x] **0 erreur bloquante** (QC validé par linter)
- [x] **14 entrées vérifiées** (64%)
- [x] **100% DOI valides**
- [x] **Provenance** : 86% T2, 100% T1, 89% Contraste
- [x] **Incertitudes** : 100% estimées (±σ)
- [x] **3 corrections** : NV bulk contraste, VV vérifiée, Protéine confirmée

### 📄 Fichiers créés (16 fichiers)
1. [x] **biological_qubits.csv** — Dataset principal (33 colonnes)
2. [x] **index.html** — Interface web (renommé depuis biological_qubits.html)
3. [x] **qubits_linter.py** — Linter automatique Python (10 checks)
4. [x] **QC_REPORT.md** — Rapport qualité (auto-généré, 0 erreur)
5. [x] **LICENSE** — CC BY 4.0 complet
6. [x] **CITATION.cff** — Citation machine-readable (Zenodo-ready)
7. [x] **CHANGELOG.md** — Historique versions 1.0 → 1.2
8. [x] **v1.2_SUMMARY.md** — Résumé exécutif
9. [x] **README.md** — Documentation complète
10. [x] **REPORT.md** — 5 papiers structurants
11. [x] **.github/workflows/ci.yml** — CI automatique
12. [x] **.github/workflows/pages.yml** — Déploiement Pages
13. [x] **.github/ISSUE_TEMPLATE/** — Bug report + Data entry
14. [x] **.github/PULL_REQUEST_TEMPLATE.md** — Template PR
15. [x] **.gitignore** — Fichiers exclus
16. [x] **GITHUB_SETUP.md** + **NEXT_STEPS.md** + **SETUP_INSTRUCTIONS.md** — Guides

### 🔧 Infrastructure Git
- [x] **Branche `develop`** créée avec tous les fichiers
- [x] **2 commits** sur develop
- [x] **Remote origin** préconfiguré
- [x] **GitHub CLI** installé (v2.81.0)

---

## ⚠️ CE QUI RESTE À FAIRE (Actions utilisateur requises)

### 📋 Prochaines étapes immédiates

#### 1. Authentification GitHub CLI ⏰ 2 min

```powershell
gh auth login
```

**Suivre les prompts** :
- GitHub.com
- Protocol: HTTPS
- Login with web browser (copier le code one-time)

---

#### 2. Créer le repository GitHub ⏰ 1 min

```powershell
gh repo create biological-qubits-atlas --public `
  --description "Atlas des Qubits Biologiques v1.2 (22 systèmes, 33 colonnes, QC validé)" `
  --source=. --remote=origin --push
```

**Résultat attendu** :
- Repo créé sur `https://github.com/YOUR_USERNAME/biological-qubits-atlas`
- Branche `develop` poussée automatiquement

---

#### 3. Créer branche main ⏰ 1 min

```powershell
git checkout -b main
git push -u origin main
git checkout develop
```

---

#### 4. Activer GitHub Pages ⏰ 1 min

**Via navigateur** :
1. Aller sur : `https://github.com/YOUR_USERNAME/biological-qubits-atlas/settings/pages`
2. **Source** : Sélectionner **"GitHub Actions"**
3. Sauvegarder

---

#### 5. Configurer protection branche main ⏰ 2 min

**Via navigateur** :
1. `https://github.com/YOUR_USERNAME/biological-qubits-atlas/settings/branches`
2. Ajouter règle pour `main` :
   - ✅ Require pull request before merging
   - ✅ Require approvals (1)
   - ✅ Require status checks: `qc`

---

#### 6. Créer Pull Request v1.2 ⏰ 1 min

```powershell
gh pr create --base main --head develop `
  --title "Release v1.2.0 - Publication Quality Dataset" `
  --body-file .github/PULL_REQUEST_TEMPLATE.md
```

---

#### 7. Merger la PR ⏰ 2 min

1. Vérifier CI passe (✅ job `qc`)
2. Approuver la PR
3. Merger

---

#### 8. Créer release v1.2.0 ⏰ 2 min

```powershell
git checkout main
git pull
gh release create v1.2.0 `
  --title "Atlas Biological Qubits v1.2.0" `
  --notes-file CHANGELOG.md `
  biological_qubits.csv QC_REPORT.md v1.2_SUMMARY.md LICENSE CITATION.cff
```

---

#### 9. Créer 4 issues initiales ⏰ 3 min

**Voir `SETUP_INSTRUCTIONS.md`** pour les commandes complètes :
- Issue 1: Add 10 new entries
- Issue 2: Complete provenance to 100%
- Issue 3: Add toxicity data
- Issue 4: Create figures

---

#### 10. Déposer sur Zenodo ⏰ 10 min

1. Connecter GitHub à Zenodo : `https://zenodo.org/account/settings/github/`
2. Activer le repo `biological-qubits-atlas`
3. Déclencher dépôt (automatique après release v1.2.0)
4. Obtenir DOI Zenodo
5. Mettre à jour `CITATION.cff` avec DOI
6. Ajouter badge DOI dans README

---

## 📊 Récapitulatif

### ✅ Complété
- **Dataset** : 22 systèmes, 33 colonnes, 0 erreur
- **Linter** : Python script avec 10 checks
- **Documentation** : 16 fichiers (README, LICENSE, CITATION, guides)
- **CI/CD** : Workflows GitHub Actions prêts
- **Git** : Branche develop avec 2 commits

### ⏳ En attente (actions manuelles)
- **Authentification** : gh auth login
- **Repo GitHub** : création + push
- **GitHub Pages** : activation
- **PR + Merge** : review + merge
- **Release** : v1.2.0 avec assets
- **Zenodo** : dépôt + DOI
- **Issues** : 4 issues initiales

### ⏰ Temps total estimé
- **Setup GitHub** : 15-20 minutes
- **Zenodo** : 10-15 minutes
- **Total** : 25-35 minutes

---

## 🔗 URLs finales (après setup)

Une fois toutes les étapes complétées, vous aurez :

| Resource | URL |
|----------|-----|
| **Repository** | `https://github.com/YOUR_USERNAME/biological-qubits-atlas` |
| **GitHub Pages** | `https://YOUR_USERNAME.github.io/biological-qubits-atlas/` |
| **Releases** | `https://github.com/YOUR_USERNAME/biological-qubits-atlas/releases` |
| **CI Status** | `https://github.com/YOUR_USERNAME/biological-qubits-atlas/actions` |
| **Issues** | `https://github.com/YOUR_USERNAME/biological-qubits-atlas/issues` |
| **Zenodo** | `https://zenodo.org/record/XXXXXX` (après dépôt) |

---

## 📋 Checklist complète

```
[ ] 1. gh auth login
[ ] 2. gh repo create biological-qubits-atlas
[ ] 3. git push origin develop (auto si gh repo create --push)
[ ] 4. Créer branche main et push
[ ] 5. Activer GitHub Pages (Settings → Pages → GitHub Actions)
[ ] 6. Configurer protection main (Settings → Branches)
[ ] 7. gh pr create (develop → main)
[ ] 8. Approuver et merger PR
[ ] 9. gh release create v1.2.0
[ ] 10. Créer 4 issues (gh issue create)
[ ] 11. Activer Discussions (optionnel)
[ ] 12. Connecter Zenodo
[ ] 13. Déposer v1.2.0 sur Zenodo
[ ] 14. Obtenir DOI Zenodo
[ ] 15. Mettre à jour CITATION.cff avec DOI
[ ] 16. Ajouter badge DOI dans README
[ ] 17. Annoncer release (Twitter, Reddit, mailing lists)
```

---

## 🚀 Pour commencer

**Ouvrez `SETUP_INSTRUCTIONS.md`** pour les instructions détaillées pas-à-pas.

**Commencez maintenant** :

```powershell
gh auth login
```

---

**Projet** : Atlas des Qubits Biologiques v1.2  
**Statut** : ✅ Dataset prêt, ⏳ GitHub setup en attente  
**Date** : 22 Octobre 2025

