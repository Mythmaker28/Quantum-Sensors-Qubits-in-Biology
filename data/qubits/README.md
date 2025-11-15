# 🔬 Biological Qubits Dataset

**34 vrais systèmes quantiques** - Qubits et capteurs de spin pour applications biologiques

---

## 🎯 Différence avec le Dataset Principal

### Ce Dataset (`biological_qubits.csv`) - 34 systèmes

**Type :** Vrais **qubits quantiques** et capteurs de spin

**Systèmes inclus :**
- Centres NV dans nanodiamants (Classe B)
- Défauts VSi dans SiC (Classe B) 
- Protéines fluorescentes avec ODMR (Classe A - NOUVEAU!)
- Hyperpolarisation nucléaire ^13C, ^15N (Classe C)
- Paires radicalaires (cryptochrome, photosynthèse) (Classe D)

**Propriétés mesurées :**
- **T₂ (cohérence)** : 0.8 µs - 100 µs
- **Méthode de lecture** : ODMR, NMR, ESR
- **Spin** : Électronique (S=1/2 ou S=1) ou Nucléaire
- **Température** : 4 K - 310 K

**Applications :**
- Magnétométrie quantique cellulaire
- Thermométrie nanométrique 
- Capteurs de champs biologiques

---

### Dataset Principal (`atlas_fp_optical_v2_2_curated.csv`) - 180 systèmes

**Type :** **Protéines fluorescentes** et biosenseurs

**Systèmes inclus :**
- GCaMP, XCaMP (calcium)
- ASAP3, ASAP4e (voltage)
- dLight, GRAB-DA (dopamine)
- iGluSnFR (glutamate)
- Autres biosenseurs (pH, ATP, GABA, etc.)

**Propriétés mesurées :**
- **Contraste** : Δ F/F₀ (fold-change)
- **Spectre** : Excitation/Émission (nm)
- **Température** : 270-320 K (physiologique)
- **Applications** : Imagerie calcium, voltage, neurotransmetteurs

---

## 📊 Comparaison Rapide

| Aspect | biological_qubits.csv | atlas_fp_optical_v2_2_curated.csv |
|--------|----------------------|-----------------------------------|
| **Nombre** | 34 systèmes | 180 systèmes |
| **Type** | Qubits quantiques | Protéines fluorescentes |
| **Lecture** | ODMR, NMR, ESR | Fluorescence optique |
| **Propriété clé** | T₂ (cohérence quantique) | Contraste (ΔF/F₀) |
| **Applications** | Magnétométrie, thermométrie quantique | Imagerie neuronale, biocapteurs |
| **Classes** | A, B, C, D (qubits) | Familles (Calcium, Voltage, etc.) |

---

## 🔬 Classes de Qubits (biological_qubits.csv)

### Classe A : Protéines Fluorescentes avec ODMR
- **3 systèmes**
- Génétiquement encodables
- T₂ ~ 0.8 µs
- Premier "qubit protéique" (2025)

### Classe B : Qubits de Spin Électronique
- **15 systèmes**
- Centres NV, VSi, GeV
- T₂ ~ 0.8-3.2 µs (in cellulo)
- Gold standard pour magnétométrie

### Classe C : Hyperpolarisation Nucléaire
- **12 systèmes**
- ^13C, ^15N
- T₁ = 15-900 s
- FDA-approuvé (pyruvate)

### Classe D : Paires Radicalaires
- **4 systèmes**
- Cryptochrome, photosynthèse
- T₂ < 1 ns
- Magnétoréception aviaire

---

## 📂 Structure

```
data/qubits/
├── biological_qubits.csv       # Dataset principal (34 systèmes)
└── README.md                    # Ce fichier
```

---

## 🔗 Documentation Associée

- **Mécanismes quantiques** : `docs/quantum_mechanisms.md`
- **Centres NV** : `docs/nv_centers_qubits.md`
- **Magnétoréception** : `docs/magnetoreception.md`
- **Photosynthèse** : `docs/photosynthesis.md`

---

## 🛠️ Scripts d'Analyse

- **Validation** : `scripts/qa/validate_qubits_data.py`
- **Statistiques** : `analysis/qubits_stats.py`
- **Comparaisons** : `analysis/qubits_class_comparisons.py`

---

## 🎯 Usage

```python
import pandas as pd

# Charger le dataset qubits
df_qubits = pd.read_csv('data/qubits/biological_qubits.csv')

# Filtrer les centres NV
nv = df_qubits[df_qubits['Systeme'].str.contains('NV', na=False)]

# Filtrer par classe
classe_b = df_qubits[df_qubits['Classe'] == 'B']

# Analyser T₂
print(f"T₂ moyen: {df_qubits['T2_us'].mean():.2f} µs")
```

---

## ⚠️ Note Importante

**Ce dataset est DISTINCT du dataset principal de protéines fluorescentes.**

- Utilisez `biological_qubits.csv` pour : magnétométrie quantique, thermométrie, spin qubits
- Utilisez `atlas_fp_optical_v2_2_curated.csv` pour : biosenseurs, imagerie neuronale, calcium/voltage

Ne les mélangez PAS - ce sont des domaines différents de la biologie quantique/optique !

---

**Dernière mise à jour :** 2025-11-15  
**Projet :** Biological Qubits & Quantum Sensors Atlas v2.2.2

