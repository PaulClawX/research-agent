#!/usr/bin/env python3
"""Generate repository search queries, optionally search GitHub, and rank candidates."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path


def slugify(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def load_metadata(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def github_search_repositories(query: str, per_page: int) -> list[dict]:
    url = (
        "https://api.github.com/search/repositories"
        f"?q={query.replace(' ', '%20')}&sort=stars&order=desc&per_page={per_page}"
    )
    cmd = [
        "curl",
        "-L",
        "-sS",
        "-H",
        "Accept: application/vnd.github+json",
        "-H",
        "User-Agent: research-agent-skill",
        url,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        return []
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return []
    return payload.get("items", [])


def build_queries(metadata: dict) -> list[str]:
    values = []
    for key in ["paper_title", "method_name", "task_name", "benchmark_name", "dataset_name", "metric_name"]:
        value = metadata.get(key)
        if value:
            values.append(slugify(value))
    values.extend(slugify(item) for item in metadata.get("baseline_names", []) if item)
    deduped = []
    seen = set()
    for value in values:
        if value and value not in seen:
            deduped.append(value)
            seen.add(value)
    queries = deduped[:]
    if metadata.get("paper_title") and metadata.get("benchmark_name"):
        combo = f'{metadata["paper_title"]} {metadata["benchmark_name"]}'
        if combo not in queries:
            queries.append(combo)
    if metadata.get("method_name") and metadata.get("task_name"):
        combo = f'{metadata["method_name"]} {metadata["task_name"]}'
        lowered = combo.lower()
        if not any(lowered == q.lower() or lowered in q.lower() or q.lower() in lowered for q in queries):
            queries.append(combo)
    return queries


def score_candidate(candidate: dict, metadata: dict) -> int:
    score = 0
    text = " ".join(
        str(candidate.get(key, "")) for key in ["name", "full_name", "description", "readme_summary", "role", "notes", "topics"]
    ).lower()
    for key in ["paper_title", "method_name", "task_name", "benchmark_name", "dataset_name", "metric_name"]:
        value = str(metadata.get(key, "")).lower()
        if value and value in text:
            score += 3
    for baseline in metadata.get("baseline_names", []):
        if baseline.lower() in text:
            score += 2
    if candidate.get("official"):
        score += 5
    if metadata.get("paper_title") and metadata["paper_title"].lower() in text:
        score += 6
    if candidate.get("has_eval"):
        score += 3
    if candidate.get("recent_commit"):
        score += 2
    if candidate.get("license_ok"):
        score += 1
    if candidate.get("stargazers_count", 0) >= 100:
        score += 1
    if candidate.get("stargazers_count", 0) >= 1000:
        score += 1
    return score


def normalize_github_candidate(item: dict, query: str, metadata: dict) -> dict:
    description = item.get("description") or ""
    full_name = item.get("full_name") or ""
    title = (metadata.get("paper_title") or "").lower()
    description_lower = description.lower()
    full_name_lower = full_name.lower()
    official = bool(title and (title in description_lower or title in full_name_lower))
    return {
        "name": item.get("name", ""),
        "full_name": full_name,
        "html_url": item.get("html_url", ""),
        "clone_url": item.get("clone_url", ""),
        "default_branch": item.get("default_branch", ""),
        "description": description,
        "role": "github-search",
        "match_reason": f"Returned by GitHub search for `{query}`",
        "risk": "",
        "official": official,
        "has_eval": False,
        "recent_commit": True,
        "license_ok": bool(item.get("license")),
        "stargazers_count": item.get("stargazers_count", 0),
        "forks_count": item.get("forks_count", 0),
        "topics": item.get("topics", []),
        "search_query": query,
    }


def dedupe_candidates(candidates: list[dict]) -> list[dict]:
    merged = {}
    for candidate in candidates:
        key = candidate.get("clone_url") or candidate.get("html_url") or candidate.get("full_name") or candidate.get("name")
        if not key:
            continue
        previous = merged.get(key)
        if previous is None or candidate.get("_score", 0) > previous.get("_score", 0):
            merged[key] = candidate
    return list(merged.values())


def write_markdown(queries: list[str], ranked: list[dict], output: Path) -> None:
    lines = ["# Repository Candidates", "", "## Search Queries", ""]
    for query in queries:
        lines.append(f"- `{query}`")
    lines.extend(["", "## Ranked Candidates", "", "| Repo | Score | Role | Match Reason | Risk |", "|---|---:|---|---|---|"])
    for item in ranked:
        lines.append(
            f'| {item.get("name", "")} | {item.get("_score", 0)} | {item.get("role", "")} | '
            f'{item.get("match_reason", "")} | {item.get("risk", "")} |'
        )
    lines.append("")
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("metadata_json", help="Paper metadata JSON input")
    parser.add_argument("--candidates-json", help="Optional candidate repositories JSON")
    parser.add_argument("--github-search", action="store_true", help="Search GitHub automatically using generated queries")
    parser.add_argument("--per-query", type=int, default=5, help="Max GitHub repos per query")
    parser.add_argument("--md-out", default="REPO_CANDIDATES.md", help="Markdown output")
    parser.add_argument("--json-out", default="repo_candidates.ranked.json", help="Ranked JSON output")
    args = parser.parse_args()

    metadata = load_metadata(Path(args.metadata_json))
    queries = build_queries(metadata)
    candidates = []
    if args.candidates_json:
        candidates = json.loads(Path(args.candidates_json).read_text(encoding="utf-8"))
    if args.github_search:
        for query in queries:
            for item in github_search_repositories(query, args.per_query):
                candidates.append(normalize_github_candidate(item, query, metadata))
    for candidate in candidates:
        candidate["_score"] = score_candidate(candidate, metadata)
    candidates = dedupe_candidates(candidates)
    candidates.sort(key=lambda item: item.get("_score", 0), reverse=True)

    Path(args.json_out).write_text(json.dumps({"queries": queries, "candidates": candidates}, indent=2), encoding="utf-8")
    write_markdown(queries, candidates, Path(args.md_out))


if __name__ == "__main__":
    main()
