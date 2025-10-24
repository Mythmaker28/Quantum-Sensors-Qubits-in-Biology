#!/bin/bash
# Script de démarrage rapide — Biological Qubits Atlas v2.0
# Usage: bash start_v2.0.sh [phase]

set -e

YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║   ⚛️  Biological Qubits Atlas v2.0 — Quick Start       ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# === FONCTION: Vérification Python ===
check_python() {
    echo -e "${YELLOW}🔍 Vérification environnement...${NC}"
    
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python 3 non trouvé${NC}"
        echo "   Installation: https://www.python.org/downloads/"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    echo -e "${GREEN}✅ Python ${PYTHON_VERSION} détecté${NC}"
}

# === FONCTION: Installation dépendances ===
install_deps() {
    echo -e "${YELLOW}📦 Installation dépendances...${NC}"
    
    if [ -f "requirements_v2.0.txt" ]; then
        pip3 install -q pandas numpy requests PyYAML
        echo -e "${GREEN}✅ Dépendances core installées${NC}"
        
        read -p "Installer dépendances ML (PyTorch, RDKit) ? [y/N] " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${YELLOW}⏳ Installation ML (peut prendre 5-10 min)...${NC}"
            pip3 install -q torch scikit-learn
            echo -e "${GREEN}✅ Dépendances ML installées${NC}"
        else
            echo -e "${BLUE}ℹ️  ML skippé (optionnel)${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  requirements_v2.0.txt non trouvé${NC}"
        pip3 install pandas numpy requests PyYAML
    fi
}

# === FONCTION: Configuration API ===
setup_api() {
    echo -e "${YELLOW}🔑 Configuration API...${NC}"
    
    if [ -z "$NCBI_API_KEY" ]; then
        echo -e "${BLUE}ℹ️  NCBI_API_KEY non configurée${NC}"
        echo "   Requis pour auto-harvest (Phase 2)"
        echo "   Obtenir clé: https://www.ncbi.nlm.nih.gov/account/"
        echo ""
        read -p "Configurer maintenant ? [y/N] " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            read -p "Clé NCBI: " ncbi_key
            read -p "Email: " ncbi_email
            export NCBI_API_KEY="$ncbi_key"
            export NCBI_EMAIL="$ncbi_email"
            
            # Sauvegarder dans .env
            echo "NCBI_API_KEY=$ncbi_key" > .env
            echo "NCBI_EMAIL=$ncbi_email" >> .env
            echo -e "${GREEN}✅ Configuration sauvegardée dans .env${NC}"
        fi
    else
        echo -e "${GREEN}✅ NCBI_API_KEY déjà configurée${NC}"
    fi
}

# === FONCTION: Phase 1 (Quick Wins) ===
run_phase1() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║   PHASE 1: Quick Wins (10 minutes)                      ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    # 1. FAIR metadata
    echo -e "${YELLOW}🏅 [1/3] Génération métadonnées FAIR...${NC}"
    if [ -f "scripts/fair/generate_fair_metadata.py" ]; then
        python3 scripts/fair/generate_fair_metadata.py
        echo -e "${GREEN}✅ Métadonnées FAIR générées${NC}"
    else
        echo -e "${RED}❌ Script non trouvé: scripts/fair/generate_fair_metadata.py${NC}"
    fi
    
    # 2. Dashboard
    echo -e "${YELLOW}📊 [2/3] Génération dashboard interactif...${NC}"
    if [ -f "scripts/web/generate_interactive_dashboard.py" ]; then
        python3 scripts/web/generate_interactive_dashboard.py
        echo -e "${GREEN}✅ Dashboard généré: index_v2_interactive.html${NC}"
    else
        echo -e "${RED}❌ Script non trouvé: scripts/web/generate_interactive_dashboard.py${NC}"
    fi
    
    # 3. Validation in vivo
    echo -e "${YELLOW}🔬 [3/3] Validation in vivo...${NC}"
    if [ -f "scripts/qa/in_vivo_validator.py" ]; then
        python3 scripts/qa/in_vivo_validator.py
        echo -e "${GREEN}✅ Rapport généré: reports/IN_VIVO_VALIDATION.md${NC}"
    else
        echo -e "${RED}❌ Script non trouvé: scripts/qa/in_vivo_validator.py${NC}"
    fi
    
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║   ✅ PHASE 1 TERMINÉE                                   ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    # Lancer serveur
    echo -e "${BLUE}🌐 Lancement serveur web...${NC}"
    echo -e "${YELLOW}   Ouvrir: http://localhost:8000/index_v2_interactive.html${NC}"
    echo -e "${YELLOW}   Arrêter: Ctrl+C${NC}"
    echo ""
    python3 -m http.server 8000
}

# === FONCTION: Phase 2 (Expansion) ===
run_phase2() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║   PHASE 2: Expansion (auto-harvest)                     ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    if [ -z "$NCBI_API_KEY" ]; then
        echo -e "${RED}❌ NCBI_API_KEY requise pour Phase 2${NC}"
        echo "   Lancer: bash start_v2.0.sh setup"
        exit 1
    fi
    
    echo -e "${YELLOW}🔍 Auto-extraction PubMed/FPbase...${NC}"
    if [ -f "scripts/automation/auto_harvest_v2.py" ]; then
        python3 scripts/automation/auto_harvest_v2.py
        echo -e "${GREEN}✅ Candidats extraits: data/interim/auto_harvest_v2.csv${NC}"
        echo -e "${BLUE}ℹ️  Validation manuelle requise avant merge${NC}"
    else
        echo -e "${RED}❌ Script non trouvé${NC}"
    fi
}

# === FONCTION: Tests ===
run_tests() {
    echo -e "${YELLOW}🧪 Lancement tests...${NC}"
    
    if command -v pytest &> /dev/null; then
        pytest tests/test_v2_installation.py -v
    else
        echo -e "${BLUE}ℹ️  pytest non installé, utilisation python${NC}"
        python3 tests/test_v2_installation.py
    fi
}

# === FONCTION: Aide ===
show_help() {
    echo "Usage: bash start_v2.0.sh [commande]"
    echo ""
    echo "Commandes disponibles:"
    echo "  setup      Configuration initiale (deps + API)"
    echo "  phase1     Quick Wins (FAIR + Dashboard + Validation)"
    echo "  phase2     Expansion (auto-harvest PubMed)"
    echo "  test       Tests validation installation"
    echo "  serve      Lance serveur web uniquement"
    echo "  help       Affiche cette aide"
    echo ""
    echo "Exemples:"
    echo "  bash start_v2.0.sh setup"
    echo "  bash start_v2.0.sh phase1"
}

# === MAIN ===
case "${1:-setup}" in
    setup)
        check_python
        install_deps
        setup_api
        echo -e "${GREEN}"
        echo "╔══════════════════════════════════════════════════════════╗"
        echo "║   ✅ SETUP TERMINÉ                                      ║"
        echo "║   Prochaine étape: bash start_v2.0.sh phase1           ║"
        echo "╚══════════════════════════════════════════════════════════╝"
        echo -e "${NC}"
        ;;
    
    phase1)
        check_python
        run_phase1
        ;;
    
    phase2)
        check_python
        run_phase2
        ;;
    
    test)
        check_python
        run_tests
        ;;
    
    serve)
        echo -e "${BLUE}🌐 Serveur web (Ctrl+C pour arrêter)${NC}"
        echo -e "${YELLOW}   URL: http://localhost:8000/${NC}"
        python3 -m http.server 8000
        ;;
    
    help|--help|-h)
        show_help
        ;;
    
    *)
        echo -e "${RED}❌ Commande inconnue: $1${NC}"
        show_help
        exit 1
        ;;
esac


