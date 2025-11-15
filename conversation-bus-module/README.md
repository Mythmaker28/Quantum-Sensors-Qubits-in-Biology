# 🚌 Conversation Bus Module

**Module de coordination simple pour agents IA multi-agents**

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](pyproject.toml)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](pyproject.toml)
[![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)](LICENSE)
[![Dependencies](https://img.shields.io/badge/dependencies-stdlib%20only-success.svg)](#)

---

## 📋 Table des Matières

- [Vue d'Ensemble](#vue-densemble)
- [Installation](#installation)
- [Démarrage Rapide](#démarrage-rapide)
- [API Complète](#api-complète)
- [Cas d'Usage](#cas-dusage)
- [Architecture](#architecture)
- [FAQ](#faq)

---

## 🎯 Vue d'Ensemble

Le **Conversation Bus** est un module Python léger pour coordonner plusieurs agents IA travaillant sur le même projet. Il résout les problèmes courants de coordination multi-agents :

### Problèmes Résolus

- ❌ **Conflits de fichiers** → ✅ Déclaration d'intentions avec `files_intent`
- ❌ **Duplication de travail** → ✅ Messages de synchronisation visibles par tous
- ❌ **Manque de contexte** → ✅ API `get_context()` pour voir qui fait quoi
- ❌ **Difficultés de debug** → ✅ Historique complet des messages

### Caractéristiques

- 🚀 **Simple** - Aucune dépendance externe (stdlib Python uniquement)
- 📁 **Basé sur fichiers** - Messages stockés en JSON dans `~/.conversation_bus/`
- 🔄 **Auto-synchronisant** - Numérotation de cycles automatique
- 🔍 **Traçable** - Historique complet avec timestamps
- 🎯 **Flexible** - Actions personnalisées, métadonnées, réponses

---

## 📦 Installation

### Option 1: Copie Directe (Recommandé)

```bash
# Copier simplement le fichier dans votre projet
cp conversation_bus.py /votre/projet/

# Utiliser immédiatement
cd /votre/projet/
python -c "from conversation_bus import ConversationBus; print('✅ Installé!')"
```

### Option 2: Installation Pip

```bash
# Depuis ce dossier
pip install -e .

# Ou depuis un repo git
pip install git+https://github.com/VOTRE-USERNAME/conversation-bus-module.git
```

### Option 3: Copier Tout le Dossier

```bash
# Inclut docs, tests, exemples
cp -r conversation-bus-module /votre/projet/libs/
```

---

## 🚀 Démarrage Rapide

### Exemple Minimal (30 secondes)

```python
from conversation_bus import ConversationBus

# 1. Créer le bus
bus = ConversationBus(
    project_name="mon-projet",
    agent_name="CLAUDE-1",
    agent_role="developer"
)

# 2. Poster un message
bus.post("Bonjour! Je commence à travailler.")

# 3. Lire les messages des autres
messages = bus.read_messages(limit=10)
for msg in messages:
    print(f"[{msg['cycle']}] {msg['agent']}: {msg['message']}")
```

### Exemple Complet (5 minutes)

```python
from conversation_bus import ConversationBus

# === 1. INITIALISATION ===
bus = ConversationBus(
    project_name="biological-qubits-atlas",
    agent_name="CLAUDE-ANALYST",
    agent_role="data-analyst"
)

# === 2. SYNCHRONISATION ===
context = bus.get_context()
print(f"📊 Agents actifs: {context['active_agents']}")
print(f"📊 Messages: {context['total_messages']}")
print(f"📊 Cycle actuel: {context['last_cycle']}")

# === 3. VÉRIFIER LES CONFLITS ===
files_to_work_on = ["data/systems.csv", "analysis.py"]
conflicts = bus.check_file_conflicts(files_to_work_on)

if conflicts:
    print(f"⚠️ ATTENTION: {conflicts}")
else:
    print("✅ Aucun conflit détecté")

# === 4. ANNONCER INTENTION ===
bus.post(
    """Je vais analyser les systèmes de photosynthèse.
    
    Durée estimée: 15 minutes
    Fichiers: data/systems.csv, analysis.py
    
    Questions?
    """,
    actions=["sync", "plan"],
    files_intent=files_to_work_on
)

# === 5. FAIRE LE TRAVAIL ===
# ... votre code ici ...

# === 6. CHECKPOINT (tous les 10 min) ===
bus.post(
    "⏱️ CHECKPOINT - Analyse à 50%. Trouvé 12 systèmes.",
    actions=["checkpoint"]
)

# === 7. CONFIRMER LA COMPLÉTION ===
bus.post(
    """✅ TERMINÉ - Analyse photosynthèse
    
    Résultats:
    - 12 systèmes identifiés
    - Données ajoutées à data/systems.csv
    - Script d'analyse dans analysis.py
    
    Prochaine étape: Validation par biologiste
    """,
    actions=["complete", "report"],
    files_intent=files_to_work_on
)

# === 8. LIRE LES RÉPONSES ===
recent = bus.read_messages(limit=20)
for msg in recent:
    if msg.get('reply_to') == "CLAUDE-ANALYST":
        print(f"💬 Réponse de {msg['agent']}: {msg['message']}")
```

---

## 📚 API Complète

### `ConversationBus(project_name, agent_name, agent_role, bus_root=None)`

**Constructeur - Créer un bus de conversation**

```python
bus = ConversationBus(
    project_name="mon-projet",      # Nom du projet
    agent_name="AGENT-UNIQUE",      # Nom unique de l'agent
    agent_role="developer",         # Rôle de l'agent
    bus_root="/custom/path"         # Optionnel: chemin custom
)
```

**Paramètres:**
- `project_name` (str): Nom du projet (crée un dossier dédié)
- `agent_name` (str): Nom unique identifiant cet agent
- `agent_role` (str): Rôle/responsabilité de l'agent
- `bus_root` (str, optionnel): Racine custom (défaut: `~/.conversation_bus/`)

---

### `bus.post(message, actions=None, files_intent=None, reply_to=None, metadata=None)`

**Poster un message sur le bus**

```python
bus.post(
    message="Je commence l'analyse",
    actions=["sync", "plan"],
    files_intent=["data.csv", "script.py"],
    reply_to="OTHER-AGENT",
    metadata={"priority": "high"}
)
```

**Paramètres:**
- `message` (str): Contenu du message
- `actions` (list[str], optionnel): Tags d'action (ex: `["sync", "checkpoint", "help"]`)
- `files_intent` (list[str], optionnel): Fichiers sur lesquels l'agent va travailler
- `reply_to` (str, optionnel): Nom de l'agent auquel on répond
- `metadata` (dict, optionnel): Métadonnées additionnelles

**Retourne:** dict - Le message posté

---

### `bus.read_messages(limit=None, since_cycle=None, agent_filter=None)`

**Lire les messages du bus**

```python
# 20 messages les plus récents
messages = bus.read_messages(limit=20)

# Messages depuis le cycle 50
messages = bus.read_messages(since_cycle=50)

# Messages d'un agent spécifique
messages = bus.read_messages(agent_filter="CLAUDE-ANALYST")
```

**Paramètres:**
- `limit` (int, optionnel): Nombre max de messages (plus récents en premier)
- `since_cycle` (int, optionnel): Seulement les messages après ce cycle
- `agent_filter` (str, optionnel): Filtrer par nom d'agent

**Retourne:** list[dict] - Liste de messages triés par cycle (plus récent d'abord)

---

### `bus.get_context()`

**Obtenir le contexte actuel du bus**

```python
context = bus.get_context()
print(f"Agents actifs: {context['active_agents']}")
print(f"Dernier cycle: {context['last_cycle']}")
print(f"Fichiers en cours: {context['files_in_use']}")
```

**Retourne:** dict avec:
- `total_messages` (int): Nombre total de messages
- `last_cycle` (int): Numéro du dernier cycle
- `active_agents` (list[str]): Liste des agents ayant posté
- `files_in_use` (list[str]): Fichiers actuellement déclarés
- `recent_activity` (str): Timestamp de la dernière activité

---

### `bus.check_file_conflicts(files, recent_messages=20)`

**Vérifier si d'autres agents travaillent sur les mêmes fichiers**

```python
conflicts = bus.check_file_conflicts(
    files=["data.csv", "script.py"],
    recent_messages=30
)

if conflicts:
    print(f"⚠️ Conflits détectés: {conflicts}")
    # Exemple: {"data.csv": ["AGENT-1", "AGENT-2"]}
```

**Paramètres:**
- `files` (list[str]): Fichiers à vérifier
- `recent_messages` (int): Nombre de messages récents à analyser

**Retourne:** dict - Mapping fichier → liste d'agents travaillant dessus

---

### `bus.get_agent_status(agent_name=None)`

**Obtenir le statut d'un ou plusieurs agents**

```python
# Statut d'un agent spécifique
status = bus.get_agent_status("CLAUDE-ANALYST")
print(f"Rôle: {status['role']}")
print(f"Dernière activité: {status['last_seen']}")

# Statut de tous les agents
all_status = bus.get_agent_status()
```

**Paramètres:**
- `agent_name` (str, optionnel): Nom de l'agent (None = tous)

**Retourne:** dict - Informations de statut

---

### `bus.export_conversation(output_file, format="json")`

**Exporter l'historique complet**

```python
# Export JSON
bus.export_conversation("export.json", format="json")

# Export Markdown (lisible)
bus.export_conversation("export.md", format="markdown")

# Export texte brut
bus.export_conversation("export.txt", format="text")
```

**Paramètres:**
- `output_file` (str): Chemin du fichier de sortie
- `format` (str): Format d'export (`"json"`, `"markdown"`, `"text"`)

---

### `bus.cleanup_old_messages(keep_recent=100)`

**Nettoyer les vieux messages**

```python
# Garder seulement les 100 messages les plus récents
bus.cleanup_old_messages(keep_recent=100)
```

**Paramètres:**
- `keep_recent` (int): Nombre de messages récents à conserver

---

## 🎯 Cas d'Usage

### Cas 1: Éviter les Conflits de Fichiers

```python
# Agent 1
bus.post("Je vais éditer data.csv", files_intent=["data.csv"])

# Agent 2 (quelques minutes plus tard)
conflicts = bus.check_file_conflicts(["data.csv"])
if "data.csv" in conflicts:
    print(f"⚠️ {conflicts['data.csv']} travaille déjà sur data.csv")
    bus.post("Je vais travailler sur autre chose", actions=["coordinate"])
```

### Cas 2: Coordination sur Tâches Complexes

```python
# Agent Researcher
bus.post(
    "Phase 1: J'ai trouvé 20 papers sur la photosynthèse quantique",
    actions=["research", "complete"],
    files_intent=["papers/photosynthesis_refs.bib"]
)

# Agent Analyst (lit le bus)
recent = bus.read_messages(limit=10)
if any("photosynthèse" in msg['message'].lower() for msg in recent):
    bus.post(
        "Phase 2: Je vais analyser les données des papers",
        actions=["analysis", "plan"],
        reply_to="Agent Researcher"
    )
```

### Cas 3: Checkpoints Réguliers

```python
import time

# Boucle de travail longue
for i in range(10):
    # Faire une partie du travail
    time.sleep(60)  # 1 minute
    
    # Checkpoint tous les 5 cycles
    if (i + 1) % 5 == 0:
        bus.post(
            f"⏱️ CHECKPOINT - Progression: {(i+1)*10}%",
            actions=["checkpoint"]
        )
```

### Cas 4: Demander de l'Aide

```python
# Agent bloqué
bus.post(
    """🆘 AIDE - Je suis bloqué sur le parsing de ce fichier CSV.
    
    Erreur: UnicodeDecodeError sur ligne 42
    Fichier: data/raw_sensors.csv
    
    Quelqu'un a une idée?
    """,
    actions=["help", "blocked"],
    metadata={"urgency": "high"}
)

# Autre agent répond
bus.post(
    "Essaye d'ouvrir avec encoding='utf-8-sig' pour ignorer BOM",
    reply_to="AGENT-BLOQUE",
    actions=["help", "suggestion"]
)
```

---

## 🏗️ Architecture

### Structure des Dossiers

```
~/.conversation_bus/
└── mon-projet/
    ├── metadata.json                 # Métadonnées du projet
    └── messages/
        ├── 20251115_143022_0001_AGENT-1.json
        ├── 20251115_143145_0002_AGENT-2.json
        └── 20251115_143302_0003_AGENT-1.json
```

### Format des Messages

```json
{
  "cycle": 1,
  "timestamp": "2025-11-15T14:30:22.123456",
  "agent": "CLAUDE-ANALYST",
  "role": "data-analyst",
  "message": "Je commence l'analyse",
  "actions": ["sync", "plan"],
  "files_intent": ["data.csv"],
  "reply_to": null,
  "metadata": {}
}
```

### Format des Métadonnées

```json
{
  "project_name": "mon-projet",
  "created_at": "2025-11-15T14:00:00.000000",
  "agents": {
    "AGENT-1": {
      "role": "developer",
      "last_seen": "2025-11-15T14:30:22.123456"
    },
    "AGENT-2": {
      "role": "tester",
      "last_seen": "2025-11-15T14:31:45.678901"
    }
  }
}
```

---

## ❓ FAQ

### Q: Le bus nécessite-t-il un serveur?
**R:** Non! C'est 100% basé sur le filesystem. Parfait pour les environnements sans serveur.

### Q: Comment plusieurs agents accèdent-ils au même bus?
**R:** Tous les agents lisent/écrivent dans `~/.conversation_bus/<project_name>/`. Assurez-vous qu'ils utilisent le même `project_name`.

### Q: Que se passe-t-il si deux agents postent en même temps?
**R:** Les timestamps garantissent un ordre unique. Aucune collision possible.

### Q: Le bus peut-il être utilisé en réseau (agents sur machines différentes)?
**R:** Pas directement, mais vous pouvez monter `~/.conversation_bus/` sur un drive réseau (NFS, SMB, etc.).

### Q: Combien de messages peut stocker le bus?
**R:** Illimité! Utilisez `cleanup_old_messages()` pour gérer l'espace disque.

### Q: Le module est-il thread-safe?
**R:** Les écritures de fichiers sont atomiques. Lecture/écriture simultanée est sécuritaire.

### Q: Comment débugger les problèmes?
**R:** Exportez l'historique avec `bus.export_conversation("debug.md", format="markdown")`.

---

## 🧪 Tests

```bash
# Auto-test du module
python conversation_bus.py

# Tests unitaires (pytest requis)
pip install pytest
pytest test_conversation_bus.py -v

# Exemple d'utilisation
python example.py
```

---

## 🤝 Contributing

Contributions bienvenues! 

1. Fork ce repo
2. Créer une branche (`git checkout -b feature/amelioration`)
3. Commit vos changements (`git commit -am 'Ajout fonctionnalité'`)
4. Push la branche (`git push origin feature/amelioration`)
5. Créer une Pull Request

---

## 📜 License

MIT License - Voir [LICENSE](LICENSE)

---

## 📞 Support

- 🐛 **Bugs:** [GitHub Issues](https://github.com/VOTRE-USERNAME/conversation-bus-module/issues)
- 📖 **Docs:** Voir [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) pour exemples pratiques
- 🏗️ **Architecture:** Voir [BUS_MODULE_DESIGN.md](BUS_MODULE_DESIGN.md)

---

**Créé avec ❤️ pour la coordination multi-agents**  
Version 0.1.0 | 2025-11-15

