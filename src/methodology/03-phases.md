## 3. Algorithm Generation Phases

Five sequential phases. Each phase produces a concrete artifact that the
next phase reads.

### 3.0 Artifact and Review Gates

**Every phase boundary is a hard gate.** Phase N+1 cannot begin until
Phase N has produced its artifact AND passed review (§6).

Gate protocol: (1) produce artifact → (2) review → (3) resolve Category A
items → (4) advance.

Artifact existence is a precondition. A phase that ends without its
required artifact has not completed.

---

### Phase 1: Design

**Goal:** A written algorithm design a Gaudi developer could implement from.

**The agent must:**
- Parse the prompt: identify inputs, outputs, configurable properties, and
  purpose.
- Select the correct Gaudi pattern. Decision tree:
  - Produces data products, takes no inputs → `k4FWCore::Producer`
  - Consumes data products, produces no output → `k4FWCore::Consumer`
  - Takes inputs and produces outputs → `k4FWCore::Transformer`
  - Needs full lifecycle control (init/execute/finalize), complex service
    access, or ROOT histogram booking across events → `Gaudi::Algorithm`
- Identify EDM4hep types for all input/output collections.
- Define all `Gaudi::Property<T>` parameters with names, types, defaults,
  and docstrings.
- Specify the CMake module name and library target.
- Specify the Python steering file structure.
- Identify any services needed (e.g., `ITHistSvc` for histograms,
  `IDataProviderSvc`, etc.).
- List which Key4hep packages are required (`LINK_LIBRARIES`).

**Pattern justification:** If choosing traditional `Gaudi::Algorithm` over
a functional pattern, document why. "Needs histogram service across events"
is valid. "It seemed simpler" is not.

**Artifact:** `DESIGN.md` — algorithm design document with:
  - Algorithm class name and chosen pattern (with justification)
  - File layout: `src/components/MyAlg.h`, `src/components/MyAlg.cpp`,
    `options/myAlg.py`, updated `CMakeLists.txt`
  - Data product table: collection name, EDM4hep type, direction (in/out)
  - Property table: name, C++ type, default, description
  - Steering file outline

**Review:** 1-bot (critical reviewer checks design completeness and
correctness of pattern selection).

---

### Phase 2: Implementation

**Goal:** Complete, compilable source files matching the design.

**The agent must:**
- Generate the C++ header (`MyAlg.h`):
  - Correct inheritance (`Gaudi::Algorithm` or functional base)
  - All property declarations as `Gaudi::Property<T>` members
  - All data handle declarations (`DataHandle<T>` or functional signatures)
  - Constructor, destructor, and lifecycle method declarations
- Generate the C++ source (`MyAlg.cpp`):
  - `DECLARE_COMPONENT(MyAlg)` macro
  - Constructor: pass name + svcLoc, initialize data handles with
    collection names from properties
  - `initialize()`: acquire services, book histograms if needed, call base
    `initialize()`
  - `execute()` (or `operator()` for functional): implement algorithm logic
  - `finalize()`: release resources, call base `finalize()`
  - Logging with `info()`, `debug()`, `warning()` (not `std::cout`)
- Generate / update `CMakeLists.txt`:
  - `gaudi_add_module(...)` with correct `SOURCES` and `LINK_LIBRARIES`
  - Install rules
- Generate the Python steering file (`options/myAlg.py`):
  - Import and configure the algorithm
  - Set property values
  - `ApplicationMgr(TopAlg=[...], EvtSel=..., EvtMax=...)` or `k4run`-
    compatible structure with `IOSvc` if reading/writing collections
- Generate a test script (`test/test_myAlg.sh` or equivalent) that
  exercises the algorithm end-to-end via `k4run` on the steering file
  (or a dedicated minimal test steering) and exits non-zero on failure.
  The test must be runnable from the repository root without manual setup
  beyond the standard build environment. Wire it into CTest via
  `test/CMakeLists.txt` (`add_test(...)`) so `ctest` picks it up.

**Self-check before artifact submission:**
- [ ] Header compiles standalone (no circular includes)
- [ ] `DECLARE_COMPONENT` present
- [ ] All properties have a default and docstring
- [ ] Data handles consistent between header and source
- [ ] CMake target name matches `DECLARE_COMPONENT` class name convention
- [ ] No `std::cout` — use Gaudi `MsgStream` (`info()`, `debug()`, etc.)
- [ ] No raw `new`/`delete` — use PODIO/EDM4hep collection APIs
- [ ] Test script exists under `test/` and is registered with CTest

**Artifact:** All source files in place:
  - `src/components/MyAlg.h`
  - `src/components/MyAlg.cpp`
  - `options/myAlg.py`
  - Updated `CMakeLists.txt`
  - `test/test_myAlg.sh` (or equivalent) + `test/CMakeLists.txt` with `add_test`

**Review:** 1-bot (critical reviewer — code correctness, Gaudi idioms,
EDM4hep API usage).

---

### Phase 3: Build & Run

**Goal:** Prove the algorithm compiles and runs without errors.

**The agent must:**
- Run the CMake build:
  ```bash
  mkdir -p build && cd build
  cmake -G Ninja ..
  ninja install
  ```
- Fix any compiler errors or warnings. A warning about unused variables,
  missing overrides, or deprecated API is Category B — fix before
  advancing.
- Run the steering file:
  ```bash
  k4run options/myAlg.py
  # or: gaudirun.py options/myAlg.py
  ```
- Verify clean execution: no `ERROR` or `FATAL` messages in the log.
- Capture the output log as `build_run.log`.
- Run the test script via CTest from the build directory:
  ```bash
  ctest --output-on-failure
  ```
  All tests must pass. A failing or missing test is a Category A blocker.

**Failure protocol:**
- Compiler error → fix source, re-run, do not advance until clean.
- Linker error → check `LINK_LIBRARIES` in CMakeLists.txt.
- Runtime `FATAL` → read the Gaudi exception, fix initialize/execute.
- Missing collection → check collection name in steering file matches
  property default.

**Artifact:** `BUILD_RUN.md` — summary of:
  - CMake/ninja output (last 20 lines or first error)
  - `k4run` output (last 20 lines or first ERROR/FATAL)
  - `ctest` output with the list of tests executed and their status
  - PASS / FAIL verdict with specific error if FAIL

**Review:** 1-bot (critical reviewer checks build log for warnings and
runtime log for any non-clean output).

---

### Phase 4: Validation & Plots

**Goal:** Verify the algorithm produces correct, meaningful output.

**The agent must:**
- Run the algorithm on suitable input data (real events, generated events,
  or a minimal synthetic dataset if no data is available).
- Inspect output ROOT file or stdout for expected content:
  - If producing a collection: check it exists and has the expected size/content.
  - If booking histograms: verify histograms are filled with sensible values
    (non-empty, reasonable range).
  - If a Transformer: verify output collection size is consistent with input.
- Generate diagnostic plots:
  - For each output histogram: save as PNG with axis labels, title, units.
  - For output collections: plot key kinematic distributions (pT, energy,
    eta, phi as applicable to the EDM4hep type).
  - Add a summary plot showing event counts or fill rates per event.
- Cross-check at least one numeric output against an expectation:
  - If producing MCParticles with known mass: plot invariant mass, verify peak.
  - If counting events: compare to steering file `EvtMax`.
  - If applying a cut: verify efficiency is in a physically reasonable range.

**Plotting standards:**
- All plots: axis labels with units, title, legend if >1 series.
- No empty plots accepted — an empty histogram is a bug, not a result.
- Save all plots to `outputs/figures/`.

**Artifact:** `VALIDATION.md` + figures in `outputs/figures/`:
  - Table of output collections/histograms with fill counts
  - Path to each figure
  - Pass/fail for each cross-check with observed vs. expected value

**Review:** 1-bot (critical reviewer + plot validator).

---

### Phase 5: Documentation

**Goal:** Self-contained, usable documentation for the generated algorithm.

**The agent must:**
- Add doxygen-style comments to the class header:
  - Class-level: purpose, pattern, key references
  - Each property: what it controls, valid range, effect on output
  - `execute()` / `operator()`: brief description of algorithm logic
- Write `README.md` for the algorithm package:
  - What the algorithm does
  - Algorithm type and Gaudi pattern used
  - Input/output collections with EDM4hep types
  - All configurable properties with defaults
  - Build instructions (cmake/ninja)
  - Run instructions (`k4run options/myAlg.py`)
  - Example output (reference one plot from `outputs/figures/`)
- Update `DESIGN.md` to mark all design decisions as implemented or
  deviated from (with justification for deviations).

**Artifact:** Updated `README.md`, annotated `src/components/MyAlg.h`,
`phase5_documentation/outputs/REPORT.md`, and compiled `REPORT.pdf`.

Compile with:
```bash
pixi run build-report
```

`REPORT.pdf` must exist and be non-empty before review.

**Review:** 2-bot (critical + constructive reviewers — completeness and
clarity of documentation; PDF must compile cleanly).

---

### Review Classification

| Cat | Meaning | Action |
|-----|---------|--------|
| **A** | Blocks use (compile error, runtime crash, wrong output) | Fix + re-review |
| **B** | Weakens quality (warning, missing docstring, poor plot) | Fix before PASS |
| **C** | Style / clarity | Executor applies before commit |
