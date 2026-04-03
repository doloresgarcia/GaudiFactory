# Appendix: Session Isolation and Logging

## Core Principle: Session Isolation

Every agent invocation — execution, review, arbitration — is a **separate,
isolated session** with explicitly defined inputs and outputs. No shared
conversation history, no shared memory, no implicit state. Each session
reads files, writes files, and exits. The files are the interface.

```
┌─────────────┐     ┌──────────┐     ┌──────────────┐
│   inputs/   │────►│  agent   │────►│   outputs/   │
│  (read-only)│     │ session  │     │  (new files) │
└─────────────┘     └──────────┘     └──────────────┘
                         │
                         ▼
                    logs/{role}_{timestamp}.md
```

**Exception: the experiment log.** Each phase has an `experiment_log.md` that
persists across executor sessions within that phase. Every executor session
reads the existing log and appends to it. This prevents agents from
re-trying failed approaches.

## Session Log Format

Every agent session writes a log to `phase*/logs/`:

**Filename:** `{role}_{YYYYMMDD_HHMM}.md`

Examples:
- `executor_20240315_1423.md`
- `critical_reviewer_20240315_1510.md`

**Contents:**
```markdown
# {Role} — {Phase} — {timestamp}

## Task
Brief description of what this session was asked to do.

## Actions taken
- Read DESIGN.md
- Generated MyAlg.h and MyAlg.cpp
- Updated CMakeLists.txt
- Ran cmake build → PASS

## Issues encountered
- Missing include for ITHistSvc — added Gaudi/ITHistSvc.h

## Output
- src/components/MyAlg.h
- src/components/MyAlg.cpp
- Appended to experiment_log.md
```

## Orchestrator Responsibilities

- Before spawning each subagent: commit current state.
- After each subagent completes: read the session log to confirm outputs.
- If an agent is stalled or crashed: read the session log to determine
  what was completed before respawning from that checkpoint.

## Review File Naming

Review findings go in `phase*/review/{role}/`:

**Filename:** `review_{role}_{YYYYMMDD_HHMM}.md`

Each review file contains the findings classified as A/B/C and a
recommendation (PASS / ITERATE / ESCALATE).
