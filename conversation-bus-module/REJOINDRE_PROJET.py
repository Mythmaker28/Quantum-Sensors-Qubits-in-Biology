#!/usr/bin/env python3
"""
Script ULTRA-SIMPLE pour rejoindre Biological Qubits Atlas
Modifie juste ton nom en haut et lance!
"""

import sys
from pathlib import Path
from datetime import datetime
import json

# ============================================================================
# ✏️ MODIFIE ICI TON NOM ET TON RÔLE
# ============================================================================
MON_NOM = "TON-AGENT-NAME"  # Ex: GPT-DOCS, GEMINI-VIZ, CHATGPT-STATS
MON_ROLE = "ton-role"        # Ex: documentation, analysis, visualization

# ============================================================================
# NE TOUCHE PAS EN-DESSOUS
# ============================================================================

print("=" * 80)
print(f"🤖 {MON_NOM} rejoint Biological Qubits Atlas")
print("=" * 80)

# Import du bus
sys.path.insert(0, str(Path(__file__).parent / 'conversation-bus-module'))
from conversation_bus import ConversationBus

# Connexion
print("\n🚌 Connexion au bus...")
bus = ConversationBus('biological-qubits-atlas', MON_NOM, MON_ROLE)

# État actuel
ctx = bus.get_context()
print(f"\n📊 État du bus:")
print(f"   Agents actifs: {ctx['active_agents']}")
print(f"   Messages: {ctx['total_messages']}")
print(f"   Dernier cycle: {ctx['last_cycle']}")

# Lire messages récents
print(f"\n📬 Derniers messages:")
msgs = bus.read_messages(limit=5)
for m in msgs[-3:]:
    print(f"   [{m['agent']}] {m['message'][:80]}...")

# ============================================================================
# ✏️ TON MESSAGE ICI
# ============================================================================
mon_message = f"""CYCLE {ctx['last_cycle'] + 1} - {MON_NOM} ARRIVE!

Salut CLAUDE-DATA!

J'ai lu le bus. Je vois que:
- CLAUDE-LIT-ANALYST a analysé 37 papers (23 systèmes catalogués)
- Toi tu vas faire data/ et src/ (base de données + backend)

💼 MOI JE PROPOSE DE FAIRE:

[ÉCRIS ICI TON PLAN - Exemples:]

Option A - DOCUMENTATION:
- docs/photosynthesis.md (FMO complex, PSII, etc.)
- docs/magnetoreception.md (cryptochrome, radical pairs)
- docs/nv_centers.md (centres azote-lacune)
- README.md complet

Option B - ANALYSE:
- analysis/stats.py (statistiques sur les systèmes)
- analysis/compare.py (comparaisons cohérence/température)
- analysis/trends.py (tendances par catégorie)

Option C - VISUALISATION:
- viz/plots.py (graphiques cohérence vs température)
- viz/categories.py (distribution par catégorie)
- viz/timeline.py (découvertes chronologiques)

[CHOISIS ET PRÉCISE]

🤝 ON SE COORDONNE:
Tu fais data/ et src/, moi je fais [TA ZONE].
On évite les conflits, on se parle sur le bus!

OK pour toi?
"""

# Poster au bus
print(f"\n{'='*80}")
print("📤 Posting au bus...")
print("="*80)

bus.post(mon_message, actions=['join', 'accept', 'propose'])

print("✅ Message posté!")
print("\nContenu:")
print(mon_message)

print(f"\n{'='*80}")
print("🎉 TU ES SUR LE BUS!")
print("="*80)
print("\nProchaines étapes:")
print("1. Attends la réponse de CLAUDE-DATA (5-10 min)")
print("2. Lis les messages: bus.read_messages(limit=10)")
print("3. Commence à bosser sur ta zone")
print("4. Annonce chaque fichier: bus.post('Je crée X', files_intent=['X'])")
print("5. Update toutes les 15-20 min")
print("\n💬 Communication:")
print("   bus.post('Mon message')")
print("   bus.read_messages(limit=10)")
print("   bus.get_context()")
print("\n✅ C'est parti!")
print("="*80)

