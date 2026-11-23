# Sources and reuse

The [root MIT license](LICENSE) covers this project's original work. Redistributed files retain their upstream notices and licenses.

| Source at the revision used | How this project uses it |
|---|---|
| [AutoSciRub `2c6c5839`](https://github.com/zjunlp/AutoSciRub/tree/2c6c58392ee6399e08f2526e35176f0e2c716e16/plugins/autoscirub/skills) (MIT) | The criterion-level verification and targeted revision protocols are reproduced unchanged in `skills/ai4sci-experiment/references/autoscirub/`, alongside their license. |
| [AI4S Research `1dc2cbd8`](https://github.com/ai4s-research/open-science/tree/1dc2cbd8eb6b58887a1e6c41f80c797051f07700/runtime/skills/core/stats-integrity) (MIT) | `vendor/ai4s-desktop/` contains the upstream statistical risk scanner, its regression tests and its [license](vendor/ai4s-desktop/LICENSE). |
| [ARIS `4ba94ae2`](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/tree/4ba94ae2a1c1fbbb14858750dd8764cabf6c28bd) (MIT) | The [Codex image integration](integrations/codex-image/guide.md) adapts the upstream MCP server and tests. ARIS also informed the instructions for idea discovery, novelty checks, drafting and independent review. |
| [Synthetic Sciences `dbb60cba`](https://github.com/synthetic-sciences/openscience/tree/dbb60cba76afa518941a70ec4c25febba3114f4b/backend/cli/skills/core) | The `sources` and `peer-review` instructions, credited upstream to K-Dense, informed how reviewers assess the scope of a claim and distinguish blocking issues from observations. |
| [OpenResearch `b7427582`](https://github.com/alphaXiv/OpenResearch/tree/b74275826e1a5e2fb2c65cc6497d5683a1f07818/agent-skills/orx-experiment-tree) | Informed the policy of comparing experimental variants against a common baseline and retaining valid negative results. |
| [AIPOCH `9d42705b`](https://github.com/aipoch/open-science/tree/9d42705b02783d4ac96a55f183d3c99998e1ee13/packages/reproducibility) | Key-aligned output comparison and acceptance criteria informed the local comparator. |
