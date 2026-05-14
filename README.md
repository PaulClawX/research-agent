> Language / 语言: **中文** | **[English](./README.en.md)**

# Research Agent

最小入口：

| 任务 | 入口 |
| --- | --- |
| 论文润色 | `paper/polish-paper/` |
| 中英改写 | `paper/polish-paper-bilingual/` |
| 论文审稿 | `paper/experiment-grounded-paper-review/` |
| teaser prompt | `teaser/gpt-image-teaser/` |
| teaser chain | `teaser/paperbanana-teaser/` |

目录只保留两层：

```text
.
├── README.md
├── README.en.md
├── paper/
└── teaser/
```

先看目标 `SKILL.md`，再看 `references/`。审计类任务直接用 `paper/experiment-grounded-paper-review/scripts/`。
