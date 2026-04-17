@echo off
REM Script automatisé de génération et validation bioRxiv
REM Usage: double-cliquer ou lancer depuis cmd

echo ========================================
echo   bioRxiv Submission Pack Generator
echo ========================================
echo.

REM Aller dans le bon répertoire
cd /d "%~dp0"

echo [1/4] Vérification fichiers sources...
if not exist "BQA_manuscript_bioRxiv.md" (
    echo ERREUR: BQA_manuscript_bioRxiv.md manquant
    pause
    exit /b 1
)
echo   ✓ Manuscrit Markdown trouvé

if not exist "BQA_Supplement_bioRxiv.md" (
    echo ATTENTION: Supplément manquant (optionnel)
) else (
    echo   ✓ Supplément Markdown trouvé
)

echo.
echo [2/4] Génération PDFs...
python generate_biorxiv_pdfs.py
if %ERRORLEVEL% NEQ 0 (
    echo ERREUR: Génération PDF échouée
    echo.
    echo Solutions:
    echo 1. Installer pandoc: winget install pandoc
    echo 2. OU installer weasyprint: pip install markdown weasyprint
    echo.
    pause
    exit /b 1
)

echo.
echo [3/4] Vérification PDFs...
if not exist "BQA_manuscript_bioRxiv.pdf" (
    echo ERREUR: BQA_manuscript_bioRxiv.pdf non généré
    pause
    exit /b 1
)
echo   ✓ Manuscrit PDF présent

if exist "BQA_Supplement_bioRxiv.pdf" (
    echo   ✓ Supplément PDF présent
)

echo.
echo [4/4] Récapitulatif paquet...
echo.
echo ┌─────────────────────────────────────────┐
echo │  PAQUET bioRxiv PRÊT                   │
echo └─────────────────────────────────────────┘
echo.
dir /B BQA_*.pdf 2>nul
echo.
echo README_bioRxiv_pack.txt
echo.

echo ========================================
echo  ✓ PAQUET PRÊT POUR SOUMISSION
echo ========================================
echo.
echo Prochaines étapes:
echo 1. Ouvrir BQA_manuscript_bioRxiv.pdf et vérifier
echo 2. Lire README_bioRxiv_pack.txt pour upload
echo 3. Aller sur https://www.biorxiv.org/submit-a-manuscript
echo 4. Drag & drop BQA_manuscript_bioRxiv.pdf
echo.

pause


