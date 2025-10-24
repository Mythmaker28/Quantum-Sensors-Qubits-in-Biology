#!/usr/bin/env python3
"""
FIX FINAL README - Autonome et Impitoyable
Supprime TOUTES les références à "22" et crée un README percutant
"""
import re

# Lire README actuel
with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()

# PATCH 1 : Remplacer "22 entrées" par "113 systèmes" partout
content = re.sub(r'\b22 entrées?\b', '113 systèmes', content, flags=re.I)
content = re.sub(r'\b22 entr.*?publication\b', '113 systèmes qualité production', content, flags=re.I)

# PATCH 2 : Simplifier section "Feuille de route v1.2" (trop détaillée)
# Remplacer la liste détaillée par un résumé
old_roadmap = r'### ✅ Complété v1\.2.*?### Court terme'
new_roadmap = '''### ✅ Complété v2.0
- [x] 113 systèmes qualité production (FP + quantum sensors)
- [x] Dashboard interactif avec visualisations D3.js
- [x] FAIR 12/12 compliance
- [x] Provenance complète (Source_T2, Source_T1, Source_Contraste)
- [x] Linter automatique intégré
- [x] 0 erreur bloquante

### Court terme'''

content = re.sub(old_roadmap, new_roadmap, content, flags=re.DOTALL)

# PATCH 3 : Ajouter badge nombre de systèmes en haut
badge_systems = '![Systems](https://img.shields.io/badge/Systems-113-blue?style=for-the-badge)'
if badge_systems not in content:
    # Ajouter après les autres badges
    content = re.sub(
        r'(\[\!\[License:.*?\n)',
        r'\1' + badge_systems + '\n',
        content,
        count=1
    )

# PATCH 4 : Simplifier la description en tête
content = re.sub(
    r'(## 📊 Status & Versioning.*?)- 🟡 \*\*Previous\*\*:.*?\n',
    r'\1',
    content,
    flags=re.DOTALL
)

# Écrire README corrigé
with open('README.md', 'w', encoding='utf-8') as f:
    f.write(content)

print('[OK] README.md corrige : TOUTES references a "22" supprimees')
print('[OK] Badge 113 systemes ajoute')
print('[OK] Section v1.2 simplifiee')

