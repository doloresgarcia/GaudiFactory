# GaudiFactory

GaudiFactory generates Gaudi/k4FWCore algorithms from a natural-language
prompt. Given a description of what an algorithm should do, it produces
complete, compilable C++ source files, a CMakeLists.txt, a Python steering
file, runs the algorithm, and generates diagnostic plots.

## Quick start

```bash
pixi run scaffold algorithms/my_algorithm --name MyProducer
cd algorithms/my_algorithm
# Edit prompt.md with your algorithm description
source /cvmfs/sw.hsf.org/key4hep/setup.sh
claude   # pass your algorithm prompt
```

## How it works

```
┌─────────────────────────────────────────────────────────┐
│                     ORCHESTRATOR                         │
│  Never writes C++ code. Holds: prompt, summaries only    │
└─────┬───────────────────────────────────────────────────┘
      │
      ▼
 ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
 │ Phase 1  │──▶│ Phase 2  │──▶│ Phase 3  │──▶│ Phase 4  │──▶│ Phase 5  │
 │  Design  │   │ Implement│   │Build/Run │   │ Validate │   │  Document│
 │ (1-bot)  │   │ (1-bot)  │   │ (1-bot)  │   │(1-bot+plt)   │ (2-bot)  │
 └──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
```

Each phase runs the same loop:

```
  1. EXECUTE — spawn executor subagent
  2. REVIEW  — spawn reviewer(s)
  3. CHECK:
       A/B items? → fix agent + re-review
       Only C?    → PASS, executor applies Cs before commit
  4. COMMIT
  5. ADVANCE
```

### Phases

| Phase | Key deliverable | Review |
|-------|-----------------|--------|
| **1. Design** | `DESIGN.md` — pattern, data products, properties, CMake plan | 1-bot |
| **2. Implementation** | C++ header+source, CMakeLists.txt, Python steering file | 1-bot |
| **3. Build & Run** | `BUILD_RUN.md` — clean cmake/ninja build + clean `k4run` execution | 1-bot |
| **4. Validation** | `VALIDATION.md` + diagnostic plots in `outputs/figures/` | 1-bot + plot validator |
| **5. Documentation** | Doxygen comments, `README.md` with build/run instructions | 2-bot |

**Phase 3 is a hard gate.** Code that does not compile and run cleanly
does not advance.

### Supported algorithm patterns

| Pattern | When to use |
|---------|------------|
| `k4FWCore::Producer` | Creates a collection from scratch |
| `k4FWCore::Consumer` | Reads collections, no event output (e.g., histograms) |
| `k4FWCore::Transformer` | Reads and produces collections |
| `Gaudi::Algorithm` | Needs persistent state, complex services, or ROOT histogram booking |

See `src/conventions/gaudi_algorithm.md` for the full decision tree and
code patterns.

### Review classification

| Cat | Meaning | Action |
|-----|---------|--------|
| **A** | Blocks use (compile error, crash, wrong output) | Fix + re-review |
| **B** | Weakens quality (warning, missing docstring) | Fix before PASS |
| **C** | Style / clarity | Applied before commit |

## Directory structure

```
GaudiFactory/
  src/                        Framework infrastructure
    methodology/              Full spec: phases, review, orchestration
    conventions/              Gaudi/k4FWCore patterns (gaudi_algorithm.md)
    templates/                CLAUDE.md templates per phase
    scaffold_analysis.py      Scaffolder
  algorithms/                 Each is its own git repo
    <name>/
      CLAUDE.md               Orchestrator instructions
      prompt.md               The user's algorithm description
      src/components/         Generated C++ files
      options/                Generated Python steering file
      CMakeLists.txt          Generated build configuration
      phase{1..5}_*/          Phase dirs with CLAUDE.md, outputs/, review/
```

## Requirements

- [Key4hep software stack](https://key4hep.github.io/key4hep-doc/) (via cvmfs or local install)
- [Claude Code](https://claude.ai/claude-code) as the agent runtime
- [pixi](https://pixi.sh) for environment management (optional)
