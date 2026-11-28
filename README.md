# AI4Sci Workflow

中文 · [English](README.en.md) · [开始使用](#开始使用) · [查看研究成品](#研究成品)

AI4Sci Workflow 是一套用于 [OpenCode](https://opencode.ai/) 的科研工作流。你可以从一个感兴趣的方向出发，查文献、选课题、设计实验，也可以从手头的数据、论文初稿或审稿意见接着做。计算实验的方案、代码、运行命令和原始结果留在课题目录里，方便别人复算，也方便返修时查清一个结论是怎么来的。

## 内置科研技能

| 你要做什么 | 技能 | 能得到什么 |
| --- | --- | --- |
| 开始或接着做一个课题 | [`ai4sci`](skills/ai4sci/SKILL.md) | 按研究目标选用下面的技能。只要书单就停在书单，接手已有课题则先读方案和结果，再决定下一步。 |
| 查文献、选课题 | [`ai4sci-idea`](skills/ai4sci-idea/SKILL.md) | 书单注明出处和每篇论文回答的问题。选题时，从文献分歧或意外观测出发，结合可用数据推荐一个能区分几种解释的小实验。 |
| 做实验或复现 | [`ai4sci-experiment`](skills/ai4sci-experiment/SKILL.md) | 先定指标、可比条件和预算，在同一基线上比较几种改法，保留运行命令、原始结果和未奏效的方案。用已看过的测试数据补做对照时，区分敏感性分析和独立验证。 |
| 绘制结果图 | [`ai4sci-figures`](skills/ai4sci-figures/SKILL.md) | 用代码从结果文件绘图，标出单位和误差条的含义，保留重绘命令。需要解释方法时，可以另做示意图。 |
| 写稿、准备投稿或返修 | [`ai4sci-paper`](skills/ai4sci-paper/SKILL.md) | 根据现有结果写稿，按期刊要求准备 Word 稿或 LaTeX 源文件和 PDF。返修可以从别处写的稿件、审稿意见和现有记录开始。需要新增对照时先单独定方案，再把结果写进修订稿和逐条回复。 |
| 核对结论 | [`ai4sci-review`](skills/ai4sci-review/SKILL.md) | 对照原文核引文，从原始数据复算关键指标。复核意见指明有问题的段落、对应证据，以及哪些结论需要缩小范围或补充验证。 |

---
## 协作与接续

配合 [omo-slim](https://github.com/alvinunreal/oh-my-opencode-slim) 使用[面向投稿的研究流程](skills/ai4sci/references/publication.md)时，主 Agent 从现有配置中分派角色：

- **选题时**，主 Agent 派两位 Explorer 或同类角色并行调查。一位看目标会议最近收了哪些相关论文，再查其他地方是否已经发表过同样的结果。另一位检查可用数据、对照和计算成本。主 Agent 请 Oracle 或其他擅长科研评审的角色挑出最有力的反例，判断推荐的题目还值不值得做。只要选题，到这里就给出建议和理由。
- **做实验时**，方法审查者先看基线、数据划分和评价指标，再由负责实验的 Agent 按方案运行和分析。第一项关键结果出来后，写稿前先请同一位审查者判断数据支持哪种解释。比较方法或主要结论有实质变化时，再请其复核。
- **交稿前**，写作者根据实测结果成稿。主 Agent 另开审稿会话，交给未参与方法审查、分析或写稿的科研评审专家。终审者从原始材料复算关键结果，核对最终稿里的结论。稿件有问题，改好后交回同一位终审者。只有一个 Agent 时，结果标为自查。

**只要[远程实验包](skills/ai4sci/references/remote-package.md)时**，交付的是代码和启动说明，不在本地或远程运行实验。写代码前，主 Agent 先请擅长研究方法的审查者找出设计中可能让比较失效的问题。如果实现与方案有实质偏差，再请原审查者判断是否需要调整。

交付前，主 Agent 按模型专长另开两个审查会话。两位审查者都未参与设计或编写实验包，各自检查同一份最终包：一位核对代码是否实现了约定的对照和指标，另一位检查依赖、数据路径和远程启动步骤。作者的检查记为自查，未收到独立审查意见的那一项仍待审。

启用 [Magic Context](https://docs.cortexkit.io/magic-context/getting-started/introduction/) 后，隔几天回到长会话，还能翻出当时讨论基线的那段对话。在同一 OpenCode 项目里另开会话，也可以查到项目记忆保存的决定，比如最后选了哪条基线、为什么选它。

跨会话做研究时，工作流还会把进展、证据位置和下一步写进课题目录的 `research/handoff.md`。同事接手时可以直接从这份文件读起，见[电力预测课题的交接记录](examples/power-forecast/research/handoff.md)。

---
## 开始使用

仓库自带六个科研技能，克隆一次，各个课题都可以用，不用逐个初始化或复制技能。在 OpenCode 里配置好模型后，在终端运行：
```sh
git clone https://github.com/KomeijiReimu/ai4sci-workflow.git
cd ai4sci-workflow
pwd
```

在仓库根目录运行 `opencode`，说清研究方向和你想拿到的成果。只想先读论文，可以说“用 ai4sci 给我一份日前负荷预测的入门书单”。准备投稿时，可以指定会议，也可以只给 CCF B 类这样的范围：

> 用 ai4sci 给我推荐一个适合投 ACM e-Energy 的日前负荷预测选题。

> 用 ai4sci 做一项日前负荷预测研究，选好题、做完实验，按 ACM e-Energy 的要求写成论文。

> 用 ai4sci 给我准备一份能在集群上跑的日前负荷预测实验包，先别运行。

新课题需要保存文件时，OpenCode 会在 `studies/` 下为它单独建一个目录。同一课题的文献、实验和稿件都放在原目录里。继续时，只要能确定你指的是哪个课题，直接说下一步想做什么就行。如果指向不清，OpenCode 会先问清楚再写文件。本仓库默认不提交 `studies/` 下的课题文件。

在自己的课题目录中做研究时，从该目录运行 `opencode`，把提示中的路径换成刚才 `pwd` 显示的仓库路径：

> 读取 `/path/to/ai4sci-workflow`，按审稿意见修改当前目录的 Word 投稿稿件，给我修订稿和逐条回复。

---
## 文献检索与文档工具

查论文、追查引文时，建议使用 paper-search MCP。先用 `opencode mcp list` 查看已有连接。如果尚未配置，用 [uv](https://docs.astral.sh/uv/) 安装[本项目使用的上游版本](https://github.com/openags/paper-search-mcp/tree/cab1b5cc276a0cd004a0044003926a6440088049)，再将它注册为 OpenCode 2 的全局工具：
```sh
uv tool install git+https://github.com/openags/paper-search-mcp.git@cab1b5cc276a0cd004a0044003926a6440088049
opencode mcp add paper-search --global -- "$(uv tool dir --bin)/paper-search-mcp"
opencode mcp list
```

列表中出现 `paper-search connected` 表示已连接，如果刚启动时列表为空，等几秒后在同一课题目录再运行一次 `opencode mcp list`。

在 OpenCode 中可以这样核对一条引文：

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
