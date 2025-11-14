# Coherence Timescales — All Modalities

**Date :** 2025-11-13  
**Purpose :** Compare T2 coherence times across optical, spin, radical pair, and nuclear spin systems

---

## Timescale Spectrum (4K → 298K)

```
10 fs ──────── 1 ps ──────── 1 ns ──────── 1 µs ──────── 1 ms ──────── 1 s ──────── 1000 s
  │              │              │              │              │              │              │
  │         Radical        Cryptochrome    NV (RT)      NV (77K)       ¹³C-NV      ³¹P Si
  │         pairs          Photolyase      SiC (RT)     P1 center      @ RT        @ 2K
  │         PSII                                                        
  │         (10-1000ns)                                                 
  │                                                                     
Optical FP                                                              
(no T2,                                                                 
intensity                                                               
readout)                                                                
```

---

## Summary Table

| Modality | System | T2 (typical) | Temperature | Regime | Functional Role |
|----------|--------|--------------|-------------|--------|-----------------|
| **Optical FP** | GCaMP8 | N/A (optical intensity) | 298K | — | Calcium sensing (90× contrast) |
| **Radical Pairs** | Cryptochrome | 1000 ns (1 µs) | 298K | **Ultra-fast** | Magnetoreception (proposed) |
| **Radical Pairs** | Photolyase | 1000 ns (1 µs) | 298K | **Ultra-fast** | DNA repair (>90% efficiency) |
| **Radical Pairs** | PSII | 100 ns | 298K | **Ultra-fast** | Charge separation |
| **Spin Qubits** | NV- (RT) | 1800 µs (1.8 ms) | 298K | **Short (RT)** | Thermometry, magnetometry |
| **Spin Qubits** | NV- (77K) | 600 ms | 77K | **Long (cryo)** | Extended coherence |
| **Spin Qubits** | SiC VSi | 160 µs | 298K | **Short (RT)** | Biocompatible, NIR |
| **Nuclear Spins** | ¹³C-NV | 1000 ms (1 s) | 298K | **Very long (RT)** | Quantum memory |
| **Nuclear Spins** | ³¹P Si | 30,000 ms (30 s) | 2K | **Ultra-long (cryo)** | Quantum computing |

---

## Key Insights

### 1. Temperature Dependence (Critical)

**RT (298K) vs Cryogenic (4-77K) :**
- **NV centers :** T2(RT) = 1.8ms → T2(77K) = 600ms (**333× improvement**)
- **Nuclear spins :** T2(¹³C, RT) = 1s → T2(³¹P, 2K) = 30s (**30× improvement**)

**Mechanism :** Phonon decoherence dominates @ RT, suppressed @ cryo

---

### 2. Functional Timescale Match

**Radical Pairs (ns-µs) :**
- **Function :** Electron transfer, charge separation (**ps-ns** processes)
- **T2 ~ 100-1000 ns** sufficient (>> transfer time)
- **Example :** Photolyase repair ~1 µs, T2 ~ 1 µs → **match**

**Spin Qubits (µs-ms) :**
- **Function :** Sensing (magnetic, temperature) — **ms-s** integration times
- **T2 ~ 1-1000 µs** limits sensitivity (√T2 scaling)
- **Example :** NV thermometry needs ~10ms integration → T2 = 1.8ms @ RT **marginal**

**Nuclear Spins (ms-s) :**
- **Function :** Quantum memory, entanglement storage
- **T2 ~ 1-30 s** enables multi-qubit gates
- **Example :** ¹³C-NV T2 = 1s @ RT → **100+ gate operations** possible

---

### 3. "Quantum Advantage" Threshold?

| System | T2 | Functional Time | Ratio (T2/τ_func) | Quantum Advantage? |
|--------|----|-----------------|--------------------|-------------------|
| PSII | 100 ns | 10 ns (charge sep) | **10×** | ⚠️ Debated (classical OK) |
| Photolyase | 1000 ns | 1000 ns (repair) | **1×** | ⚠️ Marginal (classical OK) |
| Cryptochrome | 1000 ns | ~100 ns (MFE) | **10×** | ⚠️ Sufficient, but not "advantage" |
| NV (RT) | 1800 µs | 10 ms (sensing) | **0.2×** | ❌ **Insufficient** (needs averaging) |
| ¹³C-NV | 1000 ms | 10 ms (gate) | **100×** | ✅ **Yes** (quantum memory) |

**Conclusion :** T2 >> τ_functional **does NOT prove quantum advantage**, just compatibility. Classical mechanisms can match performance if T2 ~ τ_functional.

---

## Modality-Specific Analysis

### Optical FP (No T2 Concept)

**Readout :** Fluorescence intensity (photon count)  
**"Coherence" :** N/A (classical light)  
**Timescale :** µs-ms (sensor response time, not coherence)  
**Advantage :** High contrast (10-90×), genetically encoded, mature

**Note :** FP sensors are **not quantum** (no coherence), but **functional** (high SNR, specificity)

---

### Radical Pairs (ns-µs, RT)

**Coherence regime :** Singlet-triplet mixing (spin coherence ~ns-µs)  
**Function :** Electron transfer faster than T2  
**Observation :** MFE% (10-20%), anisotropy, yield modulation

**Limitation :** **No direct T2 measurement** (inferred from kinetics, MFE timescales)

**Critical question :** Is T2 ~ 1 µs "coherence" or just radical pair lifetime? (Debate ongoing)

---

### Spin Qubits (µs-ms, RT; ms-s, cryo)

**Coherence regime :** Electron spin precession (MHz-GHz)  
**Function :** Sensing (magnetic, temperature, electric) — integration time ~ms  
**Observation :** ODMR contrast (10-30%), Ramsey/Hahn echo

**Limitation @ RT :** T2 (1.8ms NV) << integration time (10ms) → **averaging required** (√N_meas)

**Advantage @ cryo :** T2 (600ms @ 77K) >> integration time → **single-shot possible**

---

### Nuclear Spins (ms-s, RT; s-min, cryo)

**Coherence regime :** Nuclear spin precession (kHz-MHz)  
**Function :** Quantum memory, multi-qubit gates  
**Observation :** NMR/ODMR, dynamical decoupling

**Advantage :** **Longest T2 at RT** (1s for ¹³C-NV) → enables complex quantum protocols

**Limitation :** **Weak coupling** (kHz-MHz vs GHz electron spins) → slow gates

---

## Design Choices & Trade-offs

### Fast Sensing (ms response) → Spin Qubits Better

**Use case :** Neural activity, fast chemical transients  
**Requirement :** T2 ~ ms (NV @ RT marginal), **OR use FP optical** (faster, no T2)

**Winner :** **Optical FP** (GCaMP8 : 10ms rise time, 90× contrast) >> NV (1.8ms T2, 30% contrast)

---

### Slow Sensing (s integration) → Nuclear Spins Better

**Use case :** Weak magnetic fields, single-molecule detection  
**Requirement :** T2 ~ s (¹³C-NV : 1s @ RT, ³¹P : 30s @ 2K)

**Winner :** **Nuclear spins** (long coherence enables √T2 sensitivity scaling)

---

### Quantum Memory → Nuclear Spins Only

**Use case :** Store entanglement, multi-qubit gates  
**Requirement :** T2 > 100× gate time

**Winner :** **¹³C-NV** (T2 = 1s, gate ~10ms → 100× margin) **@ RT**

---

## Connexions Écosystème

### ising-life-lab
**Metrics :** Robustness ~ T2 degradation under noise  
**Compare :** NV (1800 µs → 1 µs in cellulo) vs ¹³C-NV (1s → ? in cellulo, unknown)

### fp-qubit-design
**Design goal :** Engineer proteins with T2-like stability (not quantum, but analogy)  
**Example :** FP photobleaching lifetime ~ "T2" for fluorescence

### arrest-molecules
**Hypothesis :** Arrest duration (min-h) >> all T2 timescales (ns-s)  
**Implication :** Molecular arrest ≠ quantum coherence (different regimes)

---

## TODO

- [ ] Add FMO complex (coherence debate, ~600 fs claimed)
- [ ] Add ²⁹Si nuclear spins (T2 ~ 1800s @ 4K, longest known)
- [ ] Extract T2 vs temperature curves (4K → 298K sweep for NV, SiC)
- [ ] Add in cellulo T2 data (NV : 1-10 µs confirmed, ¹³C-NV : unknown)

---

**Last updated :** 2025-11-13  
**Conclusion :** T2 spans **10 orders of magnitude** (100ns → 30s). Functional relevance depends on **matching timescale to task**, not maximizing T2.

