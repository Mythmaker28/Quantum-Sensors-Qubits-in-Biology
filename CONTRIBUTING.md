# 🤝 Guide de Contribution — Biological Qubits Atlas

Merci de votre intérêt pour contribuer à l'Atlas des Qubits Biologiques ! Ce guide vous explique comment ajouter des données, corriger des erreurs, ou améliorer la documentation.

---

## 📋 Table des Matières

1. [Comment Ajouter une Nouvelle Entrée](#ajouter-une-entrée)
2. [Comment Corriger des Données](#corriger-des-données)
3. [Standards de Qualité](#standards-de-qualité)
4. [Workflow Git](#workflow-git)
5. [Validation Automatique](#validation)

---

## 🆕 Ajouter une Nouvelle Entrée

### Critères d'Inclusion

Une entrée est acceptée si :
- ✅ **Système quantique** utilisé/utilisable en contexte biologique (in vitro, in cellulo, in vivo)
- ✅ **Publication peer-reviewed** avec DOI valide
- ✅ **Données quantitatives** : T2, T1, ou contraste mesurés
- ✅ **Pas de doublon** : vérifier qu'une entrée similaire n'existe pas déjà

### Processus en 7 Étapes (< 10 minutes)

#### 1. Créer une Issue

Aller sur : https://github.com/Mythmaker28/biological-qubits-atlas/issues/new

Titre : `[New Entry] Nom du système`

Contenu minimal :
```markdown
**Système** : [ex: Nanodiamants NV en cellules souches]
**DOI** : [10.xxxx/xxxxx]
**Classe** : [A/B/C/D - voir README]
**Contexte** : [in vitro / in cellulo / in vivo]
**Méthode** : [ODMR / ESR / NMR]
**Données clés** :
- T2 : [valeur ± erreur] µs
- T1 : [valeur ± erreur] s (si applicable)
- Contraste : [valeur ± erreur] %
- Température : [valeur] K
- Champ B0 : [valeur] T

**Source des données** : [DOI + Figure/Tableau]
```

#### 2. Fork le Repository

Cliquer sur **Fork** en haut à droite : https://github.com/Mythmaker28/biological-qubits-atlas

#### 3. Cloner Localement

```bash
git clone https://github.com/VOTRE_USERNAME/biological-qubits-atlas.git
cd biological-qubits-atlas
```

#### 4. Créer une Branche

```bash
git checkout -b add-entry-SYSTEME-NOM
# Exemple : git checkout -b add-entry-nv-stem-cells
```

#### 5. Ajouter l'Entrée au CSV

Ouvrir `biological_qubits.csv` et ajouter une nouvelle ligne **à la fin** (avant la dernière ligne vide).

**Ordre des colonnes** (33 colonnes) :
```
Systeme,Classe,Hote_contexte,Methode_lecture,Frequence,B0_Tesla,Spin_type,
Defaut,Polytype_Site,T1_s,T2_us,Contraste_%,Temperature_K,Taille_objet_nm,
Source_T2,Source_T1,Source_Contraste,T2_us_err,T1_s_err,Contraste_err,
Hyperpol_flag,Cytotox_flag,Toxicity_note,Temp_controlled,Photophysique,
Conditions,Limitations,In_vivo_flag,DOI,Annee,Qualite,Verification_statut,Notes
```

**Exemple** :
```csv
"NV nanodiamants (30 nm) en cellules souches",B,"Cellules souches (in_cellulo)",ODMR,"2.87 GHz",0.005,Electron,NV,NA,NA,1.1,14,295,30,"DOI:10.xxxx/xxxxx Fig.3a",NA,"DOI:10.xxxx/xxxxx Fig.2b",0.3,NA,3,0,1,"Cytotoxicité faible <50 µg/mL",1,"em_637-800nm; ZPL_637nm","Milieu culture DMEM+FBS, laser 532 nm, champ B 5 mT","Agrégation possible, T2 réduit vs bulk",0,"10.xxxx/xxxxx",2023,2,a_confirmer,"Description contexte et résultats clés"
```

**Conseils** :
- Mettre `NA` pour les champs non applicables
- `Verification_statut` : `a_confirmer` (sera `verifie` après review)
- `Qualite` : 1 (exploratoire) / 2 (solide) / 3 (robuste)
- `In_vivo_flag` : 0 (in vitro/cellulo) ou 1 (organisme entier)

#### 6. Valider Localement

```bash
# Installer Python 3.8+ si nécessaire
python qubits_linter.py
```

Le linter doit afficher : `[OK] No blocking errors`

Si erreurs :
- Corriger selon les suggestions
- Relancer `python qubits_linter.py`

#### 7. Commit & Push

```bash
git add biological_qubits.csv
git commit -m "feat(data): add [Nom du système] from DOI:10.xxxx/xxxxx"
git push origin add-entry-SYSTEME-NOM
```

Puis créer une **Pull Request** sur GitHub vers `infra/pages+governance` (ou `main`).

---

## 🔧 Corriger des Données

### Si vous trouvez une erreur

1. **Créer une Issue** : https://github.com/Mythmaker28/biological-qubits-atlas/issues/new
   - Titre : `[Data Fix] Nom du système - Description erreur`
   - Indiquer : ligne CSV, champ concerné, valeur actuelle, valeur correcte, source

2. **Ou proposer directement un fix** :
   ```bash
   git checkout -b fix-SYSTEME-CHAMP
   # Éditer biological_qubits.csv
   python qubits_linter.py  # Valider
   git commit -m "fix(data): correct [CHAMP] for [SYSTEME] (source: DOI)"
   git push origin fix-SYSTEME-CHAMP
   ```

3. **Pull Request** avec justification et source de la correction

---

## 📊 Standards de Qualité

### Données Requises (Minimum)

| Champ | Obligatoire | Format | Exemple |
|-------|-------------|--------|---------|
| `Systeme` | ✅ | Texte descriptif | "NV nanodiamants (50 nm) en cellules HeLa" |
| `Classe` | ✅ | A/B/C/D | B |
| `Hote_contexte` | ✅ | "Organisme/tissu (contexte)" | "Cellules HeLa (in_cellulo)" |
| `Methode_lecture` | ✅ | ODMR/ESR/NMR/Optical/Indirect | ODMR |
| `DOI` | ✅ | 10.xxxx/xxxxx | 10.1073/pnas.0912611107 |
| `T2_us` ou `T1_s` | ✅ (au moins 1) | Nombre (µs ou s) | 1.2 |
| `Source_T2/T1` | ✅ | DOI:xxx Fig.X | DOI:10.xxx Fig.3a |
| `Verification_statut` | ✅ | verifie/a_confirmer | a_confirmer |

### Provenance (v1.2+)

**Chaque valeur quantitative doit avoir sa source** :
- `T2_us` → `Source_T2` : "DOI:10.xxxx/xxxxx Fig.3a"
- `T1_s` → `Source_T1` : "DOI:10.xxxx/xxxxx Table1"
- `Contraste_%` → `Source_Contraste` : "DOI:10.xxxx/xxxxx Fig.2b"

Format source : `DOI:10.xxxx/xxxxx Fig.X` ou `DOI:10.xxxx/xxxxx Table X`

### Incertitudes

Toujours inclure les incertitudes si disponibles :
- `T2_us_err` : Incertitude sur T2 (µs)
- `T1_s_err` : Incertitude sur T1 (s)
- `Contraste_err` : Incertitude sur contraste (%)

Si non publiées, estimer ±10-20% basé sur le contexte.

---

## 🔀 Workflow Git

### Structure des Branches

```
main / infra/pages+governance  ← Branche stable
  ↑
  └─ add-entry-SYSTEME  ← Votre feature branch
  └─ fix-SYSTEME-CHAMP  ← Votre fix branch
```

### Conventions de Commit

Format : `type(scope): description`

**Types** :
- `feat(data)` : Ajout d'entrée(s)
- `fix(data)` : Correction de donnée(s)
- `docs` : Documentation
- `chore` : Maintenance

**Exemples** :
```bash
git commit -m "feat(data): add hyperpolarized lactate NMR from DOI:10.xxxx"
git commit -m "fix(data): correct T2 for NV bulk (source: DOI:10.yyyy Fig.2)"
git commit -m "docs: update README with new citation format"
```

---

## ✅ Validation Automatique

### Linter Local

Le linter (`qubits_linter.py`) vérifie automatiquement :
- ✅ Cohérence des valeurs (contraste 0-100%, températures plausibles)
- ✅ Fréquences cohérentes (NV à 2.87 GHz, etc.)
- ✅ Champs obligatoires remplis
- ✅ Format DOI valide
- ✅ Relations physiques (T2 ≤ 2×T1)
- ✅ Provenance des données

**Exécution** :
```bash
python qubits_linter.py
```

**Sortie attendue** :
```
[LINT] Analysing biological_qubits.csv...
[OK] Lint completed: XX systems analysed
   [ERROR] Errors: 0
   [WARN]  Warnings: X
[OK] No blocking errors. Dataset ready!
```

### Résolution des Erreurs

**Erreur fréquente 1** : "Contraste hors plage [0-100]%"
- **Solution** : Vérifier que c'est bien un pourcentage (pas une fraction)

**Erreur fréquente 2** : "NV doit être à 2.87±0.3 GHz"
- **Solution** : Vérifier la fréquence dans la publication

**Erreur fréquente 3** : "T2 sans source de provenance"
- **Solution** : Ajouter `Source_T2` avec DOI+Figure

---

## 🎯 Checklist Avant Pull Request

- [ ] Linter passe (`python qubits_linter.py` → 0 erreurs)
- [ ] Toutes les valeurs quantitatives ont une `Source_*`
- [ ] DOI valide et accessible
- [ ] Pas de doublon évident (vérifier systèmes similaires)
- [ ] Commit message suit la convention
- [ ] Issue créée ou référencée (#XX)

---

## 📧 Questions ?

- **Issues** : https://github.com/Mythmaker28/biological-qubits-atlas/issues
- **Discussions** : https://github.com/Mythmaker28/biological-qubits-atlas/discussions
- **Email** : Voir README.md pour contact mainteneur

---

## 🙏 Merci !

Chaque contribution, même petite, améliore la qualité et la couverture de l'atlas. Votre nom sera crédité dans les release notes et le fichier CONTRIBUTORS.md.

**Citation du projet** :
```bibtex
@dataset{lepesteur_2025_biological_qubits,
  author    = {Lepesteur, Tommy},
  title     = {Biological Qubits Atlas},
  year      = 2025,
  publisher = {Zenodo},
  version   = {1.2.1},
  doi       = {10.5281/zenodo.17420604}
}
```

---

**Dernière mise à jour** : 2025-10-23  
**Version** : 1.2.1
