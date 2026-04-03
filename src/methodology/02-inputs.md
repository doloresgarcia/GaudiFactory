## 2. Inputs

### 2.1 Algorithm Prompt

A natural-language description of what the Gaudi algorithm should do.
May specify:
- The physics purpose (e.g., "reads MCParticles and histograms their energy")
- Input/output data products and their EDM4hep types
- Configurable properties (thresholds, collection names, etc.)
- Whether a specific pattern is desired (Producer, Consumer, Transformer, or
  traditional Gaudi::Algorithm)

The prompt need not specify implementation details — the agent infers the
correct Gaudi pattern and EDM4hep types from the description.

### 2.2 Gaudi/k4FWCore Environment Context

The agent operates inside a Key4hep software environment. Key dependencies:

| Package | Purpose |
|---------|---------|
| `Gaudi` | Core framework — Algorithm, Property, StatusCode, MsgStream |
| `k4FWCore` | Functional algorithm wrappers — Producer, Consumer, Transformer |
| `EDM4hep` | Event data model — MCParticleCollection, TrackCollection, etc. |
| `ROOT` | Histogramming and output (TH1, TTree, TFile) |
| `PODIO` | Persistent I/O backend |

Standard environment setup (CERN lxplus / cvmfs):
```bash
source /cvmfs/sw.hsf.org/key4hep/setup.sh
```

When the environment is not available, generate code that is correct given
the standard k4-project-template structure and note that build verification
requires the Key4hep stack.

### 2.3 Conventions Reference

Read `conventions/gaudi_algorithm.md` at Phases 1 and 2. It specifies:
- When to use Producer / Consumer / Transformer vs. Gaudi::Algorithm
- EDM4hep collection naming conventions
- Property declaration patterns
- CMake target patterns (`gaudi_add_module`)
- Python steering file structure (`k4run` / `ApplicationMgr`)

### 2.4 No Invented API

Never invent Gaudi, k4FWCore, or EDM4hep API calls from training memory.
If uncertain whether a method or type exists, consult the conventions file
or fetch from the key4hep documentation. An algorithm that calls
non-existent methods will not compile — this is Category A at review.

---
