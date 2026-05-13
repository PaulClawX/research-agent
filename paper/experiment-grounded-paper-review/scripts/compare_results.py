#!/usr/bin/env python3
"""Compare claimed numbers against experimental numbers and emit discrepancies."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def index_experiments(experiments: list[dict]) -> dict[str, dict]:
    indexed = {}
    for experiment in experiments:
        key = experiment.get("experiment_id")
        if key:
            indexed[key] = experiment
    return indexed


def compare(claimed: list[dict], experiments: dict[str, dict], tolerance: float) -> list[dict]:
    mismatches = []
    for item in claimed:
        exp = experiments.get(item["experiment_id"])
        if not exp:
            mismatches.append(
                {
                    "kind": "missing_experiment",
                    "experiment_id": item["experiment_id"],
                    "claim_text": item.get("claim_text", ""),
                    "message": "No matching experiment record was found.",
                }
            )
            continue
        claimed_value = item.get("claimed_value")
        result_value = exp.get("result_value")
        if claimed_value is None or result_value is None:
            continue
        delta = abs(float(claimed_value) - float(result_value))
        if delta > tolerance:
            mismatches.append(
                {
                    "kind": "value_mismatch",
                    "experiment_id": item["experiment_id"],
                    "claim_text": item.get("claim_text", ""),
                    "claimed_value": claimed_value,
                    "result_value": result_value,
                    "delta": delta,
                    "message": "Claimed value differs from recorded experiment result.",
                }
            )
    return mismatches


def write_markdown(mismatches: list[dict], output: Path) -> None:
    lines = ["# Result Comparison Report", ""]
    if not mismatches:
        lines.extend(["No mismatches found within the configured tolerance.", ""])
        output.write_text("\n".join(lines), encoding="utf-8")
        return
    lines.extend(["| Kind | Experiment | Claimed | Result | Delta | Message |", "|---|---|---:|---:|---:|---|"])
    for item in mismatches:
        lines.append(
            f'| {item.get("kind", "")} | {item.get("experiment_id", "")} | {item.get("claimed_value", "")} | '
            f'{item.get("result_value", "")} | {item.get("delta", "")} | {item.get("message", "")} |'
        )
    lines.append("")
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("claimed_json", help="JSON list of claimed values keyed by experiment id")
    parser.add_argument("experiments_json", help="JSON experiment ledger")
    parser.add_argument("--tolerance", type=float, default=1e-6, help="Allowed absolute difference")
    parser.add_argument("--json-out", default="result_comparison.json", help="Mismatch JSON output")
    parser.add_argument("--md-out", default="result_comparison.md", help="Mismatch Markdown output")
    args = parser.parse_args()

    claimed = json.loads(Path(args.claimed_json).read_text(encoding="utf-8"))
    experiments = json.loads(Path(args.experiments_json).read_text(encoding="utf-8"))
    mismatches = compare(claimed, index_experiments(experiments), args.tolerance)

    Path(args.json_out).write_text(json.dumps(mismatches, indent=2), encoding="utf-8")
    write_markdown(mismatches, Path(args.md_out))


if __name__ == "__main__":
    main()
