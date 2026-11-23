# Sources and reuse

The [root MIT license](LICENSE) covers this project's original work. Redistributed files retain their upstream notices and licenses.

The [Palmer penguin measurements](examples/penguins/data/PROVENANCE.md) are distributed under [CC0](examples/penguins/data/LICENSE.md). The [climate note](examples/climate-sources/research/paper.md) summarizes two bulletins from the World Meteorological Organization and Copernicus. Short English excerpts are kept in the study's [inputs directory](examples/climate-sources/inputs/). The [source record](examples/climate-sources/research/sources.json) links each excerpt to the original publication and passage. The project's MIT license does not relicense these sources.

The local reading task in the [paired pilot](evaluations/paired-pilot/method.md) includes excerpts from the CPython and NumPy documentation. Their [license notices](evaluations/paired-pilot/source-notices/) accompany the task. The original prompts, submissions and run records in `evaluations/` are preserved as evaluation evidence.

The [astronomy spot check](evaluations/discoverybench-771/README.md) uses a pinned public task from Allen Institute for AI's DiscoveryBench. The case report credits the organizers, links the original dataset and identifies its [Open Data Commons Attribution License](https://github.com/allenai/discoverybench/blob/c31fcf011e070f021a5f5b906896d0821f6880e8/discoverybench/license.md). The raw table and answer key are not bundled.

| Source at the revision used | How this project uses it |
|---|---|
| [AutoSciRub `2c6c5839`](https://github.com/zjunlp/AutoSciRub/tree/2c6c58392ee6399e08f2526e35176f0e2c716e16/plugins/autoscirub/skills) (MIT) | The criterion-level verification and targeted revision protocols are reproduced unchanged in `skills/ai4sci-experiment/references/autoscirub/`, alongside their license. |
| [AI4S Research `1dc2cbd8`](https://github.com/ai4s-research/open-science/tree/1dc2cbd8eb6b58887a1e6c41f80c797051f07700/runtime/skills/core/stats-integrity) (MIT) | `vendor/ai4s-desktop/` contains the upstream statistical risk scanner, its regression tests and its [license](vendor/ai4s-desktop/LICENSE). |
| [ARIS `4ba94ae2`](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/tree/4ba94ae2a1c1fbbb14858750dd8764cabf6c28bd) (MIT) | The [Codex image integration](integrations/codex-image/guide.md) adapts the upstream MCP server and tests. ARIS also informed the instructions for idea discovery, novelty checks, drafting and independent review. |
| [Synthetic Sciences `dbb60cba`](https://github.com/synthetic-sciences/openscience/tree/dbb60cba76afa518941a70ec4c25febba3114f4b/backend/cli/skills/core) | The `sources` and `peer-review` instructions, credited upstream to K-Dense, informed how reviewers assess the scope of a claim and distinguish blocking issues from observations. |
| [OpenResearch `b7427582`](https://github.com/alphaXiv/OpenResearch/tree/b74275826e1a5e2fb2c65cc6497d5683a1f07818/agent-skills/orx-experiment-tree) | Informed the policy of comparing experimental variants against a common baseline and retaining valid negative results. |
| [AIPOCH `9d42705b`](https://github.com/aipoch/open-science/tree/9d42705b02783d4ac96a55f183d3c99998e1ee13/packages/reproducibility) | Key-aligned output comparison and acceptance criteria informed the local comparator. |
