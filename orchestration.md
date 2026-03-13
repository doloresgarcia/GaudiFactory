# Orchestration Guide

How to execute the methodology specification using Claude Code or any
multi-session LLM agent system.

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
                    session.log
                (full conversation transcript)
```

**Exception: the experiment log.** Each phase has an `experiment_log.md` that
persists across executor sessions within that phase. Every executor session
reads the existing log and appends to it. This is the only mutable shared state
within a phase — it prevents agents from re-trying failed approaches and gives
humans visibility into decision-making.

## Directory Layout

```
analysis_name/
  prompt.md
  regression_log.md              # Tracks any phase regressions (if triggered)

  calibrations/                  # Shared sub-analyses (may scale to near-full
    btag/                        #   sub-analysis structure if complexity warrants)
      experiment_log.md
      retrieval_log.md
      CALIBRATION_BTAG.md
      scripts/
      figures/
    jet_corrections/
      experiment_log.md
      retrieval_log.md
      CALIBRATION_JEC.md
      scripts/
      figures/

  phase1_strategy/
    experiment_log.md            # Lab notebook for this phase
    retrieval_log.md
    UPSTREAM_FEEDBACK.md         # Feedback from downstream phases (if any)
    REGRESSION_TICKET.md         # Regression investigation output (if triggered)
    scripts/                     # Phase-level codebase (can grow to thousands of lines)
    figures/
    exec/
      inputs.md
      session.log
      plan.md
      STRATEGY.md
    review/
      critical/
        inputs.md
        session.log
        STRATEGY_CRITICAL_REVIEW.md
      constructive/
        inputs.md
        session.log
        STRATEGY_CONSTRUCTIVE_REVIEW.md
      arbiter/
        inputs.md
        session.log
        STRATEGY_ARBITER.md

  phase2_exploration/
    experiment_log.md
    retrieval_log.md
    UPSTREAM_FEEDBACK.md
    REGRESSION_TICKET.md
    scripts/
    figures/
    exec/
      ...
    # Self-review only — no review/ directory

  phase3_selection/              # Per-channel if multi-channel
    channel_nunu/
      experiment_log.md
      retrieval_log.md
      sensitivity_log.md         # Tracks optimization attempts
      UPSTREAM_FEEDBACK.md
      REGRESSION_TICKET.md
      scripts/                   # Per-channel codebase
      figures/
      exec/
        ...
        SELECTION_NUNU.md
      review/
        critical/                # 1-bot review per channel
          ...
    channel_llbb/
      experiment_log.md
      retrieval_log.md
      sensitivity_log.md
      UPSTREAM_FEEDBACK.md
      REGRESSION_TICKET.md
      scripts/
      figures/
      exec/
        ...
        SELECTION_LLBB.md
      review/
        critical/
          ...
    SELECTION_COMBINED.md        # Consolidation artifact

  phase4_inference/
    4a_expected/
      experiment_log.md
      retrieval_log.md
      UPSTREAM_FEEDBACK.md
      REGRESSION_TICKET.md
      scripts/
      figures/
      exec/
        ...
        INFERENCE_EXPECTED.md
      review/
        critical/               # 3-bot review (agent gate)
          ...
        constructive/
          ...
        arbiter/
          ...
    4b_partial/
      experiment_log.md
      retrieval_log.md
      UPSTREAM_FEEDBACK.md
      REGRESSION_TICKET.md
      scripts/
      figures/
      exec/
        ...
        INFERENCE_PARTIAL.md
        ANALYSIS_NOTE_DRAFT.md
        UNBLINDING_CHECKLIST.md
      review/
        critical/               # 3-bot review before human
          ...
        constructive/
          ...
        arbiter/
          ...
    4c_observed/                 # Only created after human approval
      retrieval_log.md
      UPSTREAM_FEEDBACK.md
      REGRESSION_TICKET.md
      scripts/
      figures/
      exec/
        ...
        INFERENCE_OBSERVED.md
      review/
        critical/               # 1-bot review
          ...

  phase5_documentation/
    retrieval_log.md
    UPSTREAM_FEEDBACK.md
    REGRESSION_TICKET.md
    exec/
      ...
      ANALYSIS_NOTE.md
    review/
      critical/                 # 3-bot review
        ...
      constructive/
        ...
      arbiter/
        ...
```

## Git Integration

All work is tracked in git with conventional commits (see methodology §11.1).

**Branch strategy:**
```
main                           # Always reflects reviewed, passed work
├── phase1_strategy            # Merged after arbiter PASS
├── phase2_exploration         # Merged after self-review complete
├── phase3_selection           # Merged after 1-bot review PASS
├── phase4a_expected           # Merged after 3-bot PASS
├── phase4b_partial            # Merged after 3-bot PASS + human approval
├── phase4c_observed           # Merged after 1-bot review
└── phase5_documentation       # Merged after 3-bot PASS (final)
```

Agents commit frequently within their branch. Each commit is a checkpoint.
If an agent session crashes mid-phase, the next session picks up from the
last commit on the branch.

## Review Tiers

The review structure varies by phase (see methodology §6.2):

```
Phase 1:  Executor → [Critical + Constructive] → Arbiter  (3-bot)
Phase 2:  Executor (self-review)                           (self)
Phase 3:  Executor → Critical                              (1-bot)
Phase 4a: Executor → [Critical + Constructive] → Arbiter  (3-bot, agent gate)
Phase 4b: Executor → [Critical + Constructive] → Arbiter  (3-bot, → human)
Phase 4c: Executor → Critical                              (1-bot)
Phase 5:  Executor → [Critical + Constructive] → Arbiter  (3-bot)
```

## Model Tiering

The orchestrator assigns model tiers based on task type. Controlled by a
top-level switch with two effective tiers — opus (high reasoning) and
sonnet (fast execution):

```yaml
# analysis_config.yaml (or equivalent)
model_tier: auto  # auto | uniform_high | uniform_mid

# uniform_high: everything opus (max effort, for benchmarking)
# uniform_mid:  everything sonnet (budget mode)
# auto:         opus for strategy/reviewers/arbiter, sonnet for execution/1-bot-review

# When model_tier: auto, the orchestrator uses:
tiers:
  executor_strategy: opus      # Phase 1 — physics reasoning
  executor_default: sonnet     # Phases 2-4 — code iteration, I/O plumbing, fits
  reviewer_3bot: opus          # All 3-bot reviews (critical, constructive, arbiter)
  reviewer_1bot: sonnet        # Single critical reviewer
  arbiter: opus                # All arbiters
  investigator: opus           # Regression investigation
  calibration: sonnet          # Shared sub-analyses
  plot_generation: haiku       # Mechanical plot tasks
  smoke_tests: haiku           # Test execution
```

## Cost Controls

**Review iteration warnings:** Review cycles emit warnings to flag runaway
iteration, but the arbiter's ESCALATE mechanism is the actual termination
condition.

- After 3 iterations: orchestrator logs a warning
- After 5 iterations: orchestrator logs a strong warning and notifies human
- Termination: arbiter issues ESCALATE, which pauses for human review

**Execution budget:** Configurable per-phase (tokens or iterations).
When approached, the agent produces best-effort artifact with open issues.

**Total budget:** Orchestrator tracks cumulative cost. Pauses for human
review if threshold exceeded.

```yaml
cost_controls:
  review_warn_threshold: 3       # Warn after this many iterations
  review_strong_warn_threshold: 5 # Strongly warn; rely on ESCALATE to terminate
  phase2_max_iterations: 20
  phase3_max_iterations: 30
  total_budget_warn: 500000  # tokens, or dollar amount
  on_budget_exceeded: pause  # pause | warn_and_continue
```

## Phase Regression

When a reviewer or executor discovers a fundamental issue from an earlier phase:

```
1. Document the issue + identify origin phase
2. Tag as "regression trigger" in review artifact
3. Log in analysis_name/regression_log.md
4. Orchestrator re-runs the identified phase with new context
5. All downstream phases re-run from the regressed phase
```

The regression input for the re-run phase includes a brief describing what
was discovered and why the original output was insufficient.

## Agent Session Definitions

### Execution agent

**Reads:** methodology spec, physics prompt, upstream artifacts, experiment
log (if exists), experiment corpus (via RAG)

**Writes:** `plan.md`, primary artifact (in `exec/`), `scripts/` and `figures/`
(at phase level), appends to `experiment_log.md`

**Instruction core:**
```
Execute Phase N of this HEP analysis. Read the methodology spec and upstream
artifacts listed in inputs.md. Query the retrieval corpus as needed.

Before writing code, produce plan.md. As you work:
- Write analysis code to ../scripts/, figures to ../figures/ (phase level)
- Commit frequently with conventional commit messages
- Append to experiment_log.md: what you tried, what worked, what didn't
- Produce your primary artifact as {ARTIFACT_NAME}.md

When complete, state what you produced and any open issues.
```

### Critical reviewer ("bad cop")

**Reads:** methodology spec, artifact under review, upstream artifacts,
experiment log, experiment corpus (via RAG)

**Writes:** `{NAME}_CRITICAL_REVIEW.md`

**Instruction core:**
```
You are a critical reviewer. Your job is to find flaws. Read the artifact
and the experiment log (to understand what was tried).

Look for: incomplete background estimates, missing systematics, unjustified
assumptions, potential biases, incorrect statistical treatment, physics
errors, structural bugs in analysis code, and anything that would cause a
collaboration reviewer to reject this analysis.

Classify every issue as (A) must resolve, (B) should address, (C) suggestion.
Err on the side of strictness.
```

### Constructive reviewer ("good cop")

**Reads:** same as critical reviewer

**Writes:** `{NAME}_CONSTRUCTIVE_REVIEW.md`

**Instruction core:**
```
You are a constructive reviewer. Your job is to strengthen the analysis.
Read the artifact and experiment log.

Identify where the argument could be clearer, where additional validation
would build confidence, and where the presentation could be improved.
Focus on Category B and C issues, but escalate to A if you find genuine
errors.
```

### Arbiter

**Reads:** methodology spec, artifact, both reviews

**Writes:** `{NAME}_ARBITER.md`

**Instruction core:**
```
You are the arbiter. Read the artifact and both reviews. For each issue:
- If both agree: accept the classification
- If they disagree: assess independently with justification
- If both missed something: raise it yourself

End with: PASS / ITERATE (list Category A items) / ESCALATE (document why).
```

## Automation

```bash
# --- Regression detection and upstream feedback ---

run_regression_check() {
  # Checks arbiter/reviewer output for regression triggers and dispatches fixes.
  dir=$1
  review_artifact=$(find_latest_review_artifact "$dir")

  if grep -q "regression trigger" "$review_artifact"; then
    origin_phase=$(extract_regression_origin "$review_artifact")
    echo "REGRESSION detected in $dir — origin: $origin_phase"

    # Log to top-level regression log
    echo "$(date): $dir -> $origin_phase" >> regression_log.md

    # Spawn investigator agent (opus-tier) with structured instructions
    run_agent --model opus --output "$origin_phase/REGRESSION_TICKET.md" \
      "Investigate regression trigger from $dir. Read the trigger in $review_artifact. \
       Trace impact through artifacts selectively (do not re-read everything). \
       Produce REGRESSION_TICKET.md with: root cause, affected phases, proposed fix."

    # Dispatch fixes to the origin phase
    run_agent --model $exec_model --output "$origin_phase/exec" \
      "Fix regression described in $origin_phase/REGRESSION_TICKET.md"

    # Re-review at the original tier for that phase
    tier=$(get_review_tier "$origin_phase")
    if [ "$tier" = "3bot" ]; then
      run_3bot_review "$origin_phase"
    else
      run_1bot_review "$origin_phase"
    fi

    # Re-run all downstream phases from the regressed phase
    rerun_downstream_from "$origin_phase"
    return 1  # signal that regression was found
  fi
  return 0
}

check_upstream_feedback() {
  # After each phase, check for UPSTREAM_FEEDBACK.md and route to next review.
  dir=$1
  feedback_file="$dir/UPSTREAM_FEEDBACK.md"
  if [ -f "$feedback_file" ]; then
    echo "Upstream feedback found in $dir — routing to next review"
    # The feedback file is already in the directory; reviewers will see it
    # via their inputs.md which includes all files in the phase directory.
    return 0
  fi
  return 1
}

# --- Review tier functions ---

run_3bot_review() {
  dir=$1; iter_warn=${2:-3}; strong_warn=${3:-5}
  i=0
  while true; do
    i=$((i + 1))
    if [ $i -gt $iter_warn ]; then
      echo "WARNING: review iteration $i for $dir (warn threshold: $iter_warn)"
    fi
    if [ $i -gt $strong_warn ]; then
      echo "STRONG WARNING: review iteration $i for $dir — consider ESCALATE"
    fi
    run_agent --model opus --output "$dir/review/critical" "critical review" &
    run_agent --model opus --output "$dir/review/constructive" "constructive review" &
    wait
    run_agent --model opus --output "$dir/review/arbiter" "arbitrate"
    decision=$(extract_decision "$dir/review/arbiter")
    case $decision in
      PASS)
        run_regression_check "$dir"
        check_upstream_feedback "$dir"
        return 0
        ;;
      ITERATE)
        # Back up original inputs before first overwrite
        if [ $i -eq 1 ] && [ -f "$dir/exec/inputs.md" ]; then
          cp "$dir/exec/inputs.md" "$dir/exec/inputs.md.orig"
        fi
        # Write inputs for executor re-run that includes arbiter assessment
        cat > "$dir/exec/inputs.md" <<INPUTS
# Iteration $((i+1)) Inputs

## Arbiter Assessment (iteration $i)
$(cat "$dir/review/arbiter/"*_ARBITER.md)

## Category A Issues to Address
$(extract_category_a "$dir/review/arbiter")

## Original inputs
$(cat "$dir/exec/inputs.md.orig" 2>/dev/null || echo "See upstream artifacts.")
INPUTS
        run_agent --model $exec_model --output "$dir/exec" "iterate v$((i+1))"
        ;;
      ESCALATE)
        present_for_human_review "$dir"
        wait_for_human_input
        ;;
    esac
  done
}

run_1bot_review() {
  dir=$1; iter_warn=${2:-3}; strong_warn=${3:-5}
  i=0
  while true; do
    i=$((i + 1))
    if [ $i -gt $iter_warn ]; then
      echo "WARNING: review iteration $i for $dir (warn threshold: $iter_warn)"
    fi
    if [ $i -gt $strong_warn ]; then
      echo "STRONG WARNING: review iteration $i for $dir — consider escalation"
    fi
    run_agent --model sonnet --output "$dir/review/critical" "critical review"
    if ! review_has_category_a "$dir/review/critical"; then
      run_regression_check "$dir"
      check_upstream_feedback "$dir"
      return 0
    fi
    # Back up original inputs before first overwrite
    if [ $i -eq 1 ] && [ -f "$dir/exec/inputs.md" ]; then
      cp "$dir/exec/inputs.md" "$dir/exec/inputs.md.orig"
    fi
    # Write inputs for executor re-run that includes critical review
    cat > "$dir/exec/inputs.md" <<INPUTS
# Iteration $((i+1)) Inputs

## Critical Review (iteration $i)
$(cat "$dir/review/critical/"*_CRITICAL_REVIEW.md)

## Category A Issues to Address
$(extract_category_a_from_review "$dir/review/critical")

## Original inputs
$(cat "$dir/exec/inputs.md.orig" 2>/dev/null || echo "See upstream artifacts.")
INPUTS
    run_agent --model $exec_model --output "$dir/exec" "iterate v$((i+1))"
  done
}

# --- Main pipeline ---

run_agent --model opus --output "phase1_strategy/exec" "execute phase 1"
run_3bot_review "phase1_strategy"
git merge phase1_strategy

run_agent --model sonnet --output "phase2_exploration/exec" "execute phase 2"
# Self-review only — no external review
git merge phase2_exploration

# Phase 3 — per channel if multi-channel
for channel in nunu llbb; do
  run_agent --model sonnet --output "phase3_selection/channel_$channel/exec" "execute phase 3 ($channel)" &
done
wait
# Per-channel 1-bot reviews before consolidation
for channel in nunu llbb; do
  run_1bot_review "phase3_selection/channel_$channel"
done
run_agent --model sonnet --output "phase3_selection/exec" "consolidate channels"
git merge phase3_selection

# Shared calibrations (can run in parallel with phases 2-3)
for cal in btag jet_corrections; do
  run_agent --model sonnet --output "calibrations/$cal" "calibration: $cal" &
done

# Wait for calibrations to complete before Phase 4a — calibration artifacts
# (b-tagging scale factors, JEC) are required inputs for inference.
wait

# Phase 4a — agent gate
run_agent --model sonnet --output "phase4_inference/4a_expected/exec" "execute phase 4a"
run_3bot_review "phase4_inference/4a_expected"
if [ $? -ne 0 ]; then
  echo "ERROR: Phase 4a review did not pass. Cannot proceed to partial unblinding."
  exit 1
fi
git merge phase4a_expected

# Phase 4b — 3-bot review then human gate
run_agent --model sonnet --output "phase4_inference/4b_partial/exec" "partial unblinding"
run_3bot_review "phase4_inference/4b_partial"
present_for_human_review "phase4_inference/4b_partial"
wait_for_human_decision  # APPROVE / REQUEST CHANGES / HALT
git merge phase4b_partial

# Phase 4c + 5 after human approval
run_agent --model sonnet --output "phase4_inference/4c_observed/exec" "full unblinding"
run_1bot_review "phase4_inference/4c_observed"
git merge phase4c_observed

run_agent --model sonnet --output "phase5_documentation/exec" "execute phase 5"
run_3bot_review "phase5_documentation"
git merge phase5_documentation
```

## Session Logs

Every agent session produces a `session.log`. Not read by other agents
(artifacts are the interface), but serves as audit trail for debugging and
reproducibility.

## RAG Integration

Available to all sessions as a tool call. Agents query as needed, cite
sources in artifacts. Failed retrievals logged in experiment log (see
methodology §2.2).

## Mapping to Claude Code Agent Teams

### Team Structure

The **lead agent** is the orchestrator — spawns teammates, manages
dependencies, handles gates. Does not do analysis work.

Per phase (3-bot example):
```
Lead (orchestrator, opus)
  ├── Executor      (sonnet for phases 2-4, opus for phase 1)
  ├── Critical Rev  (opus)
  ├── Constructive Rev (opus)
  └── Arbiter       (opus)
```

For 1-bot phases, the lead spawns only Executor + Critical Rev.
For self-review phases, only Executor.

### Isolation Guarantees

- Each teammate has its **own context window**
- Communication via **shared files only**
- Critical and constructive reviewers cannot see each other's work
- The experiment log is the only shared mutable state within a phase

### Configuration

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  },
  "mcpServers": {
    "scitreerag": {
      "command": "...",
      "args": ["--corpus", "path/to/experiment/corpus"]
    }
  }
}
```

### Cost Estimates (with tiering)

| Phase | Sessions (no iteration) | Model mix (auto mode) | Relative cost |
|-------|------------------------|-----------------------|---------------|
| Phase 1 | 4 (exec + 3-bot) | 1 opus exec + 3 opus review | ████████ |
| Phase 2 | 1 (exec, self-review) | 1 sonnet | █ |
| Phase 3 | 4-6 (exec per channel + 1-bot per channel + consolidate) | sonnet | ██ |
| Calibrations | 2-3 | sonnet | █ |
| Phase 4a | 4 | 1 sonnet exec + 3 opus review | ███████ |
| Phase 4b | 4 | 1 sonnet exec + 3 opus review | ███████ |
| Phase 4c | 2 | sonnet | █ |
| Phase 5 | 4 | 1 sonnet exec + 3 opus review | ███████ |
| **Total** | **~26-30** | | |

With `auto` tiering, opus is used for strategy execution (Phase 1) and all
3-bot review sessions (critical, constructive, arbiter). Sonnet handles all
other execution and 1-bot reviews. The `uniform_high` switch runs everything
on opus for benchmarking quality differences. The `uniform_mid` switch runs
everything on sonnet for budget-constrained analyses.

## Adapting to Other Agent Systems

Requirements:
- Isolated agent sessions with file read/write and code execution
- RAG corpus accessible as a tool
- Parallel execution support
- Model selection per session (for tiering)
- Mechanism to pause for human review
- Git integration

The methodology spec is portable; this orchestration doc is the Claude Code
adapter.
