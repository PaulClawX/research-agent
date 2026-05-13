#!/usr/bin/env python3
"""Extract likely paper claims from TeX or plain-text sources into a ledger."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable


SECTION_PATTERN = re.compile(r"\\(section|subsection|subsubsection)\{([^}]*)\}")
COMMAND_PATTERN = re.compile(r"\\[a-zA-Z@]+(\[[^\]]*\])?(\{[^{}]*\})?")
CLAIM_CUES = [
    "improve",
    "improves",
    "improved",
    "outperform",
    "outperforms",
    "significant",
    "state-of-the-art",
    "robust",
    "generalize",
    "generalizes",
    "efficient",
    "faster",
    "lower cost",
    "novel",
    "first",
    "better than",
    "superior",
    "we show",
    "we demonstrate",
]


def read_sources(root: Path) -> list[Path]:
    if root.is_file():
        return [root]
    exts = {".tex", ".txt", ".md"}
    return sorted(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in exts)


def clean_tex(text: str) -> str:
    text = re.sub(r"(?<!\\)%.*", "", text)
    text = text.replace("~", " ")
    text = COMMAND_PATTERN.sub(" ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_sentences(text: str) -> Iterable[str]:
    for part in re.split(r"(?<=[.!?])\s+", text):
        part = part.strip()
        if part:
            yield part


def detect_claim_type(sentence: str) -> str:
    lower = sentence.lower()
    if any(word in lower for word in ["robust", "perturb", "noisy", "stability"]):
        return "robustness"
    if any(word in lower for word in ["generalize", "transfer", "across domains", "real-world"]):
        return "generalization"
    if any(word in lower for word in ["latency", "faster", "efficient", "runtime", "cost", "token"]):
        return "efficiency"
    if any(word in lower for word in ["first", "novel", "new paradigm", "unlike prior work"]):
        return "novelty"
    if any(word in lower for word in ["because", "reason", "due to", "module", "ablation"]):
        return "mechanistic"
    if any(word in lower for word in ["qualitative", "interpret", "case study", "human study"]):
        return "qualitative"
    if any(word in lower for word in ["could", "may", "potentially", "future"]):
        return "speculative"
    if any(word in lower for word in ["better than", "outperform", "compared with", "versus", "than prior"]):
        return "comparative"
    return "empirical"


def sentence_has_claim_cue(sentence: str) -> bool:
    lower = sentence.lower()
    return any(cue in lower for cue in CLAIM_CUES)


def extract_claims(path: Path, start_id: int) -> tuple[list[dict], int]:
    raw = path.read_text(encoding="utf-8", errors="ignore")
    current_section = "Unknown"
    claims: list[dict] = []
    lines = raw.splitlines()
    for line_no, line in enumerate(lines, start=1):
        section_match = SECTION_PATTERN.search(line)
        if section_match:
            current_section = section_match.group(2).strip() or current_section
        cleaned = clean_tex(line)
        if not cleaned:
            continue
        for sentence in split_sentences(cleaned):
            if not sentence_has_claim_cue(sentence):
                continue
            claim_id = f"C-{start_id:03d}"
            claims.append(
                {
                    "claim_id": claim_id,
                    "section": current_section,
                    "source_file": str(path),
                    "location": f"line {line_no}",
                    "text": sentence,
                    "claim_type": detect_claim_type(sentence),
                    "scope": "",
                    "required_evidence": [],
                    "current_evidence": [],
                    "status": "pending",
                    "supports": [],
                    "contradictions": [],
                    "required_revision": "",
                }
            )
            start_id += 1
    return claims, start_id


def write_markdown(claims: list[dict], output: Path) -> None:
    lines = ["# Claim Ledger", ""]
    if not claims:
        lines.extend(["No claims were extracted by heuristic rules.", ""])
        output.write_text("\n".join(lines), encoding="utf-8")
        return
    lines.extend(["| Claim ID | Section | Type | Location | Text | Status |", "|---|---|---|---|---|---|"])
    for claim in claims:
        text = claim["text"].replace("|", "\\|")
        lines.append(
            f'| {claim["claim_id"]} | {claim["section"]} | {claim["claim_type"]} | '
            f'{claim["location"]} | {text} | {claim["status"]} |'
        )
    lines.append("")
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_path", help="Path to a TeX project, TeX file, or text file")
    parser.add_argument("--json-out", default="CLAIMS.json", help="Output JSON path")
    parser.add_argument("--md-out", default="CLAIM_LEDGER.md", help="Output Markdown path")
    args = parser.parse_args()

    sources = read_sources(Path(args.input_path))
    claims: list[dict] = []
    next_id = 1
    for source in sources:
        extracted, next_id = extract_claims(source, next_id)
        claims.extend(extracted)

    Path(args.json_out).write_text(json.dumps(claims, indent=2, ensure_ascii=False), encoding="utf-8")
    write_markdown(claims, Path(args.md_out))


if __name__ == "__main__":
    main()
