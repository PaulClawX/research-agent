# Research Agent

This repository is a curated library of reusable research-assistant skills.

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

- `polish-paper`: English academic editing and rebuttal polishing
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
