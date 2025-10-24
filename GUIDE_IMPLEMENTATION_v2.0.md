# 🚀 Guide d'Implémentation — Atlas v2.0

Ce guide vous accompagne dans l'implémentation des 5 améliorations prioritaires.

---

## 📋 Prérequis

### Dépendances Python

```bash
# Installation complète
pip install pandas numpy requests PyYAML
pip install torch torch-geometric  # Pour ML (optionnel)
pip install rdkit scikit-learn     # Pour ML (optionnel)
pip install biopython              # Pour extraction PDB (optionnel)
```

### Clés API Nécessaires

1. **NCBI E-utilities** (gratuit, requis pour PubMed)
   - Inscription : https://www.ncbi.nlm.nih.gov/account/
   - Génération clé : https://www.ncbi.nlm.nih.gov/account/settings/

2. **FPbase** (optionnel, API publique)
   - Pas de clé requise pour accès basique

### Configuration

Créez un fichier `.env` à la racine :

```bash
NCBI_API_KEY=votre_cle_ncbi
NCBI_EMAIL=votre@email.com
FPBASE_API_KEY=  # Optionnel
```

---

## 🎯 Phase 1 : Quick Wins (Semaine 1-4)

### ✅ Semaine 1: Métadonnées FAIR

**Effort** : 1-2 jours  
**Impact** : Immédiat (indexation Google Dataset Search)

```bash
# Génération métadonnées
python scripts/fair/generate_fair_metadata.py

# Vérification
ls -lh metadata/fair/
# Doit contenir:
# - schema_org.json
# - datacite.xml
# - dcat.json
```

**Intégration dans README.md** :

```html
<!-- Ajouter dans <head> de index.html -->
<script type="application/ld+json">
  <!-- Copier contenu de metadata/fair/schema_org.json -->
</script>
```

**DOI Zenodo** :

1. Aller sur https://zenodo.org/
2. Upload → New upload
3. Copier `metadata/fair/datacite.xml` dans les métadonnées
4. Publier → Récupérer DOI
5. Mettre à jour tous les fichiers avec le nouveau DOI

---

### ✅ Semaine 2-3: Dashboard Interactif D3.js

**Effort** : 5-7 jours  
**Impact** : Adoption facilitée, viralité

```bash
# Génération dashboard
python scripts/web/generate_interactive_dashboard.py

# Test local
python -m http.server 8000
# Ouvrir http://localhost:8000/index_v2_interactive.html
```

**Personnalisation** :

- Modifier couleurs dans `<style>` (ligne 20-30)
- Ajouter familles dans légende (ligne 350)
- Ajuster tailles graphiques (variables `width`, `height`)

**Déploiement GitHub Pages** :

```bash
# Copier dashboard vers racine
cp index_v2_interactive.html index.html

# Commit
git add index.html
git commit -m "feat(web): Dashboard interactif D3.js v2.0"
git push origin main

# Activer GitHub Pages
# Settings → Pages → Source: main branch
```

---

### ✅ Semaine 4: Validation In Vivo

**Effort** : 3-4 jours  
**Impact** : Crédibilité accrue

```bash
# Génération rapport
python scripts/qa/in_vivo_validator.py

# Vérification
cat reports/IN_VIVO_VALIDATION.md

# Intégration dans pipeline CI/CD
# Ajouter dans .github/workflows/ci.yml :
# - name: In vivo validation
#   run: python scripts/qa/in_vivo_validator.py
```

**Amélioration manuelle** :

1. Réviser systèmes score < 50
2. Compléter champ `context` avec organisme explicite
3. Relancer validation

---

## 🔬 Phase 2 : Expansion (Semaine 5-12)

### 🔄 Semaine 5-8: Pipeline Auto-Harvest

**Effort** : 4 semaines  
**Impact** : +120 systèmes

```bash
# Configuration
export NCBI_API_KEY="votre_cle"
export NCBI_EMAIL="votre@email.com"

# Lancement extraction
python scripts/automation/auto_harvest_v2.py

# Résultat : data/interim/auto_harvest_v2.csv
```

**Validation manuelle (CRUCIAL)** :

```bash
# 1. Révision experts (20% échantillon)
head -n 25 data/interim/auto_harvest_v2.csv

# 2. Validation linter
python qubits_linter.py data/interim/auto_harvest_v2.csv

# 3. Merge sélectif
# NE PAS fusionner automatiquement!
# Réviser ligne par ligne
```

**Amélioration patterns NLP** :

Éditer `scripts/automation/auto_harvest_v2.py`, ligne 120 :

```python
# Ajouter patterns spécifiques à votre domaine
t2_patterns = [
    r'T[_\s]?2[_\s]*[=:≈~]\s*([0-9.]+)\s*(µs|us|μs)',
    # NOUVEAU: Pattern pour figures
    r'Figure\s+\d+[A-Z]?[:\s]+T2\s*=\s*([0-9.]+)\s*(µs|ms)',
]
```

---

### 🔄 Semaine 9-12: Curation 150 → 200 systèmes

**Plan de curation** :

| Semaine | Cible | Familles Prioritaires |
|---------|-------|----------------------|
| 9 | +20 systèmes | Calcium (GCaMP variants) |
| 10 | +20 systèmes | Voltage (ASAP, Archon) |
| 11 | +20 systèmes | Dopamine, Serotonin |
| 12 | +20 systèmes | Métabolique (ATP, pH) |

**Workflow par système** :

1. Identifier DOI publication
2. Extraire métriques (T2, contraste, température)
3. Vérifier licence (CC BY/CC0 requis)
4. Ajouter ligne CSV
5. Valider linter

---

## 🧠 Phase 3 : Innovation ML (Semaine 13-24)

### 🚧 Semaine 13-16: Collecte Features

**Objectif** : Enrichir atlas avec SMILES/PDB

```bash
# Extraction PDB depuis Uniprot
python scripts/etl/fetch_uniprot_bulk.py

# Résultat : data/raw/external/uniprot/
```

**Conversion chromophore → SMILES** :

Utiliser RDKit ou extraction manuelle depuis littérature.

---

### 🚧 Semaine 17-24: Entraînement GNN

```bash
# Entraînement modèle
python scripts/ml/predict_quantum_proxies.py

# Monitoring (tensorboard optionnel)
tensorboard --logdir=logs/

# Export modèle
# Résultat : models/quantum_proxy_gnn.pth
```

**Optimisation hyperparamètres** :

```python
# Éditer scripts/ml/predict_quantum_proxies.py
hidden_dim = 128  # Tester 64, 128, 256
learning_rate = 0.001  # Tester 0.0001, 0.001, 0.01
```

**Validation externe** :

Tester sur systèmes récents (2024-2025) non inclus dans training set.

---

## 📊 Métriques de Succès

### KPIs à Suivre

| Métrique | Baseline (v1.3) | Cible v2.0 | Outil |
|----------|-----------------|------------|-------|
| **Total systèmes** | 80 | 200+ | CSV count |
| **Avec contraste mesuré** | 65 | 150+ | Filtrage CSV |
| **Validés in vivo** | 30% | 60%+ | in_vivo_validator.py |
| **Familles (≥5 systèmes)** | 5 | 12+ | Analyse pandas |
| **Citations/an** | ~50 | 200+ | Google Scholar |
| **Visites web** | ~500 | 10K+ | Google Analytics |

### Rapports Mensuels

```bash
# Génération rapport automatique
python scripts/reports/generate_monthly_report.py

# Contenu:
# - Nouveaux systèmes ajoutés
# - Familles couvertes
# - Métriques FAIR
# - Citations détectées (Google Scholar API)
```

---

## 🐛 Troubleshooting

### Erreur: "NCBI API rate limit"

**Solution** :
```python
# Augmenter délai dans auto_harvest_v2.py, ligne 95
time.sleep(0.5)  # Au lieu de 0.34
```

### Erreur: "FPbase GraphQL timeout"

**Solution** :
```python
# Réduire limite requête, ligne 180
query($family: String) {
  proteins(family: $family, limit: 50) {  # Au lieu de 200
```

### Erreur GNN: "CUDA out of memory"

**Solution** :
```python
# Réduire batch size, ligne 240
train_loader = DataLoader(train_graphs, batch_size=8)  # Au lieu de 16
```

---

## 📧 Support

- **Issues GitHub** : https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/issues
- **Discussions** : Label `[v2.0]` pour questions liées aux améliorations

---

## 📚 Ressources Complémentaires

### Tutoriels

- **D3.js** : https://observablehq.com/@d3/gallery
- **PyTorch Geometric** : https://pytorch-geometric.readthedocs.io/
- **FAIR Principles** : https://www.go-fair.org/fair-principles/

### Datasets Externes

- **FPbase** : https://www.fpbase.org/
- **PDB** : https://www.rcsb.org/
- **UniProt** : https://www.uniprot.org/

---

**Bonne implémentation ! 🚀**


