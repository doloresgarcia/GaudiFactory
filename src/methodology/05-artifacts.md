## 5. Artifact Format

### 5.1 Experiment Log

Each phase maintains `experiment_log.md` — an append-only log of what was
tried and what happened. Never deleted, never modified retroactively. An
empty log at phase end is a review finding.

Append after every material decision, build attempt, or fix. Subsequent
sessions read the log to avoid re-trying failed approaches.

### 5.2 Primary Artifact

Every phase produces a markdown artifact — the handoff to subsequent phases
and the permanent record.

**Standard sections for all artifacts:**
1. **Summary** — what was accomplished (1 paragraph)
2. **Method** — reproducible detail (commands run, decisions made)
3. **Results** — build output, run output, figures (by path), numbers
4. **Validation** — checks performed, quantitative outcomes
5. **Open issues** — what subsequent phases should be aware of

**Artifacts are self-contained.** A reader with only the artifact should
understand what was done and why.

### 5.3 Artifact Index by Phase

| Phase | Artifact | Location |
|-------|----------|----------|
| 1 Design | `DESIGN.md` | `phase1_design/outputs/` |
| 2 Implementation | Source files | `src/components/`, `options/`, `CMakeLists.txt` |
| 3 Build/Run | `BUILD_RUN.md` | `phase3_build/outputs/` |
| 4 Validation | `VALIDATION.md` + figures | `phase4_validation/outputs/` |
| 5 Documentation | `README.md` + annotated header | package root + `src/components/` |

### 5.4 Source File Conventions

Generated C++ files go in `src/components/`. Naming:
- Header: `MyAlg.h` — class definition, property declarations
- Source: `MyAlg.cpp` — implementation, `DECLARE_COMPONENT`

Options file goes in `options/MyAlg.py` (lowercase).

### 5.5 Figure Conventions

All validation figures go in `phase4_validation/outputs/figures/`.
Naming: `<metric>_<description>.png` (e.g., `energy_spectrum_mcparticles.png`).

Figures referenced in `VALIDATION.md` use relative paths:
```markdown
![Energy spectrum of output MCParticles](outputs/figures/energy_spectrum.png)
```

### 5.6 Versioning

Phase 3 and Phase 4 artifacts may be versioned if multiple fix cycles occur:
`BUILD_RUN_v1.md`, `BUILD_RUN_v2.md`. All versions preserved on disk.
