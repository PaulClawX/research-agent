> Language / 语言: **[中文](./README.md)** | **English**

# Research Agent

Minimal entry points:

| Task | Entry |
| --- | --- |
| Paper polishing | `paper/polish-paper/` |
| Chinese or bilingual rewrite | `paper/polish-paper-bilingual/` |
| Paper audit | `paper/experiment-grounded-paper-review/` |
| Teaser prompts | `teaser/gpt-image-teaser/` |
| Teaser chains | `teaser/paperbanana-teaser/` |

Only two top-level content dirs remain:

```text
.
├── README.md
├── README.en.md
├── paper/
└── teaser/
```

Open the target `SKILL.md` first, then `references/`. For automated paper auditing, use `paper/experiment-grounded-paper-review/scripts/`.
