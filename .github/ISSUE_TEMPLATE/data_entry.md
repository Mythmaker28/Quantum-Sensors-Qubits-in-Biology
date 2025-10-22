---
name: Data Entry Request
about: Propose a new entry for the Atlas
title: '[DATA] Add: '
labels: data-entry, enhancement
assignees: ''
---

## 📝 New System Proposal

**System Name:** <!-- e.g., "SnV defects in diamond (nanoparticles)" -->

**Classe:** <!-- A / B / C / D (see README) -->

## 🔬 Core Data (Required)

### Identification
- **Systeme:** 
- **Classe:** <!-- A / B / C / D -->
- **Hote_contexte:** <!-- e.g., "Cellules HeLa (in_cellulo)" -->
- **Methode_lecture:** <!-- ODMR / ESR / NMR / Optical-only / Indirect -->
- **DOI:** <!-- 10.xxxx/yyyyy -->
- **Annee:** <!-- YYYY -->

### Quantitative Parameters
- **T2_us:** <!-- µs -->
- **T2_us_err:** <!-- ±σ -->
- **Source_T2:** <!-- DOI:10.xxxx/yyyyy Fig.X -->
- **Contraste_%:** <!-- 0-100 or NA -->
- **Contraste_err:** <!-- ±σ or NA -->
- **Source_Contraste:** <!-- DOI:10.xxxx/yyyyy Fig.X or NA -->
- **Temperature_K:** <!-- Kelvin -->
- **Frequence:** <!-- e.g., "2.87 GHz" -->
- **B0_Tesla:** <!-- Tesla -->

### Spin & Defect (if applicable)
- **Spin_type:** <!-- Electron / Noyau; ^XX -->
- **Defaut:** <!-- NV / VSi / VV / etc. or NA -->
- **Polytype_Site:** <!-- For SiC: "4H-SiC; k-site" or NA -->

### For Classe C (NMR/Hyperpolarized)
- **T1_s:** <!-- seconds -->
- **T1_s_err:** <!-- ±σ -->
- **Source_T1:** <!-- DOI:10.xxxx/yyyyy Fig.X -->
- **Hyperpol_flag:** <!-- 0 / 1 -->

### Biological Context
- **In_vivo_flag:** <!-- 0 (in vitro/cellulo) / 1 (in vivo organism) -->
- **Taille_objet_nm:** <!-- nm or NA -->
- **Cytotox_flag:** <!-- 0 / 1 -->
- **Toxicity_note:** <!-- Description or NA -->
- **Temp_controlled:** <!-- 0 / 1 -->

### Quality & Verification
- **Qualite:** <!-- 1 / 2 / 3 (see README) -->
- **Verification_statut:** <!-- verifie / a_confirmer -->

## 📚 Publication Details

**Title:** 

**Authors:** 

**Journal:** 

**Year:** 

**DOI:** 

**Key Figures:** <!-- Which figures contain T2, T1, Contraste data -->

## 📝 Notes

<!-- Additional context: conditions, limitations, significance -->

## ✅ Contributor Checklist

- [ ] I have read the contribution guidelines (README.md)
- [ ] All required fields are filled
- [ ] Units are normalized (µs, s, K, T)
- [ ] DOI is valid and accessible
- [ ] I have the full publication (not just abstract)
- [ ] Values are verified from figures/tables (not estimated)
- [ ] Incertitudes (±σ) are estimated or extracted
- [ ] Source provenance (DOI:xxx Fig.X) is provided

## 🔗 References

<!-- Links to publications, supplementary materials, datasets -->

