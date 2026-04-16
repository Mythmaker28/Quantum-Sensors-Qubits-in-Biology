# Class A' (A-prime): fluorescent-protein qubits with direct ODMR

**Status:** curated documentation for v3.0.0 release.  
**Scope:** explains the rationale, scientific evidence, and dataset encoding of the new class A' introduced in the Biological Qubits Atlas v3.0.

---

## Why a new class?

The pre-v3.0 atlas used four classes:

- A - fluorescent proteins used as optical biosensors (no spin control);
- B - solid-state spin qubits (NV, SiC, hBN, SnV, GeV, FND) integrated in biological matrices;
- C - hyperpolarised nuclei (13C, 15N, 129Xe, 31P);
- D - endogenous radical-pair systems (cryptochromes, photolyases, FMO).

That taxonomy missed an emerging category: fluorescent proteins and engineered flavin systems whose spin degrees of freedom are **directly addressable and readable** through ODMR-style techniques. These systems are simultaneously:

- genetically encoded like class A;
- coherently controllable like class B;
- biologically compatible at 295 to 310 K.

Treating them as either "A with better contrast" or "B with an FP host" loses the scientific message, so v3.0 introduces class **A' (A-prime)**.

## Included systems (v3.0)

| System | Host | Readout | Temperature | DOI |
|--------|------|---------|-------------|-----|
| EYFP - spin qubit | E. coli + HEK293 (in cellulo) | ODMR (OADF) | 80 K | 10.1038/s41586-025-09417-w |
| EYFP at room temperature | Aqueous (in vitro) | ODMR | 295 K | 10.1038/s41586-025-09417-w |
| MagLOV (parental) | Purified protein | RYDMR | 295 K | 10.1038/s41586-025-09971-3 |
| MagLOV 2 (engineered) | Purified protein | RYDMR | 295 K | 10.1038/s41586-025-09971-3 |
| mScarlet + FMN SCRP | Purified protein | RYDMR | 295 K | 10.1101/2025.02.27.640669 |
| mCherry + FMN SCRP | Purified protein | RYDMR | 295 K | 10.1101/2025.02.27.640669 |
| mScarlet-I + FMN SCRP | Purified protein | RYDMR | 295 K | 10.1101/2025.02.27.640669 |
| DmCry (Drosophila cryptochrome, purified) | Purified protein | microwave-assisted RP | 295 K | 10.1038/s41586-025-09971-3 |

Exact parameters (T2, T1, ODMR contrast, sensitivities, hosts) are stored in `data/qubits/biological_qubits_v3.csv`, class `A_prime`.

## Physical principles

Two complementary readout mechanisms dominate class A':

1. **Optically activated delayed fluorescence (OADF)** - pioneered for EYFP. A dark triplet population, formed via intersystem crossing, is coherently manipulated by microwaves and then reconverted into fluorescence photons. The resulting contrast is small but quantitative, and operates from cryogenic (80 K) to near-ambient (295 K) conditions.
2. **Radical-pair ODMR (RYDMR)** - photoexcited FMN-aromatic amino acid pairs (Trp, Tyr) form spin-correlated radical pairs (SCRPs) whose singlet-triplet interconversion is biased by microwaves. The modulation of the recombination yield is detected through FP fluorescence.

## Dataset encoding

Class A' rows follow the v3.0 schema (see `data/qubits/SCHEMA_v3.md`). Key columns:

- `Classe` = `A_prime`.
- `Methode_lecture` in `{odmr, esr, radical_pair_detection}`.
- `Spin_type` = `Electron` (for FP triplets and SCRPs).
- `Hote_contexte` captures the biological environment (in_vitro, in_cellulo, in_vivo).
- `Verification_statut` is `verifie` when the original paper directly measured the quantity, `a_confirmer` when inferred.

## Relationship with class D

Class D (radical-pair magnetoreception) shares physical mechanisms with the new class A', but the two classes differ in **intent**:

- Class D documents endogenous systems hypothesised to explain natural phenomena (animal magnetoreception, photolyase DNA repair, bacterial photosynthesis).
- Class A' documents engineered or purified systems whose spin degree of freedom is intentionally exploited as a qubit or quantum sensor.

A small number of DmCry-like systems could in principle appear in both classes; the v3.0 dataset places each row in the class that best matches the primary reference.

## Implications for the field

Class A' lowers the barrier to quantum sensing in living cells: it inherits the delivery and localisation maturity of fluorescent proteins, while opening spin-based readouts that until recently were the exclusive domain of nanodiamond labs. The first practical use cases discussed in the 2025 literature include:

- intracellular magnetometry without exogenous nanoparticles;
- subcellular temperature sensing coupled to OADF lifetime changes;
- coupled FP-FP networks for quantum-enhanced FRET.

A' is therefore both a technical category and a research invitation: it formalises a class of quantum-coherent reporters that neither class A nor class B captured adequately.

## References

- Singh R. et al., "Coherent spin control of EYFP at room temperature", Nature (2025), DOI `10.1038/s41586-025-09417-w`.
- "Engineered LOV-flavin radical pairs as room-temperature spin qubits", Nature (2025), DOI `10.1038/s41586-025-09971-3`.
- "Red fluorescent protein SCRPs for RYDMR readout", bioRxiv preprint (2025), DOI `10.1101/2025.02.27.640669`.
- Full bibliography in `data/qubits/biological_qubits_v3.csv` (class `A_prime`) and `RELEASE_NOTES_v3.0.md`.
