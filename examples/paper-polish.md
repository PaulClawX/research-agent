# Example: Paper Polish

这是一个最小可用示例，展示如何使用 `polish-paper`。

## 场景

你有一段论文 abstract，内容没问题，但表达不够紧，语气也不够像顶会论文。

## 输入示例

```text
Section type: abstract
Target venue or style: NeurIPS
Editing strength: full

Source text:
We study a new framework for agent planning. Existing methods often fail to coordinate long horizon decisions efficiently. In this paper, we propose a memory-guided planning strategy that improves stability and makes the planning process more reliable in complex environments...
```

## 推荐做法

1. 打开 `skills/paper-writing/polish-paper/SKILL.md`
2. 去 `references/prompt-templates.md`
3. 复制 `General Academic Polish` 或 `Abstract Tightening`
4. 把你的原文和约束填进去

## 预期效果

- 句子更紧凑
- 逻辑更清晰
- 术语不漂移
- 风格更接近正式投稿文本
