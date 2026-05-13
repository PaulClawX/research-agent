# PaperBanana Teaser Prompt Templates

Use this reference when the task requires actual prompt text rather than just workflow guidance.

## Input Checklist

Fill as many fields as possible before drafting prompts:

- Paper topic
- Core problem
- Key limitation of prior work
- Proposed idea or system
- Main technical components
- Main result or takeaway
- Methodology section
- Figure caption
- Target venue style
- Optional reference images for style transfer only

If some fields are missing, do not invent unsupported modules. Keep the description faithful and simplify.

## Planner Prompt

Use this to convert a paper method and caption into a detailed figure description.

```text
I am working on a task: given the Methodology section of a paper and the caption of the desired figure, automatically generate a corresponding illustrative diagram.

Input:
- Methodology section
- Figure caption
- Optional reference examples

Output:
Generate a comprehensive and detailed textual description of the methodology diagram.

The description must cover:
1. Overall layout: flow direction, major sections or phases.
2. Components: every box, module, or visual element with exact labels.
3. Connections: arrows, data flows, and directions.
4. Groupings: colored regions, dashed borders, section boundaries.
5. Labels and annotations: text labels, mathematical notations, callouts.
6. Inputs and outputs: what enters and exits the system.
7. Styling: background, color palette, line weights, icon styles.

Requirements:
- Be as detailed as possible.
- Vague or unclear specifications make the generated figure worse.
- Do not include figure titles such as "Figure 1" inside the image.
- Choose an appropriate aspect ratio based on the content structure:
  - sequential pipelines: 16:9 or 21:9
  - vertical hierarchies: 2:3 or 9:16
  - balanced architectures: 1:1, 4:3, or 3:4

Return:
- Detailed figure description
- Recommended aspect ratio
```

## Stylist Prompt

Use this after the first description is drafted. It should refine visual presentation without changing the science.

```text
You are a Lead Visual Designer for top-tier AI conferences such as NeurIPS, ICML, ICLR, and CVPR.

Your task is to transform a rough academic diagram description into a polished, publication-ready visual specification.

Input:
- Detailed diagram description
- Source context from the paper
- Figure caption
- Aesthetic guidelines

Instructions:
1. Preserve the content exactly. Do not add, remove, or modify any scientific components, connections, or labels.
2. Improve visual clarity, hierarchy, and readability.
3. Use soft, muted academic colors described in natural language, such as soft sky blue, warm peach, light sage green, pale lavender.
4. Avoid hex color codes, pixel dimensions, point sizes, or CSS-like specifications, because image models may render them as unwanted text.
5. Respect domain conventions:
   - LLM / agent papers may use lightweight icons, chat bubbles, robot avatars, API blocks.
   - CV / robotics papers may use geometric modules, camera icons, frames, point clouds.
   - Theory papers should use minimalist graph nodes, equations, and clean schematic elements.
6. Use rounded rectangles, consistent arrows, clean sans-serif labels, and balanced spacing.
7. Remove unnecessary legends if the color semantics are already visually obvious.
8. Do not include the figure title or caption inside the image.

Output only the final polished detailed description.
```

## Visualizer Prompt

Use this as the final prompt sent to an image model.

```text
You are an expert scientific diagram illustrator.

Generate a high-quality scientific diagram based on the following detailed description.

Critical requirements:
- Do not include figure titles, captions, or figure numbers inside the image.
- All text labels must be clear and readable.
- Use the exact label names specified in the description.
- Do not generate garbled, misspelled, or irrelevant text.
- Use a clean academic style suitable for NeurIPS, ICML, ICLR, CVPR, ACL, or similar venues.
- Prefer white or very light background.
- Use consistent arrows, spacing, typography, and visual hierarchy.
- Avoid decorative clutter.

Detailed description:
[PASTE THE POLISHED FIGURE DESCRIPTION HERE]
```

## Critic Prompt

Use this after an image is generated.

```text
You are a Lead Visual Designer for top-tier AI conferences.

Your task is to critique the generated academic diagram against:
- Methodology section
- Figure caption
- Detailed figure description
- The generated image

Check the following:

1. Scientific fidelity:
- Does the diagram accurately reflect the method?
- Are any critical modules missing?
- Are there hallucinated components?
- Are all arrows and relationships correct?

2. Text quality:
- Are labels readable?
- Are there misspellings or garbled text?
- Are there unwanted hex codes, CSS values, or pixel dimensions rendered as text?
- Are mathematical notations correct?

3. Caption exclusion:
- The figure title, caption, or "Figure 1" should not appear inside the image.

4. Presentation:
- Is the layout readable?
- Is the visual hierarchy clear?
- Are there overlaps or clutter?
- Are arrows easy to follow?
- Are legends redundant?

Return JSON:
{
  "critic_suggestions": [
    "specific actionable suggestion 1",
    "specific actionable suggestion 2"
  ],
  "revised_description": "complete revised description incorporating the fixes, or null if no revision is needed"
}
```

## Paste-Ready Final Prompt

Use this when the user wants a single prompt that compresses the workflow into one model-facing instruction set.

```text
You are a senior academic figure designer for top-tier AI conferences such as NeurIPS, ICML, ICLR, CVPR, ACL, and EMNLP.

Task:
Create a publication-quality teaser figure for a machine learning research paper.

Paper information:
- Paper topic: [INSERT TOPIC]
- Core problem: [INSERT PROBLEM]
- Key limitation of prior work: [INSERT LIMITATION]
- Proposed idea: [INSERT METHOD / SYSTEM / PARADIGM]
- Main technical components: [INSERT COMPONENTS]
- Main result or takeaway: [INSERT TAKEAWAY]
- Target venue style: [NeurIPS / ICML / ICLR / CVPR / ACL / etc.]

Figure goal:
The teaser should communicate the paper's central idea at a glance. It should help a reviewer understand:
1. What problem exists.
2. Why existing approaches are insufficient.
3. What the proposed method changes.
4. What benefit or capability emerges.

Recommended layout:
Use a clear left-to-right narrative unless the content strongly suggests another structure.

Panel A - Problem / Prior Work:
- Show the current fragmented, limited, or failure-prone setting.
- Use muted gray or warm warning tones.
- Use dashed arrows, broken connections, or cluttered modules only if they help explain the limitation.
- Add concise labels for the main failure modes.

Panel B - Proposed Method:
- Show the core technical abstraction or system architecture.
- Place the proposed method as the visual center of the figure.
- Show key modules, representations, training signals, agents, memory, tools, or data flows.
- Use clean grouping, clear arrows, and a more structured layout.
- Use a calm academic color palette such as soft blue, teal, lavender, sage green, and warm peach.

Panel C - Outcome / Capability:
- Show the improved behavior, unified system, better prediction, stronger generalization, or new capability.
- Use solid arrows, check marks, aligned outputs, or compact evidence panels.
- Make the final takeaway visually obvious but not exaggerated.

Visual style:
- Clean vector-like academic illustration.
- White or very light background.
- High readability at paper-column scale.
- Consistent sans-serif typography.
- Use rounded rectangles for modules.
- Use cylinders for databases or memory.
- Use grids for tensors, feature maps, or datasets.
- Use small icons only when they carry semantic meaning.
- Maintain consistent spacing, line width, arrow style, and visual hierarchy.
- Prefer natural-language color descriptions instead of hex codes.

Text rules:
- Use short labels only.
- All text must be readable and correctly spelled.
- Use exact labels provided in the description.
- Do not include the paper title, figure caption, "Figure 1", watermark, UI chrome, or unrelated text inside the image.

Scientific fidelity:
- Do not hallucinate modules or claims.
- Do not add components not described.
- Preserve the causal and data-flow relationships.
- If uncertainty exists, simplify rather than invent.

Output requirements:
- Aspect ratio: 16:9 landscape by default.
- Style: polished academic teaser figure.
- Resolution: high-resolution.
- Avoid photorealism, 3D rendering, heavy shadows, decorative clutter, and rainbow or jet colormaps.

Before finalizing, internally check:
1. Are all major components from the description present?
2. Are arrows and relationships correct?
3. Is the left-to-right story clear?
4. Are labels readable?
5. Is there any unwanted title, caption, watermark, or hallucinated text?
6. Would this look acceptable in a NeurIPS, ICML, or ICLR paper?
```

## Optional Internal-Check Wrapper

Use this when the model supports richer internal self-correction before rendering.

```text
You are a senior academic figure design expert.

Please generate a high-resolution, publication-quality academic figure based on the detailed figure description below.

Before generating, internally verify:
1. Does the image faithfully include every module and connection listed in the Figure Description?
2. Are there any extra elements not mentioned in the description?
3. Does the image accidentally include a title, caption, figure number, watermark, or unrelated text?
4. Are all labels readable and correctly spelled?
5. Are arrows, groupings, and visual hierarchy consistent with the described logic?

If any issue is found, internally correct it before producing the final image.

[Optional reference image instruction]
The reference image in the same message is only for style transfer:
- Use its flat academic illustration style, visual density, arrow style, callout style, and color harmony.
- Do not copy its specific content, objects, modules, labels, or scientific meaning.

Figure Description:
[DETAILED STRUCTURED DESCRIPTION]

Visual Specification:
- Canvas: white background, wide academic layout, preferably 16:9 unless the content suggests otherwise.
- Style: modern flat academic infographic, clean vector-like diagram.
- Typography: clean sans-serif, readable labels, no tiny text.
- Geometry: rounded rectangles for processing modules, cylinders for databases, grids for tensors, small icons only when semantically useful.
- Arrows: orthogonal or smooth directional arrows, consistent stroke width, clear data flow.
- Color semantics: use a small consistent palette; assign one color family per concept.
- Avoid: title, caption, figure number, watermark, heavy shadows, 3D effects, photorealism, decorative clutter, rainbow or jet colormap.
```

## Recommended Operating Sequence

For most papers, use this four-step flow:

1. Run the Planner prompt on the methodology section, figure caption, and any reference figures.
2. Run the Stylist prompt on the resulting description.
3. Feed the polished description into the Visualizer prompt.
4. Run the Critic prompt on the generated image and revise if needed.

If the user wants speed over modularity, use the paste-ready final prompt instead.
