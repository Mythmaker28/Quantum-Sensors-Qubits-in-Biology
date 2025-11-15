#!/usr/bin/env python3
"""
🔥 AGENT 1 - DATA & BACKEND
Biological Qubits Atlas - Système 2 agents

RESPONSABILITÉS:
- Structure de données (CSV, JSON, SQLite)
- Scripts de parsing/extraction
- Base de données des systèmes biologiques
- Backend/API si nécessaire

FICHIERS ASSIGNÉS:
- data/*.csv
- src/data_processing.py
- src/database.py
- src/parsers.py
"""

import os
import sys
import time
from pathlib import Path

# Ajouter le module conversation-bus au path
sys.path.insert(0, str(Path(__file__).parent / "conversation-bus-module"))

from conversation_bus import ConversationBus

# ============================================================================
# CONFIGURATION
# ============================================================================
AGENT_NAME = "AGENT-1"
AGENT_ROLE = "backend"
PROJECT_NAME = "biological-qubits-atlas"

# Zones de responsabilité
MY_ZONES = ["data/", "src/"]
MY_FILES_PATTERN = ["data/*.csv", "src/data_processing.py", "src/database.py", "src/parsers.py"]

# ============================================================================
# INITIALISATION
# ============================================================================

print("=" * 80)
print("🚀 DÉMARRAGE AGENT 1 - DATA & BACKEND")
print("=" * 80)

# Créer le bus
bus = ConversationBus(PROJECT_NAME, AGENT_NAME, AGENT_ROLE)
print(f"✅ Bus de communication initialisé")

# ============================================================================
# ÉTAPE 1: SYNC - VÉRIFIER QUI EST LÀ
# ============================================================================

print("\n" + "=" * 80)
print("📡 ÉTAPE 1: SYNCHRONISATION")
print("=" * 80)

ctx = bus.get_context()
print(f"\n📊 Contexte actuel:")
print(f"   - Agents actifs: {ctx['active_agents']}")
print(f"   - Messages totaux: {ctx['total_messages']}")
print(f"   - Dernier cycle: {ctx['last_cycle']}")

# Lire les 20 derniers messages
recent = bus.read_messages(limit=20)
print(f"\n📨 {len(recent)} messages récents trouvés")

if recent:
    print("\n📋 Dernières activités:")
    for msg in recent[:5]:  # Afficher seulement les 5 plus récents
        timestamp = msg['timestamp'][:19]  # Couper les microsecondes
        agent = msg['agent']
        message_preview = msg['message'][:60].replace('\n', ' ')
        files = msg.get('files_intent', [])
        print(f"   [{timestamp}] {agent}: {message_preview}...")
        if files:
            print(f"      → Fichiers: {', '.join(files)}")

# Vérifier le nombre d'agents
if len(ctx['active_agents']) > 2:
    print("\n⚠️  ERREUR: Trop d'agents détectés!")
    print(f"   Agents actifs: {ctx['active_agents']}")
    print("   SEULEMENT 2 AGENTS SONT AUTORISÉS!")
    sys.exit(1)

# ============================================================================
# ÉTAPE 2: ANNONCER MA PRÉSENCE ET MES ZONES
# ============================================================================

print("\n" + "=" * 80)
print("📢 ÉTAPE 2: ANNONCE")
print("=" * 80)

# Vérifier ce que l'autre agent fait
other_agent_files = []
for msg in recent:
    if msg['agent'] != AGENT_NAME:
        other_agent_files.extend(msg.get('files_intent', []))

if other_agent_files:
    print(f"\n⚠️  L'autre agent travaille sur: {set(other_agent_files)}")

# Poster mon message de sync
sync_msg = f"""🔵 SYNC - Agent 1 (Backend & Data)

Agents actifs: {ctx['active_agents']}

🎯 JE PRENDS EN CHARGE:
   - data/ (tous les fichiers CSV)
   - src/data_processing.py
   - src/database.py  
   - src/parsers.py

@AGENT-2: Tu prends docs/ et analysis/ OK?

ATTENTE CONFIRMATION...
"""

bus.post(sync_msg, actions=["sync"])
print("\n✅ Message de synchronisation posté")
print("\n📝 Mon message:")
print(sync_msg)

# ============================================================================
# ÉTAPE 3: ATTENDRE CONFIRMATION (3 MINUTES MAX)
# ============================================================================

print("\n" + "=" * 80)
print("⏳ ÉTAPE 3: ATTENTE CONFIRMATION")
print("=" * 80)
print("\n⏱️  Attente de 3 minutes pour confirmation de l'autre agent...")
print("   (Vous pouvez interrompre avec Ctrl+C si l'autre agent a déjà répondu)")

wait_time = 180  # 3 minutes
start_wait = time.time()

try:
    while (time.time() - start_wait) < wait_time:
        time.sleep(10)  # Vérifier toutes les 10 secondes
        
        # Relire les messages
        recent = bus.read_messages(limit=10)
        
        # Chercher une réponse de l'autre agent
        for msg in recent:
            if msg['agent'] != AGENT_NAME and msg['timestamp'] > sync_msg:
                if any(action in msg.get('actions', []) for action in ["agree", "sync", "negotiate"]):
                    print(f"\n✅ Réponse reçue de {msg['agent']}!")
                    print(f"   Message: {msg['message'][:100]}")
                    
                    # Vérifier si conflit
                    if "negotiate" in msg.get('actions', []) or "conflict" in msg.get('actions', []):
                        print("\n⚠️  CONFLIT DÉTECTÉ! Négociation nécessaire.")
                        print(f"   Message de {msg['agent']}: {msg['message']}")
                        response = input("\n➡️  Voulez-vous continuer quand même? (y/n): ")
                        if response.lower() != 'y':
                            sys.exit(0)
                    
                    # Sortir de la boucle d'attente
                    raise KeyboardInterrupt
        
        elapsed = int(time.time() - start_wait)
        remaining = wait_time - elapsed
        print(f"   ... {remaining}s restantes", end='\r')
        
except KeyboardInterrupt:
    print("\n✅ Attente interrompue (confirmation reçue ou manuelle)")

print("\n✅ Phase de synchronisation terminée")

# ============================================================================
# ÉTAPE 4: FONCTIONS UTILES POUR LE TRAVAIL
# ============================================================================

def check_file_before_work(filepath):
    """
    Vérifie si un autre agent travaille sur ce fichier
    Retourne True si OK, False si conflit
    """
    # Vérifier si le fichier existe
    if os.path.exists(filepath):
        print(f"⚠️  {filepath} existe déjà!")
    
    # Vérifier dans les messages récents
    recent = bus.read_messages(limit=30)
    for msg in recent:
        if msg['agent'] != AGENT_NAME:
            if filepath in msg.get('files_intent', []):
                print(f"⚠️  {msg['agent']} travaille sur {filepath}!")
                bus.post(
                    f"⚠️ CONFLIT détecté: {msg['agent']} travaille déjà sur {filepath}. Je fais autre chose.",
                    actions=["conflict"]
                )
                return False
    
    # OK, personne ne travaille dessus
    bus.post(f"Je commence à travailler sur {filepath}", files_intent=[filepath])
    print(f"✅ Aucun conflit pour {filepath}")
    return True


def announce_work(filepath, description):
    """Annoncer qu'on commence à travailler sur un fichier"""
    print(f"\n📝 Annonce: {description}")
    print(f"   Fichier: {filepath}")
    
    if not check_file_before_work(filepath):
        return False
    
    bus.post(
        f"Je commence: {filepath} - {description}",
        files_intent=[filepath]
    )
    print("✅ Travail annoncé")
    return True


def checkpoint(task_name, progress_pct):
    """Envoyer un checkpoint"""
    msg = f"⏱️ CHECKPOINT - {task_name} à {progress_pct}%"
    print(f"\n{msg}")
    bus.post(msg, actions=["checkpoint"])


def work_complete(filepath, summary):
    """Confirmer qu'un travail est terminé"""
    msg = f"✅ TERMINÉ: {filepath}\n\n{summary}"
    print(f"\n{msg}")
    bus.post(msg, files_intent=[filepath], actions=["complete"])


# ============================================================================
# ÉTAPE 5: INSTRUCTIONS POUR LE TRAVAIL
# ============================================================================

print("\n" + "=" * 80)
print("🎯 ÉTAPE 5: PRÊT À TRAVAILLER")
print("=" * 80)

print("""
✅ Agent 1 (Backend & Data) est prêt!

🎯 VOS TÂCHES PRIORITAIRES:
   1. Créer schéma base de données (SQLite ou CSV)
   2. Parser pour extraire données de papers
   3. Scripts d'import/export
   4. Validation des données

📁 VOS FICHIERS:
   - data/*.csv
   - src/data_processing.py
   - src/database.py
   - src/parsers.py

🔧 FONCTIONS DISPONIBLES:
   - announce_work(filepath, description)  → Annoncer avant de coder
   - checkpoint(task_name, progress_pct)    → Checkpoint toutes les 15 min
   - work_complete(filepath, summary)       → Confirmer quand terminé
   - check_file_before_work(filepath)       → Vérifier conflits

⚠️  RÈGLES:
   1. TOUJOURS annoncer avant de coder un fichier
   2. Checkpoint OBLIGATOIRE toutes les 15 minutes
   3. NE JAMAIS toucher aux fichiers de l'autre agent
   4. Relire le bus toutes les 5 minutes

📖 EXEMPLE D'UTILISATION:

   # 1. Annoncer
   if announce_work("src/database.py", "Création schéma SQLite"):
       
       # 2. Faire le travail
       # ... votre code ici ...
       
       # 3. Checkpoint si > 15 min
       checkpoint("database.py", 50)
       
       # 4. Confirmer
       work_complete("src/database.py", "Schéma créé avec 5 tables")

🚀 Vous pouvez maintenant commencer à coder!
   Utilisez les fonctions ci-dessus ou codez directement.
""")

# ============================================================================
# BOUCLE INTERACTIVE (OPTIONNEL)
# ============================================================================

print("\n💡 Mode interactif disponible (tapez 'help' pour les commandes)")
print("   Ou fermez ce script et commencez à coder!\n")

while True:
    try:
        cmd = input("agent-1> ").strip().lower()
        
        if cmd == "help":
            print("""
Commandes disponibles:
  status    - Voir le statut du bus
  read      - Lire les derniers messages
  announce  - Annoncer un fichier
  checkpoint - Envoyer un checkpoint
  complete  - Marquer un fichier comme terminé
  exit/quit - Quitter
            """)
        
        elif cmd == "status":
            ctx = bus.get_context()
            print(f"\n📊 Statut:")
            print(f"   Agents actifs: {ctx['active_agents']}")
            print(f"   Messages: {ctx['total_messages']}")
            print(f"   Cycle: {ctx['last_cycle']}")
        
        elif cmd == "read":
            recent = bus.read_messages(limit=10)
            print(f"\n📨 {len(recent)} derniers messages:")
            for msg in recent:
                print(f"\n[{msg['agent']}] {msg['message'][:100]}")
                if msg.get('files_intent'):
                    print(f"  → Fichiers: {', '.join(msg['files_intent'])}")
        
        elif cmd == "announce":
            filepath = input("  Fichier: ").strip()
            desc = input("  Description: ").strip()
            announce_work(filepath, desc)
        
        elif cmd == "checkpoint":
            task = input("  Tâche: ").strip()
            progress = input("  Progression (%): ").strip()
            checkpoint(task, progress)
        
        elif cmd == "complete":
            filepath = input("  Fichier: ").strip()
            summary = input("  Résumé: ").strip()
            work_complete(filepath, summary)
        
        elif cmd in ["exit", "quit"]:
            print("\n👋 Au revoir!")
            break
        
        elif cmd == "":
            continue
        
        else:
            print(f"❌ Commande inconnue: {cmd}")
            print("   Tapez 'help' pour voir les commandes")
    
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Au revoir!")
        break
    except EOFError:
        break

