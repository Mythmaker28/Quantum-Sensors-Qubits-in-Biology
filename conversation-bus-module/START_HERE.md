# ðŸš€ START HERE - Conversation Bus Module

**Ce dossier contient un module complet et prÃªt Ã  exporter pour la coordination multi-agents.**

---

## âœ… Fichiers PrÃ©sents

### Fichier Principal (requis)
- **conversation_bus.py** - Le module complet (~250 lignes, stdlib only)

### Tests
- **test_conversation_bus.py** - 23 tests unitaires (pytest)

### Documentation
- **README.md** - Documentation complÃ¨te avec API
- **INTEGRATION_GUIDE.md** - Guide pratique d'intÃ©gration
- **BUS_MODULE_DESIGN.md** - Document de design/architecture
- **QUICKSTART.md** - Guide de dÃ©marrage rapide

### Configuration
- **pyproject.toml** - Configuration Python/pip
- **LICENSE** - Licence MIT
- **.gitignore** - Fichiers Ã  ignorer

### Exemples
- **example.py** - Exemple d'utilisation simple

---

## ðŸŽ¯ 3 FaÃ§ons d'Utiliser ce Module

### Option 1: Copie Minimale (Plus Rapide)
```bash
# Copier SEULEMENT le fichier principal
cp conversation_bus.py /chemin/vers/votre/projet/

# Utiliser immÃ©diatement
cd /chemin/vers/votre/projet/
python
>>> from conversation_bus import ConversationBus
>>> bus = ConversationBus("mon-projet", "MON-AGENT", "dev")
>>> bus.post("Hello!")
```

### Option 2: Installation ComplÃ¨te
```bash
# Depuis ce dossier
pip install -e .

# Utiliser partout
python
>>> from conversation_bus import ConversationBus
```

### Option 3: Copier Tout le Dossier
```bash
# Copier tout dans votre projet
cp -r conversation-bus-module /chemin/vers/votre/projet/
```

---

## ðŸ§ª Tester le Module

```bash
# Test rapide
python conversation_bus.py

# Exemple complet
python example.py

# Tests unitaires
pip install pytest
pytest test_conversation_bus.py -v
```

---

## ðŸ“š Documentation

1. **DÃ©butant?** â†’ Lisez QUICKSTART.md (5 minutes)
2. **IntÃ©gration?** â†’ Lisez INTEGRATION_GUIDE.md (exemples pratiques)
3. **API complÃ¨te?** â†’ Lisez README.md (rÃ©fÃ©rence)
4. **Architecture?** â†’ Lisez BUS_MODULE_DESIGN.md (design)

---

## ðŸŽ¯ Usage Typique

```python
from conversation_bus import ConversationBus

# 1. CrÃ©er le bus
bus = ConversationBus(
    project_name="quantum-sensors",
    agent_name="CLAUDE-ANALYST",
    agent_role="data-analyst"
)

# 2. Voir qui est actif
context = bus.get_context()
print(f"Agents: {context['active_agents']}")

# 3. Annoncer intention
bus.post(
    "Je vais analyser sensor_data.csv",
    files_intent=["sensor_data.csv"]
)

# 4. Faire le travail...

# 5. Confirmer
bus.post(
    "âœ… Analyse terminÃ©e",
    files_intent=["analysis_results.md"]
)

# 6. Lire les autres
messages = bus.read_messages(limit=10)
for msg in messages:
    print(f"{msg['agent']}: {msg['message'][:50]}")
```

---

## ðŸš€ Repos Cibles

Ce module a Ã©tÃ© conÃ§u pour Ãªtre utilisÃ© dans:
- âœ… Quantum-Sensors-Qubits-in-Biology
- âœ… fp-qubit-design
- âœ… ising-life-lab
- âœ… arrest-molecules
- âœ… N'importe quel projet multi-agents

---

## ðŸ’¡ Pourquoi ce Module?

**ProblÃ¨mes rÃ©solus:**
- ðŸ”´ Conflits de fichiers entre agents
- ðŸ”´ Duplication de travail
- ðŸ”´ Manque de coordination
- ðŸ”´ DifficultÃ©s de debug

**Solution: Bus de conversation simple!**
- âœ… Communication claire
- âœ… Coordination sur fichiers
- âœ… TraÃ§abilitÃ© complÃ¨te
- âœ… Simple et portable

---

## ðŸ“¦ Contenu Minimal Requis

**Pour fonctionner, vous avez besoin de:**
- âœ… conversation_bus.py (c'est tout!)

**Le reste est documentation et tests (recommandÃ© mais optionnel).**

---

## ðŸŽ‰ PrÃªt Ã  Utiliser!

Ce dossier est **prÃªt Ã  exporter tel quel**:
1. Copiez-le dans votre projet
2. Utilisez conversation_bus.py
3. Coordonnez vos agents!

**CrÃ©Ã© par l'Ã©quipe Agent Roundtable**
Version: 0.1.0 | Date: 2025-11-15
