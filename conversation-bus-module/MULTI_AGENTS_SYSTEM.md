# 🤖 Système Multi-Agents - Biological Qubits Atlas

**Coordination avancée d'agents IA pour cartographier les qubits biologiques**

---

## 📋 Vue d'Ensemble

Ce projet inclut maintenant un **système complet de coordination multi-agents** permettant à plusieurs agents IA de travailler ensemble sur la cartographie des qubits biologiques.

### 🎯 Objectifs

- ✅ **Coordination** - Éviter les conflits entre agents
- ✅ **Traçabilité** - Historique complet des actions
- ✅ **Efficacité** - Division du travail optimale
- ✅ **Scalabilité** - Ajout facile de nouveaux agents

---

## 📦 Composants du Système

### 1. Module Conversation Bus

**Localisation:** `conversation-bus-module/`

Module Python léger pour la coordination:
- 🚌 **Bus de messages** - Communication entre agents
- 📁 **Basé sur fichiers** - Aucun serveur requis
- 🔍 **Détection de conflits** - Évite les collisions
- 📊 **Contexte partagé** - Vue globale du projet

**Fichiers principaux:**
```
conversation-bus-module/
├── conversation_bus.py          # Module principal (250 lignes)
├── README.md                     # Documentation API complète
├── INTEGRATION_GUIDE.md          # Guide pratique avec exemples
├── BUS_MODULE_DESIGN.md          # Architecture et design
├── test_conversation_bus.py      # 23 tests unitaires
├── example.py                    # Exemple simple
├── QUICKSTART.md                 # Démarrage rapide
├── pyproject.toml                # Configuration pip
└── LICENSE                       # MIT License
```

### 2. Scripts d'Initialisation

**Fichiers:**
- `init_biological_qubits_agents.py` - Script CLI pour initialiser un agent
- `demo_multi_agents.py` - Démonstration complète (3 agents)
- `MULTI_AGENTS_QUICKSTART.md` - Guide de démarrage rapide

---

## 🚀 Démarrage Rapide (5 minutes)

### Étape 1: Vérifier l'Installation

```bash
# Le module est déjà inclus dans le projet
cd C:\Users\tommy\.cursor\worktrees\biological_qubits__Workspace_\AMx51

# Vérifier que tout est là
dir conversation-bus-module
```

### Étape 2: Lancer la Démonstration

```bash
# Démonstration complète avec 3 agents
python demo_multi_agents.py

# Suivez les instructions à l'écran!
```

Cette démo montre:
- 🔬 **RESEARCHER** - Recherche de systèmes dans la littérature
- ⚛️ **PHYSICIST** - Validation des mécanismes quantiques
- 🧬 **BIOLOGIST** - Validation des contextes biologiques

### Étape 3: Initialiser Votre Propre Agent

```bash
# Voir les rôles disponibles
python init_biological_qubits_agents.py --list-roles

# Initialiser un agent
python init_biological_qubits_agents.py \
    --agent-name "CLAUDE-RESEARCHER-1" \
    --role literature-analyst
```

---

## 🎭 Rôles Disponibles

| Rôle | Description | Responsabilités |
|------|-------------|-----------------|
| **literature-analyst** | Recherche scientifique | Papers, extraction de données, références |
| **database-engineer** | Structure de données | Schéma, validation, intégrité BD |
| **quantum-physicist** | Validation quantique | Cohérence, décohérence, mécanismes |
| **biologist** | Validation biologique | Viabilité in vivo, contextes biologiques |
| **data-scientist** | Analyses et viz | Stats, graphiques, corrélations |
| **software-engineer** | Code et tests | Scripts, tests unitaires, CI/CD |
| **documentation-writer** | Documentation | Guides, README, API docs |

---

## 🔄 Workflow Type

### Cycle de Coordination Standard

```
1. SYNC 📡
   ↓
   Lire le bus (voir qui fait quoi)
   
2. ANNONCER 📢
   ↓
   "Je vais faire X sur fichiers Y"
   
3. VÉRIFIER ⚠️
   ↓
   Conflits de fichiers?
   
4. TRAVAILLER ⚙️
   ↓
   Faire le travail (max 10 min)
   
5. CHECKPOINT ⏱️
   ↓
   Poster progression tous les 10 min
   
6. CONFIRMER ✅
   ↓
   "Terminé: résultats, fichiers modifiés"
   
7. RETOUR À 1 🔄
```

### Exemple de Code

```python
import sys
from pathlib import Path

# Importer le module
sys.path.insert(0, str(Path(__file__).parent / "conversation-bus-module"))
from conversation_bus import ConversationBus

# 1. INITIALISER
bus = ConversationBus(
    "biological-qubits-atlas",
    "CLAUDE-ANALYST",  # Nom unique!
    "data-analyst"
)

# 2. SYNC
context = bus.get_context()
print(f"Agents actifs: {context['active_agents']}")

# 3. LIRE
recent = bus.read_messages(limit=20)
for msg in recent:
    print(f"[{msg['cycle']}] {msg['agent']}: {msg['message'][:50]}...")

# 4. ANNONCER
bus.post(
    "Je vais analyser les systèmes de photosynthèse",
    files_intent=["data/systems.csv"],
    actions=["analysis", "start"]
)

# 5. VÉRIFIER CONFLITS
conflicts = bus.check_file_conflicts(["data/systems.csv"])
if conflicts:
    print(f"⚠️ Conflit: {conflicts}")
    exit(1)

# 6. TRAVAILLER
# ... votre code ici ...

# 7. CHECKPOINT (si > 10 min)
bus.post("⏱️ CHECKPOINT - 50% terminé", actions=["checkpoint"])

# 8. CONFIRMER
bus.post(
    "✅ TERMINÉ - Analyse complète",
    files_intent=["data/systems.csv"],
    actions=["complete"]
)
```

---

## 📊 Architecture du Bus

### Structure des Dossiers

```
~/.conversation_bus/
└── biological-qubits-atlas/
    ├── metadata.json                 # Info projet et agents
    └── messages/
        ├── 20251115_143022_0001_RESEARCHER.json
        ├── 20251115_143045_0002_PHYSICIST.json
        ├── 20251115_143102_0003_BIOLOGIST.json
        └── ...
```

### Format de Message

```json
{
  "cycle": 1,
  "timestamp": "2025-11-15T14:30:22.123456",
  "agent": "CLAUDE-RESEARCHER",
  "role": "literature-analyst",
  "message": "Je commence la recherche...",
  "actions": ["research", "start"],
  "files_intent": ["docs/photosynthesis.md"],
  "reply_to": null,
  "metadata": {
    "priority": "high"
  }
}
```

---

## 🎯 Cas d'Usage Concrets

### Cas 1: Recherche Collaborative

```
RESEARCHER → Trouve 20 papers
    ↓
    Poste sur le bus: "20 papers trouvés"
    ↓
ANALYST ← Lit le bus
    ↓
    Extrait les données des 20 papers
    ↓
    Poste: "Données extraites, prêt pour validation"
    ↓
PHYSICIST ← Lit le bus
    ↓
    Valide les mécanismes quantiques
```

### Cas 2: Pipeline Automatisé

```python
# Agent 1: Collector
bus.post("Données collectées", metadata={"next": "cleaner"})

# Agent 2: Cleaner (surveille le bus)
recent = bus.read_messages(limit=10)
if any("Données collectées" in m['message'] for m in recent):
    # Faire le nettoyage
    bus.post("Données nettoyées", metadata={"next": "analyzer"})

# Agent 3: Analyzer
# ... même pattern ...
```

### Cas 3: Debugging Collaboratif

```python
# Agent A: Trouve un bug
bus.post("🐛 BUG: KeyError sur 'timestamp'", actions=["bug", "help"])

# Agent B: Répond
bus.post(
    "💡 Solution: Utiliser .get('timestamp', default)",
    reply_to="AGENT-A",
    actions=["help", "solution"]
)

# Agent A: Confirme
bus.post("✅ Fix appliqué, merci!", reply_to="AGENT-B")
```

---

## 🚨 Règles Critiques

### ✅ TOUJOURS

1. **Lire le bus AVANT d'agir**
   - `bus.read_messages(limit=20)`
   - Voir qui fait quoi

2. **Déclarer files_intent**
   - `files_intent=["fichier.csv"]`
   - Évite les conflits

3. **Checkpoint tous les 10 min**
   - `actions=["checkpoint"]`
   - Permet suivi en temps réel

4. **Confirmer après avoir fait**
   - `actions=["complete"]`
   - Informe les autres

### ❌ JAMAIS

1. ❌ Modifier fichiers sans annoncer
2. ❌ Ignorer les messages des autres
3. ❌ Travailler > 10 min sans checkpoint
4. ❌ Utiliser le même nom d'agent qu'un autre

---

## 📚 Documentation Complète

### Guides Disponibles

| Document | Description | Audience |
|----------|-------------|----------|
| [`conversation-bus-module/README.md`](conversation-bus-module/README.md) | API complète | Développeurs |
| [`conversation-bus-module/INTEGRATION_GUIDE.md`](conversation-bus-module/INTEGRATION_GUIDE.md) | Exemples pratiques | Tous |
| [`conversation-bus-module/BUS_MODULE_DESIGN.md`](conversation-bus-module/BUS_MODULE_DESIGN.md) | Architecture | Architectes |
| [`MULTI_AGENTS_QUICKSTART.md`](MULTI_AGENTS_QUICKSTART.md) | Démarrage rapide | Débutants |
| Ce document | Vue d'ensemble | Tous |

### Exemples et Démos

| Fichier | Description |
|---------|-------------|
| `conversation-bus-module/example.py` | Exemple simple (10 lignes) |
| `demo_multi_agents.py` | Démo complète (3 agents) |
| `init_biological_qubits_agents.py` | Script CLI interactif |

### Tests

```bash
# Tests unitaires (23 tests)
pip install pytest
pytest conversation-bus-module/test_conversation_bus.py -v

# Test du module
python conversation-bus-module/conversation_bus.py

# Démo
python demo_multi_agents.py
```

---

## 🔧 API Essentielle

### Créer un Bus

```python
bus = ConversationBus(
    project_name="biological-qubits-atlas",
    agent_name="VOTRE-NOM-UNIQUE",
    agent_role="votre-role"
)
```

### Poster un Message

```python
bus.post(
    message="Votre message",
    actions=["action1", "action2"],
    files_intent=["file1.py", "file2.csv"],
    reply_to="AUTRE-AGENT",
    metadata={"key": "value"}
)
```

### Lire les Messages

```python
# 20 plus récents
messages = bus.read_messages(limit=20)

# Depuis un cycle
messages = bus.read_messages(since_cycle=50)

# Filtre par agent
messages = bus.read_messages(agent_filter="CLAUDE-ANALYST")
```

### Obtenir le Contexte

```python
context = bus.get_context()
# Retourne:
# {
#   "total_messages": 42,
#   "last_cycle": 42,
#   "active_agents": ["AGENT-1", "AGENT-2"],
#   "files_in_use": ["data.csv", "script.py"],
#   "recent_activity": "2025-11-15T14:30:22"
# }
```

### Vérifier les Conflits

```python
conflicts = bus.check_file_conflicts(
    ["data.csv", "analysis.py"],
    recent_messages=30
)
# Retourne:
# {
#   "data.csv": ["AGENT-1", "AGENT-2"]
# }
```

---

## 🎓 Exemples de Workflows

### Workflow Séquentiel

```python
# Phase 1: Collecte
bus1.post("Collecte terminée", metadata={"next_phase": "analysis"})

# Phase 2: Analyse (surveille Phase 1)
if any("Collecte terminée" in m['message'] for m in bus2.read_messages(limit=10)):
    bus2.post("Analyse démarrée")
    # ... faire l'analyse ...
    bus2.post("Analyse terminée", metadata={"next_phase": "report"})

# Phase 3: Rapport
# ... même pattern ...
```

### Workflow Parallèle

```python
# Coordinateur divise le travail
tasks = ["photosynthesis", "magnetoreception", "enzymes"]
for task in tasks:
    bus.post(f"Tâche disponible: {task}", metadata={"task": task, "status": "open"})

# Workers prennent les tâches
recent = bus.read_messages(limit=10)
available_tasks = [m for m in recent if m.get('metadata', {}).get('status') == "open"]
if available_tasks:
    my_task = available_tasks[0]
    bus.post(f"Je prends: {my_task['metadata']['task']}", actions=["claim"])
```

---

## 🆘 Troubleshooting

### Problème: Import Échoue

**Solution:**
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "conversation-bus-module"))
from conversation_bus import ConversationBus
```

### Problème: Bus Vide

**Diagnostic:**
```python
print(f"Bus dir: {bus.project_dir}")
print(f"Messages dir: {bus.messages_dir}")
print(f"Existe: {bus.messages_dir.exists()}")
```

**Solution:** Vérifier que `project_name="biological-qubits-atlas"` est identique pour tous les agents.

### Problème: Conflits Non Détectés

**Solution:** Augmenter `recent_messages`:
```python
conflicts = bus.check_file_conflicts(files, recent_messages=50)
```

---

## 📊 Statistiques et Métriques

### Performance

- ⚡ Post message: ~2-5 ms
- ⚡ Read 100 messages: ~10-20 ms
- ⚡ Get context: ~15-30 ms

### Limites

- ✅ < 1000 messages: Performance excellente
- ⚠️ > 10000 messages: Recommander `cleanup_old_messages()`

### Scalabilité

- Agents: Illimité ✅
- Messages: ~10000 pratique (nettoyage disponible) ✅
- Taille message: Limité par RAM ⚠️

---

## 🔐 Sécurité

### Considérations

- ⚠️ **Pas d'authentification** - Tous les agents ont accès complet
- ⚠️ **Pas de chiffrement** - Messages en clair
- ✅ **Injection-safe** - JSON échappé automatiquement

### Recommandations

Pour production:
1. Permissions filesystem restrictives (`chmod 770`)
2. Monitoring de l'espace disque
3. Audit logs séparés
4. Backup régulier de `~/.conversation_bus/`

---

## 🎉 Prochaines Étapes

### Pour Commencer

1. ✅ Lire ce document
2. ✅ Lancer `python demo_multi_agents.py`
3. ✅ Consulter [`MULTI_AGENTS_QUICKSTART.md`](MULTI_AGENTS_QUICKSTART.md)
4. ✅ Initialiser votre agent avec `init_biological_qubits_agents.py`
5. ✅ Commencer à travailler!

### Pour Aller Plus Loin

- 📖 Lire [`INTEGRATION_GUIDE.md`](conversation-bus-module/INTEGRATION_GUIDE.md)
- 🔬 Étudier [`BUS_MODULE_DESIGN.md`](conversation-bus-module/BUS_MODULE_DESIGN.md)
- 🧪 Lancer les tests: `pytest conversation-bus-module/test_conversation_bus.py -v`
- 🚀 Créer vos propres workflows!

---

## 📞 Support et Contribution

### Obtenir de l'Aide

1. **Documentation**: Consulter les guides ci-dessus
2. **Bus**: Poster `🆘 AIDE - [votre question]` sur le bus
3. **Tests**: Vérifier `conversation-bus-module/test_conversation_bus.py`

### Contribuer

Le système est open source (MIT License):
1. Fork le projet
2. Créer une branche
3. Améliorer le code/docs
4. Soumettre une Pull Request

---

## 📝 Changelog

### Version 0.1.0 (2025-11-15)

**Initial Release**
- ✅ Module `conversation_bus.py` (250 lignes, stdlib only)
- ✅ Documentation complète (README, guides, design)
- ✅ 23 tests unitaires (pytest)
- ✅ Scripts d'initialisation et démos
- ✅ Intégration Biological Qubits Atlas

---

## 📜 License

- **Module Code**: MIT License
- **Documentation**: CC BY 4.0

---

**🧬 Biological Qubits Atlas - Multi-Agents Coordination System**  
Version 0.1.0 | 2025-11-15 | Construit avec ❤️ pour la science collaborative

---

**⚡ Prêt à coordonner vos agents? Lancez la démo maintenant!**

```bash
python demo_multi_agents.py
```

