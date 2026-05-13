# Quickstart

这个文档面向第一次使用这个仓库的用户。

目标只有一个：在 5 分钟内找到合适的 skill 或审计工具并开始使用。

## Step 1: 克隆仓库

```bash
git clone git@github.com:PaulClawX/research-agent.git
cd research-agent
```

## Step 2: 判断你的任务类型

### 你要处理的是文字

去看：

- [skills/paper-writing/README.md](/Users/posit/workspace/paper/research-agent/skills/paper-writing/README.md)

推荐 skill：

- `polish-paper`

### 你要处理的是 teaser 图 prompt

去看：

- [skills/teaser-figures/README.md](/Users/posit/workspace/paper/research-agent/skills/teaser-figures/README.md)

推荐 skill：

- `gpt-image-teaser`: 快速起稿
- `paperbanana-teaser`: 完整多阶段工作流

### 你要处理的是论文 claim / 实验 / 数值证据审计

去看：

- [paper/experiment-grounded-paper-review/SKILL.md](/Users/posit/workspace/paper/research-agent/paper/experiment-grounded-paper-review/SKILL.md)

推荐入口：

- `scripts/run_paper_audit.py`
- `scripts/extract_numeric_evidence.py`

## Step 3: 打开目标 Skill

每个 skill 都从 `SKILL.md` 开始。

你主要看四件事：

- 是否适合当前任务
- 需要准备什么输入
- 默认工作流是什么
- 输出格式有哪些

## Step 4: 直接复制模板

如果你已经确定要用哪个 skill，不要从空白 prompt 开始写。

直接去它的 `references/`：

- 论文润色模板：
  [skills/paper-writing/polish-paper/references/prompt-templates.md](/Users/posit/workspace/paper/research-agent/skills/paper-writing/polish-paper/references/prompt-templates.md)
- GPT Image teaser 模板：
  [skills/teaser-figures/gpt-image-teaser/references/gpt-image-prompts.md](/Users/posit/workspace/paper/research-agent/skills/teaser-figures/gpt-image-teaser/references/gpt-image-prompts.md)
- PaperBanana teaser 模板：
  [skills/teaser-figures/paperbanana-teaser/references/prompt-templates.md](/Users/posit/workspace/paper/research-agent/skills/teaser-figures/paperbanana-teaser/references/prompt-templates.md)

## 最常见的两种起手式

### 起手式 A：我要改论文

```text
1. 打开 polish-paper/SKILL.md
2. 看它的 input 要求
3. 从 references 复制一个最接近的模板
4. 把你的原文、section 类型、venue 风格填进去
```

### 起手式 B：我要做 teaser 图

```text
1. 选 gpt-image-teaser 或 paperbanana-teaser
2. 准备 method summary / caption / figure brief
3. 从 references 复制模板
4. 先出第一版，再根据 critic 或 revision prompt 调整
```

### 起手式 C：我要核对论文证据

```text
1. 打开 experiment-grounded-paper-review/SKILL.md
2. 先看 references 里的 schema 和规则
3. 运行 extract_numeric_evidence.py 或 run_paper_audit.py
4. 根据结果回查 claim、表格、实验段落
```
