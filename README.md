# Research Agent

This repository collects reusable research-assistant skills for two focused workflows:

- `paper/`: academic writing and paper-polishing skills
- `teaser/`: academic teaser figure and method-diagram prompting skills

Each skill package includes:

- `SKILL.md`: the skill definition and operating workflow
- `agents/openai.yaml`: agent configuration
- `references/`: reusable prompt templates or prompt references

## Repository Layout

```text
.
├── README.md
├── paper/
│   ├── polish-paper/
│   └── polish-paper-bilingual/
└── teaser/
    ├── gpt-image-teaser/
    └── paperbanana-teaser/
```

## Paper Skills

### `paper/polish-paper`

Use this skill for English academic writing improvement without changing the science.

Best for:

- polishing abstracts, introductions, methods, experiments, and conclusions
- rewriting rebuttals in a clearer and more conference-ready style
- tightening wording, structure, and logical flow while preserving technical claims

### `paper/polish-paper-bilingual`

Use this skill for Chinese-first academic writing and bilingual academic rewriting.

Best for:

- polishing Chinese research drafts
- translating Chinese drafts into natural paper-style English
- translating English academic text into precise Chinese
- preparing aligned bilingual revisions or rebuttals

## Teaser Skills

### `teaser/gpt-image-teaser`

Use this skill when the goal is a concise GPT Image-oriented workflow for academic figures.

Best for:

- turning a paper summary into a GPT Image prompt
- drafting method-overview or teaser prompts quickly
- issuing targeted follow-up prompts to repair clutter, labels, or layout

### `teaser/paperbanana-teaser`

Use this skill when the user wants a more structured multi-stage academic figure prompting workflow.

Best for:

- planner-stylist-visualizer-critic pipelines
- conference-style teaser figures and system diagrams
- critique-and-revise loops for generated academic visuals

## How To Use

1. Pick the skill that matches the task.
2. Read the corresponding `SKILL.md`.
3. Reuse the prompts in `references/` when you need a paste-ready template.
4. Use `agents/openai.yaml` when the skill is being wired into an agent workflow.

## Notes

- `paper/` focuses on writing quality, bilingual rewriting, and rebuttal polishing.
- `teaser/` focuses on prompt workflows for academic figures rather than direct design-tool implementation.
- The repository is organized as a skill library, not as an executable application.
