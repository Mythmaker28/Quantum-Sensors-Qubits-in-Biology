# 🔧 QBitAtlas Agent TODO - Amélioration Systématique

**Agent :** CLAUDE-MAINTAINER  
**Date :** 2025-11-15  
**Session :** Implémentation recommendations STRICT_EVAL + ROUNDTABLE_EVAL

---

## 📊 Phase 1 – Quick, Low-Risk Fixes

### 1. Restore analysis layer and outputs ✅ DONE
- [x] Implémenter `analysis/qubits_stats.py` (actuellement VIDE)
- [x] Implémenter `analysis/qubits_class_comparisons.py` (actuellement VIDE)
- [x] Implémenter `analysis/class_comparisons.py` (FP - actuellement VIDE)
- [x] Implémenter `analysis/descriptive_stats.py` (FP - actuellement VIDE)
- [x] Créer `analysis/output/` pour stocker résultats reproductibles
- [x] Générer JSON/Markdown summaries

**Outputs générés:**
- `analysis/output/qubits_stats.json` + `.md` (34 systèmes)
- `analysis/output/class_comparisons_qubits.json`
- `analysis/output/class_comparisons_fp.json` (30 familles)
- `analysis/output/descriptive_stats_fp.json` (180 systèmes)

### 2. Fix tests and references [DONE]
- [x] Mettre à jour tests pour v2.2.2 (pas v2.0 ou v1.3)
- [x] Vérifier `tests/test_dashboard_generation.py` (v1_3 → v2_2_curated, index_v2 → docs/index.html)
- [x] S'assurer références correctes aux fichiers actuels
- [x] Mettre à jour `tests/test_v2_installation.py` (v2.0 → v2.2.2)
- [x] Supprimer tous les emojis des tests

### 3. Make qubit validation robust [DONE]
- [x] Fix encodage UTF-8 dans `validate_qubits_data.py`
- [x] Tester sur Windows sans crash
- [x] Garder warnings pertinents
- [x] Ajouter UTF-8 wrapper pour Windows
- [x] Remplacer tous les emojis par [OK]/[ERROR]/[WARN]

### 4. Repository hygiene [DONE]
- [x] Déplacer docs bus vides vers `conversation-bus-module/docs/`
  * DEMARRAGE_RAPIDE_2_AGENTS.md
  * SYSTEME_2_AGENTS_COMPLET.md  
  * EXEMPLE_SESSION_COMPLETE.md
  * COORDINATION_MANUELLE.md
  * RATTRAPAGE_ERREURS.md
  * README_WINDOWS.md
  * GROK_DOCS_STATUS.md
  * TEST_BUS_README.md (8 fichiers déplacés)
- [x] Nettoyer structure racine

### 5. Cross-link qubit documentation [DONE]
- [x] Ajouter section "Datasets Overview" dans README.md
- [x] Lister datasets FP + qubits avec distinction claire
- [x] Pointer vers scripts QA (validate_atlas.py, validate_qubits_data.py)
- [x] Expliquer validation et analysis scripts
- [x] Ajouter section "Analysis & Reproducibility" avec exemples

---

## 📚 Phase 2 – Align docs & FAIR metadata

### 6. Update DOCUMENTATION.md [DONE]
- [x] Corriger version v2.2.2 partout (pas v2.0 avec 113 systèmes)
- [x] Comptes corrects (180 FP + 34 qubits)
- [x] Expliquer séparation FP vs qubits
- [x] Documenter tier system
- [x] Ajouter section Multi-agent & Bus (déjà présent)
- [x] Mettre à jour badge systems (113 → 214 total, 180 FP curated, 34 qubits)
- [x] Structure projet mise à jour avec analysis/ et data/qubits/

### 7. FAIR metadata completion
- [ ] Compléter licenses manquantes dans atlas FP
- [ ] Ajouter PMCIDs où possible
- [ ] Compléter pH, température
- [ ] Traiter systèmes hors physiologie (77K) dans qubits
- [ ] Ré-exécuter validation, documenter warnings restants

### 8. CITATION and Zenodo
- [ ] Mettre à jour CITATION.cff pour v2.2.2
- [ ] Mettre à jour zenodo.json
- [ ] Ajouter DOI ou TODO clair si pas encore assigné

---

## 🎨 Phase 3 – Dashboard & conversation-bus refactor

### 9. Modernize dashboard
- [ ] Refactor pour ne PAS inline CSV complet en JSON
- [ ] Générer `data/dashboard_fp.json` compact
- [ ] Générer `data/dashboard_qubits.json` compact
- [ ] Load dynamiquement avec D3.js
- [ ] Ajouter filtres FP (family/class/tier/in vivo)
- [ ] Créer vue dédiée qubits (T₂ vs temp)
- [ ] Script build dashboard (commande unique)
- [ ] Test dashboard ou checksum

### 10. Align conversation-bus implementation
- [ ] Modifier `conversation_bus.py` pour écrire dans `~/.conversation_bus/`
- [ ] Implémenter lock_file / claim_zone réels
- [ ] CLI interface (`python -m conversation_bus post ...`)
- [ ] Tests : global vs local, locking, posting/reading

---

## 🚀 Phase 4 – Prepare broader roadmap

### 11. Document the future
- [ ] Créer/mettre à jour `NEXT_STEPS.md`
- [ ] Global Quantum Sensors Atlas (au-delà biologie)
- [ ] Temperature Bridge Project
- [ ] Quantum Biology Simulator (intégration multi-repos)
- [ ] Assurer schémas/IDs stables pour consommation externe

### 12. Optional: Qubit Quality Score
- [ ] Designer score transparent (T₂, contraste, temp, toxicité)
- [ ] Implémenter ou documenter formule proposée
- [ ] Ajouter colonne au dataset qubits
- [ ] Exposer dans dashboard

---

## 📝 Final Report
- [ ] Créer `QBITATLAS_AGENT_REPORT.md`
- [ ] Lister fichiers changés et pourquoi
- [ ] Limitations/TODOs restants
- [ ] Actions suivantes (agent futur + maintainer humain)

---

**Status :** 🚀 EN COURS  
**Prochaine action :** Implémenter scripts analysis/ fonctionnels

