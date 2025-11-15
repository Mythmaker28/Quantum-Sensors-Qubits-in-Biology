# 🌿 Systèmes de Photosynthèse Quantique

La photosynthèse exploite des effets quantiques pour transférer l'énergie avec une efficacité proche de 100%.

---

## 🔬 FMO Complex (Fenna-Matthews-Olson)

### Caractéristiques

**Organisme:** *Chlorobium tepidum* (bactérie verte sulfureuse)

**Type de qubit:** Excitonique (superposition d'états électroniques)

**Longueur d'onde:** 805-825 nm

**Temps de cohérence:** ~660 femtosecondes (fs) à température physiologique

**Température d'opération:** 77-300 K

**Nombre de chromophores:** 7 molécules de bactériochlorophylle (BChl)

### Mécanisme Quantique

Le FMO complex utilise la **superposition quantique** pour explorer simultanément plusieurs chemins de transfert d'énergie:

1. **Absorption de photon** par l'antenne → création d'un exciton
2. **Superposition quantique** des 7 chromophores
3. **Transfert d'énergie** via couplage cohérent
4. **Déphasing assisté par l'environnement** optimise l'efficacité

**Équation de transfert:**

```
|ψ⟩ = Σ cᵢ|i⟩
```

où `|i⟩` représente l'exciton localisé sur le chromophore i.

### Preuves Expérimentales

**Première observation:** Engel et al. (2007) - Nature

**Technique:** Spectroscopie 2D électronique (2D-ES)

**Observation:** Oscillations quantiques persistant ~660 fs à 77K et ~300 fs à 277K

### Applications Potentielles

- Photovoltaïque quantique
- Calcul quantique photo-induit
- Capteurs quantiques ultra-sensibles

### Références

1. Engel, G. S. et al. (2007). "Evidence for wavelike energy transfer through quantum coherence in photosynthetic systems." *Nature* 446, 782-786.
2. Panitchayangkoon, G. et al. (2010). "Long-lived quantum coherence in photosynthetic complexes at physiological temperature." *PNAS* 107, 12766-12770.

---

## 🍃 Photosystem II (PSII)

### Caractéristiques

**Organisme:** Plantes, algues, cyanobactéries

**Type de qubit:** Excitonique

**Longueur d'onde:** 680 nm (P680)

**Temps de cohérence:** ~400 fs à 77K, ~100 fs à 300K

**Température d'opération:** 273-310 K (température ambiante)

**Centre réactionnel:** P680 (paire de chlorophylle a)

### Structure

- **Antenne LHC-II:** ~200 chlorophylles
- **Complexe central:** CP43, CP47
- **Centre réactionnel:** P680, phéophytine, quinones

### Mécanisme

1. **Absorption lumineuse** par LHC-II
2. **Transfert d'énergie cohérent** vers P680
3. **Séparation de charge** ultrarapide (<1 ps)
4. **Oxydation de l'eau** (4 photons → O₂ + 4H⁺ + 4e⁻)

### Cohérence Quantique

**Observation:** Collini et al. (2010)

- Cohérences électroniques persistant jusqu'à 300K
- Superposition de plusieurs chemins d'excitation
- Rôle du "bruit" environnemental dans l'optimisation

### Importance Biologique

- Source de **tout l'oxygène atmosphérique**
- Convertit ~10¹⁷ W de lumière solaire
- Efficacité quantique: ~95%

### Références

1. Collini, E. et al. (2010). "Coherently wired light-harvesting in photosynthetic marine algae at ambient temperature." *Nature* 463, 644-647.
2. Romero, E. et al. (2014). "Quantum coherence in photosynthesis for efficient solar energy conversion." *Nature Physics* 10, 676-682.

---

## 🌱 Photosystem I (PSI)

### Caractéristiques

**Organisme:** Plantes, algues, cyanobactéries

**Type de qubit:** Excitonique

**Longueur d'onde:** 700 nm (P700)

**Temps de cohérence:** ~500 fs

**Efficacité quantique:** ~100% (meilleure machine photochimique connue)

### Particularités

- **Plus ancien** système photosynthétique (~3 milliards d'années)
- **Efficacité parfaite:** quasi 1 électron par photon absorbé
- **96 chlorophylles** dans l'antenne centrale
- **Transfert d'énergie** en ~20 ps

### Cohérence Quantique

- Superposition de 96 chromophores
- Transport balistique de l'exciton
- Couplage fort avec vibrations moléculaires

### Applications

- **Bioélectronique:** PSI intégré dans circuits
- **Bio-photovoltaïque:** Cellules solaires biologiques
- **Calcul quantique:** Substrat pour portes quantiques

### Références

1. Jennings, R. C. et al. (2018). "Photosystem I, when excited in the chlorophyll Q_y absorption band, feeds on negative entropy." *Biophys. Chem.* 233, 36-46.

---

## 🦠 LH2 Complex (Light-Harvesting 2)

### Caractéristiques

**Organisme:** *Rhodopseudomonas acidophila* (bactérie pourpre)

**Structure:** Anneau de 18 bactériochlorophylles

**Longueur d'onde:** 800 nm (B800), 850 nm (B850)

**Temps de cohérence:** ~200 fs

**Symétrie:** C9 (9 fois symétrique)

### Mécanisme

- **Excitons délocalisés** sur l'anneau B850
- **Transfert ultra-rapide** B800 → B850 en ~700 fs
- **Couplage fort** entre molécules adjacentes

### Observation

**Technique:** Spectroscopie femtoseconde

**Résultat:** Battements quantiques révélant la cohérence

### Références

1. van Amerongen, H., Valkunas, L. & van Grondelle, R. (2000). *Photosynthetic Excitons*. World Scientific.

---

## 📊 Comparaison des Systèmes

| Système | Organisme | λ (nm) | T₂ (fs) | T (K) | Efficacité |
|---------|-----------|--------|---------|-------|------------|
| FMO | Bactérie | 810 | 660 | 77-300 | >99% |
| PSII | Plantes | 680 | 400 | 273-310 | ~95% |
| PSI | Plantes | 700 | 500 | 273-310 | ~100% |
| LH2 | Bactérie | 850 | 200 | 273-310 | ~95% |

---

## 🎯 Implications pour le Calcul Quantique

### Avantages

✅ **Opération à température ambiante**
✅ **Auto-assemblage** (pas de nanofabrication)
✅ **Protégé par protéines** (décoherence réduite)
✅ **Évolution de 3 milliards d'années** (optimisé)

### Défis

❌ Temps de cohérence courts (~100-600 fs)
❌ Difficile à interfacer avec électronique
❌ Lecture des états quantiques
❌ Contrôle individuel des qubits

### Voies de Recherche

1. **Protéines artificielles** avec T₂ prolongés
2. **Hybrides biologiques-électroniques**
3. **Algorithmes inspirés de la photosynthèse**
4. **Capteurs quantiques bio-mimétiques**

---

## 📚 Ressources Supplémentaires

### Revues Clés

- Scholes, G. D. et al. (2017). "Using coherence to enhance function in chemical and biophysical systems." *Nature* 543, 647-656.
- Lambert, N. et al. (2013). "Quantum biology." *Nature Physics* 9, 10-18.

### Bases de Données

- [RCSB Protein Data Bank](https://www.rcsb.org/) - Structures 3D
- [Photosynthetic Antenna Research Center](https://parc.wustl.edu/)

### Groupes de Recherche

- Graham Fleming Lab (UC Berkeley)
- Gregory Scholes Lab (Princeton)
- Alexandra Olaya-Castro Lab (UCL)

---

*Dernière mise à jour: 2025-11-15*
*Atlas Biological Qubits - Documentation Scientifique*

