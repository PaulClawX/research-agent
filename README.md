> Language / 语言: **中文** | **[English](./README.en.md)**

# Research Agent

一个精简的研究技能仓库。

只保留三类核心能力：

- `paper/`：论文润色与论文证据审计
- `teaser/`：学术 teaser 图 prompt
- `README.md` / `README.en.md`：双语入口

## 最快入口

| 任务 | 入口 |
| --- | --- |
| 论文润色 | `paper/polish-paper/` |
| 中文或双语改写 | `paper/polish-paper-bilingual/` |
| 论文证据审计 | `paper/experiment-grounded-paper-review/` |
| teaser 图 prompt | `teaser/gpt-image-teaser/` |
| 完整 teaser chain | `teaser/paperbanana-teaser/` |

## 目录

```text
.
├── README.md
├── README.en.md
├── paper/
└── teaser/
```

## 使用方式

先打开对应 `SKILL.md`，再看它的 `references/`。  
需要自动化审计时，直接用 `paper/experiment-grounded-paper-review/scripts/`。
