#!/usr/bin/env python3
"""Prepare an automatic reproduction config from ranked repository candidates."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


README_NAMES = ["README.md", "readme.md", "README", "Readme.md"]
PYTHON_EVAL_PATTERNS = [
    re.compile(r"python\s+([^\n`]*?(?:eval|test|infer|demo)[^\n`]*)", re.IGNORECASE),
    re.compile(r"python\s+([^\n`]*?main\.py[^\n`]*)", re.IGNORECASE),
]
RUN_FILE_PATTERNS = [
    re.compile(r"Run\s+`([^`]+?\.(?:lua|py|sh))`", re.IGNORECASE),
    re.compile(r"run\s+([A-Za-z0-9_./-]+?\.(?:lua|py|sh))", re.IGNORECASE),
]


def load_ranked_candidates(path: Path) -> list[dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload.get("candidates", payload if isinstance(payload, list) else [])


def discover_setup_commands(repo_path: Path) -> list[str]:
    has_lua = any(repo_path.glob("**/*.lua"))
    commands = []
    if has_lua and not (repo_path / "requirements.txt").exists() and not (repo_path / "pyproject.toml").exists():
        return commands
    commands.append("python3 -m venv .venv")
    if (repo_path / "requirements.txt").exists():
        commands.append(". .venv/bin/activate && pip install -r requirements.txt")
    elif (repo_path / "pyproject.toml").exists():
        commands.append(". .venv/bin/activate && pip install -e .")
    elif (repo_path / "setup.py").exists():
        commands.append(". .venv/bin/activate && pip install -e .")
    return commands


def read_readme(repo_path: Path) -> str:
    for name in README_NAMES:
        path = repo_path / name
        if path.exists():
            return path.read_text(encoding="utf-8", errors="ignore")
    return ""


def infer_eval_command_from_readme(repo_path: Path) -> tuple[str, str]:
    readme = read_readme(repo_path)
    for pattern in PYTHON_EVAL_PATTERNS:
        match = pattern.search(readme)
        if match:
            command = match.group(0).strip()
            script_match = re.search(r"python\s+([^\s]+\.py)", command)
            if script_match:
                script_path = script_match.group(1)
                return f". .venv/bin/activate && python {script_path} --help", f"Derived from README command `{command}`"
    for pattern in RUN_FILE_PATTERNS:
        match = pattern.search(readme)
        if not match:
            continue
        script_path = match.group(1).strip()
        if script_path.endswith(".lua"):
            return f"th {script_path} -h", f"Derived from README run instruction for `{script_path}`"
        if script_path.endswith(".py"):
            return f". .venv/bin/activate && python {script_path} --help", f"Derived from README run instruction for `{script_path}`"
        if script_path.endswith(".sh"):
            return f"bash {script_path} --help", f"Derived from README run instruction for `{script_path}`"
    return "", ""


def infer_eval_command_from_files(repo_path: Path) -> tuple[str, str]:
    for pattern in ["**/*eval*.py", "**/*test*.py", "**/demo.py", "**/inference.py", "**/infer.py"]:
        for path in sorted(repo_path.glob(pattern)):
            if ".venv" in path.parts or "site-packages" in path.parts:
                continue
            rel = path.relative_to(repo_path)
            return f". .venv/bin/activate && python {rel} --help", f"Discovered candidate script `{rel}`"
    for path in sorted(repo_path.glob("**/*.sh")):
        lower = path.name.lower()
        if any(token in lower for token in ["eval", "test", "demo", "infer"]):
            rel = path.relative_to(repo_path)
            return f"bash {rel} --help", f"Discovered candidate shell script `{rel}`"
    for pattern in ["**/*train*.lua", "**/*test*.lua", "**/*eval*.lua"]:
        for path in sorted(repo_path.glob(pattern)):
            if any(part.startswith(".") for part in path.parts):
                continue
            rel = path.relative_to(repo_path)
            return f"th {rel} -h", f"Discovered candidate Lua script `{rel}`"
    return "", ""


def build_experiment(repo_path: Path, candidate: dict, idx: int) -> dict:
    command, note = infer_eval_command_from_readme(repo_path)
    if not command:
        command, note = infer_eval_command_from_files(repo_path)
    status = "smoke_test_only"
    if not command:
        command = "pwd"
        note = "No eval or test command could be inferred automatically; falling back to repository accessibility probe."
        status = "cloned_only"

    return {
        "experiment_id": f"E-{idx:03d}",
        "repo_name": candidate.get("full_name") or candidate.get("name") or repo_path.name,
        "repo_path": str(repo_path.resolve()),
        "dataset": "",
        "split": "",
        "metric": "",
        "result_value": None,
        "baseline_value": None,
        "status_on_success": status,
        "setup_commands": discover_setup_commands(repo_path),
        "command": command,
        "supports": [],
        "notes": note,
    }


def write_markdown(config: dict, output: Path) -> None:
    lines = ["# Auto Reproduction Plan", "", "| Experiment | Repo | Command | Status On Success | Notes |", "|---|---|---|---|---|"]
    for experiment in config.get("experiments", []):
        lines.append(
            f'| {experiment["experiment_id"]} | {experiment["repo_name"]} | `{experiment["command"]}` | '
            f'{experiment["status_on_success"]} | {experiment["notes"].replace("|", "/")} |'
        )
    lines.append("")
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ranked_candidates_json", help="Ranked repository candidates JSON")
    parser.add_argument("--repos-dir", required=True, help="Directory containing cloned repositories")
    parser.add_argument("--top-k", type=int, default=3, help="Number of top repositories to include")
    parser.add_argument("--json-out", default="AUTO_REPRO_CONFIG.json", help="Output reproduction config JSON")
    parser.add_argument("--md-out", default="AUTO_REPRO_PLAN.md", help="Markdown summary output")
    args = parser.parse_args()

    repos_dir = Path(args.repos_dir).resolve()
    candidates = load_ranked_candidates(Path(args.ranked_candidates_json))[: args.top_k]
    experiments = []
    for idx, candidate in enumerate(candidates, start=1):
        repo_name = candidate.get("full_name") or candidate.get("name") or f"repo-{idx}"
        repo_dir_name = repo_name.split("/")[-1]
        repo_path = repos_dir / repo_dir_name
        if not repo_path.exists():
            continue
        experiments.append(build_experiment(repo_path, candidate, idx))

    payload = {"experiments": experiments}
    Path(args.json_out).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, Path(args.md_out))


if __name__ == "__main__":
    main()
