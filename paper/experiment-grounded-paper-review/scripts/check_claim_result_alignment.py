#!/usr/bin/env python3
"""Check whether claim records are supported by experiment records."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


RESTRICTED_TERMS = {
    "significant": "No statistical evidence recorded.",
    "state-of-the-art": "Strongest-baseline coverage not automatically verified.",
    "robust": "Robustness requires perturbation or transfer experiments.",
    "generalizes": "Generalization requires held-out-domain evidence.",
    "generalize": "Generalization requires held-out-domain evidence.",
}


def index_support(experiments: list[dict]) -> dict[str, list[dict]]:
    support = {}
    for experiment in experiments:
        for claim_id in experiment.get("supports", []):
            support.setdefault(claim_id, []).append(experiment)
    return support


def evaluate_claim(claim: dict, support_map: dict[str, list[dict]]) -> dict:
    experiments = support_map.get(claim["claim_id"], [])
    status = "unsupported"
    reasons = []
    if experiments:
        if any(exp.get("status") in {"verified_main_table", "verified_multi_seed"} for exp in experiments):
            status = "supported"
        else:
            status = "partially_supported"
    else:
        reasons.append("No supporting experiment was linked.")

    lower = claim["text"].lower()
    for term, reason in RESTRICTED_TERMS.items():
        if term in lower:
            reasons.append(reason)
            if status == "supported":
                status = "partially_supported"

    return {
        "claim_id": claim["claim_id"],
        "location": claim.get("location", ""),
        "section": claim.get("section", ""),
        "text": claim["text"],
        "status": status,
        "linked_experiments": [exp["experiment_id"] for exp in experiments],
        "required_action": "weaken or verify" if status != "supported" else "none",
        "reasons": reasons,
    }


def write_markdown(report: list[dict], output: Path) -> None:
    lines = ["# Inconsistency Report", "", "| Claim ID | Section | Status | Linked Experiments | Required Action |", "|---|---|---|---|---|"]
    for item in report:
        lines.append(
            f'| {item["claim_id"]} | {item["section"]} | {item["status"]} | '
            f'{", ".join(item["linked_experiments"])} | {item["required_action"]} |'
        )
        if item["reasons"]:
            lines.append(f'|  |  |  |  | {"; ".join(item["reasons"]).replace("|", "/")} |')
    lines.append("")
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("claims_json", help="Claim ledger JSON")
    parser.add_argument("experiments_json", help="Experiment ledger JSON")
    parser.add_argument("--json-out", default="INCONSISTENCY_REPORT.json", help="JSON report output")
    parser.add_argument("--md-out", default="INCONSISTENCY_REPORT.md", help="Markdown report output")
    args = parser.parse_args()

    claims = json.loads(Path(args.claims_json).read_text(encoding="utf-8"))
    experiments = json.loads(Path(args.experiments_json).read_text(encoding="utf-8"))
    support_map = index_support(experiments)
    report = [evaluate_claim(claim, support_map) for claim in claims]

    Path(args.json_out).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    write_markdown(report, Path(args.md_out))


if __name__ == "__main__":
    main()
