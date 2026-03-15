#!/usr/bin/env python3
"""Convert ANALYSIS_NOTE.md to LaTeX with embedded figures, then compile to PDF.

Usage: pixi run py phase5_documentation/exec/build_pdf.py
"""
import re
import subprocess
import logging
from pathlib import Path
from rich.logging import RichHandler

logging.basicConfig(level=logging.INFO, format="%(message)s", handlers=[RichHandler(rich_tracebacks=True)])
log = logging.getLogger(__name__)

EXEC_DIR = Path(__file__).parent
AN_MD = EXEC_DIR / "ANALYSIS_NOTE.md"
AN_TEX = EXEC_DIR / "ANALYSIS_NOTE.tex"
AN_PDF = EXEC_DIR / "ANALYSIS_NOTE.pdf"

def md_to_latex_with_figures(md_text: str) -> str:
    """Convert markdown to LaTeX, embedding figure references as includegraphics."""

    # First pass: convert figure references from inline text to ![](path) syntax
    # Pattern: **Figure:** `path` — caption  OR  **Figures:** `path`, `path`
    def replace_single_figure(m):
        path = m.group(1)
        caption = m.group(2).strip().rstrip('.').strip() if m.group(2) else ""
        return f"![{caption}]({path})"

    # Single figure: **Figure:** `path` — caption
    md_text = re.sub(
        r'\*\*Figure:\*\*\s*`([^`]+\.pdf)`\s*[—–-]\s*(.*?)(?:\n|$)',
        replace_single_figure,
        md_text
    )

    # Multiple figures on one line: **Figures:** `path1`, `path2` — caption
    def replace_multi_figures(m):
        paths_str = m.group(1)
        caption = m.group(2).strip().rstrip('.').strip() if m.group(2) else ""
        paths = re.findall(r'`([^`]+\.pdf)`', paths_str)
        result = []
        for p in paths:
            result.append(f"![{caption}]({p})")
        return "\n\n".join(result)

    md_text = re.sub(
        r'\*\*Figures?:\*\*\s*((?:`[^`]+\.pdf`[,\s]*)+)[—–-]?\s*(.*?)(?:\n|$)',
        replace_multi_figures,
        md_text
    )

    # Also catch any remaining backtick-wrapped figure paths not caught above
    # Pattern: `../../phase*/figures/*.pdf`
    def replace_orphan_figure_ref(m):
        full = m.group(0)
        path = m.group(1)
        # Only replace if this looks like a standalone figure reference (not in a sentence)
        return f"![Figure]({path})"

    # Don't replace paths that are inside longer text — only standalone ones
    md_text = re.sub(
        r'^`(\.\.\/\.\.\/phase[^`]+\.pdf)`\s*$',
        replace_orphan_figure_ref,
        md_text,
        flags=re.MULTILINE
    )

    return md_text


def main():
    log.info("Reading %s", AN_MD)
    md_text = AN_MD.read_text()

    # Fix the one broken reference
    md_text = md_text.replace(
        "../../phase4_inference/figures/closure_chi2_vs_iter.pdf",
        "../../phase3_selection/figures/closure_chi2_vs_iter.pdf"
    )

    # Convert figure references to markdown image syntax
    md_text = md_to_latex_with_figures(md_text)

    # Write intermediate markdown
    fixed_md = EXEC_DIR / "ANALYSIS_NOTE_with_figures.md"
    fixed_md.write_text(md_text)
    log.info("Wrote intermediate markdown with figure syntax: %s", fixed_md)

    # Count figures
    n_figs = len(re.findall(r'!\[', md_text))
    log.info("Found %d figure references", n_figs)

    # Run pandoc
    log.info("Running pandoc...")
    cmd = [
        "pandoc", str(fixed_md),
        "-o", str(AN_TEX),
        "--standalone",
        "-V", "geometry:margin=1in",
        "-V", "documentclass:article",
        "-V", "fontsize:11pt",
        "--number-sections",
        "--toc",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(EXEC_DIR))
    if result.returncode != 0:
        log.error("pandoc failed: %s", result.stderr)
        return

    # Post-process the LaTeX to fix figure sizing
    tex_text = AN_TEX.read_text()

    # Make figures fit in the page width
    tex_text = tex_text.replace(
        r"\includegraphics{",
        r"\includegraphics[width=\textwidth,height=0.4\textheight,keepaspectratio]{"
    )

    # No additional packages needed beyond pandoc defaults

    AN_TEX.write_text(tex_text)
    log.info("Wrote %s", AN_TEX)

    # Compile twice for cross-references
    for pass_num in (1, 2):
        log.info("pdflatex pass %d...", pass_num)
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", str(AN_TEX)],
            capture_output=True, text=True, cwd=str(EXEC_DIR),
            timeout=120,
        )
        if result.returncode != 0:
            # Check for actual errors vs warnings
            errors = [l for l in result.stdout.split('\n') if l.startswith('!')]
            if errors:
                log.warning("LaTeX errors (pass %d):", pass_num)
                for e in errors[:10]:
                    log.warning("  %s", e)

    if AN_PDF.exists():
        size_kb = AN_PDF.stat().st_size / 1024
        log.info("SUCCESS: %s (%.0f KB)", AN_PDF, size_kb)
    else:
        log.error("PDF not produced! Check ANALYSIS_NOTE.log")


if __name__ == "__main__":
    main()
