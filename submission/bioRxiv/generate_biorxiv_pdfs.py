#!/usr/bin/env python3
"""
Génère les PDFs bioRxiv depuis Markdown
Conforme specs: polices intégrées, 300 dpi, A4/Letter, ABSTRACT header

Dépendances:
  pip install markdown weasyprint
  OU
  pandoc (externe): https://pandoc.org/installing.html

Licence: MIT
"""

import os
import subprocess
import sys
from pathlib import Path

def check_pandoc():
    """Vérifie si pandoc est installé"""
    try:
        result = subprocess.run(['pandoc', '--version'], 
                                capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def generate_with_pandoc(md_file, pdf_file, title=""):
    """Génère PDF avec pandoc (méthode recommandée)"""
    cmd = [
        'pandoc',
        md_file,
        '-o', pdf_file,
        '--pdf-engine=xelatex',  # Meilleure gestion polices
        '--variable', 'geometry:margin=1in',
        '--variable', 'fontsize=11pt',
        '--variable', 'linestretch=1.5',
        '--number-sections',
        '--toc',
        '--metadata', f'title={title}' if title else 'title=Manuscript'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ Généré avec pandoc: {pdf_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur pandoc: {e.stderr}")
        return False

def generate_with_weasyprint(md_file, pdf_file):
    """Génère PDF avec weasyprint (fallback)"""
    try:
        import markdown
        from weasyprint import HTML, CSS
        from weasyprint.text.fonts import FontConfiguration
        
        # Lire Markdown
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convertir MD → HTML
        html_content = markdown.markdown(
            md_content,
            extensions=['tables', 'fenced_code', 'toc']
        )
        
        # Style CSS pour bioRxiv
        css_content = """
        @page {
            size: A4;
            margin: 2.5cm;
        }
        
        body {
            font-family: 'Times New Roman', Times, serif;
            font-size: 11pt;
            line-height: 1.5;
            color: #000;
        }
        
        h1 {
            font-size: 16pt;
            font-weight: bold;
            margin-top: 1em;
            margin-bottom: 0.5em;
            text-align: center;
        }
        
        h2 {
            font-size: 14pt;
            font-weight: bold;
            margin-top: 1em;
            margin-bottom: 0.5em;
            border-bottom: 1px solid #ccc;
        }
        
        h3 {
            font-size: 12pt;
            font-weight: bold;
            margin-top: 0.8em;
            margin-bottom: 0.4em;
        }
        
        p {
            margin-bottom: 0.5em;
            text-align: justify;
        }
        
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
            font-size: 10pt;
        }
        
        th, td {
            border: 1px solid #000;
            padding: 8px;
            text-align: left;
        }
        
        th {
            background-color: #f0f0f0;
            font-weight: bold;
        }
        
        code {
            font-family: 'Courier New', Courier, monospace;
            font-size: 10pt;
            background-color: #f5f5f5;
            padding: 2px 4px;
        }
        
        pre {
            font-family: 'Courier New', Courier, monospace;
            font-size: 9pt;
            background-color: #f5f5f5;
            padding: 10px;
            border: 1px solid #ccc;
            overflow-x: auto;
        }
        
        a {
            color: #0066cc;
            text-decoration: none;
        }
        
        .figure-caption {
            font-size: 10pt;
            font-style: italic;
            margin-top: 0.5em;
        }
        """
        
        # HTML wrapper
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>BioRxiv Manuscript</title>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        # Générer PDF
        font_config = FontConfiguration()
        html = HTML(string=full_html)
        css = CSS(string=css_content, font_config=font_config)
        
        html.write_pdf(pdf_file, stylesheets=[css], font_config=font_config)
        print(f"✅ Généré avec weasyprint: {pdf_file}")
        return True
        
    except ImportError:
        print("❌ weasyprint non installé")
        print("   Installation: pip install markdown weasyprint")
        return False
    except Exception as e:
        print(f"❌ Erreur weasyprint: {e}")
        return False

def main():
    """Pipeline principal"""
    
    # Chemins
    base_dir = Path(__file__).parent
    manuscript_md = base_dir / "BQA_manuscript_bioRxiv.md"
    supplement_md = base_dir / "BQA_Supplement_bioRxiv.md"
    
    manuscript_pdf = base_dir / "BQA_manuscript_bioRxiv.pdf"
    supplement_pdf = base_dir / "BQA_Supplement_bioRxiv.pdf"
    
    # Vérifier fichiers source
    if not manuscript_md.exists():
        print(f"❌ Fichier manquant: {manuscript_md}")
        return 1
    
    print("🔨 Génération PDFs bioRxiv...")
    print("="*60)
    
    # Méthode 1: Pandoc (recommandé)
    if check_pandoc():
        print("✅ Pandoc détecté (méthode recommandée)")
        
        success_manuscript = generate_with_pandoc(
            str(manuscript_md),
            str(manuscript_pdf),
            title="Biological Qubits Atlas"
        )
        
        success_supplement = False
        if supplement_md.exists():
            success_supplement = generate_with_pandoc(
                str(supplement_md),
                str(supplement_pdf),
                title="Supplementary Materials"
            )
        
        if success_manuscript:
            print(f"\n✅ MANUSCRIT: {manuscript_pdf}")
            if success_supplement:
                print(f"✅ SUPPLÉMENT: {supplement_pdf}")
            return 0
    
    # Méthode 2: Weasyprint (fallback)
    else:
        print("⚠️  Pandoc non trouvé, essai weasyprint...")
        
        success_manuscript = generate_with_weasyprint(
            str(manuscript_md),
            str(manuscript_pdf)
        )
        
        success_supplement = False
        if supplement_md.exists():
            success_supplement = generate_with_weasyprint(
                str(supplement_md),
                str(supplement_pdf)
            )
        
        if success_manuscript:
            print(f"\n✅ MANUSCRIT: {manuscript_pdf}")
            if success_supplement:
                print(f"✅ SUPPLÉMENT: {supplement_pdf}")
            return 0
    
    # Échec
    print("\n❌ Génération PDF échouée")
    print("\n📚 Solutions:")
    print("1. Installer pandoc: https://pandoc.org/installing.html")
    print("   Windows: winget install pandoc")
    print("   macOS: brew install pandoc")
    print("   Linux: sudo apt install pandoc texlive-xetex")
    print("\n2. OU installer weasyprint:")
    print("   pip install markdown weasyprint")
    print("\n3. OU conversion manuelle:")
    print(f"   pandoc {manuscript_md} -o {manuscript_pdf}")
    
    return 1

if __name__ == "__main__":
    sys.exit(main())

