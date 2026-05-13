# Example: Teaser Prompt

这是一个最小可用示例，展示如何使用 teaser figure skills。

## 场景

你要把论文方法概括成一张 teaser 图，并送给图像模型生成第一版草图。

## 输入示例

```text
Paper topic: multi-agent planning
Core problem: existing agents lose global context over long horizons
Prior-work limitation: weak coordination and unstable tool usage
Proposed method: a memory-grounded planner with iterative tool feedback
Main components: planner, memory, tool executor, verifier
Main takeaway: more stable and coherent long-horizon reasoning
```

## 两种走法

### 走法 A：先快后细

适合快速起稿：

1. 用 `gpt-image-teaser`
2. 先写 figure brief
3. 直接生成主 prompt
4. 如果首图有标签或布局问题，再用 revision prompt 修

### 走法 B：完整链路

适合你想要更强控制力：

1. 用 `paperbanana-teaser`
2. 先做 planner
3. 再做 stylist
4. 再给 visualizer
5. 最后用 critic 返回修订意见

## 预期效果

- prompt 更结构化
- 图像模型更容易理解方法关系
- 后续 revision 更可控
