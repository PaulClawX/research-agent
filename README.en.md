> Language / 语言: **[中文](./README.md)** | **English**

# Research Agent

A compact repository of research skills.

It keeps only three core areas:

- `paper/`: paper polishing and evidence-grounded paper auditing
- `teaser/`: academic teaser-figure prompts
- `README.md` / `README.en.md`: bilingual entry points

## Fast Entry

| Task | Entry |
| --- | --- |
| Polish a paper draft | `paper/polish-paper/` |
| Rewrite in Chinese or bilingual form | `paper/polish-paper-bilingual/` |
| Audit paper evidence | `paper/experiment-grounded-paper-review/` |
| Generate teaser prompts | `teaser/gpt-image-teaser/` |
| Build a full teaser chain | `teaser/paperbanana-teaser/` |

## Layout

```text
.
├── README.md
├── README.en.md
├── paper/
└── teaser/
```

## How to Use

Open the target `SKILL.md` first, then its `references/`.  
For automated paper auditing, use the scripts under `paper/experiment-grounded-paper-review/scripts/`.
