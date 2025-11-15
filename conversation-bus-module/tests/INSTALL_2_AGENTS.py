#!/usr/bin/env python3
"""
🔥 INSTALLATION ET VÉRIFICATION - SYSTÈME 2 AGENTS
Biological Qubits Atlas

Ce script vérifie que tout est prêt pour démarrer les 2 agents.
"""

import os
import sys
from pathlib import Path

print("=" * 80)
print("🔥 INSTALLATION ET VÉRIFICATION - SYSTÈME 2 AGENTS")
print("=" * 80)

# ============================================================================
# VÉRIFICATION 1: Module conversation_bus
# ============================================================================

print("\n📦 VÉRIFICATION 1: Module conversation_bus")
print("-" * 80)

conversation_bus_path = Path("conversation-bus-module/conversation_bus.py")

if conversation_bus_path.exists():
    print(f"✅ Module trouvé: {conversation_bus_path}")
    
    # Essayer de l'importer
    sys.path.insert(0, str(Path("conversation-bus-module")))
    try:
        from conversation_bus import ConversationBus
        print("✅ Import réussi: ConversationBus")
        
        # Tester l'initialisation
        test_bus = ConversationBus("test-install", "test-agent", "tester")
        print("✅ Initialisation réussie")
        
        # Nettoyer le test
        import shutil
        test_dir = Path.home() / ".conversation_bus" / "test-install"
        if test_dir.exists():
            shutil.rmtree(test_dir)
            print("✅ Test nettoyé")
        
    except Exception as e:
        print(f"❌ ERREUR lors de l'import: {e}")
        sys.exit(1)
else:
    print(f"❌ Module NON TROUVÉ: {conversation_bus_path}")
    print("\n💡 Solution:")
    print("   Le module doit être dans: conversation-bus-module/conversation_bus.py")
    sys.exit(1)

# ============================================================================
# VÉRIFICATION 2: Scripts agents
# ============================================================================

print("\n🤖 VÉRIFICATION 2: Scripts agents")
print("-" * 80)

agent_scripts = {
    "start_agent_1_backend.py": "Agent 1 (Backend & Data)",
    "start_agent_2_analysis.py": "Agent 2 (Analysis & Docs)"
}

all_scripts_ok = True
for script, desc in agent_scripts.items():
    if Path(script).exists():
        print(f"✅ {desc}: {script}")
    else:
        print(f"❌ {desc}: {script} NON TROUVÉ")
        all_scripts_ok = False

if not all_scripts_ok:
    print("\n💡 Solution:")
    print("   Créez les scripts manquants dans le répertoire courant")
    sys.exit(1)

# ============================================================================
# VÉRIFICATION 3: Structure du projet
# ============================================================================

print("\n📁 VÉRIFICATION 3: Structure du projet")
print("-" * 80)

directories_to_check = {
    "data/": "Données (Agent 1)",
    "docs/": "Documentation (Agent 2)",
    "atlas/": "Atlas existant"
}

for directory, desc in directories_to_check.items():
    dir_path = Path(directory)
    if dir_path.exists() and dir_path.is_dir():
        print(f"✅ {desc}: {directory}")
    else:
        print(f"⚠️  {desc}: {directory} n'existe pas (sera créé si nécessaire)")

# ============================================================================
# VÉRIFICATION 4: Python version
# ============================================================================

print("\n🐍 VÉRIFICATION 4: Python")
print("-" * 80)

python_version = sys.version_info
print(f"Version Python: {python_version.major}.{python_version.minor}.{python_version.micro}")

if python_version.major >= 3 and python_version.minor >= 7:
    print("✅ Version Python compatible (>= 3.7)")
else:
    print("❌ Version Python trop ancienne (requiert >= 3.7)")
    sys.exit(1)

# ============================================================================
# VÉRIFICATION 5: Espace disque
# ============================================================================

print("\n💾 VÉRIFICATION 5: Espace disque")
print("-" * 80)

bus_dir = Path.home() / ".conversation_bus"
print(f"Répertoire bus: {bus_dir}")

if bus_dir.exists():
    # Compter les fichiers
    import os
    file_count = sum(1 for _ in bus_dir.rglob("*.json"))
    print(f"✅ Répertoire existe ({file_count} messages existants)")
else:
    print(f"ℹ️  Répertoire sera créé au premier démarrage")

# ============================================================================
# RÉSUMÉ
# ============================================================================

print("\n" + "=" * 80)
print("📊 RÉSUMÉ DE L'INSTALLATION")
print("=" * 80)

print("""
✅ Tous les prérequis sont satisfaits!

🚀 PROCHAINES ÉTAPES:

1. DÉMARRER AGENT 1 (Backend & Data):
   
   python start_agent_1_backend.py
   
   Responsabilités:
   - data/*.csv
   - src/data_processing.py
   - src/database.py
   - src/parsers.py

2. DÉMARRER AGENT 2 (Analysis & Docs) dans un autre terminal:
   
   python start_agent_2_analysis.py
   
   Responsabilités:
   - docs/*.md
   - analysis/*.py
   - viz/*.py
   - README.md

⚠️  RÈGLES IMPORTANTES:

   1. SEULEMENT 2 AGENTS simultanés
   2. Chaque agent doit ANNONCER avant de coder
   3. Checkpoint OBLIGATOIRE toutes les 15 minutes
   4. NE JAMAIS toucher aux fichiers de l'autre
   5. Vérifier le bus toutes les 5 minutes

📖 WORKFLOW:

   1. LIRE le bus (messages récents)
   2. ANNONCER le fichier exact
   3. ATTENDRE 3 minutes (vérifier conflits)
   4. CODER (max 15 min avant checkpoint)
   5. CHECKPOINT si > 15 min
   6. CONFIRMER quand terminé
   7. RETOUR à l'étape 1

🔍 MONITORING:

   Voir les messages du bus:
   - Depuis les scripts agents (commande "read")
   - Directement dans: ~/.conversation_bus/biological-qubits-atlas/

💡 EN CAS DE PROBLÈME:

   - Si duplication détectée: Arrêter immédiatement et négocier
   - Si conflit de fichiers: Poster sur le bus avec action=["conflict"]
   - Si bloqué: Demander aide sur le bus avec action=["help"]

🎯 OBJECTIF:

   CODE UTILE, PAS DE RAPPORTS, PAS DE DUPLICATION!
""")

print("\n" + "=" * 80)
print("✅ Installation vérifiée avec succès!")
print("=" * 80)
print("\n🚀 Vous pouvez maintenant démarrer les agents.\n")

