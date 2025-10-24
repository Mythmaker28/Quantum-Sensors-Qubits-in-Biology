┌─────────────────────────────────────────────────────────────────────┐
│  BIOLOGICAL QUBITS ATLAS — bioRxiv Submission Pack                 │
│  Version: v1.3.0-beta                                              │
│  Date: 2025-10-24                                                  │
└─────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════
 CONTENU DU PAQUET
═══════════════════════════════════════════════════════════════════════

📄 MANUSCRIT (OBLIGATOIRE)
  • BQA_manuscript_bioRxiv.pdf
    Manuscrit complet avec figures intégrées
    Sections: ABSTRACT, Introduction, Methods, Results, Discussion,
              Data Availability, References
    Pages: ~15-20

📄 SUPPLÉMENT (OPTIONNEL mais recommandé)
  • BQA_Supplement_bioRxiv.pdf
    Matériels supplémentaires détaillés
    Sections: Field schema, Quality tiers, Evidence examples,
              Build artifacts, License tracking
    Pages: ~10-12

📄 SOURCES MARKDOWN (pour génération)
  • BQA_manuscript_bioRxiv.md
  • BQA_Supplement_bioRxiv.md

🔧 SCRIPTS
  • generate_biorxiv_pdfs.py (génération PDF automatisée)

📋 DOCUMENTATION
  • README_bioRxiv_pack.txt (ce fichier)

═══════════════════════════════════════════════════════════════════════
 GÉNÉRATION DES PDFs
═══════════════════════════════════════════════════════════════════════

MÉTHODE 1 : Script Automatisé (Recommandé)
───────────────────────────────────────────
cd C:\Users\tommy\Documents\tableau proteine fluo\submission\bioRxiv
python generate_biorxiv_pdfs.py

Dépendances:
  Option A (recommandée): Installer pandoc
    Windows: winget install pandoc
    macOS: brew install pandoc
    Linux: sudo apt install pandoc texlive-xetex

  Option B (fallback): Python packages
    pip install markdown weasyprint


MÉTHODE 2 : Pandoc Manuel
──────────────────────────
pandoc BQA_manuscript_bioRxiv.md -o BQA_manuscript_bioRxiv.pdf \
  --pdf-engine=xelatex \
  --variable geometry:margin=1in \
  --variable fontsize=11pt \
  --number-sections

pandoc BQA_Supplement_bioRxiv.md -o BQA_Supplement_bioRxiv.pdf \
  --pdf-engine=xelatex \
  --variable geometry:margin=1in \
  --variable fontsize=11pt \
  --number-sections


MÉTHODE 3 : Conversion en Ligne (si pandoc indisponible)
─────────────────────────────────────────────────────────
1. Ouvrir https://www.markdowntopdf.com/
2. Upload BQA_manuscript_bioRxiv.md
3. Télécharger PDF généré
4. Vérifier: polices intégrées, images 300 dpi

═══════════════════════════════════════════════════════════════════════
 VÉRIFICATION CONFORMITÉ bioRxiv
═══════════════════════════════════════════════════════════════════════

✅ CHECKLIST TECHNIQUE

 [ ] PDF s'ouvre correctement (Adobe Reader, Chrome, Firefox)
 [ ] Texte net et lisible (polices intégrées)
 [ ] Titres hiérarchisés (H1, H2, H3 visibles)
 [ ] Section ABSTRACT présente en début de manuscrit
 [ ] Figures intégrées (pas de fichiers séparés)
 [ ] Images 300 dpi minimum
 [ ] Pages format A4 ou Letter
 [ ] Pas de protection / mot de passe
 [ ] Nom fichier sans espaces ni caractères spéciaux
 [ ] Taille fichier < 100 MB

✅ CHECKLIST CONTENU

 [ ] Titre: "Biological Qubits Atlas: a curated, reproducible catalog 
           of quantum-enabled biosensing systems"
 [ ] Auteur: Tommy Lepesteur
 [ ] Affiliation: Independent researcher, France
 [ ] ORCID: 0009-0009-0577-9563
 [ ] Email correspondant: tommy.lepesteur@hotmail.fr
 [ ] Chiffres clés visibles: 80 total, 65 measured
 [ ] Liens GitHub et Zenodo cliquables
 [ ] DOI citations correctement formatés
 [ ] Déclaration competing interests: "The author declares no 
                                       competing interests"
 [ ] Data availability section présente

═══════════════════════════════════════════════════════════════════════
 MÉTADONNÉES bioRxiv (à remplir sur le site)
═══════════════════════════════════════════════════════════════════════

TITRE
  Biological Qubits Atlas: a curated, reproducible catalog of 
  quantum-enabled biosensing systems

AUTEUR(S)
  Name: Tommy Lepesteur
  Affiliation: Independent researcher
  Country: France
  ORCID: 0009-0009-0577-9563
  Corresponding: Yes
  Email: tommy.lepesteur@hotmail.fr

CATÉGORIE
  Primary: Biophysics
  Secondary: Systems Biology, Neuroscience (optionnel)

ABSTRACT (copier depuis manuscrit)
  We present the Biological Qubits Atlas, an open, curated dataset of 
  quantum-enabled biosensing systems (fluorescent protein sensors, 
  voltage indicators, metabolic reporters, etc.). [...]
  
  (Voir BQA_manuscript_bioRxiv.md section ABSTRACT pour texte complet)

MOTS-CLÉS
  biosensors, fluorescent proteins, quantum biology, calcium indicators,
  voltage sensors, optical physiology, open data, FAIR principles

LIENS EXTERNES
  Code & Data: https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology
  Archive: https://doi.org/10.5281/zenodo.17420604 (v1.2.1 stable)
           (Mettre à jour avec DOI v1.3.0-beta une fois déposé)

DÉCLARATIONS
  Competing Interests: The author declares no competing interests.
  
  Ethics: This study involves no research on humans or animals.
  
  Data/Code Availability: All code, curation scripts, and data builds 
  are openly available at the GitHub link above; archived snapshot on 
  Zenodo as cited.

LICENCE
  CC-BY 4.0 (bioRxiv standard pour prépublications)

═══════════════════════════════════════════════════════════════════════
 UPLOAD SUR bioRxiv
═══════════════════════════════════════════════════════════════════════

ÉTAPES DÉPÔT:

1. Aller sur https://www.biorxiv.org/submit-a-manuscript

2. Login / Créer compte

3. New Submission

4. Upload Manuscript Files:
   • Drag & drop BQA_manuscript_bioRxiv.pdf dans "Drop manuscript 
     Files here"
   
   • [OPTIONNEL] Drag & drop BQA_Supplement_bioRxiv.pdf dans 
     "Drop supplemental Files here"

5. Remplir métadonnées (voir section ci-dessus)

6. Preview HTML:
   • Vérifier que section ABSTRACT est détectée
   • Vérifier figures affichées
   • Vérifier références formatées

7. Submit for Processing

8. Attendre email confirmation (généralement 24-48h)

═══════════════════════════════════════════════════════════════════════
 TROUBLESHOOTING
═══════════════════════════════════════════════════════════════════════

PROBLÈME: PDF ne se génère pas (pandoc error)
SOLUTION: Installer texlive-xetex complet
  Windows: MiKTeX (https://miktex.org/download)
  macOS: MacTeX (brew install --cask mactex)
  Linux: sudo apt install texlive-full

PROBLÈME: Figures mal rendues
SOLUTION: Vérifier images sources en 300 dpi minimum
  Utiliser ImageMagick pour upscale si besoin:
    magick convert image.png -density 300 image_300dpi.png

PROBLÈME: Section ABSTRACT non détectée par bioRxiv
SOLUTION: S'assurer que le titre "## ABSTRACT" est en H2 (Markdown)
  Ou ajouter manuellement "ABSTRACT" en début de texte dans PDF

PROBLÈME: Liens non cliquables dans PDF
SOLUTION: Pandoc ajoute automatiquement hyperlinks
  Vérifier avec: pdfinfo BQA_manuscript_bioRxiv.pdf | grep Links

═══════════════════════════════════════════════════════════════════════
 INFORMATIONS VERSION
═══════════════════════════════════════════════════════════════════════

DATASET VERSION: v1.3.0-beta
GIT COMMIT: (à remplir après commit final)
GIT TAG: v1.3.0-beta
BUILD DATE: 2025-10-24

MÉTRIQUES CLÉS:
  • Total systèmes: 80
  • Mesures (Tier B): 65
  • Familles: 17 (Calcium, Voltage, Dopamine, etc.)
  • DOIs uniques: 20
  • Contraste moyen: 8.98-fold
  • Contraste médian: 1.40-fold

FICHIERS RÉFÉRENCÉS:
  • atlas_fp_optical_v1_3.csv (dataset principal)
  • TRAINING.METADATA.v1.3.json (métadonnées)
  • reports/AUDIT_v1.3_fp_optical.md (audit QA)
  • reports/METRICS_v1.3.json (métriques)
  • reports/EVIDENCE_SAMPLES_v1.3.md (table évidence)

═══════════════════════════════════════════════════════════════════════
 CONTACTS & SUPPORT
═══════════════════════════════════════════════════════════════════════

AUTEUR: Tommy Lepesteur
EMAIL: tommy.lepesteur@hotmail.fr
ORCID: 0009-0009-0577-9563

GITHUB: https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology
ISSUES: https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/issues

ZENODO: https://doi.org/10.5281/zenodo.17420604

═══════════════════════════════════════════════════════════════════════
 LICENCE
═══════════════════════════════════════════════════════════════════════

DONNÉES (Atlas CSV): CC BY 4.0
CODE (Scripts): MIT License
MANUSCRIT (bioRxiv preprint): CC BY 4.0 (standard bioRxiv)

═══════════════════════════════════════════════════════════════════════

📅 Date création paquet: 2025-10-24
✍️  Créé par: Tommy Lepesteur
🔬 Version Atlas: v1.3.0-beta
📦 Ready for bioRxiv submission

═══════════════════════════════════════════════════════════════════════


