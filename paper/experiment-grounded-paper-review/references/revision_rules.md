# Revision Rules

## Allowed Revisions

- fix incorrect numbers
- narrow benchmark scope
- narrow dataset scope
- narrow metric wording
- downgrade unsupported confidence words
- add explicit limitations
- convert strong mechanism claims into hypotheses
- expose reproduction failures honestly

## Forbidden Revisions

- invent new experimental results
- round numbers upward to fit the narrative
- silently remove negative results
- describe subset evidence as full-benchmark evidence
- write `significant` without statistical support
- write `state-of-the-art` without strong baseline coverage
- imply reproducibility when the code was not actually validated

## Rewrite Patterns

### Scope Narrowing

- `On GUIBench, our method achieves state-of-the-art performance.`
- `On the evaluated GUIBench subset, our method outperforms the baselines tested in this paper.`

### Statistical Downgrade

- `significantly outperforms`
- `achieves higher average performance in our runs`

### Mechanistic Downgrade

- `The verification module is the main reason for the improvement.`
- `The verification module may contribute to the improvement; isolating its effect requires further ablation.`

### Generalization Downgrade

- `generalizes to real-world websites`
- `shows promising performance on the evaluated website categories`
