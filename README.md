# AI4Sci Workflow

中文 · [English](README.en.md) · [查看研究成品](#研究成品)

AI4Sci Workflow 是一套用于 [OpenCode](https://opencode.ai/) 的科研工作流。你可以从一个感兴趣的方向出发，查文献、选课题、设计实验，也可以从手头的数据、论文初稿或审稿意见接着做。计算实验的方案、代码、运行命令和原始结果留在课题目录里，方便别人复算，也方便返修时查清一个结论是怎么来的。

## 可以从哪一步开始

- **查文献、选课题**：书单会给出原文出处，说明每篇论文回答了什么。选题可以从论文之间的分歧、与预期不符的观测，或手头需要做的决定出发。工作流先查原始研究是否已经回答了问题，再看可用数据能否区分几种解释。你可以拿到推荐问题和一个成本较低的验证方案，再决定要不要做实验。
- **做实验或复现**：先约定基线、比较条件、指标和预算。比较几种改法时，从同一基线分别运行，保留每次结果，包括不支持预期的结果。若两种解释都说得通，就挑一个能让它们给出不同预测的对照。已经看过的测试数据可以用于敏感性分析，独立验证要另用未参与选题或调参的数据。
- **写稿、投稿准备和返修**：可以从现有结果起草论文，也可以给出期刊要求，让 OpenCode 按模板准备 Word 稿，或交付 LaTeX 源文件和编译出的 PDF。在别处写的论文也可以交给工作流返修，提供上次提交的版本、审稿意见和手头的研究记录即可。已有结果能回答的意见，指出具体位置。需要新增对照的，在运行前单独记下这次比较的方案，做完后保存结果。据此修改受影响的摘要、图表和结论，在回复信里逐条说明。

配合 OpenCode 的多 Agent 插件 [omo-slim](https://github.com/alvinunreal/oh-my-opencode-slim)，一个 Agent 可以查最接近的论文和反例，另一个同时检查数据和计算成本。主 Agent 统筹分工。复核时，未参与实验和写稿的 Agent 从原始材料重算关键指标，并检查结论是否超出了研究对象和实验条件。

---
## 开始使用

仓库自带六个科研技能，克隆一次，各个课题都可以用，不用逐个初始化或复制技能。在 OpenCode 里配置好模型后，在终端运行：
```sh
git clone https://github.com/KomeijiReimu/ai4sci-workflow.git
cd ai4sci-workflow
pwd
```

在工作流仓库中做研究时，从仓库根目录运行 `opencode`，然后说：

> 用 ai4sci 查一下短期负荷预测里，遇到连续缺测时通常怎么处理。找最接近的对照研究和可用数据，推荐一个值得先做的小实验，先别运行。

新课题需要保存文件时，OpenCode 会在 `studies/` 下创建课题目录。要继续已有课题，告诉它课题目录（如 `studies/my-study/`）和接下来想做什么。课题文件默认不随仓库提交。

在自己的课题目录中做研究时，从该目录运行 `opencode`，把提示中的路径换成刚才 `pwd` 显示的仓库路径：

> 读取 `/path/to/ai4sci-workflow`，用这个工作流处理当前目录的审稿意见和上次提交的 Word 稿。先看审稿人要求的对照能否用现有结果回答，再给我修订稿和逐条回复。

---
## 文献检索与文档工具

查论文、追查引文时，建议使用 [paper-search MCP](https://github.com/openags/paper-search-mcp)。先用 `opencode mcp list` 查看已有连接。尚未配置时，安装 [uv](https://docs.astral.sh/uv/) 以取得 `uvx`，再为 OpenCode 2 添加全局连接：
```sh
opencode mcp add paper-search --global -- uvx paper-search-mcp
opencode mcp list
```

连接后，可以在 OpenCode 中核对一条具体引文：

> 用 paper-search 在 Crossref 查 DOI `10.3390/math12010019`，核对这篇欧洲日前负荷预测论文的题名、作者和期刊。

精读论文时建议使用 [`paper-reader`](https://github.com/KomeijiReimu/my-skills)。处理投稿文件时，[文档技能](https://github.com/anthropics/skills)各有用途：`docx` 修改 Word 模板，`xlsx` 核对 Excel 补充表，`pdf` 检查排版页面，`pptx` 制作报告幻灯片。用 [Bun](https://bun.sh) 为 OpenCode 全局安装，只选尚未安装且会用到的技能：
```sh
bun x skills add KomeijiReimu/my-skills -g -a opencode --skill paper-reader
bun x skills add anthropics/skills -g -a opencode --skill docx xlsx pdf pptx
```

---
## 研究成品

- [德国电力需求：日前预测在哪些时段输给了上周同期？](examples/power-forecast/) 在 2019 年可以配对的 8756 个小时里，日前预测比直接使用上周同期负荷的平均绝对误差低 540 MW。但在实际需求最高的 876 个小时里，日前预测的误差反而高了 159 MW。改用两种预测的均值选取高需求时段，日前预测在这组时段的误差仍高出 161 MW。
- [2024 年全球升温：两份评估的数值为何不同？](examples/climate-sources/research/paper.md) 世界气象组织综合了多套数据，哥白尼气候变化服务使用的是 ERA5 再分析资料。这篇短文对照两份公告，解释两项估计的差别，以及为什么不能只看一年就判断是否突破了长期温控目标。附[公告出处与摘录](examples/climate-sources/research/sources.json)。
- [一次关于预测基线的返修](examples/penguins-revision/research/response.md)：[原研究](examples/penguins/research/paper.md)用训练集平均体重作为对照。复核者指出，训练集中位数能使训练集绝对误差最小。补上这个对照后，鳍长模型在同一批记录上的平均绝对误差优势从约 385 克缩小到 372 克。[修订稿（Word）](examples/penguins-revision/paper/final.docx)将这一结果限定为在已知测试集上更换基线的敏感性分析。

[研究工作流选型与比较](docs/comparison.md) · [证据核查规则](checks/contract.md) · [投稿文件核查](checks/submission.md) · [绘制方法示意图](integrations/codex-image/guide.md) · [来源与许可](SOURCES.md)
