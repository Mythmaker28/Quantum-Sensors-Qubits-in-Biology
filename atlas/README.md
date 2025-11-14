# Atlas Structure — Systems by Modality

**Purpose :** Synthesis sheets, comparative notes, and ecosystem bridges for all quantum systems  
**Organization :** By physical modality (optical, spin, radical pairs, nuclear spins)

---

## Directory Structure

```
atlas/
├── systems_by_modality/
│   ├── optical/                    # 180 Tier 1 curated FP biosensors
│   │   ├── families/               # (To be created: CALCIUM_SENSORS.md, etc.)
│   │   └── comparative_notes/      # (To be created)
│   │
│   ├── spin_qubits/                # 13 systems (NV, SiC, diamond vacancies)
│   │   ├── families/
│   │   │   ├── NV_CENTERS.md       ✅ STABLE
│   │   │   └── SIC_DEFECTS.md      ✅ STABLE
│   │   └── comparative_notes/      # (Future: NV vs SiC biocompat)
│   │
│   ├── radical_pairs/              # 11 systems (Cryptochrome, Photolyase, PSII, etc.)
│   │   ├── families/
│   │   │   ├── CRYPTOCHROME.md     ✅ STABLE
│   │   │   └── PHOTOLYASE.md       ✅ STABLE
│   │   └── evidence_grades/
│   │       └── RADICAL_PAIRS_AVERE_vs_HYPOTHESE.md  ✅ STABLE
│   │
│   └── nuclear_spins/              # 11 systems (¹³C-NV, ³¹P, hyperpolarized tracers)
│       ├── families/
│       │   └── NV_COUPLED_SPINS.md  ✅ STABLE
│       └── comparative_notes/      # (Future)
│
├── comparative_notes_cross_modality/
│   ├── NV_vs_FP_intracellular.md           ✅ STABLE
│   └── COHERENCE_TIMESCALES_all_modalities.md  ✅ STABLE
│
├── ecosystem/
│   ├── BRIDGE_ISING_LIFE_LAB.md            ✅ MVP (v0.1)
│   ├── BRIDGE_FP_QUBIT_DESIGN_NONOPTICAL.md  ✅ MVP (v0.1)
│   └── BRIDGE_ARREST_MOLECULES_QUANTUM.md  ✅ MVP (v0.1)
│
└── applications/                   # (Future: INDEX for use-case oriented access)
```

---

## Quick Access

**Spin Qubits :** [NV Centers](systems_by_modality/spin_qubits/families/NV_CENTERS.md) | [SiC Defects](systems_by_modality/spin_qubits/families/SIC_DEFECTS.md)

**Radical Pairs :** [Cryptochrome](systems_by_modality/radical_pairs/families/CRYPTOCHROME.md) | [Photolyase](systems_by_modality/radical_pairs/families/PHOTOLYASE.md) | [[AVÉRÉ] vs [HYPOTHÈSE]](systems_by_modality/radical_pairs/evidence_grades/RADICAL_PAIRS_AVERE_vs_HYPOTHESE.md)

**Nuclear Spins :** [NV-Coupled Spins](systems_by_modality/nuclear_spins/families/NV_COUPLED_SPINS.md)

**Comparisons :** [NV vs FP](comparative_notes_cross_modality/NV_vs_FP_intracellular.md) | [Coherence Timescales](comparative_notes_cross_modality/COHERENCE_TIMESCALES_all_modalities.md)

**Bridges :** [ising-life-lab](ecosystem/BRIDGE_ISING_LIFE_LAB.md) | [fp-qubit-design](ecosystem/BRIDGE_FP_QUBIT_DESIGN_NONOPTICAL.md) | [arrest-molecules](ecosystem/BRIDGE_ARREST_MOLECULES_QUANTUM.md)

---

## Metrics (As of 2025-11-13)

| Modality | Systems | Fiches | Comparative Notes |
|----------|---------|--------|-------------------|
| Optical FP | 180 | 0 (planned) | 0 |
| Spin Qubits | 13 | 2 | 0 |
| Radical Pairs | 11 | 2 + 1 evidence | 0 |
| Nuclear Spins | 11 | 1 | 0 |
| **Cross-Modality** | — | — | 2 |

---

**See also :** [docs/LAB_USAGE_GUIDE.md](../docs/LAB_USAGE_GUIDE.md) for practical experiment design workflows

