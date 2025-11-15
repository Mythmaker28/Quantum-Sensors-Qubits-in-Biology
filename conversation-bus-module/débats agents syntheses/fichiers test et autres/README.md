# 🧬 Biological Qubits Atlas

**Atlas complet des systèmes biologiques exploitant la cohérence quantique**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](.) 
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](.)
[![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)](LICENSE)

---

## 📋 Table des Matières

- [Vue d'Ensemble](#-vue-densemble)
- [Systèmes Répertoriés](#-systèmes-répertoriés)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Structure du Projet](#-structure-du-projet)
- [Documentation](#-documentation)
- [Contribuer](#-contribuer)
- [Références](#-références)

---

## 🎯 Vue d'Ensemble

Le **Biological Qubits Atlas** est une base de données scientifique qui catalogue et analyse les systèmes biologiques présentant des phénomènes de **cohérence quantique** et pouvant potentiellement servir de **qubits biologiques**.

### Qu'est-ce qu'un Qubit Biologique?

Un qubit biologique est un système biologique qui:

✅ Maintient une **superposition quantique** d'états
✅ Présente de la **cohérence quantique** mesurable
✅ Fonctionne à **température physiologique** (ou proche)
✅ Est **protégé de la décoherence** par des structures biologiques

### Domaines Couverts

1. **🌿 Photosynthèse** - FMO complex, PSII, PSI
2. **🧭 Magnétoréception** - Cryptochrome, radical pairs
3. **💎 Centres NV** - Nanodiamants en systèmes biologiques
4. **🧬 ADN & Protéines** - Transfert d'électrons, tunneling
5. **👃 Olfaction** - Théorie quantique des odeurs
6. **🦠 Enzymes** - Tunneling protonique/électronique

---

## 📊 Systèmes Répertoriés

### Statistiques

- **Total:** 35+ systèmes biologiques
- **Organismes:** Bactéries, plantes, animaux
- **Températures:** 4K à 310K
- **Temps de cohérence:** 100 fs à 100 μs

### Exemples Majeurs

| Système | Organisme | Type | T₂ | Temp |
|---------|-----------|------|-----|------|
| FMO Complex | *C. tepidum* | Excitonique | 660 fs | 77-300K |
| Cryptochrome | Oiseaux | Radical pair | 1-100 μs | 310K |
| PSII | Plantes | Excitonique | 400 fs | 273-310K |
| DNA | Universel | Électronique | Variable | 310K |

---

## 🚀 Installation

### Prérequis

```bash
# Python 3.8+
python --version

# Git (optionnel)
git --version
```

### Cloner le Repo

```bash
git clone https://github.com/votre-username/biological-qubits-atlas.git
cd biological-qubits-atlas
```

### Installer les Dépendances

```bash
pip install -r requirements.txt
```

**Dépendances:**
- `pandas` - Manipulation de données
- `numpy` - Calculs numériques
- `matplotlib` - Visualisations
- `scipy` - Analyses statistiques

---

## 💻 Utilisation

### 1. Explorer les Données

```python
import pandas as pd

# Charger l'atlas
atlas = pd.read_csv('data/biological_qubits.csv')

# Afficher les systèmes
print(atlas.head())

# Filtrer par catégorie
photosynthesis = atlas[atlas['category'] == 'photosynthesis']
print(f"Systèmes de photosynthèse: {len(photosynthesis)}")
```

### 2. Analyser les Systèmes

```python
from src.atlas_analyzer import BiologicalQubitsAtlas

# Créer l'analyseur
analyzer = BiologicalQubitsAtlas('data/biological_qubits.csv')

# Statistiques
stats = analyzer.get_statistics()
print(stats)

# Grouper par catégorie
by_category = analyzer.group_by_category()
```

### 3. Visualiser

```python
from analysis.stats import plot_coherence_times

# Graphique temps de cohérence vs température
plot_coherence_times()

# Sauvegarde automatique dans viz/
```

### 4. Exporter

```python
# Exporter en JSON
analyzer.to_json('output/atlas.json')

# Exporter en Markdown
analyzer.to_markdown('output/atlas.md')
```

---

## 📁 Structure du Projet

```
biological-qubits-atlas/
│
├── data/                          # Données brutes
│   ├── biological_qubits.csv      # Dataset principal
│   └── references.bib             # Références bibliographiques
│
├── src/                           # Code source
│   ├── atlas_analyzer.py          # Analyseur principal
│   ├── database.py                # Interface base de données
│   └── parsers.py                 # Parsers de données
│
├── docs/                          # Documentation scientifique
│   ├── photosynthesis.md          # Systèmes photosynthétiques
│   ├── magnetoreception.md        # Magnétoréception aviaire
│   ├── nv_centers.md              # Centres NV dans diamants
│   └── dna_proteins.md            # ADN et protéines
│
├── analysis/                      # Scripts d'analyse
│   ├── stats.py                   # Analyses statistiques
│   └── correlations.py            # Corrélations
│
├── viz/                           # Visualisations
│   ├── plot_systems.py            # Graphiques systèmes
│   └── coherence_plots.py         # Graphiques cohérence
│
├── tests/                         # Tests unitaires
│   └── test_analyzer.py
│
├── README.md                      # Ce fichier
├── requirements.txt               # Dépendances Python
└── LICENSE                        # Licence MIT
```

---

## 📚 Documentation

### Documentation Scientifique

- **[Photosynthèse Quantique](docs/photosynthesis.md)** - FMO, PSII, PSI, LH2
- **[Magnétoréception](docs/magnetoreception.md)** - Cryptochrome, oiseaux migrateurs
- **[Centres NV](docs/nv_centers.md)** - Nanodiamants biologiques
- **[ADN & Protéines](docs/dna_proteins.md)** - Transfert quantique

### Guides

- **[Guide d'Installation](docs/INSTALL.md)**
- **[Guide de Contribution](CONTRIBUTING.md)**
- **[API Documentation](docs/API.md)**

---

## 🤝 Contribuer

Nous accueillons les contributions! Voici comment:

### 1. Ajouter un Système

```csv
# Ajouter une ligne dans data/biological_qubits.csv
FMO Complex,Chlorobium tepidum,photosynthesis,exciton,810,660e-15,77-300,doi:10.1038/nature05678
```

### 2. Soumettre une Pull Request

```bash
# Fork le repo
git checkout -b feature/nouveau-systeme

# Faire vos changements
git commit -m "Ajout système X"

# Push
git push origin feature/nouveau-systeme

# Créer PR sur GitHub
```

### 3. Proposer une Amélioration

Ouvrez une [Issue](https://github.com/votre-username/biological-qubits-atlas/issues) avec:

- Description du problème/amélioration
- Références scientifiques (si applicable)
- Exemple de code (si applicable)

---

## 🔬 Critères d'Inclusion

Pour qu'un système soit inclus dans l'atlas:

✅ **Preuve expérimentale** de cohérence quantique
✅ **Publication peer-reviewed** (journal reconnu)
✅ **Temps de cohérence mesurable** (>10 fs)
✅ **Température physiologique** OU démonstration à basse température
✅ **Reproductibilité** (multiple labs si possible)

---

## 📖 Références Clés

### Revues Majeures

1. **Lambert, N. et al. (2013).** "Quantum biology." *Nature Physics* 9, 10-18.
2. **Scholes, G. D. et al. (2017).** "Using coherence to enhance function in chemical and biophysical systems." *Nature* 543, 647-656.
3. **Hore, P. J. & Mouritsen, H. (2016).** "The radical-pair mechanism of magnetoreception." *Annu. Rev. Biophys.* 45, 299-344.

### Livres

- **Quantum Biology** - McFadden & Al-Khalili (2014)
- **Life on the Edge** - McFadden & Al-Khalili (2015)

### Bases de Données

- [RCSB Protein Data Bank](https://www.rcsb.org/)
- [arXiv Quantum Biology](https://arxiv.org/list/q-bio.QM/recent)

---

## 🏆 Laboratoires Actifs

- **Graham Fleming Lab** (UC Berkeley) - Photosynthèse
- **Gregory Scholes Lab** (Princeton) - Cohérence quantique
- **Henrik Mouritsen Lab** (Oldenburg) - Magnétoréception
- **Peter Hore Lab** (Oxford) - Radical pairs
- **Alexandra Olaya-Castro Lab** (UCL) - Biologie quantique théorique

---

## 📜 License

Ce projet est sous licence **MIT** - voir [LICENSE](LICENSE) pour détails.

**Vous êtes libre de:**

✅ Utiliser commercialement
✅ Modifier
✅ Distribuer
✅ Utiliser en privé

**Conditions:**

📋 Inclure la licence et copyright
📋 Pas de garantie

---

## 📧 Contact

- **Email:** biological.qubits@example.com
- **GitHub:** [@biological-qubits-atlas](https://github.com/biological-qubits-atlas)
- **Twitter:** [@BioQubitsAtlas](https://twitter.com/BioQubitsAtlas)

---

## 🌟 Citation

Si vous utilisez cet atlas dans vos recherches, merci de citer:

```bibtex
@misc{biological_qubits_atlas_2025,
  title={Biological Qubits Atlas: Comprehensive Database of Quantum Coherence in Biological Systems},
  author={Your Team},
  year={2025},
  publisher={GitHub},
  url={https://github.com/your-username/biological-qubits-atlas}
}
```

---

## 🚀 Roadmap

### Version 1.1 (Q1 2026)

- [ ] +20 systèmes nouveaux
- [ ] Interface web interactive
- [ ] API REST
- [ ] Intégration bases de données externes

### Version 2.0 (Q3 2026)

- [ ] Machine learning pour prédire T₂
- [ ] Simulations quantiques
- [ ] Benchmarks standardisés
- [ ] Plateforme collaborative

---

## 🙏 Remerciements

Merci à:

- La communauté de biologie quantique
- Les laboratoires ayant publié les données
- Les contributeurs open-source
- Les reviewers et testeurs

---

## ⚡ Quick Start

```bash
# Clone
git clone https://github.com/your-username/biological-qubits-atlas.git

# Install
cd biological-qubits-atlas
pip install -r requirements.txt

# Explore
python
>>> from src.atlas_analyzer import BiologicalQubitsAtlas
>>> atlas = BiologicalQubitsAtlas('data/biological_qubits.csv')
>>> atlas.summary()

# Done! 🎉
```

---

**Explorez le monde fascinant de la biologie quantique! 🧬⚛️**

*Dernière mise à jour: 2025-11-15*
