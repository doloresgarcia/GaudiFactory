# Phase 2: Implementation

> Read `methodology/03-phases.md` → "Phase 2" for full requirements.
> Read `conventions/gaudi_algorithm.md` before writing any code.
> Read `phase1_design/outputs/DESIGN.md` — implement exactly what was designed.

**Goal:** Complete, compilable source files matching the Phase 1 design.

**Start in plan mode.** Before writing code, list every file you will
create/modify and what each section will contain. Execute after the plan.

## Files to produce

### 1. Header: `src/components/MyAlg.h`
- Include guards (`#pragma once`)
- Correct base class include (`Gaudi/Algorithm.h` or k4FWCore functional header)
- All `Gaudi::Property<T>` member declarations
- All data handle or functional signature declarations
- Constructor, destructor, lifecycle method declarations
- See `conventions/gaudi_algorithm.md §1-4` for exact patterns.

### 2. Source: `src/components/MyAlg.cpp`
- `#include "MyAlg.h"` as first include
- `DECLARE_COMPONENT(MyAlg)` immediately after includes
- Constructor body: call base constructor, set data handle keys from properties
- `initialize()`: acquire services, book histograms, call `Algorithm::initialize()`
- `execute()` (or `operator()`): algorithm logic
- `finalize()`: release resources, call `Algorithm::finalize()`
- Use `info()`, `debug()`, `warning()` — never `std::cout`

### 3. `CMakeLists.txt`
- `gaudi_add_module(...)` with `SOURCES` and `LINK_LIBRARIES`
- Install rules for library and options directory
- See `conventions/gaudi_algorithm.md §6` for exact pattern.

### 4. Steering file: `options/myAlg.py`
- Import and configure the algorithm
- Set all properties that differ from defaults
- `ApplicationMgr(...)` or `k4run`-compatible structure
- See `conventions/gaudi_algorithm.md §7` for exact patterns.

## Self-check before submitting for review

- [ ] `#pragma once` in header
- [ ] `DECLARE_COMPONENT(ClassName)` in source
- [ ] All properties have a default and docstring
- [ ] All includes resolve to real headers (no invented paths)
- [ ] No `std::cout` or `printf`
- [ ] No raw `new`/`delete` — use PODIO/EDM4hep collection APIs
- [ ] Data handles consistent between header and source
- [ ] CMake target name matches class name convention
- [ ] Steering file sets `EvtMax` and `EvtSel`

## Review

1-bot: critical reviewer checks code against `conventions/gaudi_algorithm.md`
— correct API usage, property declarations, CMake structure, no invented headers.
