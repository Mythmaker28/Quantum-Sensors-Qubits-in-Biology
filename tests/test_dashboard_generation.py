#!/usr/bin/env python3
"""
Tests unitaires pour génération dashboard D3.js
Licence: Apache-2.0
"""

import pytest
import os
import subprocess
from pathlib import Path

class TestDashboardGeneration:
    """Tests génération dashboard interactif"""
    
    def test_script_exists(self):
        """Vérifie existence script génération"""
        script = Path("scripts/web/generate_interactive_dashboard.py")
        assert script.exists(), "Script dashboard manquant"
        assert script.is_file(), "Chemin invalide"
    
    def test_atlas_dataset_exists(self):
        """Vérifie dataset source existe"""
        atlas = Path("data/processed/atlas_fp_optical_v1_3.csv")
        
        if not atlas.exists():
            pytest.skip("Dataset v1.3 non trouvé (normal si test isolé)")
        
        assert atlas.stat().st_size > 1000, "Dataset trop petit"
    
    def test_dashboard_generation_success(self):
        """Test génération dashboard complète"""
        script = Path("scripts/web/generate_interactive_dashboard.py")
        
        if not script.exists():
            pytest.skip("Script dashboard manquant")
        
        # Exécuter script
        result = subprocess.run(
            ["python", str(script)],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        
        # Vérifier exécution réussie
        assert result.returncode == 0, f"Erreur génération: {result.stderr}"
        
        # Vérifier output
        assert "Dashboard généré" in result.stdout or "✅" in result.stdout, "Pas de confirmation génération"
    
    def test_dashboard_html_exists(self):
        """Vérifie fichier HTML généré"""
        dashboard = Path("index_v2_interactive.html")
        
        if not dashboard.exists():
            pytest.skip("Dashboard non généré (exécuter script d'abord)")
        
        # Taille minimale (doit contenir D3.js code)
        assert dashboard.stat().st_size > 10000, "Dashboard trop petit (<10KB)"
    
    def test_dashboard_content_validity(self):
        """Vérifie contenu HTML valide"""
        dashboard = Path("index_v2_interactive.html")
        
        if not dashboard.exists():
            pytest.skip("Dashboard non généré")
        
        content = dashboard.read_text(encoding='utf-8')
        
        # Vérifications critiques
        assert "<!DOCTYPE html>" in content, "DOCTYPE HTML manquant"
        assert "<html" in content, "Balise HTML manquante"
        assert "</html>" in content, "Balise HTML fermante manquante"
    
    def test_dashboard_d3js_integration(self):
        """Vérifie intégration D3.js"""
        dashboard = Path("index_v2_interactive.html")
        
        if not dashboard.exists():
            pytest.skip("Dashboard non généré")
        
        content = dashboard.read_text(encoding='utf-8')
        
        # D3.js CDN
        assert "d3.js" in content.lower() or "d3.v7" in content, "D3.js CDN manquant"
        
        # Scripts D3.js
        assert "<script" in content, "Balise script manquante"
        assert "d3.select" in content or "const data" in content, "Code D3.js manquant"
    
    def test_dashboard_visualizations(self):
        """Vérifie visualisations présentes"""
        dashboard = Path("index_v2_interactive.html")
        
        if not dashboard.exists():
            pytest.skip("Dashboard non généré")
        
        content = dashboard.read_text(encoding='utf-8')
        
        # Scatter plot
        assert "scatter" in content.lower() or "scatter-t2-temp" in content, "Scatter plot T2 vs Temp manquant"
        
        # Barplot
        assert "bar" in content.lower() or "bar-families" in content, "Barplot familles manquant"
    
    def test_dashboard_responsiveness(self):
        """Vérifie responsive design"""
        dashboard = Path("index_v2_interactive.html")
        
        if not dashboard.exists():
            pytest.skip("Dashboard non généré")
        
        content = dashboard.read_text(encoding='utf-8')
        
        # Meta viewport
        assert "viewport" in content, "Meta viewport manquant (non-responsive)"
        assert "width=device-width" in content, "Viewport width manquant"
    
    def test_dashboard_stats_display(self):
        """Vérifie affichage statistiques"""
        dashboard = Path("index_v2_interactive.html")
        
        if not dashboard.exists():
            pytest.skip("Dashboard non généré")
        
        content = dashboard.read_text(encoding='utf-8')
        
        # Statistiques temps réel
        assert "stat" in content.lower() or "stats" in content.lower(), "Section stats manquante"

class TestDashboardPerformance:
    """Tests performance dashboard"""
    
    def test_html_size_reasonable(self):
        """Vérifie taille HTML raisonnable"""
        dashboard = Path("index_v2_interactive.html")
        
        if not dashboard.exists():
            pytest.skip("Dashboard non généré")
        
        size_kb = dashboard.stat().st_size / 1024
        
        # Taille raisonnable : 10 KB - 500 KB
        assert 10 < size_kb < 500, f"Taille anormale: {size_kb:.1f} KB"
    
    def test_no_external_dependencies_except_d3(self):
        """Vérifie pas de dépendances externes sauf D3.js"""
        dashboard = Path("index_v2_interactive.html")
        
        if not dashboard.exists():
            pytest.skip("Dashboard non généré")
        
        content = dashboard.read_text(encoding='utf-8')
        
        # D3.js via CDN est OK
        # Mais pas d'autres CDN (jQuery, Bootstrap, etc.)
        assert "jquery" not in content.lower(), "jQuery non requis (éviter bloat)"
        assert "bootstrap" not in content.lower(), "Bootstrap non requis"

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])


