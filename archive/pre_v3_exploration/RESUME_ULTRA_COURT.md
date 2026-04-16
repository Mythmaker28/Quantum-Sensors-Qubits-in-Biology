# RÉSUMÉ ULTRA-COURT : Systèmes Quantiques Biologiques

**Date :** 2025-11-19

---

## LES 34 SYSTÈMES NON-OPTIQUES

**Fichier envoyé :** `data/qubits/quantum_systems_unified.csv`

```
TOTAL : 34 systèmes quantiques non-optiques

DÉCOMPOSITION :
├─ Classe A (Protéines bio-intrinsèques) : 3 systèmes
├─ Classe B (Capteurs inorganiques) : 15 systèmes
├─ Classe C (Noyaux hyperpolarisés) : 12 systèmes
└─ Classe D (Mécanismes candidats) : 4 systèmes

IN VIVO : 18/34 systèmes testés in vivo
FDA-APPROVED : Pyruvate [13C] (2023)

COHERENCE METRICS :
├─ Avec T2 : 33/34 systèmes
├─ Avec T1 : 14/34 systèmes
└─ Temp range : 4-310 K
```

---

## SOURCES ADDITIONNELLES IDENTIFIÉES

### Priorité HAUTE (faire maintenant)

1. **NV Centers** (literature mining 2010-2025)
   - Gain : **+50-100 systèmes**
   - Temps : 4-8 heures
   - PubMed : "NV center" + "T2" + "biological"

2. **ising-life-lab** (repo GitHub)
   - URL : https://github.com/Mythmaker28/ising-life-lab
   - À explorer : contient-il des T1/T2 ?
   - Temps : 1-2 heures

### Priorité MOYENNE

3. **SiC Defects** (literature mining)
   - Gain : +20-50 systèmes
   - Temps : 3-5 heures

4. **Hyperpolarized 13C** (clinical trials)
   - Gain : +10-20 systèmes
   - Temps : 2-4 heures

### Priorité BASSE

5. **Radical Pairs** (literature mining)
   - Gain : +10-30 systèmes
   - Temps : 3-6 heures

---

## ESTIMATION TOTALE

```
ACTUEL :
- Optical FP : 180
- Non-optical : 34
- TOTAL : 214 systèmes

AVEC MINING (conservative) :
- Optical FP : 180
- Non-optical : 34 + 90
- TOTAL : 304 systèmes

AVEC MINING (optimiste) :
- Optical FP : 180
- Non-optical : 34 + 200
- TOTAL : 414 systèmes
```

---

## POUR LE BRIDGE

```
n_total = n_ising + n_fp + n_qs

ACTUEL :
n_qs = 34

AVEC MINING :
n_qs = 124-254

EXEMPLE (si n_ising = 10) :
- Actuel : n_total = 10 + 180 + 34 = 224
- Avec mining : n_total = 10 + 180 + 124-254 = 314-444
```

---

## ACTIONS SUIVANTES

1. **[FAIT]** Envoyer les 34 systèmes non-optiques
2. **[FAIT]** Identifier sources additionnelles
3. **[TODO]** Explorer ising-life-lab (1-2h)
4. **[TODO]** Literature mining NV centers (4-8h, gain +50-100)

---

**Pas de duplication** avec atlas_fp_optical (modalités différentes)

