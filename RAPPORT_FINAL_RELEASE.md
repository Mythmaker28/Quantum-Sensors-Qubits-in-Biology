# 🎯 RAPPORT FINAL - Publication Release v1.2.0

**Date** : 2025-10-23  
**Repository** : Mythmaker28/biological-qubits-atlas  
**Rôle** : Release Engineer & SRE

---

## ✅ ÉTAT DES LIEUX (Vérifié)

### Dataset
- ✅ **biological_qubits.csv** : **27 lignes** (26 entrées + en-tête) ✓
- ✅ **QC_REPORT.md** : Présent, 26 systèmes analysés, 0 erreurs
- ✅ **Figures** : Régénérées (T2 vs Temp, Timeline)
- ✅ **RELEASE_NOTES_v1.2.0.md** : Présent

### Git & Branches
- ✅ **Tag v1.2.0** : Créé et poussé
- ✅ **Branches mergées** : `chore/zenodo-metadata`, `feat/data-v1.2-extended`
- ✅ **Branche active** : `infra/pages+governance`

### Fichiers Infrastructure
- ✅ **zenodo.json** : Présent avec métadonnées complètes
- ✅ **CITATION.cff** : Présent (DOI placeholder)
- ✅ **LICENSE** : CC BY 4.0
- ✅ **index.html** : Interface web présente

---

## 🔲 ACTIONS REQUISES (Sans Token GitHub)

### ⚠️ PROBLÈME : API GitHub nécessite authentification

Les opérations suivantes **nécessitent un token GitHub** avec scope `repo` :
- Créer/modifier une release GitHub
- Merger des PRs
- Modifier des workflows

**Solution** : Instructions manuelles ci-dessous.

---

## 📋 INSTRUCTIONS MANUELLES (3 Étapes Critiques)

### ÉTAPE 1 : Créer la Release GitHub ⚡ PRIORITÉ MAX

**Pourquoi** : C'est cette action qui déclenche l'intégration Zenodo automatique.

**Action** :

1. **Aller sur** : https://github.com/Mythmaker28/biological-qubits-atlas/releases/new

2. **Remplir le formulaire** :
   ```
   Tag version: v1.2.0  (sélectionner le tag existant)
   Release title: Biological Qubits Atlas v1.2.0
   Target: infra/pages+governance  (ou main si mergé)
   
   Description: [Copier-coller le contenu de RELEASE_NOTES_v1.2.0.md]
   ```

3. **Attacher les assets** (glisser-déposer) :
   - `biological_qubits.csv` (26 entrées)
   - `QC_REPORT.md`
   - `LICENSE`
   - `CITATION.cff`
   - `RELEASE_NOTES_v1.2.0.md`

4. **Publier** : Cliquer **"Publish release"**

5. **URL finale** : https://github.com/Mythmaker28/biological-qubits-atlas/releases/tag/v1.2.0

---

### ÉTAPE 2 : Récupérer le DOI Zenodo ⏱️ Attendre 2-10 minutes

**Action après publication de la release** :

1. **Attendre 2-5 minutes** que Zenodo détecte la release

2. **Vérifier l'intégration** :
   - Aller sur : https://zenodo.org/account/settings/github/
   - Chercher `biological-qubits-atlas` dans la liste
   - Si absent : cliquer **"Sync now"** puis activer le toggle

3. **Récupérer les DOIs** :
   - Le repository devrait apparaître avec un badge DOI
   - Cliquer sur le DOI pour accéder à la page Zenodo
   - **Noter 2 DOIs** :
     * **Concept DOI** (permanent, pour badge) : `10.5281/zenodo.XXXXXXX`
     * **Version DOI** (v1.2.0 spécifique) : `10.5281/zenodo.XXXXXXX+1`

4. **Si pas d'intégration Zenodo** :
   - Aller sur : https://zenodo.org/deposit/new
   - Upload manuel : CSV, README, LICENSE, CITATION.cff
   - Utiliser `zenodo.json` pour les métadonnées
   - Publier et récupérer le DOI

---

### ÉTAPE 3 : Mettre à Jour le Badge DOI 🏷️

**Après avoir récupéré le DOI réel** :

```powershell
cd "C:\Users\tommy\Documents\tableau proteine fluo"
git checkout infra/pages+governance
git pull origin infra/pages+governance
```

**Éditer `README.md`** :
```markdown
# Ligne 3, remplacer
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXX)

# Par (exemple si DOI = 10.5281/zenodo.1234567)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1234567.svg)](https://doi.org/10.5281/zenodo.1234567)
```

**Éditer `CITATION.cff`** :
```yaml
# Ligne 10, remplacer
doi: 10.5281/zenodo.XXXXXX

# Par
doi: 10.5281/zenodo.1234567
```

```powershell
git add README.md CITATION.cff
git commit -m "docs(doi): add real Zenodo DOI badge"
git push origin infra/pages+governance
```

---

## 🌐 GITHUB PAGES - État et Corrections

### État Actuel
- ✅ **Site accessible** : https://mythmaker28.github.io/biological-qubits-atlas/
- ⚠️ **Version affichée** : Ancienne (21 entrées au lieu de 26)
- ✅ **CSV accessible** : https://mythmaker28.github.io/biological-qubits-atlas/biological_qubits.csv

### Cause
Le workflow Pages n'a pas redéployé après les derniers commits.

### Solution A : Redéploiement Automatique (Recommandé)

**Forcer un redéploiement** :

```powershell
cd "C:\Users\tommy\Documents\tableau proteine fluo"
git checkout infra/pages+governance
git commit --allow-empty -m "chore: trigger Pages redeploy for v1.2.0"
git push origin infra/pages+governance
```

Attendre 2-3 minutes, puis vérifier : https://mythmaker28.github.io/biological-qubits-atlas/

### Solution B : Re-run Manuel du Workflow

1. Aller sur : https://github.com/Mythmaker28/biological-qubits-atlas/actions
2. Trouver le workflow **"pages build and deployment"** ou **"Deploy Pages"**
3. Cliquer sur le dernier run
4. Cliquer **"Re-run all jobs"**
5. Attendre 2-3 minutes

### Vérification Post-Déploiement

Ouvrir : https://mythmaker28.github.io/biological-qubits-atlas/

**Dans la console navigateur (F12)** :
```javascript
fetch('biological_qubits.csv')
  .then(r => r.text())
  .then(csv => {
    const lines = csv.trim().split('\n').length;
    console.log(`CSV contient ${lines} lignes (${lines-1} entrées)`);
  });
```

**Résultat attendu** : `CSV contient 27 lignes (26 entrées)`

---

## 🔧 SI LE CSV NE CHARGE TOUJOURS PAS (Cache Busting)

### Problème
Cache navigateur peut afficher l'ancienne version.

### Solution

**Éditer `index.html`** :

Trouver la ligne (environ ligne 723) :
```javascript
const response = await fetch('biological_qubits.csv');
```

Remplacer par :
```javascript
const response = await fetch('biological_qubits.csv?v=' + Date.now());
```

Puis :
```powershell
git add index.html
git commit -m "fix(ui): add cache busting to CSV fetch"
git push origin infra/pages+governance
```

---

## 📊 STATISTIQUES FINALES v1.2.0

| Métrique | Valeur | Statut |
|----------|--------|--------|
| **Total systèmes** | 26 | ✅ Vérifié |
| **Lignes CSV** | 27 (26+1) | ✅ Confirmé |
| **Vérifiés** | 20 (77%) | ✅ QC validé |
| **Erreurs bloquantes** | 0 | ✅ Linter OK |
| **In vivo** | 11 (42%) | ✅ |
| **Provenance T2** | 88% | ✅ |
| **Tag Git** | v1.2.0 | ✅ Poussé |

---

## ✅ CHECKLIST COMPLÈTE

### Préparation (COMPLÉTÉ)
- [x] Dataset étendu à 26 systèmes
- [x] Linter validé (0 erreurs)
- [x] QC_REPORT.md régénéré
- [x] Figures régénérées
- [x] zenodo.json créé
- [x] RELEASE_NOTES_v1.2.0.md créé
- [x] README.md mis à jour (badge placeholder)
- [x] Tag v1.2.0 créé et poussé

### Publication (ACTIONS MANUELLES REQUISES)
- [ ] **Release GitHub créée** → https://github.com/Mythmaker28/biological-qubits-atlas/releases/new
- [ ] **DOI Zenodo récupéré** → https://zenodo.org/account/settings/github/
- [ ] **Badge DOI mis à jour** (README + CITATION.cff)
- [ ] **GitHub Pages redéployé** (26 entrées visibles)

---

## 🎯 COMMANDES DE VÉRIFICATION

### Vérifier le nombre d'entrées CSV local
```powershell
(Get-Content biological_qubits.csv | Measure-Object -Line).Lines
# Résultat attendu : 27
```

### Vérifier le CSV en ligne (après déploiement)
```powershell
Invoke-WebRequest https://mythmaker28.github.io/biological-qubits-atlas/biological_qubits.csv | Select-Object -ExpandProperty Content | Measure-Object -Line
# Résultat attendu : 27
```

### Vérifier le tag Git
```powershell
git tag -l "v1.2.0"
git show v1.2.0 --stat
```

---

## 🔗 LIENS RAPIDES

### GitHub
- **Repository** : https://github.com/Mythmaker28/biological-qubits-atlas
- **Créer Release** : https://github.com/Mythmaker28/biological-qubits-atlas/releases/new
- **Tag v1.2.0** : https://github.com/Mythmaker28/biological-qubits-atlas/tree/v1.2.0
- **Actions** : https://github.com/Mythmaker28/biological-qubits-atlas/actions
- **Settings Pages** : https://github.com/Mythmaker28/biological-qubits-atlas/settings/pages

### Zenodo
- **GitHub Integration** : https://zenodo.org/account/settings/github/
- **My Uploads** : https://zenodo.org/deposit
- **New Upload** : https://zenodo.org/deposit/new

### Live
- **Site** : https://mythmaker28.github.io/biological-qubits-atlas/
- **CSV Direct** : https://mythmaker28.github.io/biological-qubits-atlas/biological_qubits.csv

---

## 💡 ALTERNATIVE : Script PowerShell Automatisé

Si vous avez un token GitHub, voici un script PowerShell complet :

```powershell
# Définir le token (scope: repo)
$TOKEN = "ghp_VOTRE_TOKEN_ICI"

# Créer la release
$headers = @{
    "Authorization" = "Bearer $TOKEN"
    "Accept" = "application/vnd.github+json"
}

$body = Get-Content "RELEASE_NOTES_v1.2.0.md" -Raw

$payload = @{
    tag_name = "v1.2.0"
    name = "Biological Qubits Atlas v1.2.0"
    body = $body
    draft = $false
    prerelease = $false
    target_commitish = "infra/pages+governance"
} | ConvertTo-Json

$release = Invoke-RestMethod -Uri "https://api.github.com/repos/Mythmaker28/biological-qubits-atlas/releases" `
    -Method POST `
    -Headers $headers `
    -Body $payload `
    -ContentType "application/json"

Write-Host "Release creee: $($release.html_url)"
```

---

## 🚨 TROUBLESHOOTING

### Problème : Site Pages affiche 404
**Solution** :
1. Vérifier Settings → Pages → Source = "GitHub Actions"
2. Re-run le workflow Pages
3. Attendre 2-3 minutes

### Problème : CSV affiche ancienne version (21 entrées)
**Solutions** (dans l'ordre) :
1. Vider cache navigateur (Ctrl+F5)
2. Redéployer Pages (commit vide)
3. Ajouter cache busting (voir section dédiée)

### Problème : Zenodo ne génère pas de DOI
**Causes possibles** :
1. Intégration pas activée → Activer sur https://zenodo.org/account/settings/github/
2. Release pas assez récente → Créer v1.2.1
3. Repo privé → Zenodo ne fonctionne que sur repos publics

**Solution fallback** : Upload manuel sur Zenodo

---

## 📅 TIMELINE ESTIMÉE

| Étape | Durée | Cumul |
|-------|-------|-------|
| Créer release GitHub | 2 min | 2 min |
| Zenodo génère DOI | 2-10 min | 12 min |
| Mettre à jour badge DOI | 2 min | 14 min |
| Redéployer Pages | 2-3 min | 17 min |
| **TOTAL** | **~17 minutes** | |

---

## 🎉 CONCLUSION

**État** : ✅ **Prêt pour publication finale**

**Travail automatisé complété** :
- ✅ Dataset finalisé (26 entrées)
- ✅ Tag v1.2.0 créé
- ✅ Documentation complète
- ✅ Infrastructure Zenodo prête

**Actions manuelles nécessaires** (3 étapes, ~17 min) :
1. Créer la release GitHub
2. Récupérer le DOI Zenodo
3. Mettre à jour le badge DOI

**Limitation technique** : L'API GitHub REST nécessite un token d'authentification pour créer des releases. Sans token, ces opérations doivent être effectuées manuellement via l'interface web.

---

**📧 Support** : Voir README.md pour contact mainteneur  
**📊 Version** : v1.2.0  
**📅 Généré** : 2025-10-23  
**🤖 Par** : Release Engineer & SRE Bot



