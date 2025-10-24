# 📦 Livraison Paquet bioRxiv — Biological Qubits Atlas

**Date** : 24 octobre 2025  
**Version Atlas** : v1.3.0-beta  
**Statut** : ✅ Prêt pour soumission

---

## ✅ Fichiers Créés (7 fichiers)

### 📄 Manuscrit & Supplément (Markdown → PDF)

| Fichier | Type | Statut | Description |
|---------|------|--------|-------------|
| **BQA_manuscript_bioRxiv.md** | Markdown | ✅ | Source manuscrit complet |
| **BQA_Supplement_bioRxiv.md** | Markdown | ✅ | Source supplément |
| `BQA_manuscript_bioRxiv.pdf` | PDF | 🔄 À générer | Manuscrit final (upload bioRxiv) |
| `BQA_Supplement_bioRxiv.pdf` | PDF | 🔄 À générer | Supplément final (optionnel) |

### 🔧 Scripts & Documentation

| Fichier | Utilité |
|---------|---------|
| **generate_biorxiv_pdfs.py** | Script Python génération PDF (pandoc/weasyprint) |
| **generate_and_validate.bat** | Script Windows automatisé (double-clic) |
| **README_bioRxiv_pack.txt** | Documentation complète (métadonnées, upload, troubleshooting) |
| **QUICK_START.md** | Démarrage rapide (2 minutes) |
| **LIVRAISON_bioRxiv.md** | Ce fichier (récapitulatif) |

---

## 🚀 Génération PDFs (Choisir une méthode)

### Méthode 1 : Script Automatisé ⚡ (Recommandé)

**Windows** :
```batch
cd C:\Users\tommy\Documents\tableau proteine fluo\submission\bioRxiv
generate_and_validate.bat
```

OU double-cliquer sur `generate_and_validate.bat`

**macOS/Linux** :
```bash
python generate_biorxiv_pdfs.py
```

**Prérequis** : Installer pandoc OU weasyprint (voir ci-dessous)

---

### Méthode 2 : Installation Prérequis

#### Option A : Pandoc (Recommandé — meilleur rendu)

**Windows** :
```batch
winget install pandoc
```

**macOS** :
```bash
brew install pandoc
```

**Linux** :
```bash
sudo apt install pandoc texlive-xetex
```

**Vérification** :
```bash
pandoc --version
```

---

#### Option B : Weasyprint (Fallback Python)

```bash
pip install markdown weasyprint
```

**Note** : Weasyprint peut avoir des problèmes avec certaines polices sur Windows. Pandoc est plus fiable.

---

### Méthode 3 : Conversion Manuelle (Experts)

```bash
pandoc BQA_manuscript_bioRxiv.md -o BQA_manuscript_bioRxiv.pdf \
  --pdf-engine=xelatex \
  --variable geometry:margin=1in \
  --variable fontsize=11pt \
  --number-sections

pandoc BQA_Supplement_bioRxiv.md -o BQA_Supplement_bioRxiv.pdf \
  --pdf-engine=xelatex \
  --variable geometry:margin=1in \
  --variable fontsize=11pt
```

---

## 📋 Checklist Conformité bioRxiv

### ✅ Technique

- [ ] PDF s'ouvre correctement (tester avec Adobe Reader)
- [ ] Polices intégrées (vérifier dans propriétés PDF)
- [ ] Section **ABSTRACT** visible en début de manuscrit
- [ ] Figures intégrées (pipeline diagram, table statistiques)
- [ ] Images 300 dpi minimum (diagrammes ASCII OK)
- [ ] Pages format A4 ou Letter
- [ ] Nom fichier sans espaces : `BQA_manuscript_bioRxiv.pdf` ✅
- [ ] Taille < 100 MB (attendu ~1-2 MB)

### ✅ Contenu Scientifique

- [ ] Titre exact : *"Biological Qubits Atlas: a curated, reproducible catalog of quantum-enabled biosensing systems"*
- [ ] Auteur : **Tommy Lepesteur**
- [ ] Affiliation : **Independent researcher, France**
- [ ] ORCID : **0009-0009-0577-9563**
- [ ] Email : **tommy.lepesteur@hotmail.fr**
- [ ] Métriques clés : **80 systèmes total, 65 measured**
- [ ] Lien GitHub cliquable
- [ ] Lien Zenodo présent
- [ ] Competing interests : *"The author declares no competing interests"*

---

## 🌐 Upload sur bioRxiv

### Étapes

1. **Aller sur** : https://www.biorxiv.org/submit-a-manuscript

2. **Login** / Créer compte (gratuit)

3. **New Submission**

4. **Upload Files** :
   - Drag & drop `BQA_manuscript_bioRxiv.pdf` dans "Drop manuscript Files here"
   - [Optionnel] Drag & drop `BQA_Supplement_bioRxiv.pdf` dans "Drop supplemental Files here"

5. **Remplir Métadonnées** :

**Title** :
```
Biological Qubits Atlas: a curated, reproducible catalog of quantum-enabled biosensing systems
```

**Authors** :
```
Name: Tommy Lepesteur
Affiliation: Independent researcher
Country: France
ORCID: 0009-0009-0577-9563
Corresponding: Yes
Email: tommy.lepesteur@hotmail.fr
```

**Category** :
- Primary: **Biophysics**
- Secondary: **Systems Biology** (optionnel)

**Abstract** : (copier depuis manuscrit PDF section ABSTRACT)

**Keywords** :
```
biosensors, fluorescent proteins, quantum biology, calcium indicators, voltage sensors, optical physiology, open data, FAIR principles
```

**External Links** :
```
Code & Data: https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology
Archive: https://doi.org/10.5281/zenodo.17420604
```

**Declarations** :
- **Competing Interests** : The author declares no competing interests.
- **Ethics** : This study involves no research on humans or animals.
- **Data/Code Availability** : All code, curation scripts, and data builds are openly available at the GitHub link above; archived snapshot on Zenodo as cited.

**License** : CC-BY 4.0 (standard bioRxiv)

6. **Preview HTML** : Vérifier que section ABSTRACT est détectée

7. **Submit for Processing**

8. **Attendre email confirmation** (24-48h généralement)

---

## 📊 Métriques Dataset (pour référence)

### v1.3.0-beta

| Métrique | Valeur |
|----------|--------|
| **Total systèmes** | 80 |
| **Mesures (Tier B)** | 65 |
| **Familles** | 17 |
| **DOIs uniques** | 20 |
| **Biosenseurs** | 33 |
| **FPs standards** | 47 |

### Top Familles

| Famille | Count | Exemples |
|---------|-------|----------|
| Calcium | 12 | GCaMP6s, jGCaMP7b, R-GECO1, NIR-GECO2 |
| GFP-like | 8 | EGFP, Clover, mNeonGreen |
| RFP | 6 | TagRFP, FusionRed, Katushka |
| Dopamine | 5 | dLight1.1/1.2/1.3b, GRAB-DA2m/h |
| Voltage | 4 | ASAP2s/3, ArcLight, VSFP-Butterfly |

### Statistiques Contraste

- **Moyenne** : 8.98-fold
- **Médiane** : 1.40-fold
- **Min** : 0.21-fold (background)
- **Max** : 90-fold (outlier)

---

## 🔗 Liens Importants

- **GitHub Repository** : https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology
- **Zenodo Archive** : https://doi.org/10.5281/zenodo.17420604 (v1.2.1 stable)
- **bioRxiv Submit** : https://www.biorxiv.org/submit-a-manuscript

---

## 🆘 Support & Troubleshooting

### Problème: Script génération ne fonctionne pas

**Solutions** :
1. Vérifier Python installé : `python --version` (≥3.8)
2. Installer pandoc : `winget install pandoc`
3. OU installer weasyprint : `pip install markdown weasyprint`
4. Consulter `README_bioRxiv_pack.txt` section "TROUBLESHOOTING"

### Problème: PDF ne s'ouvre pas

**Solutions** :
1. Vérifier avec Adobe Reader (pas seulement Chrome)
2. Regénérer avec pandoc : `pandoc BQA_manuscript_bioRxiv.md -o output.pdf --pdf-engine=xelatex`

### Problème: Section ABSTRACT non détectée par bioRxiv

**Solutions** :
1. Vérifier que `## ABSTRACT` est bien en H2 dans Markdown (déjà correct)
2. Ouvrir PDF et vérifier manuellement que "ABSTRACT" apparaît en titre
3. Si problème persiste, ajouter manuellement dans metadata bioRxiv

---

## 📧 Contact Auteur

**Nom** : Tommy Lepesteur  
**Email** : tommy.lepesteur@hotmail.fr  
**ORCID** : 0009-0009-0577-9563  
**Affiliation** : Independent researcher, France

---

## 📜 Licences

- **Manuscrit (bioRxiv preprint)** : CC BY 4.0
- **Dataset (Atlas CSV)** : CC BY 4.0
- **Code (Scripts)** : MIT License

---

## ✅ Résumé Exécutif

### Ce qui a été livré

1. ✅ **Manuscrit complet** (15-20 pages) : Introduction, Methods, Results, Discussion, References
2. ✅ **Supplément** (10-12 pages) : Schema détaillé, Quality tiers, Evidence examples
3. ✅ **Scripts automatisés** : Génération PDF en 1 clic
4. ✅ **Documentation complète** : README, Quick Start, Troubleshooting

### Prochaines étapes

1. **Générer PDFs** : Lancer `generate_and_validate.bat`
2. **Vérifier** : Ouvrir `BQA_manuscript_bioRxiv.pdf`, contrôler checklist
3. **Upload** : Aller sur bioRxiv, drag & drop, remplir métadonnées
4. **Attendre** : Confirmation email dans 24-48h

### Timeline estimée

- **Génération PDFs** : 2 minutes (si pandoc installé)
- **Vérification** : 10 minutes (lecture manuscrit)
- **Upload bioRxiv** : 15 minutes (remplir formulaire)
- **Total** : ~30 minutes → manuscrit soumis ✅

---

**⚛️ Paquet bioRxiv complet et prêt pour soumission ! 🧬**

📅 Date : 2025-10-24  
✍️ Créé par : Assistant IA expert  
🔬 Pour : Tommy Lepesteur  
📦 Statut : PRÊT ✅


