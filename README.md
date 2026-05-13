# research-agent

This repository is a curated library of reusable research-assistant skills for paper writing, bilingual rewriting, teaser-figure prompting, and experiment-grounded paper verification.

The goal is to keep the top level easy to scan while letting each skill remain self-contained.

## Repository Structure

```text
.
├── README.md
├── paper/
│   ├── polish-paper/
│   ├── polish-paper-bilingual/
│   └── experiment-grounded-paper-review/
└── teaser/
    ├── gpt-image-teaser/
    └── paperbanana-teaser/
```

## Paper Review + Polish: One-Line Use

### For Agent

```text
Use $polish-paper on <paper-path-or-text> in review-and-polish mode: run the review gate first, then the SciWrite clarity pass, then return safe revised text and the remaining issues.
```

### For Human

```bash
codex "Use \$polish-paper on <paper-path-or-text> in review-and-polish mode; target venue: <venue>; output language: en or zh."
```

## What Lives In A Skill

Each skill package follows the same pattern:

- `SKILL.md`: purpose, workflow, inputs, output modes, and usage rules
- `agents/openai.yaml`: agent-facing metadata and starter prompt
- `references/`: reusable prompt templates, rubrics, or reference material
- `scripts/`: deterministic helper tools when the workflow benefits from execution

## Skill Index

### Paper Skills

| Skill | Path | Purpose |
|---|---|---|
| `polish-paper` | `paper/polish-paper` | English-first academic paper polishing plus optional review gate and SciWrite-style clarity audit |
| `polish-paper-bilingual` | `paper/polish-paper-bilingual` | Chinese-first and bilingual academic rewriting for paper sections and rebuttals |
| `experiment-grounded-paper-review` | `paper/experiment-grounded-paper-review` | Verify paper claims against code, experiments, tables, logs, and reproducible probes; force the manuscript to obey the evidence |

### Teaser Skills

| Skill | Path | Purpose |
|---|---|---|
| `gpt-image-teaser` | `teaser/gpt-image-teaser` | Lightweight GPT Image prompt and revision workflow for academic teaser figures |
| `paperbanana-teaser` | `teaser/paperbanana-teaser` | Multi-stage planner/stylist/visualizer/critic workflow for academic teaser figures |

## Navigation

1. Pick the workflow family that matches the task: `paper/` or `teaser/`.
2. Open the target skill's `SKILL.md` for the exact operating instructions.
3. Reuse prompt text from that skill's `references/` directory when needed.
4. Use scripts from that skill's `scripts/` directory when the workflow includes deterministic execution.

## Suggested Usage

- Use `polish-paper` when the draft is already in English and mainly needs academic rewriting.
- Use `polish-paper-bilingual` when the draft is Chinese, mixed-language, or needs aligned Chinese and English outputs.
- Use `experiment-grounded-paper-review` when the goal is not just writing quality, but paper-code-experiment consistency and reproducible evidence.
- Use `gpt-image-teaser` or `paperbanana-teaser` when the output is an academic figure prompt rather than final publication prose.
