# Review-And-Polish Reference

This reference adapts two external workflows into `polish-paper`:

- OpenJudge `agentscope-ai/openjudge`, `skills/paper-review/SKILL.md`, Apache-2.0, reviewed at commit `f56134aaf29f110ab745d138e5184e87045b59ac`: multi-stage paper review with safety/format checks, correctness review, reviewer scoring, criticality assessment, and BibTeX verification.
- `labarba/sciwrite`, CC BY 4.0, reviewed at commit `8a57fa73d541bdcf7d8501db61c018cb454e9afa`: scientific writing-quality review based on clutter removal, active verbs, sentence architecture, terminology consistency, and numerical/citation consistency.

The merged behavior must remain a local research-writing workflow, not a verbatim copy of either upstream skill.

## Owner Defaults

Use these defaults unless the user gives a stronger instruction:

- Treat the user as the paper author or author-side editor.
- Prefer CS/AI/ML conference expectations when the venue is unspecified.
- Keep the tone direct, reviewer-aware, and non-hype.
- Preserve technical claims, notation, model names, dataset names, metric names, and numbers.
- If output language is unspecified, answer in the user's language; keep rewritten English manuscript text in English.
- Never invent experiments, baselines, citations, ablations, limitations, or results.

## Review Gate

Run this before heavy polishing when the user asks for `review-and-polish`, full paper cleanup, reviewer simulation, submission preparation, or reference checking.

1. `Input And Format Check`
   Identify whether the input is pasted text, `.tex`, `.pdf`, `.bib`, or a compressed TeX package. Note missing files explicitly.
2. `Correctness Risk Scan`
   Flag objective risks: inconsistent definitions, impossible equations, mismatched claims and numbers, unsupported comparisons, unclear assumptions, and contradictions between abstract, method, experiments, tables, and conclusion.
3. `Reviewer Quality Scan`
   Assess clarity, novelty framing, significance, experimental adequacy, limitations, related-work positioning, and reproducibility cues. Use venue-specific expectations if known.
4. `Criticality Ranking`
   Rank findings by whether they can change acceptance risk: blocking scientific issue, major reviewer concern, writing issue, or minor copyedit.
5. `Reference Check`
   If a `.bib` file or references are available, flag incomplete entries, suspicious title/author mismatches, missing venue/year data, duplicate references, and claims that rely on secondary sources when a primary source is needed.
6. `Polish Permission Boundary`
   Only rewrite text whose scientific meaning can be preserved. If the review gate finds unsupported content, weaken or mark it instead of polishing it into a stronger claim.

## SciWrite Clarity Pass

Apply this after the review gate or as the main workflow for `sciwrite-pass`.

1. `Clutter`
   Delete filler openings, throat-clearing, redundant modifiers, and wordy connectors. Prefer direct, compact phrasing.
2. `Voice And Verbs`
   Replace weak nominalizations with active verbs when doing so does not violate field convention. Do not mechanically remove every passive construction.
3. `Sentence Architecture`
   Fix buried predicates, run-ons, overloaded clauses, monotonous sentence rhythm, and paragraphs without a clear progression.
4. `Terminology`
   Keep technical terms stable. Do not vary defined terms merely to avoid repetition.
5. `Numbers And Citations`
   Check internal consistency of sample sizes, percentages, metrics, significant figures, table mentions, figure mentions, and citation support.

## Output Contract

For `review-and-polish`, use this compact output unless the user requests a longer report:

```text
## Review Gate
- Blocking:
- Major:
- Minor:

## Revised Text
[safe polished version]

## Residual Author Decisions
- [items requiring author judgment, new experiments, or source verification]
```

For a full manuscript or file-based task, create or update task-local artifacts only when useful:

- `REVIEW_GATE.md`
- `SCIWRITE_PASS.md`
- `POLISHED_DRAFT.md`
- `REVISION_NOTES.md`

## External Pipeline Option

If the user explicitly asks to run OpenJudge and the environment has `py-openjudge` plus model credentials, run the upstream pipeline instead of simulating it manually. Use the full pipeline result as evidence, then apply the local `polish-paper` rewrite rules. If the pipeline fails, diagnose the root cause and report it; do not pretend a manual read is equivalent to the full OpenJudge pipeline.
