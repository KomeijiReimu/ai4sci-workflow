# 用 Codex 绘制方法示意图

此工具适合画实验步骤、系统组成和模块之间的关系。实验曲线、误差条和热图请用绘图代码从结果文件生成。

## 从命令行生成一张图

使用 Python 3.11 或更高版本、Pillow 和支持 `app-server --listen stdio://` 的 [Codex CLI](https://github.com/openai/codex)。在本机运行 `codex login`，登录有原生图像生成权限的账号。生图使用该账号的额度；只提交可以交由服务商处理的提示词和参考图。

在**课题目录**打开终端。将下面的 `/path/to/ai4sci-workflow` 换成工作流仓库的绝对路径。工具从仓库运行，任务记录和图片保存在当前课题。若当前 Python 环境缺少 Pillow，在虚拟环境中运行 `python3 -m pip install Pillow`。

```sh
bridge="/path/to/ai4sci-workflow/integrations/codex-image"
export CODEX_IMAGE2_PROJECT_DIR="$PWD"
python3 "$bridge/cli.py" doctor
```

`doctor` 检查本地依赖和登录状态。准备好提示词后，提交一次：

```sh
python3 "$bridge/cli.py" generate '绘制数据分析流程示意图，从左到右依次为采样、校准、估计。用箭头连接三个步骤，在校准步骤下方标出参考样本。'
```

保存返回的 `jobId`。将下面的 `JOB_ID` 换成这个值，在同一课题目录查询；若仍在排队或运行，重复**查询**即可。

```sh
python3 "$bridge/cli.py" status JOB_ID --wait 20
```

`status` 为 `completed` 时，打开 `outputPath` 指向的 PNG。工具已检查文件能够解码；请对照方法原文核对图中的文字、箭头方向和步骤关系，再将选用的图复制到稿件目录，在图注中注明“方法示意图”。

## 失败或中断后接手

- **`failed`**：查看 `error`。若 Codex 拒绝认证，用 `codex login` 重新登录；若提示缺少生图权限，先确认账号是否支持该功能。
- **`unknown`**：请求可能已送达 Codex。保留 `jobId` 和 `.local/codex-image/jobs/JOB_ID.json`，用记录中已有的 `threadId` 或 `turnId` 核对原请求的活动。结果查清前不要重新提交，也不要换接口再发一次。

图片保存在课题的 `.local/codex-image/images/`。任务记录可能包含提示词、参考文件路径或服务商回复；分享图片时不要一并公开任务目录。

## 在 OpenCode 中调用（可选）

若希望通过 MCP 调用生图工具，可在课题目录显式添加本地服务。这一步会修改该项目的 OpenCode 配置。沿用上面的 `bridge` 路径和装有 Pillow 的 Python：

```sh
opencode mcp add codex-image --env "CODEX_IMAGE2_PROJECT_DIR=$PWD" -- \
  "$(command -v python3)" "$bridge/server.py"
opencode mcp list
```

若 `mcp add` 成功后列表仍显示 `No MCP servers configured`，留在同一课题根目录，将服务注册到当前运行的 OpenCode 实例。若使用 `--server` 连接指定实例，下面两条 `opencode` 命令都要指定同一个服务地址。

```sh
payload=$(python3 -c '
import json, sys
from pathlib import Path
root = Path.cwd()
print(json.dumps({"config": {"type": "local", "command": [sys.executable, sys.argv[1]],
                             "environment": {"CODEX_IMAGE2_PROJECT_DIR": str(root)}}}))' "$bridge/server.py")
opencode api PUT /api/experimental/mcp/codex-image --data "$payload" && opencode mcp list
```

`codex-image` 显示 `connected` 后，用 `generate_start` 提交提示词，用 `generate_status` 和返回的 `jobId` 查询。命令行和 MCP 共用课题目录中的任务记录：已经从命令行提交的图，在 OpenCode 里直接查原任务。没有连接时仍可在命令行查询。

本工具改编自 ARIS 的 [codex-image2 服务](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/4ba94ae2a1c1fbbb14858750dd8764cabf6c28bd/mcp-servers/codex-image2/server.py)及其[测试](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/4ba94ae2a1c1fbbb14858750dd8764cabf6c28bd/tests/test_codex_image2_server.py)。再分发时请保留[原 MIT 许可证及版权声明](LICENSE)。
