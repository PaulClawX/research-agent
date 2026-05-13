---
name: polish-paper
description: Use this skill when the user wants to polish an academic paper, workshop paper, rebuttal, abstract, introduction, method section, experiment section, conclusion, or related research writing for clarity, structure, grammar, concision, tone, and conference-style presentation while preserving the original technical claims.
---

# Polish Paper

## Overview

This skill improves research writing without changing the science. It is for tightening prose, sharpening contributions, reducing ambiguity, improving logical flow, and aligning wording with common ML, NLP, CV, systems, and broader academic-paper conventions.

Use it when the user wants an editing workflow, a rewrite prompt, or a section-by-section polish pass for a draft paper or rebuttal.

## When To Use

Use this skill when the user asks for any of the following:

- Polish a paper draft
- Rewrite an abstract, introduction, related work, method, experiments, or conclusion
- Improve academic English while keeping the technical meaning
- Make writing more concise, more formal, or more conference-ready
- Reduce repetition, weak claims, vague wording, or awkward transitions
- Turn bullet notes into paper-style prose
- Prepare a rebuttal or response letter in a professional academic tone

Do not use this skill when the main need is:

- Substantive scientific critique of correctness or novelty
- Reference formatting only
- Latex build debugging, figure creation, or citation-tool configuration
- Journal-specific copyediting that depends on a proprietary style guide the user has not provided

## Inputs

Gather as many of these as available:

- Target text to revise
- Paper title or topic
- Venue or target style such as NeurIPS, ICML, ICLR, ACL, EMNLP, CVPR, ICCV, or a journal
- Section type such as abstract, intro, method, experiments, rebuttal, or conclusion
- Constraints on length, tone, or aggressiveness
- Terms, notation, or claims that must remain unchanged
- Whether the user wants light edit, full rewrite, or tracked suggestions

If the draft is incomplete, preserve the known content and improve wording and structure only. Do not invent experiments, results, citations, or claims.

## Default Workflow

Follow this sequence unless the user asks for only one part:

1. `Intent Lock`
   Identify the section goal, target audience, and any claims or terminology that must not drift.
2. `Issue Scan`
   Detect verbosity, repetition, weak transitions, ambiguous pronouns, unsupported emphasis, inconsistent terminology, and tone mismatches.
3. `Rewrite`
   Produce a cleaner version that is tighter, more readable, and more conference-appropriate while preserving the technical meaning.
4. `Verification Pass`
   Check that notation, claims, numbers, model names, dataset names, and limitations remain faithful to the source.
5. `Optional Notes`
   If useful, briefly list high-impact edits or unresolved issues that still require author judgment.

## Working Rules

- Preserve scientific fidelity. Do not add experiments, numbers, baselines, references, or conclusions not present in the source.
- Keep terminology and notation consistent with the original draft unless the user asks to normalize them.
- Prefer concrete wording over hype.
- Remove redundancy, filler, and throat-clearing.
- Strengthen logical transitions between sentences and paragraphs.
- Keep claims calibrated. Replace overstated language with precise academic phrasing when the evidence is limited.
- If the user asks for a full rewrite, retain the argument structure unless it is clearly harming readability.
- When polishing rebuttals, be firm, specific, and professional rather than defensive or emotional.

## Output Modes

- `light-polish`: minimally invasive wording cleanup
- `full-rewrite`: stronger structural and sentence-level rewrite while preserving meaning
- `with-rationale`: revised text plus a short list of major edit rationales
- `review-notes`: issue list first, then a suggested rewrite
- `rebuttal-mode`: concise, professional author-response style

## Reference File

When you need reusable prompt patterns, read:

- [references/prompt-templates.md](./references/prompt-templates.md)

Use that file for paste-ready prompts covering abstract polishing, section rewrites, rebuttal editing, and issue-first review passes.
