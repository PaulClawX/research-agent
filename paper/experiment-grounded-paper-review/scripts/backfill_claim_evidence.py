#!/usr/bin/env python3
"""Backfill claim records with numeric and structured-table evidence."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SECTION_HINTS = ["imagenet", "cifar", "coco", "pascal", "mnist", "voc"]
NUMBER_RE = re.compile(r"(?<![A-Za-z0-9])(\d+(?:\.\d+)?)(%|x)?")
WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9.+-]{2,}")
STOPWORDS = {
    "the",
    "and",
    "with",
    "from",
    "this",
    "that",
    "these",
    "those",
    "using",
    "results",
    "result",
    "method",
    "paper",
    "show",
    "shows",
    "than",
    "into",
    "were",
    "have",
    "also",
    "their",
    "which",
}


def extract_numbers(text: str) -> list[float]:
    values = []
    for match in NUMBER_RE.finditer(text):
        try:
            values.append(float(match.group(1)))
        except ValueError:
            continue
    return values


def extract_keywords(text: str) -> set[str]:
    return {word.lower() for word in WORD_RE.findall(text) if word.lower() not in STOPWORDS}


def score_evidence(claim: dict, evidence: dict) -> tuple[int, bool]:
    score = 0
    claim_text = claim["text"]
    claim_keywords = extract_keywords(claim_text)
    evidence_keywords = set(evidence.get("keywords", [])) or extract_keywords(evidence.get("snippet", ""))
    overlap = claim_keywords & evidence_keywords
    score += min(len(overlap), 6) * 2

    claim_numbers = extract_numbers(claim_text)
    evidence_numbers = [item["value"] for item in evidence.get("numbers", [])]
    exact_numeric_match = False
    for claim_value in claim_numbers:
        for evidence_value in evidence_numbers:
            if abs(claim_value - evidence_value) < 1e-6:
                exact_numeric_match = True
                score += 8
            elif abs(claim_value - evidence_value) <= max(0.5, claim_value * 0.05):
                score += 3

    section_lower = claim.get("section", "").lower()
    snippet_lower = evidence.get("snippet", "").lower()
    for hint in SECTION_HINTS:
        if hint in section_lower and hint in snippet_lower:
            score += 4

    if claim.get("claim_type") == "comparative" and any(token in snippet_lower for token in ["improvement", "better", "error", "acc", "top-1", "top-5"]):
        score += 2
    if claim.get("claim_type") == "efficiency" and any(token in snippet_lower for token in ["faster", "speed", "latency", "flops", "cost"]):
        score += 2

    return score, exact_numeric_match


def score_table_evidence(claim: dict, evidence: dict) -> tuple[int, bool]:
    score = 0
    claim_text = claim["text"]
    claim_keywords = extract_keywords(claim_text)
    evidence_keywords = set(evidence.get("keywords", []))
    overlap = claim_keywords & evidence_keywords
    score += min(len(overlap), 8) * 3

    claim_numbers = extract_numbers(claim_text)
    exact_numeric_match = False
    for claim_value in claim_numbers:
        for cell in evidence.get("numeric_cells", []):
            for value in cell.get("values", []):
                if abs(claim_value - value) < 1e-6:
                    exact_numeric_match = True
                    score += 12
                elif abs(claim_value - value) <= max(0.5, abs(claim_value) * 0.05):
                    score += 4

    row_label = evidence.get("row_label", "").lower()
    if row_label and any(token in row_label for token in claim_keywords):
        score += 4

    caption = evidence.get("table_caption", "").lower()
    section_lower = claim.get("section", "").lower()
    for hint in SECTION_HINTS:
        if hint in section_lower and (hint in caption or hint in row_label):
            score += 5

    if claim.get("claim_type") == "comparative":
        if any("error" in cell.get("header", "").lower() or "acc" in cell.get("header", "").lower() for cell in evidence.get("numeric_cells", [])):
            score += 3
    if claim.get("claim_type") == "efficiency":
        if any(token in caption for token in ["flops", "latency", "speed", "time", "cost"]):
            score += 3

    return score, exact_numeric_match


def enrich_claim(claim: dict, evidence_items: list[dict], table_items: list[dict], experiments_by_id: dict[str, dict]) -> dict:
    scored = []
    any_exact_numeric_match = False
    for evidence in evidence_items:
        score, exact_numeric_match = score_evidence(claim, evidence)
        if score <= 0:
            continue
        if exact_numeric_match:
            any_exact_numeric_match = True
        scored.append((score, evidence))
    for evidence in table_items:
        score, exact_numeric_match = score_table_evidence(claim, evidence)
        if score <= 0:
            continue
        if exact_numeric_match:
            any_exact_numeric_match = True
        scored.append((score, evidence))
    scored.sort(key=lambda item: item[0], reverse=True)
    top_items = [item for _, item in scored[:3]]

    enriched = dict(claim)
    enriched.setdefault("current_evidence", [])
    enriched.setdefault("supports", [])
    enriched.setdefault("contradictions", [])

    evidence_strings = []
    support_ids = []
    for item in top_items:
        if item["source_type"] in {"markdown_table_row", "latex_table_row"}:
            numeric_summary = ", ".join(
                f'{cell.get("header", "")}={",".join(str(value) for value in cell.get("values", []))}'
                for cell in item.get("numeric_cells", [])
            )
            evidence_strings.append(
                f'{item["source_type"]}:{Path(item["source_file"]).name}:{item.get("row_label", "")}: {numeric_summary}'
            )
        else:
            evidence_strings.append(
                f'{item["source_type"]}:{Path(item["source_file"]).name}: {item["snippet"]}'
            )
        exp_id = item.get("experiment_id")
        if exp_id and exp_id not in support_ids:
            support_ids.append(exp_id)

    enriched["current_evidence"] = evidence_strings
    enriched["supports"] = support_ids

    if top_items:
        if any_exact_numeric_match:
            enriched["status"] = "partially_supported"
        else:
            enriched["status"] = "needs_manual_review"
    else:
        enriched["status"] = "pending"

    enriched["evidence_matches"] = [
        {
            "source_type": item["source_type"],
            "source_file": item["source_file"],
            "experiment_id": item.get("experiment_id"),
            "snippet": item["snippet"],
            "numbers": item.get("numbers", []),
        }
        for item in top_items
    ]

    if support_ids:
        for support_id in support_ids:
            experiment = experiments_by_id.get(support_id)
            if not experiment:
                continue
            if claim["claim_id"] not in experiment.get("supports", []):
                experiment.setdefault("supports", []).append(claim["claim_id"])

    return enriched


def write_markdown(claims: list[dict], output: Path) -> None:
    lines = [
        "# Claim Ledger",
        "",
        "| Claim ID | Section | Type | Location | Status | Supports | Evidence |",
        "|---|---|---|---|---|---|---|",
    ]
    for claim in claims:
        evidence_preview = "; ".join(claim.get("current_evidence", [])[:2]).replace("|", "/")
        lines.append(
            f'| {claim["claim_id"]} | {claim.get("section", "")} | {claim.get("claim_type", "")} | '
            f'{claim.get("location", "")} | {claim.get("status", "")} | '
            f'{", ".join(claim.get("supports", []))} | {evidence_preview[:220]} |'
        )
    lines.append("")
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("claims_json", help="Input claims JSON")
    parser.add_argument("evidence_json", help="Extracted evidence JSON")
    parser.add_argument("table_evidence_json", help="Structured table evidence JSON")
    parser.add_argument("experiments_json", help="Experiment ledger JSON")
    parser.add_argument("--claims-json-out", default="CLAIMS_ENRICHED.json", help="Enriched claims JSON output")
    parser.add_argument("--claims-md-out", default="CLAIM_LEDGER_ENRICHED.md", help="Enriched claims Markdown output")
    parser.add_argument("--experiments-json-out", default="EXPERIMENTS_ENRICHED.json", help="Updated experiment JSON output")
    args = parser.parse_args()

    claims = json.loads(Path(args.claims_json).read_text(encoding="utf-8"))
    evidence_items = json.loads(Path(args.evidence_json).read_text(encoding="utf-8"))
    table_items = json.loads(Path(args.table_evidence_json).read_text(encoding="utf-8"))
    experiments = json.loads(Path(args.experiments_json).read_text(encoding="utf-8"))
    experiments_by_id = {experiment["experiment_id"]: experiment for experiment in experiments}

    enriched_claims = [enrich_claim(claim, evidence_items, table_items, experiments_by_id) for claim in claims]

    Path(args.claims_json_out).write_text(json.dumps(enriched_claims, indent=2, ensure_ascii=False), encoding="utf-8")
    write_markdown(enriched_claims, Path(args.claims_md_out))
    Path(args.experiments_json_out).write_text(json.dumps(list(experiments_by_id.values()), indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
