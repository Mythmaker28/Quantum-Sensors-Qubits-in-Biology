# 🚀 Quick Start — bioRxiv Submission

**Date**: 2025-10-24  
**Version Atlas**: v1.3.0-beta

---

## ⚡ Génération Automatique (2 minutes)

### Windows

```batch
cd C:\Users\tommy\Documents\tableau proteine fluo\submission\bioRxiv
generate_and_validate.bat
```

Double-cliquer sur `generate_and_validate.bat` fonctionne aussi.

### macOS / Linux

```bash
cd /path/to/submission/bioRxiv
python generate_biorxiv_pdfs.py
```

---

## 📦 Résultat Attendu

Après exécution, vous devriez avoir :

```
submission/bioRxiv/
├─ BQA_manuscript_bioRxiv.pdf   ✅ OBLIGATOIRE
├─ BQA_Supplement_bioRxiv.pdf   ✅ Recommandé
└─ README_bioRxiv_pack.txt      📖 Instructions détaillées
```

---

## ✅ Checklist Rapide

### Avant Upload

- [ ] PDF manuscrit s'ouvre correctement
- [ ] Section **ABSTRACT** visible en début
- [ ] Figures intégrées (pipeline diagram, table stats)
- [ ] Chiffres clés visibles : **80 total, 65 measured**
- [ ] Auteur : **Tommy Lepesteur**, Independent researcher, France
- [ ] ORCID : **0009-0009-0577-9563**
- [ ] Email : **tommy.lepesteur@hotmail.fr**

### Sur bioRxiv

1. Aller sur https://www.biorxiv.org/submit-a-manuscript
2. Créer compte / Login
3. New Submission
4. **Drag & drop** `BQA_manuscript_bioRxiv.pdf`
5. [Optionnel] Drag & drop `BQA_Supplement_bioRxiv.pdf`
6. Remplir métadonnées (voir README_bioRxiv_pack.txt)
7. Submit

---

## 🆘 Problèmes Fréquents

### PDF ne se génère pas

**Cause** : pandoc ou weasyprint manquant

**Solution** :
```bash
# Option 1 (recommandé)
winget install pandoc

# Option 2
pip install markdown weasyprint
```

### Figures mal rendues

**Cause** : Images basse résolution

**Solution** : Vérifier images sources en 300 dpi  
(Les figures actuelles sont des diagrammes texte ASCII, OK pour bioRxiv)

### Section ABSTRACT non détectée

**Cause** : Formatage Markdown incorrect

**Solution** : Vérifier que `## ABSTRACT` est bien en H2  
(Déjà correct dans `BQA_manuscript_bioRxiv.md`)

---

## 📊 Métriques Clés (à mentionner)

- **Total systèmes** : 80
- **Mesures Tier B** : 65
- **Familles** : 17 (Calcium, Voltage, Dopamine, Glutamate, etc.)
- **DOIs uniques** : 20
- **Contraste médian** : 1.40-fold
- **Contraste moyen** : 8.98-fold

---

## 🔗 Liens Importants

- **GitHub** : https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology
- **Zenodo** : https://doi.org/10.5281/zenodo.17420604 (v1.2.1)
- **bioRxiv Submit** : https://www.biorxiv.org/submit-a-manuscript

---

## 📧 Support

**Auteur** : Tommy Lepesteur  
**Email** : tommy.lepesteur@hotmail.fr  
**ORCID** : 0009-0009-0577-9563

---

**⚛️ Ready for bioRxiv submission ! 🧬**


