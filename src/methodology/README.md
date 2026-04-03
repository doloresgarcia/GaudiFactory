# Methodology Specification

## Structure

### Tier 1: Algorithm generation — "what to do"
- `03-phases.md` — Phase 1–5 definitions (design, implement, build/run, validate, document)

### Tier 2: Process — "how to manage it"
- `01-principles.md` — Scope and design principles
- `02-inputs.md` — Algorithm prompt, Gaudi environment context
- `03a-orchestration.md` — Orchestrator loop, subagent management, context
- `05-artifacts.md` — Artifact format and experiment log
- `06-review.md` — Review protocol (classification, tiers, checklists)
- `12-downscoping.md` — Scope management and constraint handling

### Tier 3: Craft — "how to write good code and plots"
- `07-tools.md` — Tool choices, Key4hep environment, ROOT file reading
- `11-coding.md` — Git, C++ quality, CMake practices, Python steering files
- `appendix-heuristics.md` — Gaudi/EDM4hep idioms and pitfalls (agent-maintained)

### Appendices — operational
- `appendix-sessions.md` — Session naming, directory layout, isolation model

## Reading guide

- **For a new algorithm:** Read `03-phases.md` and `conventions/gaudi_algorithm.md`
- **For orchestration:** Read `03a-orchestration.md` and `appendix-sessions.md`
- **For coding:** Read `07-tools.md` and `11-coding.md`
- **Templates** (`src/templates/`) are the operational entry points agents read at runtime
