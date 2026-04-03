# Phase 3: Build & Run

> Read `methodology/03-phases.md` → "Phase 3" for full requirements.

**Goal:** Prove the algorithm compiles and runs without errors.

**This phase is a hard gate.** Do not advance to Phase 4 until build and
run are both clean.

## Build

```bash
source /cvmfs/sw.hsf.org/key4hep/setup.sh   # if not already sourced
mkdir -p build && cd build
cmake -G Ninja ..
ninja install
```

- Fix ALL compiler errors before advancing.
- Fix ALL compiler warnings (warnings are Category B — treat them as
  bugs).
- Common errors and fixes:
  - `undefined reference` → add missing target to `LINK_LIBRARIES`
  - `no member named X` → check EDM4hep accessor name in
    `conventions/gaudi_algorithm.md §8`
  - `cannot convert` → check collection vs. object type usage
  - `DECLARE_COMPONENT not found` → missing `#include "Gaudi/Plugin.h"`
    or wrong base class

## Run

```bash
k4run options/myAlg.py
# or: gaudirun.py options/myAlg.py
```

- Verify: no `ERROR` or `FATAL` lines in the output log.
- Verify: algorithm initializes, processes `EvtMax` events, finalizes.
- Common runtime errors and fixes:
  - `Collection not found` → check collection name matches between
    producer and consumer; verify `IOSvc` input path
  - `Service not found` → add service to `ExtSvc` in steering file
  - `StatusCode::FAILURE` in initialize → check service acquisition and
    histogram booking

## Artifact

Write `BUILD_RUN.md` to `phase3_build/outputs/BUILD_RUN.md`:

```markdown
## Build

**Status:** PASS / FAIL

Last 20 lines of ninja output:
...

## Run

**Status:** PASS / FAIL

Last 20 lines of k4run output:
...

## Warnings (Category B — must fix)
- ...
```

If FAIL: the artifact records the first error and fix applied. Stay in
this phase until both Build and Run are PASS.

## Review

1-bot: critical reviewer reads `BUILD_RUN.md` and verifies:
- No compiler errors
- No compiler warnings left unaddressed
- No ERROR/FATAL in run log
- `EvtMax` events actually processed (check "Events processed" counter)
