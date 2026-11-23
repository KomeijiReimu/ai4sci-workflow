# AI4Sci Workflow

中文 · [English](README.en.md) · [查看研究成品](#研究成品)

AI4Sci Workflow 是一套用于 [OpenCode](https://opencode.ai/) 的科研工作流。你可以从一个感兴趣的方向出发，查文献、选课题、设计实验，也可以分析手头的观测数据，或把已有结果写成论文。做计算实验或复现时，方案、代码、运行命令和原始结果都留在课题目录里，方便接着做，也方便别人复算。

## 工作流特点

- **先定问题和比较条件**：选题时，对照已有研究和可用数据，判断新实验能回答什么。只要书单或选题，可以在这里结束。如果继续做实验，先定好数据、基线和评价标准。报告会区分哪些结果没能复现，哪些因为缺数据还没检验。
- **稿件里的结论有据可查**：交稿前，核查程序把稿件中标出的实测值与结果表逐项比对，引用的数字则与保存的原文摘录核对。审稿者再看研究对象和实验条件，判断稿件的结论有没有超出证据支持的范围。
- **多 Agent 协作**：配合 OpenCode 的多 Agent 插件 [omo-slim](https://github.com/alvinunreal/oh-my-opencode-slim)，一个 Agent 可以查相关论文和反例，另一个同时检查可用数据。主 Agent 安排分工，你不用逐个交代任务或转述结果。复核时，未参与实验和写稿的 Agent 可以按实验方案从原始材料重算关键指标，再用自己算出的数值核对稿件。

---
## 开始使用

仓库只需克隆一次，以后做其他课题也可以用它。在 OpenCode 里配置好模型后，在终端运行：
```sh
git clone https://github.com/KomeijiReimu/ai4sci-workflow.git
cd ai4sci-workflow
pwd
```

在工作流仓库中做研究时，从仓库根目录运行 `opencode`，然后说：

> 用 ai4sci 帮我查一下时间序列缺失值的处理方法，找几个值得做实验的问题。

新课题需要保存文件时，OpenCode 会在 `studies/` 下创建课题目录。要继续已有课题，告诉它课题目录（如 `studies/my-study/`）和接下来想做什么。课题文件默认不随仓库提交。

在自己的课题目录中做研究时，从该目录运行 `opencode`，把提示中的路径换成刚才 `pwd` 显示的仓库路径：

> 读取 `/path/to/ai4sci-workflow`，用这个工作流把当前目录里的实验结果写成一篇短论文。

稿件保存在 `<课题目录>/research/paper.md`。OpenCode 会在交稿前运行证据核查程序，这一步需要 Python 3.10 或更高版本。

---
## 研究成品

- [用鳍长预测企鹅体重](examples/penguins/research/paper.md)：用前两年的记录拟合模型，用 2009 年鳍长和体重齐全的 119 条记录检验两种预测方法。按训练集平均体重预测，平均绝对误差约为 710 克。用鳍长做线性预测，平均绝对误差约为 326 克。附[逐条预测记录](examples/penguins/research/predictions.csv)和[独立复核报告](examples/penguins/research/review.md)。
- [2024 年全球升温：两份评估的数值为何不同？](examples/climate-sources/research/paper.md) 世界气象组织综合了多套数据，哥白尼气候变化服务使用的是 ERA5 再分析资料。这篇短文对照两份公告，解释两项估计的差别，以及为什么不能只看一年就判断是否突破了长期温控目标。附[公告出处与摘录](examples/climate-sources/research/sources.json)。

[研究工作流选型与比较](docs/comparison.md) · [证据核查规则](checks/contract.md) · [从两份笔记到一篇短论文](examples/opencode-study/REQUEST.md) · [绘制方法示意图](integrations/codex-image/guide.md) · [来源与许可](SOURCES.md)
