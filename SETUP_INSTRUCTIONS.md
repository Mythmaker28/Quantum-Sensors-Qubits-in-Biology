# 🚀 Instructions de Setup — ACTIONS REQUISES

## ✅ État actuel

- [x] GitHub CLI installé (v2.81.0) ✅
- [x] Branche `develop` créée avec tous les fichiers
- [x] `index.html` créé (renommé depuis biological_qubits.html)
- [x] Workflows CI/CD configurés
- [x] Templates issues/PR créés
- [x] Commit initial fait

## ⚠️ ACTION IMMÉDIATE REQUISE

### 1. Authentifier GitHub CLI

**Exécutez dans PowerShell** :

```powershell
gh auth login
```

**Suivez les prompts** :
1. Choisir **GitHub.com**
2. Protocole : **HTTPS** (recommandé)
3. Authentification : **Login with a web browser** (plus simple)
4. Copier le code one-time affiché
5. Appuyer Enter pour ouvrir le navigateur
6. Coller le code et autoriser GitHub CLI

**Vérifier l'authentification** :

```powershell
gh auth status
```

Vous devriez voir : `✓ Logged in to github.com as YOUR_USERNAME`

---

### 2. Créer le repository GitHub

**Une fois authentifié, exécutez** :

```powershell
gh repo create biological-qubits-atlas --public `
  --description "Atlas des Qubits Biologiques : Dataset structuré des systèmes quantiques en contexte biologique (v1.2 - 22 systèmes, 33 colonnes, QC validé)" `
  --source=. --remote=origin --push
```

**Cela va** :
- Créer un repo public `biological-qubits-atlas` sur GitHub
- Ajouter le remote `origin`
- Pousser la branche `develop` automatiquement

---

### 3. Créer et pousser la branche main

```powershell
git checkout -b main
git push -u origin main
git checkout develop
```

---

### 4. Activer GitHub Pages

**Via navigateur** :

1. Aller sur : `https://github.com/YOUR_USERNAME/biological-qubits-atlas/settings/pages`
2. **Source** : Sélectionner **"GitHub Actions"**
3. Sauvegarder

**Pages sera déployé automatiquement** lors du prochain push sur `main`

---

### 5. Configurer les protections de branche main

**Via navigateur** :

1. Aller sur : `https://github.com/YOUR_USERNAME/biological-qubits-atlas/settings/branches`
2. **Ajouter une règle** pour `main`
3. Cocher :
   - ✅ Require pull request before merging
   - ✅ Require approvals (1 minimum)
   - ✅ Require status checks to pass : `qc`
4. Sauvegarder

---

### 6. Créer la Pull Request v1.2

**Exécuter** :

```powershell
gh pr create --base main --head develop `
  --title "Release v1.2.0 - Publication Quality Dataset" `
  --body "## 🎉 Version 1.2.0 - Qualité Publication

### ✨ Nouveautés
- 10 colonnes provenance/incertitudes/flags
- 0 erreur bloquante (QC validé)
- Linter automatique intégré
- LICENSE CC BY 4.0 + CITATION.cff
- CI/CD GitHub Actions
- GitHub Pages configuré

### 📊 Dataset
- 22 systèmes (4 classes: A/B/C/D)
- 33 colonnes (vs 23 en v1.1)
- 14 entrées vérifiées (64%)
- 100% DOI valides

### 🔍 Quality Control
\`\`\`
python qubits_linter.py
→ 0 errors ✅
→ 3 warnings (non bloquants)
→ 22 systems OK
\`\`\`

### ✅ Checklist
- [x] 0 erreur lint
- [x] Tous DOI valides
- [x] Documentation complète
- [x] CI/Pages configurés
- [ ] 1 review approuvée (requis)
"
```

---

### 7. Approuver et merger la PR

1. **Vérifier la PR** sur GitHub
2. **Vérifier que CI passe** (job `qc` doit être ✅)
3. **Approuver la PR** (bouton "Review changes" → "Approve")
4. **Merger** (bouton "Merge pull request")

---

### 8. Créer la release v1.2.0

**Après merge de la PR, exécuter** :

```powershell
git checkout main
git pull origin main

gh release create v1.2.0 `
  --title "Atlas Biological Qubits v1.2.0" `
  --notes-file CHANGELOG.md `
  biological_qubits.csv `
  QC_REPORT.md `
  v1.2_SUMMARY.md `
  LICENSE `
  CITATION.cff
```

**Cela va** :
- Créer un tag Git `v1.2.0`
- Créer une release GitHub avec :
  - Notes de version (depuis CHANGELOG.md)
  - Assets téléchargeables (CSV, QC_REPORT, etc.)

---

### 9. Activer Discussions (optionnel)

1. Aller sur : `https://github.com/YOUR_USERNAME/biological-qubits-atlas/settings`
2. Section **Features** → Cocher **Discussions**
3. Créer catégories :
   - General
   - Q&A
   - Data Contributions
   - Feature Requests

---

### 10. Créer les 4 issues initiales

**Issue 1 : Add 10 new entries**

```powershell
gh issue create `
  --title "Add 10 new entries (priority NV/SiC in vivo)" `
  --body "**Objectif** : Enrichir le dataset avec 10 nouvelles entrées

**Priorités** :
- [ ] 5 systèmes NV nanodiamants in vivo (2023-2025)
- [ ] 3 systèmes SiC (3C-SiC, 6H-SiC)
- [ ] 2 systèmes classe A (qubits protéiques)

**Target** : v1.3 (Nov-Déc 2025)" `
  --label "enhancement,data-entry,priority-high"
```

**Issue 2 : Complete provenance coverage**

```powershell
gh issue create `
  --title "Complete provenance coverage to 100%" `
  --body "**État actuel** :
- Source_T2: 86% (19/22)
- Source_T1: 100% (9/9 NMR)
- Source_Contraste: 89% (16/18 ODMR/ESR)

**À faire** :
- [ ] Compléter Source_T2 (3 systèmes)
- [ ] Compléter Source_Contraste (2 systèmes)

**Target** : v1.3" `
  --label "documentation,quality-improvement"
```

**Issue 3 : Add toxicity data**

```powershell
gh issue create `
  --title "Add toxicity data & flags for B-class entries" `
  --body "**Objectif** : Enrichir données toxicité classe B

**À faire** :
- [ ] Chercher études cytotoxicité (6 systèmes)
- [ ] Compléter Toxicity_note (doses, durées)
- [ ] Vérifier Cytotox_flag pour NV/SiC

**Target** : v1.3" `
  --label "data-entry,class-B"
```

**Issue 4 : Create figures**

```powershell
gh issue create `
  --title "Figures: T2 vs Temp, Timeline" `
  --body "**Graphiques à créer** :
- [ ] T2 vs Température (K) par classe
- [ ] Timeline publications (2006-2025)
- [ ] Distribution méthodes (pie chart)
- [ ] In vivo vs in vitro (bar chart)

**Technologie** : Plotly.js dans index.html

**Target** : v1.3" `
  --label "enhancement,visualization"
```

---

## ✅ Checklist finale

- [ ] 1. GitHub CLI authentifié : `gh auth login`
- [ ] 2. Repo créé : `gh repo create biological-qubits-atlas`
- [ ] 3. Branche `main` créée et poussée
- [ ] 4. GitHub Pages activé (Settings → Pages → GitHub Actions)
- [ ] 5. Protection branche `main` configurée
- [ ] 6. PR v1.2 créée : `gh pr create`
- [ ] 7. PR mergée (après CI ✅ et review)
- [ ] 8. Release v1.2.0 créée : `gh release create`
- [ ] 9. Discussions activées (optionnel)
- [ ] 10. 4 issues créées

---

## 🔗 URLs attendues

Après setup complet :

- **Repository** : `https://github.com/YOUR_USERNAME/biological-qubits-atlas`
- **GitHub Pages** : `https://YOUR_USERNAME.github.io/biological-qubits-atlas/`
- **PR v1.2** : Lien affiché après `gh pr create`
- **Release** : `https://github.com/YOUR_USERNAME/biological-qubits-atlas/releases/tag/v1.2.0`
- **CI Status** : `https://github.com/YOUR_USERNAME/biological-qubits-atlas/actions`

---

## 🆘 En cas de problème

**Si erreur "not authorized"** :
```powershell
gh auth refresh
```

**Si erreur remote** :
```powershell
git remote -v  # Vérifier remotes
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/biological-qubits-atlas.git
```

**Si CI ne démarre pas** :
- Vérifier que `.github/workflows/ci.yml` existe
- Push un commit vide : `git commit --allow-empty -m "trigger CI" && git push`

**Si Pages ne se déploie pas** :
- Vérifier Settings → Pages → Source = "GitHub Actions"
- Vérifier que workflow `pages.yml` existe
- Push sur `main` : `git push origin main`

---

**Temps estimé** : 15-20 minutes pour tout le setup

**Prêt ? Commencez par étape 1 : `gh auth login` 🚀**

