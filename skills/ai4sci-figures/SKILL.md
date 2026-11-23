---
name: ai4sci-figures
description: Create data-backed plots from experiment outputs, or a separate conceptual method illustration through a Codex image backend when requested. Use for 结果图、误差条、图形摘要、方法示意图.
---

# Match the tool to the figure

For measured curves, scatterplots, error bars and heatmaps, read the final result file, preserve units, check axes and sample sizes, and render from code. Keep the generation command next to the result. Define uncertainty bounds and sample size in the caption. Do not ask an image model to draw a data-bearing panel or reconstruct an experimental observation.

For a requested conceptual figure, prepare labels and relationships from the verified methods, and use the available native image tool or the optional Codex integration. For a specific Codex/GPT request, use the connected `generate_start` tool if it targets this study. Otherwise run the checkout's CLI with the study root as the current directory: `python3 "$KIT/integrations/codex-image/cli.py" doctor`, then `generate 'PROMPT'` on that same CLI and `status JOB_ID --wait 20`. Both interfaces can read the same job when scoped to the same study; submit through just one. Details: `integrations/codex-image/guide.md` in the checkout.

Preserve the returned attempt ID and check actual output before reporting completion; do not automatically resubmit an unknown outcome or switch providers. Inspect labels, direction of arrows and visual meaning before inclusion. Label it as an illustration. If image generation is unavailable, disclose this; a programmatic schematic can be used only as an identified alternative.
