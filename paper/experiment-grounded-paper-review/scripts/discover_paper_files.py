#!/usr/bin/env python3
"""Discover the core files of a paper project from a directory."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


TITLE_RE = re.compile(r"\\title\{([^}]*)\}")


def score_tex(path: Path) -> tuple[int, dict]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    score = 0
    signals = {
        "has_documentclass": "\\documentclass" in text,
        "has_begin_document": "\\begin{document}" in text,
        "has_title": "\\title{" in text,
        "has_maketitle": "\\maketitle" in text,
        "has_abstract": "\\begin{abstract}" in text,
        "has_bibliography": "\\bibliography{" in text or "\\addbibresource{" in text,
        "has_section": "\\section{" in text,
        "mentions_appendix": "\\appendix" in text,
    }
    weights = {
        "has_documentclass": 8,
        "has_begin_document": 6,
        "has_title": 5,
        "has_maketitle": 5,
        "has_abstract": 4,
        "has_bibliography": 3,
        "has_section": 2,
        "mentions_appendix": -2,
    }
    for key, enabled in signals.items():
        if enabled:
            score += weights[key]
    title_match = TITLE_RE.search(text)
    title = title_match.group(1).strip() if title_match else ""
    return score, {"path": str(path), "score": score, "title": title, **signals}


def discover(root: Path) -> dict:
    tex_files = sorted(root.rglob("*.tex"))
    pdf_files = sorted(root.rglob("*.pdf"))
    bib_files = sorted(root.rglob("*.bib"))
    bbl_files = sorted(root.rglob("*.bbl"))

    tex_scores = []
    for tex_file in tex_files:
        score, detail = score_tex(tex_file)
        tex_scores.append(detail)
    tex_scores.sort(key=lambda item: item["score"], reverse=True)
    main_tex = tex_scores[0]["path"] if tex_scores else None
    main_tex_path = Path(main_tex) if main_tex else None

    ranked_pdfs = []
    for pdf_file in pdf_files:
        score = 0
        rel_parts = [part.lower() for part in pdf_file.relative_to(root).parts]
        if any(part in {"fig", "figs", "figure", "figures", "eps", "images", "imgs"} for part in rel_parts[:-1]):
            score -= 8
        if pdf_file.parent == root:
            score += 6
        if main_tex_path and pdf_file.stem == main_tex_path.stem:
            score += 10
        if "supp" in pdf_file.stem.lower() or "appendix" in pdf_file.stem.lower():
            score -= 2
        ranked_pdfs.append({"path": str(pdf_file), "score": score})
    ranked_pdfs.sort(key=lambda item: item["score"], reverse=True)
    main_pdf = ranked_pdfs[0]["path"] if ranked_pdfs and ranked_pdfs[0]["score"] >= 0 else None

    figure_dirs = []
    table_files = []
    supplement_files = []
    for path in sorted(root.rglob("*")):
        if path.is_dir() and path.name.lower() in {"fig", "figs", "figure", "figures", "eps", "images", "imgs"}:
            figure_dirs.append(str(path))
        if path.is_file() and "table" in path.parts and path.suffix.lower() == ".tex":
            table_files.append(str(path))
        if path.is_file() and any(part.lower() in {"supp", "supplement", "appendix"} for part in path.parts):
            supplement_files.append(str(path))

    title = tex_scores[0]["title"] if tex_scores else ""
    return {
        "root": str(root),
        "main_tex": main_tex,
        "main_pdf": main_pdf,
        "title": title,
        "tex_candidates": tex_scores,
        "pdf_candidates": ranked_pdfs,
        "bib_files": [str(path) for path in bib_files],
        "bbl_files": [str(path) for path in bbl_files],
        "figure_dirs": figure_dirs,
        "table_files": table_files,
        "supplement_files": supplement_files,
    }


def write_markdown(manifest: dict, output: Path) -> None:
    lines = ["# Paper Manifest", ""]
    lines.append(f'- Root: `{manifest["root"]}`')
    lines.append(f'- Main TeX: `{manifest.get("main_tex") or ""}`')
    lines.append(f'- Main PDF: `{manifest.get("main_pdf") or ""}`')
    if manifest.get("title"):
        lines.append(f'- Title: {manifest["title"]}')
    lines.extend(["", "## TeX Candidates", "", "| Path | Score | Title |", "|---|---:|---|"])
    for item in manifest["tex_candidates"]:
        lines.append(f'| {item["path"]} | {item["score"]} | {item["title"].replace("|", "/")} |')
    if manifest.get("pdf_candidates"):
        lines.extend(["", "## PDF Candidates", "", "| Path | Score |", "|---|---:|"])
        for item in manifest["pdf_candidates"]:
            lines.append(f'| {item["path"]} | {item["score"]} |')
    lines.extend(["", "## Resource Summary", ""])
    lines.append(f'- Bib files: {len(manifest["bib_files"])}')
    lines.append(f'- BBL files: {len(manifest["bbl_files"])}')
    lines.append(f'- Figure directories: {len(manifest["figure_dirs"])}')
    lines.append(f'- Table files: {len(manifest["table_files"])}')
    lines.append(f'- Supplemental files: {len(manifest["supplement_files"])}')
    lines.append("")
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paper_root", help="Path to a paper project directory")
    parser.add_argument("--json-out", default="paper_manifest.json", help="Manifest JSON output")
    parser.add_argument("--md-out", default="paper_manifest.md", help="Manifest Markdown output")
    args = parser.parse_args()

    manifest = discover(Path(args.paper_root).resolve())
    Path(args.json_out).write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    write_markdown(manifest, Path(args.md_out))


if __name__ == "__main__":
    main()
