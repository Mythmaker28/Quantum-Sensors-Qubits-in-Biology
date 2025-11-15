#!/usr/bin/env python3
'''Exemple simple d'utilisation du Conversation Bus'''

from conversation_bus import ConversationBus

# CrÃ©er le bus
bus = ConversationBus(
    project_name="demo-project",
    agent_name="AGENT-DEMO",
    agent_role="demo"
)

print("=== Conversation Bus Demo ===\n")

# Contexte initial
ctx = bus.get_context()
print(f"Messages: {ctx['total_messages']}")
print(f"Agents: {ctx['active_agents']}\n")

# Poster quelques messages
print("Posting messages...")
bus.post("Message 1: Hello!")
bus.post("Message 2: Working on project...")
bus.post("Message 3: Done!", files_intent=["project.py"])

# Lire tous les messages
messages = bus.read_messages()
print(f"\nAll messages ({len(messages)}):")
for msg in messages:
    print(f"  [{msg['cycle']}] {msg['agent']}: {msg['message'][:40]}...")

print("\nâœ… Demo complete!")
