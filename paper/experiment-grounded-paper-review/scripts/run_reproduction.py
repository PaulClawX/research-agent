#!/usr/bin/env python3
"""Run repository setup and evaluation commands from a simple JSON config."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path


def run_command(command: str, cwd: Path, timeout_seconds: int) -> tuple[int, str, str]:
    try:
        proc = subprocess.run(
            command,
            cwd=str(cwd),
            shell=True,
            text=True,
            capture_output=True,
            env=os.environ.copy(),
            timeout=timeout_seconds,
        )
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = (exc.stderr or "") + f"\nTIMEOUT after {timeout_seconds}s"
        return 124, stdout, stderr


def git_commit(repo_path: Path) -> str:
    code, stdout, _ = run_command("git rev-parse --short HEAD", repo_path, 60)
    return stdout.strip() if code == 0 else ""


def ensure_repo(entry: dict, workspace: Path) -> Path:
    if entry.get("repo_path"):
        return Path(entry["repo_path"]).expanduser().resolve()
    repo_url = entry["repo_url"]
    repo_name = entry.get("repo_name") or Path(repo_url).stem.replace(".git", "")
    repo_path = workspace / repo_name
    if repo_path.exists():
        run_command("git fetch --all --tags", repo_path, 180)
    else:
        run_command(f'git clone "{repo_url}" "{repo_path}"', workspace, 900)
    if entry.get("checkout"):
        run_command(f'git checkout "{entry["checkout"]}"', repo_path, 120)
    return repo_path


def write_logs(log_dir: Path, experiment_id: str, stdout: str, stderr: str) -> tuple[str, str]:
    log_dir.mkdir(parents=True, exist_ok=True)
    stdout_path = log_dir / f"{experiment_id}.stdout.txt"
    stderr_path = log_dir / f"{experiment_id}.stderr.txt"
    stdout_path.write_text(stdout, encoding="utf-8")
    stderr_path.write_text(stderr, encoding="utf-8")
    return str(stdout_path), str(stderr_path)


def compute_deltas(result_value, baseline_value):
    if result_value is None or baseline_value is None:
        return None, None
    absolute_delta = round(float(result_value) - float(baseline_value), 6)
    relative_delta = None
    if float(baseline_value) != 0:
        relative_delta = round(absolute_delta / float(baseline_value) * 100.0, 6)
    return absolute_delta, relative_delta


def write_markdown(experiments: list[dict], output: Path) -> None:
    lines = ["# Experiment Ledger", "", "| Experiment | Repo | Status | Metric | Result | Baseline | Command | Supports |", "|---|---|---|---|---:|---:|---|---|"]
    for exp in experiments:
        lines.append(
            f'| {exp["experiment_id"]} | {exp.get("repo_name", "")} | {exp.get("status", "")} | '
            f'{exp.get("metric", "")} | {exp.get("result_value", "")} | {exp.get("baseline_value", "")} | '
            f'`{exp.get("command", "")}` | {", ".join(exp.get("supports", []))} |'
        )
    lines.append("")
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config_json", help="Path to reproduction config JSON")
    parser.add_argument("--workspace", default="repos", help="Clone workspace")
    parser.add_argument("--json-out", default="EXPERIMENTS.json", help="JSON ledger output")
    parser.add_argument("--md-out", default="EXPERIMENT_LEDGER.md", help="Markdown ledger output")
    parser.add_argument("--log-dir", default="logs", help="Log directory")
    parser.add_argument("--timeout-seconds", type=int, default=600, help="Timeout for each setup or eval command")
    args = parser.parse_args()

    config = json.loads(Path(args.config_json).read_text(encoding="utf-8"))
    workspace = Path(args.workspace).resolve()
    workspace.mkdir(parents=True, exist_ok=True)
    experiments = []

    for idx, entry in enumerate(config.get("experiments", []), start=1):
        experiment_id = entry.get("experiment_id") or f"E-{idx:03d}"
        repo_path = ensure_repo(entry, workspace)
        setup_status = "ready"
        for setup_cmd in entry.get("setup_commands", []):
            code, stdout, stderr = run_command(setup_cmd, repo_path, args.timeout_seconds)
            write_logs(Path(args.log_dir), f"{experiment_id}.setup", stdout, stderr)
            if code != 0:
                experiments.append(
                    {
                        "experiment_id": experiment_id,
                        "repo_name": entry.get("repo_name", repo_path.name),
                        "repo_path": str(repo_path),
                        "commit": git_commit(repo_path),
                        "dataset": entry.get("dataset", ""),
                        "split": entry.get("split", ""),
                        "metric": entry.get("metric", ""),
                        "result_value": entry.get("result_value"),
                        "baseline_value": entry.get("baseline_value"),
                        "absolute_delta": None,
                        "relative_delta_percent": None,
                        "status": "setup_failed",
                        "command": setup_cmd,
                        "stdout_log": "",
                        "stderr_log": "",
                        "return_code": code,
                        "supports": entry.get("supports", []),
                        "notes": "Setup command failed before evaluation.",
                    }
                )
                setup_status = "failed"
                break
        if setup_status == "failed":
            continue

        command = entry["command"]
        code, stdout, stderr = run_command(command, repo_path, args.timeout_seconds)
        stdout_log, stderr_log = write_logs(Path(args.log_dir), experiment_id, stdout, stderr)
        absolute_delta, relative_delta = compute_deltas(entry.get("result_value"), entry.get("baseline_value"))
        failure_status = entry.get("status_on_failure", "probe_failed")
        experiments.append(
            {
                "experiment_id": experiment_id,
                "repo_name": entry.get("repo_name", repo_path.name),
                "repo_path": str(repo_path),
                "commit": git_commit(repo_path),
                "dataset": entry.get("dataset", ""),
                "split": entry.get("split", ""),
                "metric": entry.get("metric", ""),
                "result_value": entry.get("result_value"),
                "baseline_value": entry.get("baseline_value"),
                "absolute_delta": absolute_delta,
                "relative_delta_percent": relative_delta,
                "status": entry.get("status_on_success", "ran_subset") if code == 0 else failure_status,
                "command": command,
                "stdout_log": stdout_log,
                "stderr_log": stderr_log,
                "return_code": code,
                "supports": entry.get("supports", []),
                "notes": entry.get("notes", ""),
            }
        )

    Path(args.json_out).write_text(json.dumps(experiments, indent=2), encoding="utf-8")
    write_markdown(experiments, Path(args.md_out))


if __name__ == "__main__":
    main()
