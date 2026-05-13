# Claim Schema

Each claim record should contain:

```json
{
  "claim_id": "C-001",
  "section": "Abstract",
  "source_file": "main.tex",
  "location": "Abstract sentence 2",
  "text": "Our method significantly improves long-horizon GUI task completion.",
  "claim_type": "empirical",
  "scope": "long-horizon GUI tasks on the evaluated benchmark split",
  "required_evidence": [
    "main benchmark result",
    "baseline comparison",
    "variance or significance evidence"
  ],
  "current_evidence": [],
  "status": "pending",
  "supports": [],
  "contradictions": [],
  "required_revision": ""
}
```

## Status Values

- `pending`
- `supported`
- `partially_supported`
- `unsupported`
- `contradicted`
- `needs_manual_review`

## Claim Types

- `empirical`
- `comparative`
- `robustness`
- `generalization`
- `efficiency`
- `mechanistic`
- `novelty`
- `qualitative`
- `speculative`

## Evidence Mapping

Typical mappings:

- `empirical` -> benchmark result, metric, split
- `comparative` -> same-protocol baseline comparison
- `robustness` -> perturbation or domain-shift test
- `generalization` -> held-out domains or transfer setting
- `efficiency` -> cost, latency, token, or runtime measurement
- `mechanistic` -> ablation or intervention analysis
- `novelty` -> related-work comparison and citation support
