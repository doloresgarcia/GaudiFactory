# Phase 1: Algorithm Design

> Read `conventions/gaudi_algorithm.md` before writing anything.
> Read `methodology/03-phases.md` → "Phase 1" for full requirements.

**Goal:** Produce a written algorithm design that a developer can implement
without ambiguity.

## Your task

Parse the user's algorithm prompt and produce `DESIGN.md` covering:

### 1. Algorithm identity
- Class name (CamelCase, descriptive)
- Chosen Gaudi pattern: `k4FWCore::Producer`, `k4FWCore::Consumer`,
  `k4FWCore::Transformer`, or `Gaudi::Algorithm`
- **Pattern justification** — explain why this pattern was chosen over
  alternatives. "Needs histogram service" or "transforms one collection
  to another" are valid. If choosing `Gaudi::Algorithm`, explain why
  a functional pattern is insufficient.

### 2. Data products

| Collection | EDM4hep type | Direction (in/out) | Notes |
|------------|-------------|-------------------|-------|

- Use exact EDM4hep class names from `conventions/gaudi_algorithm.md §8`.
- If the prompt doesn't specify types, infer from physics context
  (e.g., "MC particles" → `edm4hep::MCParticleCollection`).

### 3. Configurable properties

| Name | C++ type | Default | Description |
|------|----------|---------|-------------|

- Every user-configurable parameter gets a `Gaudi::Property<T>`.
- Include collection names as properties (so steering files can override them).

### 4. Services required
- List any Gaudi services needed (e.g., `ITHistSvc` for ROOT histograms).
- If no services needed beyond data handles, state "none".

### 5. File layout
```
src/components/MyAlg.h
src/components/MyAlg.cpp
options/myAlg.py
CMakeLists.txt
```

### 6. CMake details
- Module name (e.g., `MyAlgorithmPlugins`)
- Required `LINK_LIBRARIES`: always `Gaudi::GaudiKernel` + `k4FWCore::k4FWCore`;
  add `EDM4HEP::edm4hep`, `ROOT::Hist`, etc. as needed.

### 7. Steering file outline
- What the Python steering file will configure.
- If reading/writing files: include `IOSvc` configuration.
- Specify `EvtMax` and `EvtSel`.

### 8. Validation plan
- What Phase 4 will check to verify correctness.
- Expected output (histogram fill counts, collection sizes, etc.).

## Artifact

Write `DESIGN.md` to `phase1_design/outputs/DESIGN.md`.

## Self-check before submission

- [ ] Pattern choice justified
- [ ] All input/output collections have explicit EDM4hep types
- [ ] All properties have a default and docstring
- [ ] No invented API — every class/method is in `conventions/gaudi_algorithm.md`
- [ ] Services listed if histograms or complex init needed

## Review

1-bot: critical reviewer checks design completeness and correctness of
pattern selection against `conventions/gaudi_algorithm.md`.
