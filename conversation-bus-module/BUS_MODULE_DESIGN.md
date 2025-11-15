# 📐 Document de Conception : Module `ConversationBus`

Ce document explique les choix d'architecture et de conception derrière le module `conversation_bus.py`.

## 1. Objectifs et Principes de Conception

Le `ConversationBus` a été conçu pour être :

-   **Simple** : Utiliser le système de fichiers comme backend évite d'avoir à déployer et maintenir une base de données ou un service de messagerie. C'est robuste et facile à inspecter.
-   **Décentralisé** : Chaque agent interagit avec le bus de manière autonome. Il n'y a pas de serveur central ou de broker, ce qui élimine un point de défaillance unique.
-   **Asynchrone** : Les agents peuvent poster et lire des messages à leur propre rythme, ce qui est bien adapté à un environnement où les agents peuvent avoir des temps de réponse variables.
-   **Transparent** : Tous les messages sont des fichiers JSON lisibles par l'homme, ce qui facilite grandement le débogage et l'observation du comportement du système.

## 2. Architecture du Système de Fichiers

### Structure des répertoires

Le bus est stocké dans le répertoire personnel de l'utilisateur pour être globalement accessible sur la machine :

```
~/.conversation_bus/
└── <project_name>/
    ├── 20251115_204205_123456_Agent-A.json
    ├── 20251115_204310_789012_Agent-B.json
    └── ...
```

-   **`~/.conversation_bus/`** : Le répertoire racine pour tous les bus de conversation.
-   **`<project_name>/`** : Un sous-répertoire pour chaque projet, assurant l'isolation des communications. Le nom du projet est nettoyé pour être compatible avec les noms de répertoires.

### Format des Messages

Chaque message est un fichier JSON unique. Le nom du fichier est crucial pour le tri :

-   **Format** : `YYYYMMDD_HHMMSS_ffffff_agentname.json`
-   **Avantages** :
    -   Permet un tri chronologique fiable simplement en triant les noms de fichiers par ordre alphabétique.
    -   L'inclusion du nom de l'agent facilite l'identification rapide des fichiers.
    -   Le timestamp jusqu'à la microseconde réduit considérablement le risque de collisions de noms de fichiers.

Le contenu du fichier JSON est structuré pour capturer toutes les informations pertinentes d'une communication :

```json
{
  "id": "uuid-unique",
  "timestamp": "iso-8601-utc",
  "cycle": 1,
  "agent": "nom-de-l-agent",
  "role": "role-de-l-agent",
  "message": "Contenu du message.",
  "actions": ["plan", "sync"],
  "files_intent": ["path/to/file1.csv"],
  "reply_to": "autre-agent"
}
```

## 3. Détails d'Implémentation de la Classe `ConversationBus`

### `__init__(project_name, agent_name, agent_role)`

-   **Nettoyage des noms** : Les noms de projet et d'agent sont "sanitized" pour éviter les caractères invalides dans les noms de fichiers/dossiers.
-   **Création automatique** : Le répertoire du bus est créé automatiquement s'il n'existe pas, simplifiant la première utilisation.

### `post(...)`

-   **Timestamp UTC** : Utilise `datetime.now(timezone.utc)` pour garantir que les timestamps sont cohérents et non ambigus, quelle que soit la localisation de la machine exécutant l'agent.
-   **UUID** : Chaque message a un ID unique, ce qui peut être utile pour des systèmes plus avancés (par exemple, suivre des conversations).
-   **Gestion du cycle** : La logique d'incrémentation du cycle est basée sur les actions `sync` ou `join`, ce qui correspond au début d'une nouvelle unité de travail pour un agent.

### `read_messages(...)` et `get_context()`

-   **Tri inversé** : Les messages sont lus et triés du plus récent au plus ancien, car c'est le cas d'utilisation le plus courant (voir ce qui s'est passé récemment).
-   **Robustesse** : La lecture des fichiers est enveloppée dans un `try...except` pour éviter qu'un fichier corrompu ne fasse planter tout le système.
-   **Définition de l'activité** : Un agent est considéré comme "actif" s'il a posté un message dans les 15 dernières minutes. Ce seuil peut être ajusté, mais il semble un bon compromis pour équilibrer réactivité et persistance.

## 4. Limitations et Évolutions Possibles

-   **Scalabilité** : Pour un très grand nombre d'agents ou de messages, la lecture de tous les fichiers à chaque `get_context()` pourrait devenir lente. Une optimisation possible serait de mettre en cache le contexte ou d'utiliser un fichier d'index.
-   **Gestion des conflits** : Le système actuel repose sur les agents pour détecter les conflits en lisant les `files_intent`. Il n'y a pas de mécanisme de verrouillage actif. Pour des systèmes plus critiques, un mécanisme de lock (par exemple, via des fichiers `.lock`) pourrait être ajouté.
-   **Dépendance à un seul système de fichiers** : Ce bus ne fonctionne que pour les agents s'exécutant sur la même machine (ou ayant accès à un système de fichiers partagé). Pour une communication distribuée, il faudrait passer à un backend réseau (par exemple, une API REST simple, Redis, ou MQTT).
