# Experiment Schema

Each experiment record should contain:

```json
{
  "experiment_id": "E-001",
  "repo_name": "example-repo",
  "repo_path": "/abs/path/example-repo",
  "commit": "a13f9c2",
  "dataset": "GUIBench-v2 subset-500",
  "split": "subset-500",
  "metric": "task_success_rate",
  "result_value": 43.2,
  "baseline_value": 39.7,
  "absolute_delta": 3.5,
  "relative_delta_percent": 8.82,
  "status": "verified_subset_result",
  "command": "python eval.py --benchmark guibench --split subset-500 --model ours",
  "stdout_log": "logs/e001.stdout.txt",
  "stderr_log": "logs/e001.stderr.txt",
  "supports": ["C-001"],
  "notes": "Supports a subset-level claim but not a full-benchmark claim."
}
```

## Status Values

- `setup_failed`
- `smoke_test_only`
- `ran_subset`
- `verified_subset_result`
- `verified_main_table`
- `verified_multi_seed`
- `manual_entry`

## Reproduction Levels

- `L0`: README only
- `L1`: install completed
- `L2`: toy or smoke test
- `L3`: subset benchmark
- `L4`: main-table reproduction
- `L5`: multi-seed, full benchmark, or ablation-quality evidence
