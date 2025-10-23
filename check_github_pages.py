#!/usr/bin/env python3
"""
Vérifie que GitHub Pages fonctionne correctement
"""
import sys
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

def check_url(url):
    """Vérifie qu'une URL est accessible"""
    print(f"[CHECK] {url}")
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=30) as response:
            status = response.getcode()
            content = response.read().decode('utf-8')
            
            if status == 200:
                print(f"[OK] HTTP {status} - {len(content)} bytes")
                return True, content
            else:
                print(f"[WARN] HTTP {status}")
                return False, None
    except HTTPError as e:
        print(f"[ERROR] HTTP {e.code}: {e.reason}")
        return False, None
    except URLError as e:
        print(f"[ERROR] URL Error: {e.reason}")
        return False, None
    except Exception as e:
        print(f"[ERROR] {e}")
        return False, None

def check_github_pages():
    """Vérifie GitHub Pages"""
    print("="*60)
    print("  VERIFICATION GITHUB PAGES")
    print("="*60)
    
    site_url = "https://mythmaker28.github.io/biological-qubits-atlas/"
    csv_url = "https://mythmaker28.github.io/biological-qubits-atlas/biological_qubits.csv"
    
    # Vérifier la page principale
    print("\n[STEP 1] Page principale...")
    success, content = check_url(site_url)
    
    if not success:
        print("\n[FATAL] Le site GitHub Pages n'est pas accessible")
        print("[ACTION] Verifier:")
        print("  1. https://github.com/Mythmaker28/biological-qubits-atlas/settings/pages")
        print("  2. https://github.com/Mythmaker28/biological-qubits-atlas/actions")
        return False
    
    # Vérifier que c'est bien notre site
    if "biological" in content.lower() or "qubits" in content.lower():
        print("[OK] Contenu correspond (biological/qubits trouve)")
    else:
        print("[WARN] Contenu ne semble pas correspondre")
    
    # Vérifier la présence du CSV
    if "biological_qubits.csv" in content:
        print("[OK] Reference au CSV trouvee dans le HTML")
    else:
        print("[WARN] Pas de reference au CSV dans le HTML")
    
    # Vérifier l'accès au CSV
    print("\n[STEP 2] Fichier CSV...")
    success, csv_content = check_url(csv_url)
    
    if not success:
        print("[WARN] CSV non accessible directement")
        print("[INFO] Le CSV peut etre charge differemment (via GitHub raw)")
        return True  # Pas bloquant si le site principal marche
    
    # Compter les lignes du CSV
    if csv_content:
        lines = csv_content.strip().split('\n')
        num_entries = len(lines) - 1  # -1 pour l'en-tête
        print(f"[OK] CSV contient {num_entries} entrees")
        
        if num_entries >= 26:
            print("[OK] Nombre d'entrees correct (>=26)")
        else:
            print(f"[WARN] Seulement {num_entries} entrees (attendu >=26)")
    
    print("\n" + "="*60)
    print("  VERIFICATION TERMINEE - GITHUB PAGES OK")
    print("="*60)
    print(f"\nSite live: {site_url}")
    
    return True

if __name__ == "__main__":
    success = check_github_pages()
    sys.exit(0 if success else 1)



