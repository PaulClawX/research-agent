# Polish Paper Prompt Templates

## 1. General Academic Polish

Use this when the user wants a direct rewrite of a section.

```text
Polish the following academic writing for clarity, concision, logical flow, grammar, and conference-style tone.

Requirements:
- Preserve the original technical meaning and all factual claims.
- Do not invent results, citations, datasets, ablations, or limitations.
- Keep notation, terminology, and named methods consistent with the source.
- Prefer precise, compact, professional language over hype.
- If a sentence is ambiguous, rewrite it conservatively rather than adding new content.

Section type: {section_type}
Target venue or style: {venue_or_style}
Editing strength: {light_or_full}
Additional constraints: {constraints}

Source text:
{text}
```

## 2. Issue-First Then Rewrite

Use this when the user wants diagnosis before revision.

```text
Review the following paper section as an academic writing editor.

First, list the highest-impact writing issues only:
- unclear claims
- redundancy
- weak transitions
- tone mismatch
- confusing structure
- grammar only if it affects readability

Then provide a revised version that fixes those issues while preserving the technical content.

Constraints:
- Do not add new scientific claims or evidence.
- Keep all terminology and notation faithful to the source.
- Make the revision read like a polished conference submission.

Section type: {section_type}
Target venue or style: {venue_or_style}

Source text:
{text}
```

## 3. Abstract Tightening

Use this when the abstract is too long, too vague, or too soft.

```text
Rewrite this abstract to be sharper and more compact.

Goals:
- make the problem setup immediately clear
- state the method at the right abstraction level
- emphasize the main contribution without hype
- improve sentence flow
- remove redundancy and vague filler

Constraints:
- preserve all technical claims
- do not invent metrics or results
- keep it suitable for a top-tier research-paper abstract
- target length: {target_length}

Source abstract:
{text}
```

## 4. Introduction Flow Repair

Use this when the introduction lacks a clean narrative arc.

```text
Rewrite this introduction passage so the narrative flow is clearer.

Focus on:
- problem motivation
- limitation of prior approaches
- why the proposed approach is needed
- smoother transitions between paragraphs
- concise and precise academic tone

Constraints:
- keep the original scientific content
- do not introduce unsupported novelty claims
- preserve named methods, datasets, and terminology

Source text:
{text}
```

## 5. Rebuttal Polishing

Use this when the user needs an author response or rebuttal cleaned up.

```text
Polish the following rebuttal response for professionalism, clarity, and precision.

Requirements:
- keep the tone respectful, calm, and confident
- answer the reviewer directly
- remove defensive or emotional phrasing
- tighten wording and reduce repetition
- preserve all substantive claims and commitments
- do not invent experiments, promises, or clarifications not present in the source

Length preference: {length_preference}

Source rebuttal:
{text}
```

## 6. Minimal-Diff Polish

Use this when the user wants the text to stay close to the original wording.

```text
Lightly polish the following text with minimal changes.

Goals:
- fix grammar and awkward phrasing
- improve readability
- keep the original sentence structure where possible
- preserve all terminology and technical meaning

Do not substantially rewrite unless necessary for clarity.

Source text:
{text}
```

## 7. Review-And-Polish

Use this when the user wants a simple one-pass author-side review plus safe rewrite.

```text
Review and polish the following manuscript text using a two-stage workflow.

Stage 1: Review gate
- Flag correctness risks, unsupported claims, inconsistent terminology, mismatched numbers, reference issues, and reviewer-facing weaknesses.
- Classify issues as blocking, major, minor, or copyedit.
- Do not rewrite unsupported content into stronger language.

Stage 2: SciWrite clarity pass
- Remove clutter and filler.
- Prefer active, precise verbs when appropriate.
- Fix buried predicates, run-ons, and weak paragraph flow.
- Keep technical terms consistent.
- Check internal consistency of numbers, tables, figures, and citations when visible.

Then provide:
1. Review Gate: concise issue list.
2. Revised Text: safe polished version.
3. Residual Author Decisions: anything needing author judgment, evidence, or source verification.

Target venue or style: {venue_or_style}
Output language for notes: {language}
Editing strength: {light_or_full}
Additional constraints: {constraints}

Source text:
{text}
```

## 8. SciWrite Targeted Audit

Use this when the user asks for a focused writing-quality pass rather than full review.

```text
Audit the following scientific writing using only the requested SciWrite pass.

Requested pass: {clutter|voice_verbs|sentence_architecture|terminology|numbers_citations|all}

Requirements:
- Preserve scientific meaning and all factual claims.
- Show the original issue, suggested revision, and a short rationale.
- Use severity tags: critical, major, minor.
- If the text is already clear, say so instead of forcing edits.

Source text:
{text}
```
