# 🚌 Architecture du Bus de Conversation Multi-Agents

**Solution robuste pour coordination multi-agents avec migration worktree**

---

## 🎯 Problème Résolu

Le bus de conversation permet à plusieurs agents IA de collaborer sur un projet complexe SANS :
- Conflits de fichiers
- Duplication de travail
- Perte de contexte lors du changement de worktree/branche

---

## 📁 Structure Recommandée

```
~/.conversation_bus/                  # Emplacement global (hors worktree)
└── biological-qubits-atlas/
    ├── config.json                   # Configuration du projet
    ├── messages/
    │   ├── 000001.json              # Messages séquentiels
    │   ├── 000002.json
    │   └── ...
    ├── agents/
    │   ├── active.json               # Agents actuellement actifs
    │   └── registry.json             # Historique tous agents
    └── metadata/
        ├── project_state.json        # État actuel du projet
        ├── file_lock.json            # Lock pour prévenir conflits
        └── worktree_map.json         # Mapping worktrees → bus
```

---

## 🔧 Configuration Globale (`config.json`)

```json
{
  "project_name": "biological-qubits-atlas",
  "project_root": "C:/Users/tommy/Documents/tableau proteine fluo",
  "worktrees": [
    {
      "path": "C:/Users/tommy/Documents/tableau proteine fluo",
      "branch": "feat/atlas-deep-enrichment-v2_3_0",
      "is_primary": true,
      "last_sync": "2025-11-15T20:00:00Z"
    }
  ],
  "bus_version": "1.0",
  "created": "2025-11-15T18:00:00Z",
  "last_active": "2025-11-15T20:30:00Z"
}
```

---

## 🔄 Migration Worktree : Comment ça Marche

### Problème Initial

Quand tu crées un nouveau worktree Cursor :
```
C:\Users\tommy\.cursor\worktrees\biological_qubits__Workspace_\280v2  # Ancien
C:\Users\tommy\.cursor\worktrees\biological_qubits__Workspace_\new_branch  # Nouveau
```

**Risque :** Les agents dans le nouveau worktree ne voient pas l'historique du bus !

### Solution : Bus Global

Le bus est **hors du worktree**, dans `~/.conversation_bus/`.

**Avantages :**
1. ✅ Un seul bus pour tous les worktrees du projet
2. ✅ Historique préservé lors des migrations
3. ✅ Agents peuvent se synchroniser entre worktrees
4. ✅ Aucune perte de contexte

---

## 📝 Format Message (`messages/NNNNNN.json`)

```json
{
  "id": 1,
  "timestamp": "2025-11-15T20:00:00Z",
  "agent_name": "CLAUDE-BACKEND-ENGINEER",
  "agent_id": "agent_001",
  "worktree": "C:/Users/tommy/Documents/tableau proteine fluo",
  "message_type": "status_update",
  "content": {
    "action": "integration_complete",
    "files_modified": [
      "docs/quantum_mechanisms.md",
      "docs/photosynthesis.md",
      "scripts/qa/validate_qubits_data.py"
    ],
    "files_created": [
      "data/qubits/README.md",
      "conversation-bus-module/BUS_ARCHITECTURE.md"
    ],
    "summary": "Intégré 4 docs scientifiques + 5 scripts d'analyse. Nettoyé fichiers de test.",
    "next_steps": "Valider biological_qubits.csv avec validate_qubits_data.py",
    "problems": []
  },
  "metadata": {
    "duration_min": 30,
    "tool_calls": 45,
    "context_used": "75K tokens"
  }
}
```

---

## 🤝 Protocol de Coordination

### 1. Rejoindre le Projet

```python
from conversation_bus import ConversationBus

# Rejoindre (détecte automatiquement worktree actuel)
bus = ConversationBus(
    project_name="biological-qubits-atlas",
    agent_name="CLAUDE-NEW-AGENT"
)

# Le bus lit l'historique complet (tous worktrees)
history = bus.read_messages(limit=10)
```

### 2. Poster un Message

```python
bus.post_message(
    message_type="task_complete",
    content={
        "action": "validation_complete",
        "files_affected": ["data/qubits/biological_qubits.csv"],
        "summary": "34 systèmes validés, 0 erreurs critiques",
        "next_steps": "Intégrer dans dashboard",
        "problems": []
    }
)
```

### 3. Lire les Messages des Autres

```python
# Lire tous les messages depuis dernier cycle
new_messages = bus.read_new_messages(since_id=last_read_id)

for msg in new_messages:
    print(f"{msg['agent_name']}: {msg['content']['summary']}")
```

---

## 🔒 Gestion des Conflits

### File Lock

```python
# Acquérir un lock avant modifier un fichier critique
with bus.lock_file("data/qubits/biological_qubits.csv"):
    # Modifier le fichier
    df = pd.read_csv("data/qubits/biological_qubits.csv")
    # ... modifications ...
    df.to_csv("data/qubits/biological_qubits.csv", index=False)
# Lock automatiquement relâché
```

### Zones de Travail

**Principe :** Chaque agent annonce sa zone de travail pour éviter chevauchements.

```python
bus.claim_zone("docs/")  # Agent 1 travaille sur documentation
bus.claim_zone("scripts/qa/")  # Agent 2 travaille sur QA

# Si zone déjà prise → erreur
try:
    bus.claim_zone("docs/")
except ZoneClaimedException:
    print("Zone déjà prise par un autre agent!")
```

---

## 🌳 Migration entre Worktrees

### Scénario : Nouveau Worktree Cursor

```bash
# Ancien worktree
cd C:\Users\tommy\.cursor\worktrees\biological_qubits__Workspace_\280v2

# Créer nouveau worktree (Cursor le fait automatiquement)
# Nouveau chemin : C:\Users\tommy\.cursor\worktrees\biological_qubits__Workspace_\feature_branch
```

### Agent dans le Nouveau Worktree

```python
# L'agent initialise le bus
bus = ConversationBus(
    project_name="biological-qubits-atlas",
    agent_name="CLAUDE-NEW-BRANCH"
)

# AUTOMATIQUEMENT :
# 1. Détecte le nouveau worktree
# 2. Enregistre dans worktree_map.json
# 3. Lit l'historique complet (tous worktrees précédents)
# 4. L'agent peut continuer sans perte de contexte !

# Lire le dernier état du projet
last_state = bus.get_project_state()
print(f"Dernier agent actif: {last_state['last_agent']}")
print(f"Fichiers modifiés: {last_state['files_modified']}")
```

### Worktree Map (`metadata/worktree_map.json`)

```json
{
  "worktrees": [
    {
      "path": "C:/Users/tommy/.cursor/worktrees/biological_qubits__Workspace_/280v2",
      "branch": "feat/atlas-deep-enrichment-v2_3_0",
      "agents_used": ["CLAUDE-BACKEND-ENGINEER", "CLAUDE-QA"],
      "created": "2025-11-15T18:00:00Z",
      "last_active": "2025-11-15T20:30:00Z",
      "message_range": [1, 45]
    },
    {
      "path": "C:/Users/tommy/.cursor/worktrees/biological_qubits__Workspace_/feature_branch",
      "branch": "feature/new-analysis",
      "agents_used": ["CLAUDE-NEW-BRANCH"],
      "created": "2025-11-15T21:00:00Z",
      "last_active": "2025-11-15T21:30:00Z",
      "message_range": [46, 60]
    }
  ]
}
```

---

## 🎯 Cas d'Usage

### 1. Continuation après Changement de Worktree

**Problème :** Tu passes d'une branche à une autre, l'agent perd le contexte.

**Solution :**
```python
bus = ConversationBus(project_name="biological-qubits-atlas", agent_name="CLAUDE")

# Lire les 20 derniers messages (tous worktrees)
history = bus.read_messages(limit=20)

# Résumer pour l'agent
summary = bus.summarize_recent_activity(hours=24)
# → "3 agents actifs. Fichiers modifiés: docs/, scripts/qa/. Problèmes: aucun."
```

### 2. Collaboration Multi-Agents Simultanée

**Agent 1 (Documentation) :**
```python
bus.claim_zone("docs/")
bus.post_message(content={"action": "writing docs", "files": ["docs/quantum_mechanisms.md"]})
```

**Agent 2 (QA) :**
```python
bus.claim_zone("scripts/qa/")
# Lit que Agent 1 travaille sur docs → pas de conflit
bus.post_message(content={"action": "writing validation script"})
```

### 3. Handoff entre Agents

**Agent A termine :**
```python
bus.post_message(
    message_type="handoff",
    content={
        "action": "task_complete",
        "summary": "Validation terminée, 0 erreurs",
        "next_agent": "CLAUDE-INTEGRATION",
        "next_steps": "Intégrer dans dashboard"
    }
)
bus.release_all_zones()
```

**Agent B prend le relai :**
```python
last_msg = bus.read_messages(limit=1)[0]
if last_msg['content'].get('next_agent') == bus.agent_name:
    print(f"C'est mon tour ! Prochaine étape : {last_msg['content']['next_steps']}")
```

---

## 🚀 Mise en Place Rapide

### Installation

```bash
pip install conversation-bus-toolkit
```

### Configuration Initiale

```python
from conversation_bus import init_project_bus

# Première fois seulement
init_project_bus(
    project_name="biological-qubits-atlas",
    project_root=Path.cwd(),
    bus_location=Path.home() / ".conversation_bus"
)
```

### Usage Agent

```python
from conversation_bus import ConversationBus

bus = ConversationBus(
    project_name="biological-qubits-atlas",
    agent_name="CLAUDE-ANALYST"
)

# Lire historique
history = bus.read_messages(limit=10)

# Travailler
with bus.lock_file("data/qubits/biological_qubits.csv"):
    # ... modifications ...
    pass

# Poster update
bus.post_message(
    message_type="progress",
    content={"summary": "Analyse complète", "problems": []}
)
```

---

## 📚 Ressources

- **Module Python** : `conversation-bus-module/conversation_bus.py`
- **Tests** : `conversation-bus-module/tests/`
- **Exemples** : `conversation-bus-module/example.py`
- **Documentation complète** : `conversation-bus-module/README.md`

---

## ✨ Avantages de cette Architecture

✅ **Robuste** : Bus global survit aux changements de worktree  
✅ **Traçable** : Historique complet de tous les agents/worktrees  
✅ **Scalable** : Support N agents simultanés  
✅ **Sécurisé** : Lock files prévient les conflits  
✅ **Portable** : Bus indépendant du code source  
✅ **Transparent** : JSON humainement lisible  

---

**Version :** 1.0  
**Date :** 2025-11-15  
**Projet :** Biological Qubits Atlas  
**Auteur :** CLAUDE-BACKEND-ENGINEER

