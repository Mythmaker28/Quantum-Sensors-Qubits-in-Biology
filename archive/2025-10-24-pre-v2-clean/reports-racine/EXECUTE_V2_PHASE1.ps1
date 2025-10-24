# Script PowerShell Automatisation Phase 1 v2.0
# Pour Windows
# Licence: Apache-2.0

Write-Host "==========================================" -ForegroundColor Blue
Write-Host "  Phase 1 v2.0 — Quick Wins" -ForegroundColor Blue
Write-Host "  Dashboard + FAIR + Validation" -ForegroundColor Blue
Write-Host "==========================================" -ForegroundColor Blue
Write-Host ""

# Configuration environnement
$env:NCBI_API_KEY = "a0b0aa017e8720528fb9f89dc68088ce8208"
$env:NCBI_EMAIL = "tommy.lepesteur@hotmail.fr"

Write-Host "[0/3] Configuration environnement..." -ForegroundColor Yellow
Write-Host "  NCBI_API_KEY configurée" -ForegroundColor Green
Write-Host ""

# ÉTAPE 1: Dashboard
Write-Host "[1/3] Génération Dashboard D3.js..." -ForegroundColor Yellow

if (Test-Path "scripts\web\generate_interactive_dashboard.py") {
    python scripts\web\generate_interactive_dashboard.py
    
    if (Test-Path "index_v2_interactive.html") {
        $size = (Get-Item "index_v2_interactive.html").Length / 1KB
        Write-Host "  Dashboard généré: index_v2_interactive.html ($([math]::Round($size,1)) KB)" -ForegroundColor Green
    } else {
        Write-Host "  Dashboard non généré" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "  Script dashboard manquant" -ForegroundColor Red
    exit 1
}

Write-Host ""

# ÉTAPE 2: FAIR
Write-Host "[2/3] Génération Métadonnées FAIR..." -ForegroundColor Yellow

if (Test-Path "scripts\fair\generate_fair_metadata.py") {
    python scripts\fair\generate_fair_metadata.py
    
    if (Test-Path "metadata\fair\codemeta.json") {
        Write-Host "  Métadonnées FAIR générées" -ForegroundColor Green
        Get-ChildItem "metadata\fair" -Filter *.json,*.xml | ForEach-Object {
            Write-Host "    - $($_.Name)" -ForegroundColor Gray
        }
    } else {
        Write-Host "  Métadonnées FAIR non générées" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "  Script FAIR manquant" -ForegroundColor Red
    exit 1
}

Write-Host ""

# ÉTAPE 3: Validation
Write-Host "[3/3] Validation In Vivo..." -ForegroundColor Yellow

if (Test-Path "scripts\qa\in_vivo_validator.py") {
    python scripts\qa\in_vivo_validator.py
    
    if (Test-Path "reports\IN_VIVO_VALIDATION.md") {
        Write-Host "  Rapport validation généré" -ForegroundColor Green
        Write-Host "    - reports\IN_VIVO_VALIDATION.md" -ForegroundColor Gray
    } else {
        Write-Host "  Rapport non généré" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "  Script validation manquant" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "  PHASE 1 COMPLÉTÉE" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""

Write-Host "Prochaines étapes:" -ForegroundColor Yellow
Write-Host "1. Tester dashboard: python -m http.server 8000"
Write-Host "2. Ouvrir: http://localhost:8000/index_v2_interactive.html"
Write-Host ""


