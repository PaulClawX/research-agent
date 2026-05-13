# Review Rubric

## Iron Rule

The paper cannot be more confident than the experiments.

## Severity Levels

- `fatal`: core result unsupported or contradicted
- `major`: key abstract, intro, experiment, or conclusion claim exceeds verified evidence
- `moderate`: wording, scope, or numerical presentation needs narrowing
- `minor`: polish, formatting, or traceability improvement

## Required Checks

### Abstract

- Every empirical claim maps to a table, figure, or experiment id
- No unsupported `significant`, `robust`, `generalizes`, or `state-of-the-art`
- Numbers match verified evidence

### Introduction

- Contribution scope matches experimental scope
- Novelty claims are narrower than or equal to related-work support
- No general-purpose framing unless actually tested broadly

### Method

- Core modules and their purpose are identifiable
- Mechanistic claims are backed by ablations when stated strongly
- Reproduction details are discoverable

### Experiments

- Benchmarks, splits, metrics, and baselines are explicit
- Table values are internally consistent
- Best / second-best labels match the actual numbers
- Claims of robustness or efficiency have targeted tests

### Conclusion

- No broader deployment or generalization claims than the experiments support
- Limitations are not erased when evidence is incomplete

## Restricted Phrases

These require stronger evidence or must be downgraded:

- `significantly outperforms`
- `state-of-the-art`
- `robust across diverse settings`
- `generalizes to real-world deployment`
- `the main reason for improvement`
- `reproducible` when code was not actually validated

## Safer Substitutions

- `significantly outperforms` -> `achieves higher average performance in our runs`
- `state-of-the-art` -> `outperforms the evaluated baselines`
- `generalizes` -> `shows promising performance on the evaluated task categories`
- `robust` -> `improves performance under the tested perturbations`
- `is the main reason` -> `may contribute; isolating its effect requires ablation`
