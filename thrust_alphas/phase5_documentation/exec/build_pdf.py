#!/usr/bin/env python3
"""Convert ANALYSIS_NOTE.md to PDF with embedded figures.

Strategy: collect all referenced figures into a local figures/ directory
(symlinks), convert figure references to proper markdown ![](path) syntax,
run pandoc -> tex, then pdflatex.

Usage: pixi run py phase5_documentation/exec/build_pdf.py
"""
import re
import subprocess
import shutil
import logging
from pathlib import Path
from rich.logging import RichHandler

logging.basicConfig(level=logging.INFO, format="%(message)s",
                    handlers=[RichHandler(rich_tracebacks=True)])
log = logging.getLogger(__name__)

EXEC_DIR = Path(__file__).parent
AN_MD = EXEC_DIR / "ANALYSIS_NOTE.md"
FIG_DIR = EXEC_DIR / "figures"


def collect_figures(md_text: str) -> dict[str, Path]:
    """Find all figure paths in backtick references and map to local names."""
    paths = re.findall(r'`(\.\.\/\.\.\/.+?\.pdf)`', md_text)
    mapping = {}
    for rel_path in paths:
        src = (EXEC_DIR / rel_path).resolve()
        local_name = src.name
        # Handle name collisions by prepending phase
        if local_name in mapping and mapping[local_name] != src:
            parts = rel_path.split('/')
            phase = parts[2] if len(parts) > 2 else "unknown"
            local_name = f"{phase}_{local_name}"
        mapping[local_name] = src
    return mapping


def prepare_figures(mapping: dict[str, Path]) -> int:
    """Symlink or copy figures into local figures/ directory."""
    FIG_DIR.mkdir(exist_ok=True)
    # Clean old symlinks
    for f in FIG_DIR.iterdir():
        f.unlink()

    ok = 0
    for local_name, src in mapping.items():
        dst = FIG_DIR / local_name
        if src.exists():
            dst.symlink_to(src)
            ok += 1
        else:
            log.warning("MISSING: %s", src)
    return ok


def convert_references(md_text: str, mapping: dict[str, Path]) -> str:
    """Convert backtick figure references to markdown image syntax with local paths."""
    # Build reverse mapping: original relative path -> local figure name
    path_to_local = {}
    for local_name, src in mapping.items():
        # Find the original relative paths that map to this source
        for rel_path in re.findall(r'`(\.\.\/\.\.\/.+?\.pdf)`', md_text):
            if (EXEC_DIR / rel_path).resolve() == src:
                path_to_local[rel_path] = local_name

    # Replace **Figure:** `path` — caption patterns with ![caption](figures/name)
    # First: single figure lines
    def replace_fig_line(m):
        full = m.group(0)
        paths_in_line = re.findall(r'`(\.\.\/\.\.\/.+?\.pdf)`', full)
        if not paths_in_line:
            return full

        # Extract caption: everything after the last backtick-path
        caption_match = re.search(r'\.pdf`[.,]?\s*(?:[—–-]\s*)?(.+?)$', full)
        caption = caption_match.group(1).strip().rstrip('.') if caption_match else ""

        result_parts = []
        for p in paths_in_line:
            local = path_to_local.get(p, Path(p).name)
            result_parts.append(f"\n![{caption}](figures/{local})\n")

        return "\n".join(result_parts)

    # Match lines starting with **Figure(s):**
    md_text = re.sub(
        r'\*\*Figures?:\*\*.*?(?:\n(?![\n#*\-|]).*)*',
        replace_fig_line,
        md_text
    )

    # Also catch any remaining standalone backtick figure references
    def replace_standalone(m):
        rel_path = m.group(1)
        local = path_to_local.get(rel_path, Path(rel_path).name)
        return f"![](figures/{local})"

    md_text = re.sub(r'`(\.\.\/\.\.\/.+?\.pdf)`', replace_standalone, md_text)

    return md_text


def main():
    log.info("Reading %s", AN_MD)
    md_text = AN_MD.read_text()

    # Collect and prepare figures
    mapping = collect_figures(md_text)
    log.info("Found %d unique figures", len(mapping))
    n_ok = prepare_figures(mapping)
    log.info("Linked %d/%d figures into %s", n_ok, len(mapping), FIG_DIR)

    # Convert references to markdown image syntax
    md_converted = convert_references(md_text, mapping)

    # Count images
    n_imgs = len(re.findall(r'!\[', md_converted))
    log.info("Converted %d image references", n_imgs)

    # Write intermediate file
    converted_md = EXEC_DIR / "ANALYSIS_NOTE_for_pdf.md"
    converted_md.write_text(md_converted)

    # Run pandoc
    log.info("Running pandoc...")
    tex_file = EXEC_DIR / "ANALYSIS_NOTE.tex"
    cmd = [
        "pandoc", str(converted_md),
        "-o", str(tex_file),
        "--standalone",
        "-V", "geometry:margin=1in",
        "-V", "documentclass:article",
        "-V", "fontsize:11pt",
        "--number-sections",
        "--toc",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(EXEC_DIR))
    if r.returncode != 0:
        log.error("pandoc failed: %s", r.stderr)
        return

    # Post-process LaTeX: ensure figures are properly sized
    tex = tex_file.read_text()
    tex = tex.replace(
        r"\includegraphics{",
        r"\includegraphics[width=0.85\textwidth,keepaspectratio]{"
    )
    tex_file.write_text(tex)
    log.info("Wrote %s", tex_file)

    # Compile
    pdf_file = EXEC_DIR / "ANALYSIS_NOTE.pdf"
    for pass_num in (1, 2):
        log.info("pdflatex pass %d...", pass_num)
        r = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "ANALYSIS_NOTE.tex"],
            capture_output=True, text=True, cwd=str(EXEC_DIR), timeout=120,
        )
        errors = [l for l in r.stdout.split('\n') if l.startswith('!')]
        if errors:
            for e in errors[:5]:
                log.warning("  %s", e)

    if pdf_file.exists():
        import os
        pages_line = [l for l in r.stdout.split('\n') if 'Output written' in l]
        log.info("SUCCESS: %s (%.0f KB) %s",
                 pdf_file, pdf_file.stat().st_size / 1024,
                 pages_line[0] if pages_line else "")
    else:
        log.error("PDF not produced!")


if __name__ == "__main__":
    main()
