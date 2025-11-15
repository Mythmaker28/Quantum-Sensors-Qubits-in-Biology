# ðŸš€ Quickstart - 5 Minutes

## Installation Rapide
```bash
# Option 1: Copie simple
cp conversation_bus.py /votre/projet/

# Option 2: Installation pip  
pip install -e .
```

## Premier Exemple
```python
from conversation_bus import ConversationBus

# CrÃ©er le bus
bus = ConversationBus("mon-projet", "CLAUDE", "demo")

# Poster un message
bus.post("Bonjour!")

# Lire les messages
messages = bus.read_messages(limit=10)
for msg in messages:
    print(f"[{msg['cycle']}] {msg['agent']}: {msg['message']}")
```

## Documentation ComplÃ¨te
- README.md - Documentation complÃ¨te
- INTEGRATION_GUIDE.md - Guide pratique
- BUS_MODULE_DESIGN.md - Architecture

**PrÃªt Ã  coordonner vos agents! ðŸšŒ**
