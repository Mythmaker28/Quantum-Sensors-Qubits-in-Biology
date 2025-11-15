#!/usr/bin/env python3
"""
ConversationBus - Système de communication inter-agents
Empêche les duplications et coordonne le travail
"""

import json
import os
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path


class ConversationBus:
    """
    Bus de communication pour coordonner plusieurs agents.
    Gère les messages, les intentions de fichiers, et la détection de conflits.
    """
    
    def __init__(self, project_name: str, agent_name: str, agent_role: str):
        """
        Initialise le bus de conversation
        
        Args:
            project_name: Nom du projet (ex: "biological-qubits-atlas")
            agent_name: Nom de l'agent (ex: "AGENT-1")
            agent_role: Rôle de l'agent (ex: "backend", "analysis")
        """
        self.project_name = project_name
        self.agent_name = agent_name
        self.agent_role = agent_role
        
        # Créer le répertoire de communication
        self.bus_dir = Path(".conversation_bus")
        self.bus_dir.mkdir(exist_ok=True)
        
        # Fichiers de persistence
        self.messages_file = self.bus_dir / f"{project_name}_messages.jsonl"
        self.agents_file = self.bus_dir / f"{project_name}_agents.json"
        
        # S'enregistrer comme agent actif
        self._register_agent()
    
    def _register_agent(self):
        """Enregistre cet agent comme actif"""
        agents = {}
        if self.agents_file.exists():
            with open(self.agents_file, 'r', encoding='utf-8') as f:
                agents = json.load(f)
        
        agents[self.agent_name] = {
            "role": self.agent_role,
            "last_seen": datetime.now().isoformat(),
            "active": True
        }
        
        with open(self.agents_file, 'w', encoding='utf-8') as f:
            json.dump(agents, f, indent=2)
    
    def post(self, message: str, files_intent: Optional[List[str]] = None, 
             actions: Optional[List[str]] = None):
        """
        Poste un message sur le bus
        
        Args:
            message: Le message à poster
            files_intent: Liste des fichiers sur lesquels l'agent travaille
            actions: Liste des actions (sync, checkpoint, conflict, etc.)
        """
        msg = {
            "agent": self.agent_name,
            "role": self.agent_role,
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "files_intent": files_intent or [],
            "actions": actions or []
        }
        
        # Ajouter au fichier de messages
        with open(self.messages_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(msg) + "\n")
        
        # Mettre à jour last_seen
        self._register_agent()
        
        print(f"[{self.agent_name}] Message posté: {message[:50]}...")
    
    def read_messages(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Lit les messages récents du bus
        
        Args:
            limit: Nombre maximum de messages à lire (plus récents)
        
        Returns:
            Liste des messages
        """
        if not self.messages_file.exists():
            return []
        
        messages = []
        with open(self.messages_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    messages.append(json.loads(line))
        
        # Retourner les plus récents
        if limit:
            return messages[-limit:]
        return messages
    
    def get_context(self) -> Dict[str, Any]:
        """
        Récupère le contexte actuel du projet
        
        Returns:
            Dictionnaire avec les agents actifs, leurs zones, etc.
        """
        agents = {}
        if self.agents_file.exists():
            with open(self.agents_file, 'r', encoding='utf-8') as f:
                agents = json.load(f)
        
        # Filtrer les agents actifs (vus dans les 10 dernières minutes)
        now = datetime.now()
        active_agents = []
        for agent_name, agent_info in agents.items():
            last_seen = datetime.fromisoformat(agent_info["last_seen"])
            if (now - last_seen).total_seconds() < 600:  # 10 minutes
                active_agents.append(agent_name)
        
        return {
            "project": self.project_name,
            "active_agents": active_agents,
            "total_agents": len(agents),
            "all_agents": agents
        }
    
    def check_file_conflict(self, filepath: str) -> Optional[str]:
        """
        Vérifie si un autre agent travaille sur ce fichier
        
        Args:
            filepath: Le chemin du fichier à vérifier
        
        Returns:
            Le nom de l'agent en conflit, ou None
        """
        recent = self.read_messages(limit=50)
        
        for msg in reversed(recent):
            # Ignorer ses propres messages
            if msg["agent"] == self.agent_name:
                continue
            
            # Vérifier si le fichier est dans files_intent
            if filepath in msg.get("files_intent", []):
                # Vérifier que ce n'est pas un message "terminé"
                if "✅" not in msg.get("message", ""):
                    return msg["agent"]
        
        return None
    
    def get_claimed_files(self, exclude_self: bool = True) -> Dict[str, List[str]]:
        """
        Récupère tous les fichiers actuellement revendiqués par les agents
        
        Args:
            exclude_self: Si True, exclut ses propres fichiers
        
        Returns:
            Dictionnaire {agent_name: [liste de fichiers]}
        """
        recent = self.read_messages(limit=100)
        claimed = {}
        
        for msg in recent:
            agent = msg["agent"]
            
            if exclude_self and agent == self.agent_name:
                continue
            
            # Ne compter que les messages non-terminés
            if "✅" in msg.get("message", ""):
                # Retirer ces fichiers de la liste
                files = msg.get("files_intent", [])
                if agent in claimed:
                    claimed[agent] = [f for f in claimed[agent] if f not in files]
            else:
                files = msg.get("files_intent", [])
                if files:
                    if agent not in claimed:
                        claimed[agent] = []
                    claimed[agent].extend(files)
        
        # Dédupliquer
        for agent in claimed:
            claimed[agent] = list(set(claimed[agent]))
        
        return claimed
    
    def wait_for_response(self, timeout: int = 180) -> List[Dict[str, Any]]:
        """
        Attend des réponses des autres agents
        
        Args:
            timeout: Temps d'attente en secondes (défaut: 3 minutes)
        
        Returns:
            Nouveaux messages reçus pendant l'attente
        """
        initial_count = len(self.read_messages())
        start_time = time.time()
        
        print(f"[{self.agent_name}] Attente de réponses ({timeout}s)...")
        
        while time.time() - start_time < timeout:
            time.sleep(5)  # Vérifier toutes les 5 secondes
            current_messages = self.read_messages()
            if len(current_messages) > initial_count:
                new_messages = current_messages[initial_count:]
                print(f"[{self.agent_name}] {len(new_messages)} nouveaux messages reçus")
                return new_messages
            
            # Mettre à jour last_seen pour rester actif
            if int(time.time() - start_time) % 60 == 0:
                self._register_agent()
        
        print(f"[{self.agent_name}] Timeout atteint, aucune réponse")
        return []
    
    def clear_history(self):
        """Efface l'historique des messages (à utiliser avec précaution)"""
        if self.messages_file.exists():
            self.messages_file.unlink()
        print(f"[{self.agent_name}] Historique effacé")
    
    def deactivate(self):
        """Désactive cet agent"""
        agents = {}
        if self.agents_file.exists():
            with open(self.agents_file, 'r', encoding='utf-8') as f:
                agents = json.load(f)
        
        if self.agent_name in agents:
            agents[self.agent_name]["active"] = False
            agents[self.agent_name]["last_seen"] = datetime.now().isoformat()
            
            with open(self.agents_file, 'w', encoding='utf-8') as f:
                json.dump(agents, f, indent=2)
        
        print(f"[{self.agent_name}] Désactivé")


if __name__ == "__main__":
    # Test basique
    bus = ConversationBus("test-project", "TEST-AGENT", "test")
    bus.post("Message de test", files_intent=["test.py"], actions=["sync"])
    print(f"Messages: {bus.read_messages(limit=5)}")
    print(f"Context: {bus.get_context()}")
    bus.deactivate()

