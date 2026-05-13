#!/usr/bin/env python3
"""Apply exact-string LaTeX claim replacements from a JSON patch plan."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def apply_patch_to_file(file_path: Path, replacements: list[dict]) -> list[str]:
    text = file_path.read_text(encoding="utf-8")
    applied = []
    for replacement in replacements:
        old = replacement["old"]
        new = replacement["new"]
        count = text.count(old)
        if count == 0:
            continue
        text = text.replace(old, new)
        applied.append(f'{file_path}: replaced {count} occurrence(s) of "{old}"')
    file_path.write_text(text, encoding="utf-8")
    return applied


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("patch_json", help="Patch plan JSON")
    parser.add_argument("--report-out", default="latex_patch_report.md", help="Markdown report output")
    args = parser.parse_args()

    plan = json.loads(Path(args.patch_json).read_text(encoding="utf-8"))
    lines = ["# LaTeX Patch Report", ""]
    for file_entry in plan.get("files", []):
        file_path = Path(file_entry["path"]).resolve()
        applied = apply_patch_to_file(file_path, file_entry.get("replacements", []))
        if not applied:
            lines.append(f"- No replacements applied in `{file_path}`")
        else:
            lines.extend(f"- {item}" for item in applied)
    lines.append("")
    Path(args.report_out).write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
