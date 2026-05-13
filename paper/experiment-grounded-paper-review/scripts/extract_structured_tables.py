#!/usr/bin/env python3
"""Extract structured table rows from README markdown tables and LaTeX tabular blocks."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


README_CANDIDATES = ["README.md", "readme.md", "README", "Readme.md"]
NUMBER_RE = re.compile(r"[-+]?\d+(?:\.\d+)?")
LATEX_COMMAND_RE = re.compile(r"\\[a-zA-Z@]+(?:\[[^\]]*\])?(?:\{[^{}]*\})?")
CAPTION_RE = re.compile(r"\\caption\{([^}]*)\}")
TABULAR_RE = re.compile(r"\\begin\{tabular\}.*?\\end\{tabular\}", re.DOTALL)


def clean_cell(text: str) -> str:
    text = text.replace("\\\\", " ")
    text = text.replace("\\%", "%")
    text = re.sub(r"\$([^$]*)\$", r"\1", text)
    text = re.sub(r"\\textcolor\{[^}]*\}\{([^}]*)\}", r"\1", text)
    text = re.sub(r"\\(textbf|underline|mathbf|mathrm|emph)\{([^}]*)\}", r"\2", text)
    text = LATEX_COMMAND_RE.sub(" ", text)
    text = text.replace("{", " ").replace("}", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def parse_numeric_cells(headers: list[str], row: list[str]) -> list[dict]:
    numeric_cells = []
    for idx, cell in enumerate(row):
        numbers = [float(match.group(0)) for match in NUMBER_RE.finditer(cell)]
        if not numbers:
            continue
        numeric_cells.append(
            {
                "column_index": idx,
                "header": headers[idx] if idx < len(headers) else f"col_{idx}",
                "raw": cell,
                "values": numbers,
            }
        )
    return numeric_cells


def parse_markdown_table_lines(lines: list[str], source_file: str, experiment_id: str | None, table_index: int) -> list[dict]:
    parsed = []
    if len(lines) < 3:
        return parsed
    header = [cell.strip() for cell in lines[0].strip().strip("|").split("|")]
    separator = [cell.strip() for cell in lines[1].strip().strip("|").split("|")]
    if not header or not all(set(cell) <= {"-", ":"} for cell in separator if cell):
        return parsed
    for row_idx, line in enumerate(lines[2:], start=1):
        row = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(row) != len(header):
            continue
        numeric_cells = parse_numeric_cells(header, row)
        if not numeric_cells:
            continue
        row_label = row[0]
        parsed.append(
            {
                "source_type": "markdown_table_row",
                "source_file": source_file,
                "experiment_id": experiment_id,
                "table_id": f"md_table_{table_index}",
                "table_caption": "",
                "headers": header,
                "row_index": row_idx,
                "row_label": row_label,
                "row_cells": row,
                "numeric_cells": numeric_cells,
                "snippet": " | ".join(row),
                "keywords": extract_keywords(" ".join(row + header)),
            }
        )
    return parsed


def extract_keywords(text: str) -> list[str]:
    seen = set()
    out = []
    for token in re.findall(r"[A-Za-z][A-Za-z0-9.+-]{1,}", text.lower()):
        if token not in seen:
            seen.add(token)
            out.append(token)
    return out


def extract_markdown_tables(repo_path: Path, experiment_id: str | None) -> list[dict]:
    for candidate in README_CANDIDATES:
        path = repo_path / candidate
        if not path.exists():
            continue
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        tables = []
        current = []
        table_index = 1
        for line in lines:
            if "|" in line:
                current.append(line)
            else:
                if current:
                    tables.extend(parse_markdown_table_lines(current, str(path), experiment_id, table_index))
                    table_index += 1
                    current = []
        if current:
            tables.extend(parse_markdown_table_lines(current, str(path), experiment_id, table_index))
        return tables
    return []


def find_caption_near(text: str, block_start: int) -> str:
    window_start = max(0, block_start - 500)
    prefix = text[window_start:block_start]
    matches = list(CAPTION_RE.finditer(prefix))
    if not matches:
        return ""
    return clean_cell(matches[-1].group(1))


def extract_latex_tables_from_file(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    rows = []
    table_index = 1
    for match in TABULAR_RE.finditer(text):
        block = match.group(0)
        caption = find_caption_near(text, match.start())
        cleaned_block = block.replace("\n", " ")
        pieces = [piece.strip() for piece in re.split(r"\\\\", cleaned_block) if piece.strip()]
        logical_rows = []
        for piece in pieces:
            if any(token in piece for token in ["\\toprule", "\\midrule", "\\bottomrule", "\\hline"]):
                # Preserve any row content outside the rule command.
                piece = re.sub(r"\\(toprule|midrule|bottomrule)(\[[^\]]*\])?", " ", piece)
                piece = piece.replace("\\hline", " ")
            piece = clean_cell(piece)
            if "&" not in piece:
                continue
            logical_rows.append([clean_cell(cell) for cell in piece.split("&")])
        if len(logical_rows) < 2:
            table_index += 1
            continue
        header = logical_rows[0]
        for row_idx, row in enumerate(logical_rows[1:], start=1):
            if len(row) < 2:
                continue
            numeric_cells = parse_numeric_cells(header, row)
            if not numeric_cells:
                continue
            rows.append(
                {
                    "source_type": "latex_table_row",
                    "source_file": str(path),
                    "experiment_id": None,
                    "table_id": f"latex_table_{table_index}",
                    "table_caption": caption,
                    "headers": header,
                    "row_index": row_idx,
                    "row_label": row[0],
                    "row_cells": row,
                    "numeric_cells": numeric_cells,
                    "snippet": " | ".join(row),
                    "keywords": extract_keywords(" ".join(row + header + ([caption] if caption else []))),
                }
            )
        table_index += 1
    return rows


def write_markdown(items: list[dict], output: Path) -> None:
    lines = [
        "# Structured Table Evidence",
        "",
        "| Source Type | Experiment | File | Table | Row Label | Numeric Cells | Caption |",
        "|---|---|---|---|---|---|---|",
    ]
    for item in items:
        numbers = []
        for cell in item.get("numeric_cells", []):
            joined = ",".join(str(value) for value in cell.get("values", []))
            numbers.append(f'{cell.get("header", "")}={joined}')
        lines.append(
            f'| {item["source_type"]} | {item.get("experiment_id") or ""} | {item["source_file"]} | '
            f'{item["table_id"]} | {item.get("row_label", "").replace("|", "/")} | '
            f'{"; ".join(numbers).replace("|", "/")} | {item.get("table_caption", "").replace("|", "/")} |'
        )
    lines.append("")
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paper_root", help="Path to paper directory")
    parser.add_argument("experiments_json", help="Experiment ledger JSON")
    parser.add_argument("--json-out", default="TABLE_EVIDENCE.json", help="Structured table evidence JSON output")
    parser.add_argument("--md-out", default="TABLE_EVIDENCE.md", help="Structured table evidence Markdown output")
    args = parser.parse_args()

    paper_root = Path(args.paper_root).resolve()
    experiments = json.loads(Path(args.experiments_json).read_text(encoding="utf-8"))

    items = []
    for experiment in experiments:
        items.extend(extract_markdown_tables(Path(experiment["repo_path"]), experiment.get("experiment_id")))

    for tex_file in sorted(paper_root.rglob("*.tex")):
        items.extend(extract_latex_tables_from_file(tex_file))

    Path(args.json_out).write_text(json.dumps(items, indent=2, ensure_ascii=False), encoding="utf-8")
    write_markdown(items, Path(args.md_out))


if __name__ == "__main__":
    main()
