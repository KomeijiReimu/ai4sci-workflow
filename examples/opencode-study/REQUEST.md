# 从两份求积笔记到一篇中文短论文

本例保留了 OpenCode 2.3.2 从两份推导笔记出发完成的一项计算研究。一份笔记推导[梯形法的误差](inputs/trapezoid-note.md)，另一份推导[左端点法的误差](inputs/left-note.md)。

实验在六组网格上分别计算两种方法的估计值。独立复核者用整数平方和公式重算了全部十二个值，并逐条检查论文中的四项登记结论。存档保留了原始结果和图；运行记录中的本机解释器路径简写为 `python3`。

- [中文论文](research/paper.md) · [原始数据](research/results.csv) · [误差图](research/error.svg)
- [冻结方案](research/plan.json) · [证据表](research/claims.json) · [独立核查及复算命令](research/review.md)

核对这份存档：在工作流仓库根目录运行 `python3 ai4sci.py audit examples/opencode-study`。要重新计算，复制本示例目录，在副本中执行[论文图注](research/paper.md)里的两条命令。要让自己的模型从两份笔记重新选题、计算和写稿，见[运行说明](../../docs/comparison.md)。

<details>
<summary>存档：本次研究收到的任务原文</summary>

> 用 ai4sci 完成一个微型中文计算研究：仅从 inputs/ 两份笔记选一个可用均匀网格实验检验的误差问题。先冻结研究计划，执行实验，交付带实际结果和误差图的中文短论文；独立复核已登记的结论。按本地安装的 .ai4sci-kit/checks/contract.md 和 .ai4sci-kit/ai4sci.py audit . 交付，修复实际核查失败再停，不改工具。只用本目录资料、Python 标准库、CPU。不要联网、读其他课题、commit 或 push。

</details>
