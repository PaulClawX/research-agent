# Polish Paper Bilingual Prompt Templates

## 1. Chinese Academic Polish

Use this when the user wants better Chinese academic prose without translation.

```text
请润色下面的中文学术写作，使其在表达、逻辑、连贯性、正式程度和可读性上更符合论文写作风格。

要求：
- 保留原始技术含义与全部事实性陈述
- 不要新增实验、结果、引用、贡献或局限性
- 保持术语、符号、模型名、数据集名和指标名一致
- 优先使用准确、克制、自然的学术表达
- 删除重复、口语化、松散或模糊的表述

章节类型：{section_type}
目标风格：{venue_or_style}
润色强度：{light_or_full}
额外约束：{constraints}

原文：
{text}
```

## 2. Chinese To English Paper Rewrite

Use this when the source is Chinese and the output should read like a real English paper rather than a literal translation.

```text
Rewrite the following Chinese academic draft into fluent English paper prose.

Requirements:
- Preserve the original technical meaning and all factual claims.
- Do not invent results, citations, experiments, or limitations.
- Keep notation, method names, dataset names, and metric names unchanged when appropriate.
- Prefer natural, concise, conference-style English over literal translation.
- Resolve awkward direct-translation phrasing into idiomatic academic writing.

Section type: {section_type}
Target venue or style: {venue_or_style}
Editing strength: {light_or_full}
Additional constraints: {constraints}

Source Chinese text:
{text}
```

## 3. English To Chinese Academic Rewrite

Use this when the user wants a precise Chinese academic version of an English section.

```text
将下面的英文论文段落改写为准确、自然、正式的中文学术表达。

要求：
- 保留原始技术含义和事实性陈述
- 不要新增结果、引用、实验或结论
- 保持术语、符号、模型名、数据集名和指标名一致
- 避免生硬直译，优先采用自然的中文学术写法
- 如果标准写法通常保留英文术语，则保留原术语

章节类型：{section_type}
目标风格：{venue_or_style}
额外约束：{constraints}

英文原文：
{text}
```

## 4. Side-By-Side Bilingual Rewrite

Use this when the user wants both languages aligned.

```text
Produce a bilingual academic rewrite of the following text.

Tasks:
- first produce a polished Chinese academic version
- then produce a polished English academic version
- ensure both versions match in meaning, emphasis, and technical content

Constraints:
- do not invent scientific claims or evidence
- keep notation and named entities consistent
- prefer natural academic phrasing in each language rather than literal mirroring

Section type: {section_type}
Target venue or style: {venue_or_style}

Source text:
{text}
```

## 5. Bilingual Rebuttal Polish

Use this when the user is drafting a rebuttal in Chinese, English, or mixed language.

```text
Polish the following rebuttal or author response and provide bilingual output.

Requirements:
- keep the tone respectful, direct, calm, and professional
- preserve all substantive claims and commitments
- do not invent experiments, clarifications, or promises
- remove defensive, emotional, or repetitive wording
- provide aligned Chinese and English versions

Length preference: {length_preference}

Source text:
{text}
```

## 6. Minimal-Diff Bilingual Cleanup

Use this when the user wants the text kept close to the original wording.

```text
Lightly revise the following academic text with minimal semantic drift.

Goals:
- fix grammar and awkward wording
- improve readability
- preserve the original structure where possible
- keep all technical terms and claims intact

Output mode: {zh_polish_or_zh_to_en_or_en_to_zh}

Source text:
{text}
```
