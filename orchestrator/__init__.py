# slopspec — LLM-driven HEP analysis pipeline
#
# STATUS: SCAFFOLDING — NOT RUNNABLE YET
#
# This orchestrator is written against the documented claude_agent_sdk API
# but has NOT been tested with a live SDK install. It is scaffolding that
# sketches out the pipeline structure, prompt construction, and review loops.
# Expect breakage on first real run.
#
# To make this runnable:
# 1. Install claude-agent-sdk (pixi install)
# 2. Verify the SDK API matches what sessions.py expects
# 3. Test with --dry-run first
# 4. Run a single phase in isolation before the full pipeline
