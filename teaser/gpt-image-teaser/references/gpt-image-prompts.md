# GPT Image Academic Teaser Prompts

Use this reference when the task requires GPT Image-facing prompt text for academic teaser figures or method diagrams.

## Input Checklist

Fill what is available:

- Paper topic
- Core problem
- Prior-work limitation
- Proposed method or system
- Main technical components
- Main result or takeaway
- Methodology section
- Figure caption
- Desired venue style
- Optional reference image for style only

If some items are missing, keep the prompt conservative and avoid inventing unsupported scientific content.

## Figure Brief Template

Use this to compress a paper into the minimum structured context needed before writing the final GPT Image prompt.

```text
Create a structured figure brief for an academic teaser figure.

Inputs:
- Paper topic: [TOPIC]
- Core problem: [PROBLEM]
- Limitation of prior work: [LIMITATION]
- Proposed method: [METHOD]
- Main components: [COMPONENTS]
- Main takeaway: [TAKEAWAY]
- Methodology section: [OPTIONAL LONGER METHOD TEXT]
- Figure caption: [OPTIONAL CAPTION]
- Venue style: [NEURIPS / ICML / ICLR / CVPR / ACL / EMNLP / OTHER]

Return:
1. Narrative goal in one sentence
2. Recommended panel structure
3. Exact labels that must appear
4. Arrows and causal relationships
5. Groupings or colored regions
6. Input/output elements
7. Recommended aspect ratio
8. Visual style notes suitable for an academic figure image model prompt

Rules:
- Be specific and faithful to the provided paper content.
- Do not invent missing modules or results.
- Do not include a figure title or caption inside the image.
```

## Main GPT Image Prompt

Use this as the primary prompt for generating the teaser figure.

```text
Create a publication-quality academic teaser figure for a machine learning paper.

The figure should read clearly at a glance and look appropriate for a top-tier AI conference such as NeurIPS, ICML, ICLR, CVPR, ACL, or EMNLP.

Figure content:
- Problem: [INSERT PROBLEM]
- Limitation of prior work: [INSERT LIMITATION]
- Proposed method: [INSERT METHOD]
- Main components: [INSERT COMPONENTS]
- Final takeaway: [INSERT TAKEAWAY]

Detailed structure:
[INSERT STRUCTURED FIGURE BRIEF OR DESCRIPTION]

Visual requirements:
- Clean academic infographic or schematic style
- White or very light background
- Clear visual hierarchy
- Readable short labels only
- Rounded rectangles for modules
- Consistent arrows and spacing
- Natural muted academic colors such as soft blue, sage green, teal, warm peach, or pale lavender
- Small icons only when they help explain the science
- Vector-like appearance rather than painterly illustration

Text requirements:
- All labels must be spelled correctly and remain readable
- Use only the exact labels described in the structure
- Do not include the paper title, figure caption, figure number, watermark, UI chrome, or unrelated text

Scientific fidelity requirements:
- Do not add components not described
- Do not hallucinate claims or results
- Preserve all causal and data-flow relationships
- If anything is ambiguous, simplify instead of inventing

Layout guidance:
- Prefer a left-to-right narrative unless the content strongly suggests a different layout
- Use panel grouping if needed, such as problem, method, and outcome
- Keep the proposed method visually central

Final quality bar:
- The figure should look like a polished academic teaser, not a generic marketing infographic
- Avoid photorealism, 3D rendering, glossy effects, heavy shadows, decorative clutter, or rainbow color maps
```

## Caption-Safe Variant

Use this when the model tends to leak titles, captions, or extra text.

```text
Create an academic teaser figure only. Do not draw any figure title, paper title, caption, figure number, watermark, user interface text, or unrelated words anywhere in the image.

Use only the short labels explicitly listed below:
[INSERT LABEL LIST]

Figure structure:
[INSERT STRUCTURE]

Style:
- clean academic vector-like diagram
- white background
- readable labels
- consistent arrows
- restrained muted colors
```

## Revision Prompt

Use this after seeing a flawed first image. Keep it focused on corrections.

```text
Revise the previously generated academic figure.

Keep the overall concept and academic visual style, but correct the following issues:
- [ISSUE 1]
- [ISSUE 2]
- [ISSUE 3]

Important constraints:
- Do not add new scientific modules or claims
- Do not include any paper title, figure caption, or figure number inside the image
- Preserve readable short labels
- Preserve the intended problem to method to outcome narrative
- Keep the background light and the layout uncluttered

Use this target structure:
[INSERT CORRECTED STRUCTURE OR REVISED DESCRIPTION]
```

## Two-Pass Workflow

Use this when the user wants a reliable GPT Image iteration loop.

1. Build a figure brief from the paper summary, method, and caption.
2. Generate the first image with the main GPT Image prompt.
3. Inspect for four common failures:
   - title or caption accidentally rendered
   - label spelling or readability problems
   - wrong arrows or missing modules
   - cluttered layout or weak panel hierarchy
4. Issue a revision prompt that only corrects those specific failures.

## Fast Fill-In Template

Use this when speed matters more than modularity.

```text
Create a polished academic teaser figure for a research paper.

Paper topic: [TOPIC]
Core problem: [PROBLEM]
Prior-work limitation: [LIMITATION]
Proposed method: [METHOD]
Main components: [COMPONENTS]
Main takeaway: [TAKEAWAY]

Show a clear left-to-right narrative with three parts:
1. Problem or prior work limitation
2. Proposed method
3. Improved outcome or capability

Use a clean academic vector-like style with a white background, muted colors, short readable labels, rounded modules, and consistent arrows.

Do not include the paper title, figure caption, figure number, watermark, or any unrelated text.

Do not invent scientific content beyond what is described above.
```
