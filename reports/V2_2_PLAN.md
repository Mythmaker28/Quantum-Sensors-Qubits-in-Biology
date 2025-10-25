# ATLAS v2.2 DATA BOOST — Plan d'Exécution

**Date**: 2025-10-25  
**Objectif**: ≥150 systèmes utiles (vs 113 en v2.1, **gap: +37**)

---

## 🎯 CRITÈRES D'ACCEPTATION (DURS)

| Critère | Seuil | v2.1 Baseline | Gap |
|---------|-------|---------------|-----|
| **N_utiles** | ≥150 (min 120) | 113 | **+37 requis** |
| **Couverture optique** | ≥85% | 66% | **+19pp** |
| **Doublons** | ≤5 | 22 | **-17 requis** |
| **Provenance+Licence** | 100% | 87%/92% | **+13pp/+8pp** |

---

## 📊 STRATÉGIE D'ENRICHISSEMENT

### Sources Cibles (par priorité)

1. **FPbase API** (PRIORITÉ 1)
   - Potentiel : +30-50 systèmes
   - Données optiques complètes
   - Fallback : dump local ou mode offline

2. **Literature Mining Intensif** (PRIORITÉ 1)
   - Potentiel : +20-40 systèmes
   - Requêtes ciblées PubMed/PMC
   - Focus : GCaMPs récents, ASAPs, GRABs

3. **Addgene Collection** (PRIORITÉ 2)
   - Potentiel : +10-20 systèmes
   - Plasmides documentés
   - Extraction metadata

4. **Fluorescent Biosensor DB** (PRIORITÉ 3)
   - Potentiel : +5-15 systèmes
   - Biosenseurs génétiquement encodables
   - Cross-référence avec existant

### Total Projeté

**Optimiste** : +65-125 systèmes → 178-238 total  
**Réaliste** : +40-70 systèmes → 153-183 total  
**Pessimiste** : +25-40 systèmes → 138-153 total

**Faisabilité** : ✅ HAUTE (réaliste atteint objectif)

---

## 🔄 PHASES D'EXÉCUTION

### PHASE 1 : FPbase (30-60 min)

**Actions** :
1. Réessayer API GraphQL (peut-être accessible maintenant)
2. Si KO : chercher dump local ou CSV export
3. Mode offline acceptable si nécessaire
4. Mapper vers schéma Atlas v2.2

**Outputs** :
- `data/raw/fpbase/fpbase_dump_v2_2.jsonl`
- `data/processed/fpbase_mapped_v2_2.csv`
- `reports/FPBASE_INGEST_v2.2.md`

### PHASE 2 : Literature Mining (60-120 min)

**Requêtes PubMed** :
```
1. "GCaMP8" OR "jGCaMP8" (2023-2025) → nouveaux variants
2. "ASAP4" OR "Archon2" (voltage sensors récents)
3. "GRAB" AND ("serotonin" OR "acetylcholine" OR "GABA") (2022-2025)
4. "iGluSnFR" AND "variant" (glutamate sensors)
5. "calcium indicator" AND "red" (NIR-GECO, jRGECO variants)
```

**Extraction** :
- Tables de caractérisation
- Figures avec ΔF/F0 ou fold-change
- Wavelengths (excitation/emission)

**Output** :
- `data/processed/lit_extracted_v2_2.csv` (target: +30-50 systèmes)
- `reports/LIT_MINING_v2.2.md`

### PHASE 3 : Merge + Dédup (30-45 min)

**Déduplication stricte** :
- Fuzzy matching : Levenshtein distance ≤2
- Clé canonique : (name_normalized | uniprot_id | doi)
- Résolution conflits : priorité source (FPbase > Lit > v2.1)

**Outliers** :
- Z-score >5 sur log1p(contrast) → exclusion
- Wavelength hors [350-750] nm → vérification

**Outputs** :
- `atlas_fp_optical_v2_2.csv`
- `TRAINING_TABLE_v2_2.csv`
- Métadonnées JSON

### PHASE 4 : QA + Tests (15-30 min)

**Tests automatisés** :
```python
test_n_utiles_ge_150()
test_optical_coverage_ge_85()
test_duplicates_le_5()
test_provenance_license_complete()
test_schema_contract()
```

**Validation manuelle** :
- Échantillon 10% (15 systèmes) : DOI → vérif valeur
- Cross-check wavelengths avec littérature

### PHASE 5 : Décision GO/NO-GO (5-10 min)

**Si PASS** :
- Branche `release/v2.2-optical-boost`
- Tag `v2.2.0`
- Release GitHub avec assets

**Si NO-GO** :
- Rapport `V2_2_BLOCKED.md`
- Analyse gap : où gagner systèmes rapidement ?
- Plan correction (timeline 1-2 semaines)

---

## ⏱️ TIMELINE ESTIMÉE

**Total** : 2h30 - 4h30

| Phase | Durée | Dépendances |
|-------|-------|-------------|
| Phase 1 | 30-60 min | Réseau/FPbase |
| Phase 2 | 60-120 min | Accès PubMed |
| Phase 3 | 30-45 min | Phases 1+2 complètes |
| Phase 4 | 15-30 min | Phase 3 complète |
| Phase 5 | 5-10 min | Phase 4 complète |

**Lancement** : Immédiat  
**Livraison projetée** : Aujourd'hui (si sources accessibles)

---

## 🚨 RISQUES & MITIGATIONS

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| FPbase KO | HAUTE | MOYEN | Fallback dump local + mode offline |
| Lit mining < +30 | MOYENNE | MOYEN | Intensifier requêtes + Addgene |
| Doublons > 5 | FAIBLE | FAIBLE | Dédup stricte avec fuzzy matching |
| Couverture <85% | MOYENNE | MOYEN | Extraction manuelle wavelengths |

---

**Status** : ✅ PRÊT À EXÉCUTER  
**Go/No-Go** : **GO** (plan validé, sources identifiées)

