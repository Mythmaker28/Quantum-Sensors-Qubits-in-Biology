# 🚀 Guide de Configuration GitHub — Biological Qubits Atlas

## ✅ État actuel

- [x] Branche `develop` créée avec tous les fichiers v1.2
- [x] Workflows CI/CD configurés (.github/workflows/)
- [x] Templates issues/PR créés
- [x] `index.html` (renommé depuis biological_qubits.html) ✅
- [x] Commit initial fait sur `develop`

## 📋 Prochaines étapes (ACTION MANUELLE REQUISE)

### 1. Créer le nouveau repository sur GitHub

#### Option A : Via interface web GitHub (recommandé si pas de gh CLI)

1. **Aller sur** : https://github.com/new
2. **Nom du repository** : `biological-qubits-atlas`
3. **Description** : 
   ```
   Atlas des Qubits Biologiques : Dataset structuré des systèmes quantiques en contexte biologique (v1.2 - 22 systèmes, 33 colonnes, QC validé)
   ```
4. **Visibilité** : ✅ **Public**
5. **NE PAS initialiser** avec README, .gitignore ou license (on a déjà tout)
6. **Cliquer "Create repository"**

#### Option B : Via gh CLI (si installé)

```powershell
gh repo create biological-qubits-atlas --public `
  --description "Atlas des Qubits Biologiques v1.2" `
  --source=. --remote=origin --push
```

---

### 2. Changer le remote origin

Après création du repo sur GitHub, exécutez :

```powershell
# Retirer l'ancien remote
git remote remove origin

# Ajouter le nouveau remote
git remote add origin https://github.com/YOUR_USERNAME/biological-qubits-atlas.git

# Vérifier
git remote -v
```

**Remplacez `YOUR_USERNAME`** par votre nom d'utilisateur GitHub

---

### 3. Pousser la branche develop

```powershell
git push -u origin develop
```

---

### 4. Créer la branche main

```powershell
# Créer et pousser main
git checkout -b main
git push -u origin main

# Revenir sur develop
git checkout develop
```

---

### 5. Configurer GitHub Pages

1. **Aller dans** : Settings → Pages (menu gauche)
2. **Source** : Sélectionner **"GitHub Actions"**
3. **Le workflow `.github/workflows/pages.yml` se déclenchera automatiquement lors du prochain push sur `main`**

---

### 6. Configurer les protections de branche main

1. **Aller dans** : Settings → Branches
2. **Ajouter une règle** pour `main` :
   - ✅ **Require pull request before merging**
   - ✅ **Require approvals** (1 minimum)
   - ✅ **Require status checks to pass** : `qc` (nom du job CI)
   - ✅ **Require branches to be up to date before merging**
3. **Sauvegarder**

---

### 7. Activer GitHub Discussions (optionnel)

1. **Aller dans** : Settings → Features
2. **Cocher "Discussions"**
3. **Créer les catégories** :
   - General
   - Q&A
   - Data Contributions
   - Feature Requests

---

### 8. Créer la Pull Request v1.2

```powershell
# Sur la branche develop
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
- Linter: \`python qubits_linter.py\` → 0 errors ✅
- Provenance: 86% T2, 100% T1, 89% Contraste
- Incertitudes: 100% estimées

### 📄 Fichiers clés
- \`biological_qubits.csv\` (dataset principal)
- \`index.html\` (interface web)
- \`qubits_linter.py\` (QC automatique)
- \`LICENSE\`, \`CITATION.cff\`, \`CHANGELOG.md\`

### ✅ Checklist
- [x] 0 erreur lint
- [x] Tous DOI valides
- [x] Documentation complète
- [x] CI/Pages configurés
- [ ] 1 review approuvée (requis)

### 🚀 Après merge
- Tag v1.2.0
- Release GitHub
- Dépôt Zenodo
- Annonce communauté
"
```

**Si pas de gh CLI** : Créer la PR manuellement via l'interface GitHub

---

### 9. Merger la PR et créer la release

Une fois la PR approuvée et mergée :

```powershell
# Basculer sur main et récupérer les changements
git checkout main
git pull origin main

# Créer le tag
git tag -a v1.2.0 -m "Release v1.2.0 - Publication Quality Dataset"
git push origin v1.2.0

# Créer la release GitHub
gh release create v1.2.0 `
  --title "Atlas Biological Qubits v1.2.0" `
  --notes-file CHANGELOG.md `
  biological_qubits.csv `
  QC_REPORT.md `
  v1.2_SUMMARY.md `
  LICENSE `
  CITATION.cff
```

**Si pas de gh CLI** : Créer la release via https://github.com/YOUR_USERNAME/biological-qubits-atlas/releases/new

---

### 10. Créer les issues initiales

#### Issue 1: Add 10 new entries (priority NV/SiC in vivo)
```markdown
**Objectif** : Enrichir le dataset avec 10 nouvelles entrées prioritaires

**Priorité** :
- [ ] 5 systèmes NV nanodiamants in vivo (nouveaux papiers 2023-2025)
- [ ] 3 systèmes SiC (3C-SiC, 6H-SiC variants)
- [ ] 2 systèmes classe A (nouveaux qubits protéiques)

**Labels** : enhancement, data-entry, priority-high
```

#### Issue 2: Complete provenance coverage to 100%
```markdown
**Objectif** : Atteindre 100% provenance sur toutes les valeurs

**État actuel** :
- Source_T2: 86% (19/22)
- Source_T1: 100% (9/9 NMR)
- Source_Contraste: 89% (16/18 ODMR/ESR)

**À faire** :
- [ ] Compléter Source_T2 pour 3 systèmes restants
- [ ] Compléter Source_Contraste pour 2 systèmes ODMR

**Labels** : documentation, quality-improvement
```

#### Issue 3: Add toxicity data & flags for B-class entries
```markdown
**Objectif** : Enrichir données toxicité pour classe B

**À faire** :
- [ ] Chercher études cytotoxicité pour 6 systèmes classe B
- [ ] Compléter Toxicity_note avec doses/durées
- [ ] Vérifier Cytotox_flag pour tous NV/SiC

**Labels** : data-entry, class-B
```

#### Issue 4: Figures - T2 vs Temp, Timeline
```markdown
**Objectif** : Créer visualisations interactives

**Graphiques à créer** :
- [ ] T2 vs Température (K) par classe
- [ ] Timeline publications (2006-2025)
- [ ] Distribution par méthode (ODMR/ESR/NMR)
- [ ] In vivo vs in vitro (pie chart)

**Technologie** : Plotly.js dans index.html

**Labels** : enhancement, visualization
```

---

## 📊 Commandes récapitulatives

```powershell
# 1. Changer remote (après création repo GitHub)
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/biological-qubits-atlas.git

# 2. Pousser develop
git push -u origin develop

# 3. Créer et pousser main
git checkout -b main
git push -u origin main
git checkout develop

# 4. Créer PR (via web ou gh CLI si installé)
# Via web: https://github.com/YOUR_USERNAME/biological-qubits-atlas/compare/main...develop

# 5. Après merge: tag + release
git checkout main
git pull
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin v1.2.0

# 6. Tester CI localement
python qubits_linter.py
```

---

## ✅ Checklist finale

- [ ] Repo créé sur GitHub : `biological-qubits-atlas`
- [ ] Remote origin changé
- [ ] Branch `develop` poussée
- [ ] Branch `main` créée et poussée
- [ ] GitHub Pages activé (Settings → Pages → GitHub Actions)
- [ ] Protection branche `main` configurée
- [ ] PR "v1.2 publication" créée
- [ ] PR mergée (après review)
- [ ] Tag `v1.2.0` créé et poussé
- [ ] Release v1.2.0 créée avec assets
- [ ] 4 issues initiales créées
- [ ] Discussions activées (optionnel)

---

## 🔗 URLs attendues (après setup)

- **Repository** : `https://github.com/YOUR_USERNAME/biological-qubits-atlas`
- **GitHub Pages** : `https://YOUR_USERNAME.github.io/biological-qubits-atlas/`
- **Releases** : `https://github.com/YOUR_USERNAME/biological-qubits-atlas/releases`
- **CI Status** : `https://github.com/YOUR_USERNAME/biological-qubits-atlas/actions`

---

## 🆘 Support

Si vous rencontrez des problèmes :
1. Vérifiez que vous êtes connecté à GitHub : `git config user.name`
2. Vérifiez que vous avez les droits push : testez avec un autre repo
3. Consultez les logs CI : onglet "Actions" sur GitHub

---

**Prêt pour la publication ! 🚀**

