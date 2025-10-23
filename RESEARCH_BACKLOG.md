# 🔬 RESEARCH BACKLOG — Biological Qubits Atlas

**Objectif** : Répertorier et prioriser les systèmes quantiques biologiques candidats  
**Mise à jour** : 2025-10-23  
**Dataset actuel** : 32 systèmes (3 classe A)

---

## 🎯 OBJECTIF CLASSE A (Bio-Intrinsèque)

**Actuel** : 3 systèmes (9%)  
**Cible moyen terme** : 8 systèmes (25%)

**Pourquoi** : Classe A = systèmes endogènes sélectionnés par l'évolution, potentiellement optimisés pour effets quantiques

---

## A. CLASSE A — Bio-Intrinsèque (Radicaux & Métalloprotéines)

### ✅ Déjà dans l'Atlas (Ancrage)

1. **Protéine fluorescente ODMR** (GFP modifiée)
   - T2 = 0.8 µs, Contraste = 12%
   - DOI: 10.1038/s41586-024-08300-4
   - Qualité 3, vérifié ✅

2. **LOV2 flavine** (photorécepteur)
   - T2 = 0.02 µs (20 ns)
   - DOI: 10.1021/jacs.0c12505
   - Qualité 1, à confirmer

3. **Tyrosyl RNR** (ribonucléotide réductase)
   - T2 = 0.015 µs (15 ns)
   - DOI: 10.1021/bi00483a003
   - Qualité 1, à confirmer ✅

---

### 🔥 PRIORITÉ HAUTE (À Explorer d'Abord)

#### 1. Clusters [4Fe-4S] dans Ferrédoxines ⭐⭐⭐

| Champ | Valeur/Notes |
|-------|--------------|
| **Organisme** | Spinacia oleracea (épinard), Clostridium, cyanobactéries |
| **Type système** | Cluster fer-soufre [4Fe-4S]²⁺/¹⁺ |
| **Classe cible** | A (bio-intrinsèque) |
| **Mesure** | EPR bande X/Q, ENDOR |
| **Observable** | T2 (relaxation transverse), g-factor, couplage hyperfin |
| **T2 attendu** | 0.05-0.5 µs (estimation littérature EPR) |
| **Conditions** | T = 4-295 K, tampon anaérobie, spin S=1/2 (état réduit) |
| **In vivo?** | Non direct, mais in vivo végétal (chloroplastes, mitochondries) |
| **Toxicité** | Protéine endogène, non toxique |
| **DOI principal** | À rechercher : "ferredoxin EPR relaxation time" |
| **Notes/Limites** | T2 dépend fortement température, oxydation rapide à l'air, besoin anaérobiose |

**Requête de recherche** :
```
"ferredoxin" AND ("EPR" OR "ESR") AND ("T2" OR "coherence" OR "relaxation time")
Site: doi.org 10.1021 OR 10.1016 OR 10.1073
```

**Intérêt** :
- Ubiquitaire (photosynthèse ET respiration)
- Transfert électronique quantique proposé
- Littérature EPR riche (depuis 1970s)
- Bio-intrinsèque classe A

---

#### 2. Radical P680•+ dans Photosystème II ⭐⭐

| Champ | Valeur/Notes |
|-------|--------------|
| **Organisme** | Cyanobactéries, plantes (chloroplastes) |
| **Type système** | Radical chlorophylle P680 (paire spéciale PSII) |
| **Classe cible** | A (bio-intrinsèque) ou D (mécanistique si controversé) |
| **Mesure** | EPR, spectroscopie transitoire femtoseconde |
| **Observable** | Temps de vie radical (<ns), cohérence proposée |
| **T2 attendu** | 0.0001-0.001 µs (<1 ns, ultra-rapide) |
| **Conditions** | T = 77-295 K, in vitro membranes thylakoïdes, lumière |
| **In vivo?** | In vivo végétal (photosynthèse active) |
| **Toxicité** | Protéine endogène, chloroplastes |
| **DOI principal** | À rechercher : "P680 radical EPR PSII" |
| **Notes/Limites** | T2 ultra-court (<ns), radical transitoire, débat cohérence quantique vs classique |

**Requête de recherche** :
```
"P680" OR "photosystem II" AND "radical" AND "EPR"
10.1021 OR 10.1073 (JACS, PNAS)
```

**Intérêt** :
- Cohérence quantique reportée (Engel 2007, controversé)
- Photosynthèse = système biologique fondamental
- Transfert charge ultra-rapide (<ps)

---

#### 3. Radical Ascorbyl (Vitamine C Oxydée) ⭐⭐⭐

| Champ | Valeur/Notes |
|-------|--------------|
| **Organisme** | Souris, rat, humain (ubiquitaire) |
| **Type système** | Radical ascorbyl (vitamine C semi-oxydée) |
| **Classe cible** | C (spin électronique, bio-compatible exogène) |
| **Mesure** | EPR L-band (250 MHz), imagerie in vivo |
| **Observable** | T2, contraste EPR, distribution tissulaire |
| **T2 attendu** | 0.2-1 µs (similaire nitroxyde) |
| **Conditions** | T = 310 K, in vivo, injection IV ou endogène |
| **In vivo?** | Oui (stress oxydatif, EPR in vivo démontré) |
| **Toxicité** | Non toxique (vitamine endogène) |
| **DOI principal** | À rechercher : "ascorbyl radical EPR in vivo imaging" |
| **Notes/Limites** | Radical transitoire (réduction rapide), concentration faible in vivo |

**Requête de recherche** :
```
"ascorbyl radical" OR "ascorbate radical" AND "EPR" AND ("in vivo" OR "imaging")
10.1016 (Free Radical Biology & Medicine)
```

**Intérêt** :
- Ubiquitaire, non toxique
- EPR in vivo déjà démontré (stress oxydatif)
- Biomarqueur antioxydant
- Ajout "facile" avec données probablement disponibles

---

### 🟡 PRIORITÉ MOYENNE (Documentation Nécessaire)

#### 4. Radical Tryptophanyl dans DNA Photolyase

| Champ | Valeur/Notes |
|-------|--------------|
| **Organisme** | E. coli, plantes, humain (réparation ADN) |
| **Type système** | Radical tryptophanyl (Trp•) transfert électronique |
| **Classe cible** | A (bio-intrinsèque) ou D (mécanistique) |
| **Mesure** | EPR transitoire, spectroscopie résolue en temps |
| **Observable** | Temps de vie radical, transfert électronique |
| **T2 attendu** | 0.001-0.01 µs (estimé transitoire) |
| **Conditions** | T = 295 K, lumière bleue activation, anaérobie |
| **In vivo?** | In cellulo (réparation ADN endogène) |
| **Toxicité** | Protéine endogène |
| **DOI principal** | Recherche : "photolyase tryptophan radical EPR" |
| **Notes/Limites** | Radical transitoire rapide, mécanisme quantique proposé mais débattu |

---

#### 5. Radical Glycyl dans Pyruvate Formate-Lyase (PFL)

| Champ | Valeur/Notes |
|-------|--------------|
| **Organisme** | E. coli, anaérobies (métabolisme fermentation) |
| **Type système** | Radical glycyl G734 stable |
| **Classe cible** | A (bio-intrinsèque) |
| **Mesure** | EPR bande X |
| **Observable** | T2, g-factor |
| **T2 attendu** | 0.01-0.1 µs (radical protéique) |
| **Conditions** | T = 295 K, anaérobie strict, activation S-adenosylmethionine |
| **In vivo?** | In vivo bactéries anaérobies |
| **Toxicité** | Enzyme endogène E. coli |
| **DOI principal** | Recherche : "glycyl radical PFL EPR" |
| **Notes/Limites** | Anaérobiose stricte, instable à l'oxygène |

---

#### 6. Radical P700•+ dans Photosystème I

| Champ | Valeur/Notes |
|-------|--------------|
| **Organisme** | Plantes, cyanobactéries (chloroplastes) |
| **Type système** | Radical chlorophylle P700 (paire spéciale PSI) |
| **Classe cible** | A (bio-intrinsèque végétal) |
| **Mesure** | EPR, spectroscopie optique transitoire |
| **Observable** | Temps de vie radical, transfert électronique |
| **T2 attendu** | 0.001-0.01 µs (transitoire rapide) |
| **Conditions** | T = 77-295 K, membranes thylakoïdes, lumière |
| **In vivo?** | In vivo végétal (photosynthèse) |
| **Toxicité** | Protéine endogène chloroplastes |
| **DOI principal** | Recherche : "P700 radical EPR photosystem I" |
| **Notes/Limites** | T2 ultra-court, radical transitoire, mesures complexes |

---

## B. MÉTALLOPROTÉINES PARAMAGNÉTIQUES (Classe A)

### 🟡 PRIORITÉ MOYENNE

#### 7. Centre Cu(II) dans Azurine

| Champ | Valeur/Notes |
|-------|--------------|
| **Organisme** | Pseudomonas aeruginosa (protéine bleue cupro-) |
| **Type système** | Ion Cu²⁺ coordiné (transfert électronique) |
| **Classe cible** | A (bio-intrinsèque) |
| **Mesure** | EPR bande X/Q, ENDOR |
| **Observable** | T2, g-factor, couplage hyperfin Cu |
| **T2 attendu** | 0.1-1 µs (métal coordiné) |
| **Conditions** | T = 4-295 K, tampon pH 7, état oxydé Cu(II) |
| **In vivo?** | In vivo bactéries (transfert électronique) |
| **Toxicité** | Protéine endogène, non toxique |
| **DOI principal** | Recherche : "azurin copper EPR relaxation" |
| **Notes/Limites** | T2 dépend température, performances modestes vs NV |

---

#### 8. Cluster Mn₄CaO₅ (OEC) dans Photosystème II ⚠️ SPÉCULATIF

| Champ | Valeur/Notes |
|-------|--------------|
| **Organisme** | Plantes, cyanobactéries (photosynthèse) |
| **Type système** | Cluster Mn₄CaO₅ (Oxygen Evolving Complex) |
| **Classe cible** | A (bio-intrinsèque) ou D (spéculatif) |
| **Mesure** | EPR multiline, XANES, cristallographie |
| **Observable** | États de spin Mn, structure électronique |
| **T2 attendu** | Inconnu (probablement <0.01 µs) |
| **Conditions** | T = 4-295 K, lumière, photosynthèse active |
| **In vivo?** | In vivo végétal (chloroplastes) |
| **Toxicité** | Protéine endogène |
| **DOI principal** | Recherche : "Mn cluster OEC PSII EPR" |
| **Notes/Limites** | TRÈS spéculatif, pas de T2 mesuré, système complexe multi-Mn, qualité 1 probable |

---

## C. FRONTIÈRE / CONTROVERSÉ (Mécanistique)

### 🔥 HAUTE PRIORITÉ (Débat Scientifique Actif)

#### 9. Paires Radicalaires Photosynthétiques (Cohérence Quantique)

| Champ | Valeur/Notes |
|-------|--------------|
| **Organisme** | Bactéries photosynthétiques, plantes (FMO complex) |
| **Type système** | Paires radicalaires P680-Pheo, excitons FMO |
| **Classe cible** | **D (mécanistique)** — Cohérence quantique controversée |
| **Mesure** | Spectroscopie 2D électronique, EPR transitoire |
| **Observable** | Cohérence quantique (temps de vie, battements) |
| **T2 attendu** | 0.0001-0.001 µs (<1 ns, femtoseconde) |
| **Conditions** | T = 77-295 K, photosynthèse active, <ps résolution |
| **In vivo?** | In vivo végétal/bactérien (photosynthèse) |
| **Toxicité** | Système endogène |
| **DOI principal** | **10.1038/nature05678** (Engel 2007, Nature) — Référence fondatrice |
| **Notes/Limites** | **DÉBAT ACTIF** : cohérence quantique vs bruit thermique classique. Transfert énergie ultra-rapide (<100 fs). Classe D car indirect. |

**Intérêt** :
- ✅ Publication Nature majeure (Engel 2007)
- ✅ Cohérence quantique à 300K démontrée (controversée)
- ✅ Système biologique fondamental
- ⚠️ Classification difficile (A ou D?)

**Suggestion** : Ajouter comme **Classe D** avec note explicite du débat

---

#### 10. Radical Ascorbyl In Vivo ⭐⭐⭐

| Champ | Valeur/Notes |
|-------|--------------|
| **Organisme** | Souris, rat, humain (ubiquitaire) |
| **Type système** | Radical ascorbyl (vitamine C semi-oxydée) |
| **Classe cible** | **C (spin électronique, bio-compatible)** |
| **Mesure** | EPR L-band (250 MHz), imagerie in vivo |
| **Observable** | T2, distribution tissulaire, contraste EPR |
| **T2 attendu** | 0.3-0.8 µs (similaire nitroxyde TEMPO) |
| **Conditions** | T = 310 K, injection IV ou endogène, stress oxydatif |
| **In vivo?** | **Oui** (imagerie EPR in vivo démontrée) |
| **Toxicité** | Non toxique (vitamine, antioxydant) |
| **DOI principal** | Recherche : "ascorbyl radical" AND "EPR" AND "in vivo" |
| **Notes/Limites** | Radical transitoire (réduction rapide acide ascorbique), concentration faible in vivo, signal EPR faible |

**Requête** :
```
"ascorbyl radical" OR "ascorbate radical" AND "EPR" AND "in vivo"
Site: 10.1016/j.freeradbiomed (Free Radical Biology & Medicine)
```

**Intérêt** :
- ✅ Biocompatible, non toxique
- ✅ EPR in vivo démontré
- ✅ Ajout "facile" avec données accessibles

---

### 🟡 PRIORITÉ MOYENNE

#### 11. Radical Tryptophanyl dans DNA Photolyase

| Champ | Valeur/Notes |
|-------|--------------|
| **Organisme** | E. coli, Arabidopsis (réparation ADN) |
| **Type système** | Radical tryptophanyl (Trp•) chaîne de transfert |
| **Classe cible** | A (bio-intrinsèque) ou D (mécanistique) |
| **Mesure** | EPR transitoire, spectroscopie femtoseconde |
| **Observable** | Transfert électronique, temps de vie radical |
| **T2 attendu** | 0.001-0.01 µs (transitoire rapide) |
| **Conditions** | T = 295 K, lumière bleue 450 nm, DNA lié |
| **In vivo?** | In cellulo (réparation ADN endogène) |
| **Toxicité** | Enzyme endogène |
| **DOI principal** | Recherche : "photolyase tryptophan radical EPR" |
| **Notes/Limites** | Radical transitoire, mécanisme tunneling quantique proposé, mesures complexes |

---

## D. AUTRES PISTES (Priorité Basse)

#### 12. Semi-Quinones (Ubiquinone•−) Mitochondriales

| Champ | Valeur/Notes |
|-------|--------------|
| **Organisme** | Mitochondries (ubiquitaire eucaryotes) |
| **Type système** | Radical ubisemiquinone (coenzyme Q•−) |
| **Classe cible** | A (bio-intrinsèque) |
| **Mesure** | EPR bande X, mitochondries isolées |
| **Observable** | T2, g-factor |
| **T2 attendu** | 0.001-0.01 µs (radical mobile) |
| **Conditions** | T = 295 K, mitochondries, anaérobie partiel |
| **In vivo?** | In vivo mitochondrial (difficile à isoler) |
| **Toxicité** | Endogène |
| **DOI principal** | Recherche : "ubisemiquinone EPR mitochondria" |
| **Notes/Limites** | Signal EPR faible, environnement complexe, T2 court |

---

#### 13. Radicaux Peroxydases (Tyrosyl Transitoires)

| Champ | Valeur/Notes |
|-------|--------------|
| **Organisme** | Plantes (peroxydases végétales) |
| **Type système** | Radical tyrosyl transitoire (catalyse H₂O₂) |
| **Classe cible** | A (bio-intrinsèque) |
| **Mesure** | EPR transitoire |
| **Observable** | T2, cinétique formation/déclin |
| **T2 attendu** | 0.01-0.1 µs |
| **Conditions** | T = 295 K, H₂O₂ substrat, pH optimal |
| **In vivo?** | In vitro enzyme isolée principalement |
| **Toxicité** | Enzyme végétale |
| **DOI principal** | Recherche : "peroxidase tyrosyl radical EPR" |
| **Notes/Limites** | Radical très transitoire, performances probablement faibles |

---

## 📋 PROCHAINES ACTIONS

### Top 3 à Explorer (Issues GitHub)

**Issue #1** : 🔥 [Research] Clusters [4Fe-4S] dans Ferrédoxines (Classe A)
- Checklist : DOI EPR, T2 mesuré, conditions anaérobies, classification A
- Assigné : Data Curator

**Issue #2** : 🔥 [Research] Paires Radicalaires PSII (Cohérence Quantique, Classe D)
- Checklist : DOI Engel 2007, débat cohérence, classification D ou A
- Note : Controversé mais fondamental

**Issue #3** : 🔥 [Research] Radical Ascorbyl In Vivo (Classe C)
- Checklist : DOI EPR in vivo, T2 mesuré, biomarqueur stress oxydatif
- Note : Ajout "facile", données probablement disponibles

---

## 🛠️ Outils à Créer (Si Croissance)

### schema/aliases.yaml
```yaml
# Normalisation synonymes
ferredoxin:
  - Fd
  - [4Fe-4S]
  - iron-sulfur cluster
  - ferredoxine

photosystem_II:
  - PSII
  - PS II
  - photosysteme II

P680:
  - P680 radical
  - P680•+
  - chlorophylle P680

ascorbyl:
  - ascorbate radical
  - vitamin C radical
  - dehydroascorbate
```

---

## 📊 OBJECTIF COUVERTURE CLASSE A

**Actuel** : 3 systèmes
- Protéine ODMR (GFP)
- LOV2-flavine
- Tyrosyl-RNR

**Cible Court Terme** (+3 entrées) : 6 systèmes
- + [4Fe-4S] ferrédoxines
- + Radical ascorbyl
- + Paires radicalaires PSII (ou D)

**Cible Moyen Terme** (+5 entrées) : 8 systèmes (25%)
- + Tryptophanyl photolyase
- + Glycyl PFL
- + Cu(II) azurine
- + P700 PSI
- + Autre à identifier

---

## 🔍 REQUÊTES DE RECHERCHE

### PubMed

```
1. ferredoxin[Title/Abstract] AND EPR[Title/Abstract] AND (relaxation[Title/Abstract] OR coherence[Title/Abstract])

2. (P680[Title/Abstract] OR "photosystem II"[Title/Abstract]) AND radical[Title/Abstract] AND EPR[Title/Abstract]

3. (ascorbyl[Title/Abstract] OR ascorbate[Title/Abstract]) AND radical[Title/Abstract] AND EPR[Title/Abstract] AND (vivo[Title/Abstract] OR imaging[Title/Abstract])

4. photolyase[Title/Abstract] AND tryptophan[Title/Abstract] AND radical[Title/Abstract]

5. (glycyl[Title/Abstract] AND radical[Title/Abstract]) OR "pyruvate formate lyase"[Title/Abstract]
```

### Google Scholar

```
- "ferredoxin EPR T2" OR "ferredoxin relaxation time"
- "P680 radical coherence" OR "photosystem II quantum"
- "ascorbyl radical in vivo EPR imaging"
- "photolyase tryptophan electron transfer EPR"
- "glycyl radical EPR coherence"
```

---

## ✅ CRITÈRES D'ACCEPTATION (Rappel)

**Obligatoires** :
- ✅ DOI ou PMID valide (pas de source spéculative)
- ✅ Mesure explicite (T2, T1, contraste, ou proxy justifié)
- ✅ Conditions expérimentales (T, milieu, concentration)
- ✅ Classification prudente (A/B/C/D avec justification)

**Recommandés** :
- ✅ Provenance (Source_T2/T1 avec Fig/Table)
- ✅ Incertitudes (si disponibles)
- ✅ Notes de limites (T2 court, toxicité, débat)

---

## 🎯 TIMELINE SUGÉRÉE

**Semaine 1** (Court terme) :
- [ ] Chercher DOIs pour [4Fe-4S], Ascorbyl, PSII
- [ ] Ouvrir 3 issues GitHub avec checklists
- [ ] Extraire données si DOIs trouvés

**Semaine 2-4** (Moyen terme) :
- [ ] Ajouter 3-5 nouvelles entrées validées
- [ ] Créer schema/aliases.yaml
- [ ] Mettre à jour QC_REPORT avec "Classe A coverage"

**90 jours** :
- [ ] Objectif 40 systèmes (vs 32 actuels)
- [ ] 8 systèmes classe A (vs 3 actuels)
- [ ] ≥3 contributeurs externes

---

## 📝 NOTES DE RÉVISION

**Si tu veux réviser les PR** :
1. Classification A vs D (cas ambigus : PSII paires radicalaires)
2. Notes de limites (T2 ultra-courts, débats mécanistiques)
3. Qualité (1 vs 2 pour systèmes transitoires)
4. Vérification provenance (Source_T2 obligatoire si T2 fourni)

---

## 🙏 MERCI POUR CE CADRE !

Cette structure backlog + issues + critères clairs va permettre une croissance **méthodique et qualitative** du dataset.

**Prochaine étape** : Ouvrir les 3 issues GitHub pour Top 3 ?

---

**Dernière mise à jour** : 2025-10-23  
**Statut** : ✅ BACKLOG STRUCTURÉ  
**Systèmes identifiés** : 13 candidats (9 nouveaux)  
**Top 3** : Fe-S, PSII, Ascorbyl



