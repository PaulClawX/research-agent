#!/usr/bin/env python3
"""Extract numeric evidence snippets from repository READMEs and experiment logs."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


README_CANDIDATES = ["README.md", "readme.md", "README", "Readme.md"]
NUMBER_RE = re.compile(r"(?<![A-Za-z0-9])(\d+(?:\.\d+)?)(%|x)?")
KEYWORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9.+-]{2,}")
INTERESTING_HINTS = [
    "error",
    "accuracy",
    "acc",
    "top-1",
    "top-5",
    "map",
    "mAP",
    "improvement",
    "improve",
    "relative",
    "faster",
    "latency",
    "cifar",
    "imagenet",
    "coco",
    "state-of-the-art",
]


def read_text_if_exists(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8", errors="ignore")
    return ""


def extract_keywords(text: str) -> list[str]:
    keywords = []
    seen = set()
    for match in KEYWORD_RE.findall(text.lower()):
        if match not in seen:
            seen.add(match)
            keywords.append(match)
    return keywords


def parse_numbers(text: str) -> list[dict]:
    numbers = []
    for match in NUMBER_RE.finditer(text):
        try:
            value = float(match.group(1))
        except ValueError:
            continue
        unit = match.group(2) or ""
        numbers.append({"value": value, "unit": unit, "raw": match.group(0)})
    return numbers


def line_is_interesting(line: str) -> bool:
    lowered = line.lower()
    has_number = bool(NUMBER_RE.search(line))
    has_hint = any(hint.lower() in lowered for hint in INTERESTING_HINTS)
    return has_number and has_hint


def extract_snippets_from_text(text: str, source_file: str, source_type: str, experiment_id: str | None) -> list[dict]:
    snippets = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        if not line_is_interesting(line):
            continue
        cleaned = re.sub(r"\s+", " ", line).strip()
        if not cleaned:
            continue
        snippets.append(
            {
                "source_type": source_type,
                "source_file": source_file,
                "experiment_id": experiment_id,
                "line_no": line_no,
                "snippet": cleaned[:500],
                "numbers": parse_numbers(cleaned),
                "keywords": extract_keywords(cleaned),
            }
        )
    return snippets


def extract_readme_evidence(repo_path: Path, experiment_id: str | None) -> list[dict]:
    for candidate in README_CANDIDATES:
        path = repo_path / candidate
        if path.exists():
            return extract_snippets_from_text(read_text_if_exists(path), str(path), "readme", experiment_id)
    return []


def extract_log_evidence(log_path: Path, experiment_id: str | None, source_type: str) -> list[dict]:
    return extract_snippets_from_text(read_text_if_exists(log_path), str(log_path), source_type, experiment_id)


def write_markdown(items: list[dict], output: Path) -> None:
    lines = [
        "# Numeric Evidence",
        "",
        "| Source Type | Experiment | File | Line | Numbers | Snippet |",
        "|---|---|---|---:|---|---|",
    ]
    for item in items:
        number_text = ", ".join(n["raw"] for n in item.get("numbers", []))
        snippet = item["snippet"].replace("|", "/")
        lines.append(
            f'| {item["source_type"]} | {item.get("experiment_id") or ""} | {item["source_file"]} | '
            f'{item["line_no"]} | {number_text} | {snippet} |'
        )
    lines.append("")
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("experiments_json", help="Experiment ledger JSON")
    parser.add_argument("--json-out", default="NUMERIC_EVIDENCE.json", help="Extracted evidence JSON output")
    parser.add_argument("--md-out", default="NUMERIC_EVIDENCE.md", help="Extracted evidence Markdown output")
    args = parser.parse_args()

    experiments = json.loads(Path(args.experiments_json).read_text(encoding="utf-8"))
    evidence_items = []
    for experiment in experiments:
        repo_path = Path(experiment["repo_path"])
        evidence_items.extend(extract_readme_evidence(repo_path, experiment.get("experiment_id")))
        stdout_log = Path(experiment["stdout_log"])
        stderr_log = Path(experiment["stderr_log"])
        if stdout_log.exists():
            evidence_items.extend(extract_log_evidence(stdout_log, experiment.get("experiment_id"), "stdout_log"))
        if stderr_log.exists():
            evidence_items.extend(extract_log_evidence(stderr_log, experiment.get("experiment_id"), "stderr_log"))

    Path(args.json_out).write_text(json.dumps(evidence_items, indent=2, ensure_ascii=False), encoding="utf-8")
    write_markdown(evidence_items, Path(args.md_out))


if __name__ == "__main__":
    main()
