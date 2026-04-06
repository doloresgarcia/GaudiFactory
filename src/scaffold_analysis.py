#!/usr/bin/env python
"""Scaffold a new Gaudi algorithm directory with per-phase CLAUDE.md files.

Usage:
    pixi run scaffold algorithms/my_algorithm --name MyAlg

The script creates the directory structure, generates CLAUDE.md files
from src/templates/, and initializes a git repo.
"""

import argparse
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
TEMPLATES = HERE / "templates"

# ---------------------------------------------------------------------------
# Phase directories
# ---------------------------------------------------------------------------

PHASES = [
    "phase1_design",
    "phase2_implementation",
    "phase3_build",
    "phase4_validation",
    "phase5_documentation",
]

PHASE_SUBDIRS = ["outputs", "outputs/figures", "src", "review", "logs"]

PHASE_TEMPLATE_MAP = {
    "phase1_design":          "phase1_claude.md",
    "phase2_implementation":  "phase2_claude.md",
    "phase3_build":           "phase3_claude.md",
    "phase4_validation":      "phase4_claude.md",
    "phase5_documentation":   "phase5_claude.md",
}


def _read_template(name: str) -> str:
    path = TEMPLATES / name
    if not path.exists():
        raise FileNotFoundError(f"Template not found: {path}")
    return path.read_text()


def _substitute(template: str, variables: dict) -> str:
    result = template
    for key, value in variables.items():
        result = result.replace("{{" + key + "}}", value)
    return result


def scaffold(algorithm_dir: Path, alg_name: str):
    """Create the algorithm directory structure with CLAUDE.md files."""
    algorithm_dir.mkdir(parents=True, exist_ok=True)

    variables = {
        "name": alg_name or algorithm_dir.name,
    }

    # Root CLAUDE.md from template
    root_claude = algorithm_dir / "CLAUDE.md"
    if not root_claude.exists():
        template = _read_template("root_claude.md")
        root_claude.write_text(_substitute(template, variables))
        print(f"  wrote {root_claude}")

    # Per-phase directories and CLAUDE.md
    for phase_name in PHASES:
        phase_dir = algorithm_dir / phase_name
        phase_dir.mkdir(exist_ok=True)
        for subdir in PHASE_SUBDIRS:
            (phase_dir / subdir).mkdir(exist_ok=True)

        claude_path = phase_dir / "CLAUDE.md"
        template_name = PHASE_TEMPLATE_MAP.get(phase_name)
        if template_name and not claude_path.exists():
            template = _read_template(template_name)
            claude_path.write_text(_substitute(template, variables))
            print(f"  wrote {claude_path}")

    # Symlink conventions/ and methodology/ into the algorithm directory
    for link_name, src_name in [
        ("conventions", "conventions"),
        ("methodology", "methodology"),
        ("agents", "agents"),
    ]:
        link = algorithm_dir / link_name
        src = HERE / src_name
        if not link.exists() and src.exists():
            link.symlink_to(src.resolve())
            print(f"  linked {link} -> {src}")

    # Source tree for generated C++ files
    src_components = algorithm_dir / "src" / "components"
    src_components.mkdir(parents=True, exist_ok=True)
    options_dir = algorithm_dir / "options"
    options_dir.mkdir(exist_ok=True)

    # Claude Code settings — auto-approve all tools (no permission prompts)
    claude_settings_dir = algorithm_dir / ".claude"
    claude_settings_dir.mkdir(exist_ok=True)
    claude_settings = claude_settings_dir / "settings.json"
    if not claude_settings.exists():
        src_abs = str(HERE.resolve())
        claude_settings.write_text(
            '{\n'
            '  "permissions": {\n'
            '    "allow": [\n'
            '      "Bash(*)",\n'
            '      "Read(**)",\n'
            f'      "Read({src_abs}/**)",\n'
            '      "Glob(**)",\n'
            '      "Grep(**)",\n'
            '      "Write(**)",\n'
            '      "Edit(**)",\n'
            '      "MultiEdit(**)"\n'
            '    ]\n'
            '  }\n'
            '}\n'
        )
        print(f"  wrote {claude_settings}")

    # LaTeX header for pandoc PDF report (phase 5)
    latex_header = algorithm_dir / "latex-header.tex"
    if not latex_header.exists():
        src_header = TEMPLATES / "latex-header.tex"
        if src_header.exists():
            latex_header.write_text(src_header.read_text())
            print(f"  wrote {latex_header}")

    # Stub prompt file
    prompt_path = algorithm_dir / "prompt.md"
    if not prompt_path.exists():
        prompt_path.write_text(
            "# Algorithm Prompt\n\n"
            "<!-- Paste the user's algorithm description here before running claude -->\n"
        )
        print(f"  wrote {prompt_path}")

    # Initialize git repo
    git_dir = algorithm_dir / ".git"
    if not git_dir.exists():
        subprocess.run(["git", "init"], cwd=algorithm_dir, check=True,
                       capture_output=True)
        gitignore = algorithm_dir / ".gitignore"
        if not gitignore.exists():
            gitignore.write_text(
                "build/\n"
                "__pycache__/\n"
                "*.pyc\n"
                "*.so\n"
                "*.rootmap\n"
                "*.pcm\n"
            )
            print(f"  wrote {gitignore}")
        print(f"  initialized git repo")

    print(f"\nScaffolded {algorithm_dir}/")
    print(f"\nNext steps:")
    print(f"  1. Edit {algorithm_dir}/prompt.md with the algorithm description")
    print(f"  2. source /cvmfs/sw.hsf.org/key4hep/setup.sh")
    print(f"  3. cd {algorithm_dir} && claude   # pass your algorithm prompt")


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold a new Gaudi algorithm directory."
    )
    parser.add_argument("dir", type=Path, help="Algorithm directory to create")
    parser.add_argument(
        "--name",
        default="",
        help="Algorithm class name (e.g. MyProducer). Defaults to directory name.",
    )
    args = parser.parse_args()
    scaffold(args.dir, args.name)


if __name__ == "__main__":
    main()
