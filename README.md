# Research Agent

This repository is a curated library of reusable research-assistant skills.

## Paper Review + Polish: One-Line Use

### For Agent (Recommended)

```text
Use $polish-paper on <paper-path-or-text> in review-and-polish mode: run the review gate first, then the SciWrite clarity pass, then return safe revised text and the remaining issues.
```

### For Human

```bash
codex "Use \$polish-paper on <paper-path-or-text> in review-and-polish mode; target venue: <venue>; output language: en or zh."
```

This is the simplest path for paper cleanup: one request asks the agent to check correctness risk, reviewer-facing quality, references when available, and writing clarity before polishing.

It is organized around two core workflows:

- paper writing and academic rewriting
- teaser figure and method-diagram prompting

The goal is to keep the repository easy to scan at the top level while allowing each skill to remain self-contained.

## Repository Structure

```text
.
├── README.md
└── skills/
    ├── README.md
    ├── paper-writing/
    │   ├── README.md
    │   ├── polish-paper/
    │   └── polish-paper-bilingual/
    └── teaser-figures/
        ├── README.md
        ├── gpt-image-teaser/
        └── paperbanana-teaser/
```

## What Lives In A Skill

Each skill package follows the same internal pattern:

- `SKILL.md`: purpose, workflow, inputs, output modes, and usage rules
- `agents/openai.yaml`: agent-facing metadata and starter prompt
- `references/`: reusable prompt templates or prompt reference material

## Skill Groups

### `skills/paper-writing/`

This group is for improving academic text.

- `polish-paper`: English academic editing, author-side review gate, SciWrite clarity audit, and rebuttal polishing
- `polish-paper-bilingual`: Chinese-first and bilingual academic rewriting

### `skills/teaser-figures/`

This group is for academic figure prompting workflows.

- `gpt-image-teaser`: lightweight GPT Image prompt and revision workflow
- `paperbanana-teaser`: multi-stage planner/stylist/visualizer/critic workflow

## How To Navigate

1. Start in [skills/README.md](/Users/posit/workspace/paper/research-agent/skills/README.md).
2. Pick the workflow family that matches the task.
3. Open the group README for a quick comparison.
4. Open the target skill's `SKILL.md` for the exact operating instructions.
5. Reuse prompt text from that skill's `references/` directory when needed.

## Design Principles

- Keep the repository top level clean.
- Group skills by workflow, not by file type.
- Keep each skill self-contained so it can be copied or reused independently.
- Use README files as navigation layers instead of forcing users to infer structure from directory names alone.
