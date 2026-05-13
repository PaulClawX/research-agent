#!/usr/bin/env python3
"""Run a first-pass audit on a paper directory with automatic file discovery."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
TITLE_RE = re.compile(r"\\title\{([^}]*)\}")
SECTION_RE = re.compile(r"\\section\{([^}]*)\}")
CITE_RE = re.compile(r"\\cite[tpa]?\*?(?:\[[^\]]*\])?\{([^}]*)\}")


def run_python(script_name: str, args: list[str]) -> None:
    cmd = [sys.executable, str(SCRIPT_DIR / script_name), *args]
    subprocess.run(cmd, check=True)


def extract_metadata(main_tex: Path, manifest: dict) -> dict:
    text = main_tex.read_text(encoding="utf-8", errors="ignore")
    title_match = TITLE_RE.search(text)
    sections = SECTION_RE.findall(text)
    citations = []
    for match in CITE_RE.findall(text):
        citations.extend(part.strip() for part in match.split(",") if part.strip())
    unique_citations = []
    seen = set()
    for item in citations:
        if item not in seen:
            seen.add(item)
            unique_citations.append(item)

    method_name = ""
    if title_match:
        title = title_match.group(1).strip()
        method_name = title.split(":")[0].strip() if ":" in title else title
    else:
        title = ""

    task_name = ""
    title_lower = title.lower()
    if " for " in title_lower:
        task_name = title[title_lower.index(" for ") + 5 :].strip()
    elif sections:
        first_section = sections[0].strip()
        if first_section.lower() not in {"introduction", "background", "overview", "related work"}:
            task_name = first_section

    return {
        "paper_title": title,
        "method_name": method_name,
        "task_name": task_name,
        "benchmark_name": "",
        "dataset_name": "",
        "metric_name": "",
        "baseline_names": [],
        "main_tex": str(main_tex),
        "bib_files": manifest.get("bib_files", []),
        "section_names": sections,
        "citation_keys": unique_citations,
    }


def write_revision_plan(claims: list[dict], manifest: dict, output: Path) -> None:
    strong_terms = []
    for claim in claims:
        lower = claim["text"].lower()
        if any(term in lower for term in ["significant", "state-of-the-art", "robust", "generalize", "generalizes"]):
            strong_terms.append(claim)

    lines = ["# Revision Plan", ""]
    lines.append(f'- Main manuscript: `{manifest.get("main_tex") or ""}`')
    lines.append(f'- Title: {manifest.get("title") or ""}')
    lines.extend(["", "## Immediate Actions", ""])
    if strong_terms:
        lines.append("- Audit high-confidence claims first; several sentences use language that usually requires stronger evidence.")
    else:
        lines.append("- No obvious high-confidence trigger phrases were detected by the first-pass heuristic.")
    if manifest.get("supplement_files"):
        lines.append("- Review supplemental files because extra experiments may already exist there.")
    if manifest.get("table_files"):
        lines.append("- Cross-check table files against abstract and conclusion numbers.")
    lines.extend(["", "## Next Steps", ""])
    lines.append("- Fill benchmark, dataset, metric, and baseline fields in `paper_metadata.json` before repo search.")
    lines.append("- Prepare `REPRO_CONFIG.example.json` into a task-specific reproduction config once candidate repos are selected.")
    lines.append("- After experiments are linked, run claim-result alignment to downgrade unsupported wording.")
    lines.append("")
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paper_root", help="Path to a paper project directory")
    parser.add_argument("--out-dir", default="audit-output", help="Output directory for the audit artifacts")
    parser.add_argument("--skip-github-search", action="store_true", help="Disable automatic GitHub repository search")
    parser.add_argument("--per-query", type=int, default=5, help="Repositories to request per search query")
    parser.add_argument("--top-k-repos", type=int, default=3, help="Number of repositories to clone and probe")
    parser.add_argument("--skip-clone-and-probe", action="store_true", help="Stop after repo ranking")
    parser.add_argument("--probe-timeout-seconds", type=int, default=300, help="Timeout per automatic setup or probe command")
    args = parser.parse_args()

    paper_root = Path(args.paper_root).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest_json = out_dir / "paper_manifest.json"
    manifest_md = out_dir / "paper_manifest.md"
    run_python("discover_paper_files.py", [str(paper_root), "--json-out", str(manifest_json), "--md-out", str(manifest_md)])

    manifest = json.loads(manifest_json.read_text(encoding="utf-8"))
    main_tex = manifest.get("main_tex")
    if not main_tex:
        raise SystemExit("No main TeX file was discovered.")

    claims_json = out_dir / "CLAIMS.json"
    claims_md = out_dir / "CLAIM_LEDGER.md"
    run_python("extract_tex_claims.py", [main_tex, "--json-out", str(claims_json), "--md-out", str(claims_md)])

    metadata = extract_metadata(Path(main_tex), manifest)
    metadata_json = out_dir / "paper_metadata.json"
    metadata_json.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")

    repo_md = out_dir / "REPO_CANDIDATES.md"
    repo_json = out_dir / "repo_candidates.ranked.json"
    repo_args = [str(metadata_json), "--md-out", str(repo_md), "--json-out", str(repo_json), "--per-query", str(args.per_query)]
    if not args.skip_github_search:
        repo_args.append("--github-search")
    run_python("find_related_repos.py", repo_args)

    claims = json.loads(claims_json.read_text(encoding="utf-8"))
    write_revision_plan(claims, manifest, out_dir / "REVISION_PLAN.md")

    if args.skip_clone_and_probe:
        return

    repos_dir = out_dir / "repos"
    repos_dir.mkdir(parents=True, exist_ok=True)
    ranked = json.loads(repo_json.read_text(encoding="utf-8"))
    for candidate in ranked.get("candidates", [])[: args.top_k_repos]:
        clone_url = candidate.get("clone_url")
        if not clone_url:
            continue
        repo_dir = repos_dir / clone_url.rstrip("/").split("/")[-1].replace(".git", "")
        if repo_dir.exists():
            continue
        subprocess.run(["git", "clone", clone_url, str(repo_dir)], check=False)

    auto_repro_json = out_dir / "AUTO_REPRO_CONFIG.json"
    auto_repro_md = out_dir / "AUTO_REPRO_PLAN.md"
    run_python(
        "auto_prepare_reproduction.py",
        [
            str(repo_json),
            "--repos-dir",
            str(repos_dir),
            "--top-k",
            str(args.top_k_repos),
            "--json-out",
            str(auto_repro_json),
            "--md-out",
            str(auto_repro_md),
        ],
    )

    experiments_md = out_dir / "EXPERIMENT_LEDGER.md"
    experiments_json = out_dir / "EXPERIMENTS.json"
    logs_dir = out_dir / "logs"
    run_python(
        "run_reproduction.py",
        [
            str(auto_repro_json),
            "--workspace",
            str(repos_dir),
            "--json-out",
            str(experiments_json),
            "--md-out",
            str(experiments_md),
            "--log-dir",
            str(logs_dir),
            "--timeout-seconds",
            str(args.probe_timeout_seconds),
        ],
    )

    evidence_json = out_dir / "NUMERIC_EVIDENCE.json"
    evidence_md = out_dir / "NUMERIC_EVIDENCE.md"
    run_python(
        "extract_numeric_evidence.py",
        [str(experiments_json), "--json-out", str(evidence_json), "--md-out", str(evidence_md)],
    )

    table_evidence_json = out_dir / "TABLE_EVIDENCE.json"
    table_evidence_md = out_dir / "TABLE_EVIDENCE.md"
    run_python(
        "extract_structured_tables.py",
        [
            str(paper_root),
            str(experiments_json),
            "--json-out",
            str(table_evidence_json),
            "--md-out",
            str(table_evidence_md),
        ],
    )

    enriched_claims_json = out_dir / "CLAIMS_ENRICHED.json"
    enriched_claims_md = out_dir / "CLAIM_LEDGER_ENRICHED.md"
    enriched_experiments_json = out_dir / "EXPERIMENTS_ENRICHED.json"
    run_python(
        "backfill_claim_evidence.py",
        [
            str(claims_json),
            str(evidence_json),
            str(table_evidence_json),
            str(experiments_json),
            "--claims-json-out",
            str(enriched_claims_json),
            "--claims-md-out",
            str(enriched_claims_md),
            "--experiments-json-out",
            str(enriched_experiments_json),
        ],
    )

    inconsistency_json = out_dir / "INCONSISTENCY_REPORT.json"
    inconsistency_md = out_dir / "INCONSISTENCY_REPORT.md"
    run_python(
        "check_claim_result_alignment.py",
        [str(enriched_claims_json), str(enriched_experiments_json), "--json-out", str(inconsistency_json), "--md-out", str(inconsistency_md)],
    )


if __name__ == "__main__":
    main()
