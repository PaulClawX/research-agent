# Skills Index

All reusable assets in this repository live under `skills/`.

Choose a group based on the kind of task you want to solve:

- [paper-writing](./paper-writing/README.md): revise, polish, or translate academic text
- [teaser-figures](./teaser-figures/README.md): turn paper content into academic teaser-figure prompts

## Selection Guide

Use `paper-writing` when the main artifact is text:

- abstracts
- introductions
- methods
- experiments
- conclusions
- rebuttals

Use `teaser-figures` when the main artifact is a figure prompt or revision workflow:

- teaser figures
- method overviews
- academic diagrams
- iterative image-model prompt chains

## Shared Package Pattern

Every skill directory is expected to contain:

- `SKILL.md`
- `agents/openai.yaml`
- `references/`

That convention makes it easier to add more skill families later without changing the repository design.
