# 🚀 Instructions de Publication Release v1.2.0

**Statut actuel** : ✅ Tag v1.2.0 créé et poussé sur GitHub

---

## ✅ Étapes Complétées

1. ✅ Branches mergées dans `infra/pages+governance`
   - `chore/zenodo-metadata` (zenodo.json)
   - `feat/data-v1.2-extended` (+5 nouvelles entrées)

2. ✅ zenodo.json ajouté et commité

3. ✅ Tag `v1.2.0` créé et poussé sur GitHub

4. ✅ Documentation complète :
   - RELEASE_NOTES_v1.2.0.md
   - README.md mis à jour avec badge DOI placeholder
   - QC_REPORT.md régénéré (26 systèmes)
   - Figures régénérées

---

## 🔲 Actions Restantes (À FAIRE)

### 1. Créer la Release GitHub (MANUEL)

Comme l'API GitHub nécessite un token d'authentification, vous devez créer la release manuellement :

#### Option A : Via l'interface web (RECOMMANDÉ)

1. Aller sur : https://github.com/Mythmaker28/biological-qubits-atlas/releases/new

2. Remplir le formulaire :
   - **Tag** : `v1.2.0` (sélectionner le tag existant dans le menu déroulant)
   - **Release title** : `Biological Qubits Atlas v1.2.0`
   - **Description** : Copier-coller le contenu de `RELEASE_NOTES_v1.2.0.md`

3. Attacher les assets (optionnel mais recommandé) :
   - `biological_qubits.csv`
   - `QC_REPORT.md`
   - `LICENSE`
   - `CITATION.cff`

4. Cliquer sur **Publish release**

5. URL finale sera : https://github.com/Mythmaker28/biological-qubits-atlas/releases/tag/v1.2.0

#### Option B : Via GitHub CLI (si installé)

```bash
# Si gh CLI est installé et authentifié
cd "C:\Users\tommy\Documents\tableau proteine fluo"

gh release create v1.2.0 \
  --title "Biological Qubits Atlas v1.2.0" \
  --notes-file RELEASE_NOTES_v1.2.0.md \
  biological_qubits.csv \
  QC_REPORT.md \
  LICENSE \
  CITATION.cff
```

#### Option C : Via API avec token

```powershell
# Créer un token GitHub : https://github.com/settings/tokens
# Scope requis : repo

$TOKEN = "votre_token_ici"
$BODY = Get-Content RELEASE_NOTES_v1.2.0.md -Raw

$headers = @{
    "Authorization" = "Bearer $TOKEN"
    "Accept" = "application/vnd.github+json"
}

$payload = @{
    tag_name = "v1.2.0"
    name = "Biological Qubits Atlas v1.2.0"
    body = $BODY
    draft = $false
    prerelease = $false
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://api.github.com/repos/Mythmaker28/biological-qubits-atlas/releases" `
    -Method POST `
    -Headers $headers `
    -Body $payload `
    -ContentType "application/json"
```

---

### 2. Récupérer le DOI Zenodo

Une fois la release GitHub publiée, Zenodo génère automatiquement un DOI (si l'intégration est activée).

#### Vérifier l'intégration Zenodo-GitHub

1. Aller sur : https://zenodo.org/account/settings/github/

2. Vérifier que `Mythmaker28/biological-qubits-atlas` est dans la liste

3. Si absent :
   - Cliquer sur **Sync now** pour synchroniser depuis GitHub
   - Activer le toggle pour `biological-qubits-atlas`

#### Récupérer le DOI (attendre 2-5 minutes après publication release)

1. Actualiser la page Zenodo GitHub : https://zenodo.org/account/settings/github/

2. Le repository devrait apparaître avec un lien **DOI**

3. Cliquer sur le DOI pour accéder à la page Zenodo

4. Récupérer **2 DOIs** :
   - **Concept DOI** (permanent, recommandé pour README) : `10.5281/zenodo.XXXXXXX`
   - **Version DOI** (spécifique v1.2.0) : `10.5281/zenodo.XXXXXXX+1`

#### Fallback si Zenodo n'est pas configuré

1. Aller sur : https://zenodo.org/deposit/new

2. Cliquer sur **Upload** → **Select files**

3. Uploader :
   - `biological_qubits.csv`
   - `README.md`
   - `LICENSE`
   - `CITATION.cff`

4. Remplir les métadonnées :
   - Copier-coller depuis `zenodo.json`
   - Ou depuis `CITATION.cff`

5. Cliquer sur **Publish**

6. Récupérer le DOI

---

### 3. Mettre à Jour le Badge DOI

Une fois le DOI récupéré, remplacer le placeholder dans le README :

```bash
# Exemple si Concept DOI = 10.5281/zenodo.1234567
cd "C:\Users\tommy\Documents\tableau proteine fluo"
git checkout -b docs/add-real-doi
```

Dans `README.md`, remplacer :

```markdown
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXX)
```

Par :

```markdown
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1234567.svg)](https://doi.org/10.5281/zenodo.1234567)
```

Dans `CITATION.cff`, remplacer :

```yaml
doi: 10.5281/zenodo.XXXXXX
```

Par :

```yaml
doi: 10.5281/zenodo.1234567
```

Puis :

```bash
git add README.md CITATION.cff
git commit -m "docs(doi): add real Zenodo DOI badge"
git push origin docs/add-real-doi

# Créer PR puis merger
```

---

### 4. Vérifier GitHub Pages

#### Vérifier que le workflow Pages fonctionne

1. Aller sur : https://github.com/Mythmaker28/biological-qubits-atlas/actions

2. Vérifier que le workflow **pages build and deployment** est ✅ vert

3. Si rouge ❌ :
   - Cliquer sur le workflow en erreur
   - Identifier l'erreur
   - Re-run si temporaire

#### Tester le site live

1. Ouvrir : https://mythmaker28.github.io/biological-qubits-atlas/

2. Vérifier :
   - ✅ Page charge (HTTP 200)
   - ✅ Tableau affiche les données
   - ✅ CSV charge avec ≥26 entrées
   - ✅ Filtres fonctionnent
   - ✅ Export CSV fonctionne

#### Si le site ne charge pas

Vérifier la configuration :

1. Aller sur : https://github.com/Mythmaker28/biological-qubits-atlas/settings/pages

2. Vérifier :
   - **Source** : GitHub Actions (pas "Deploy from a branch")
   - **Custom domain** : vide (ou configuré correctement)

3. Si besoin, réinitialiser :
   - Changer Source vers "Deploy from a branch" → main → /root → Save
   - Puis rechanger vers "GitHub Actions" → Save

---

## 📊 Statistiques Finales v1.2.0

- **26 systèmes** (+5 vs v1.1)
- **20 entrées vérifiées** (77%, +13 points vs v1.1)
- **11 systèmes in vivo** (+3 vs v1.1)
- **0 erreurs bloquantes** (linter validé)
- **33 colonnes** (schéma complet avec provenance)
- **100% DOI valides**
- **88% provenance T2** tracée

---

## 📋 Checklist Finale

- [x] Branches mergées
- [x] Tag v1.2.0 créé et poussé
- [x] zenodo.json présent
- [x] RELEASE_NOTES_v1.2.0.md créé
- [x] README.md avec badge DOI (placeholder)
- [x] QC_REPORT.md régénéré
- [x] Figures régénérées
- [ ] **Release GitHub créée** (MANUEL)
- [ ] **DOI Zenodo récupéré** (après release)
- [ ] **Badge DOI mis à jour** (après DOI)
- [ ] **GitHub Pages vérifié**

---

## 🔗 Liens Utiles

- **Repository** : https://github.com/Mythmaker28/biological-qubits-atlas
- **Releases** : https://github.com/Mythmaker28/biological-qubits-atlas/releases
- **Actions** : https://github.com/Mythmaker28/biological-qubits-atlas/actions
- **Pages Settings** : https://github.com/Mythmaker28/biological-qubits-atlas/settings/pages
- **Zenodo GitHub** : https://zenodo.org/account/settings/github/
- **Site Live** : https://mythmaker28.github.io/biological-qubits-atlas/

---

## ⚠️ Notes Importantes

1. **Ne PAS supprimer les branches** `chore/zenodo-metadata` et `feat/data-v1.2-extended` avant d'avoir vérifié que tout fonctionne

2. **Sauvegarder le DOI** dès qu'il est généré (le noter quelque part)

3. **Vérifier GitHub Pages** après chaque push sur `infra/pages+governance`

4. **Annoncer la release** une fois le DOI ajouté :
   - Twitter/X scientifique
   - Reddit (r/QuantumComputing, r/biophysics)
   - LinkedIn
   - Liste de diffusion de la communauté

---

**📅 Date de préparation** : 2025-10-23  
**🤖 Généré par** : Release Engineer Bot  
**📧 Contact** : Voir README.md pour détails mainteneur






