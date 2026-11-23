"""Run the credentialed OpenCode acceptance task in a new, retained study directory."""
import argparse
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('directory', type=Path, help='new directory; failed and successful attempts are retained')
    cli.add_argument('--model', help='OpenCode provider/model (default: configured model)')
    cli.add_argument('--timeout', type=int, default=1200, help='wall time in seconds')
    args = cli.parse_args()
    if args.timeout <= 0:
        cli.error('--timeout must be positive')
    if not shutil.which('opencode'):
        cli.error('OpenCode must be on PATH')
    attempt = args.directory.resolve()
    if attempt.exists():
        cli.error(f'already exists: {attempt}; inspect the original attempt before starting another')
    attempt.mkdir(mode=0o700, parents=True)
    project = attempt / 'study'
    project.mkdir()
    inputs = project / 'inputs'
    inputs.mkdir()
    for note in ['trapezoid-note.md', 'left-note.md']:
        shutil.copy2(ROOT / 'examples/quadrature/research' / note, inputs / note)
    cli_path = shlex.quote(str(ROOT / 'ai4sci.py'))
    study_path = shlex.quote(str(project))
    prompt = (
        f'工具目录是 {ROOT}。先读 {ROOT / "skills/ai4sci/SKILL.md"}，再按阶段读 '
        f'{ROOT / "skills"}/ai4sci-<阶段>/SKILL.md（idea、experiment、figures、paper、review）。\n'
        f'研究目录是 {project}；仅从此目录 inputs/ 的两份笔记选一个可用均匀网格实验检验的误差问题。'
        '只在研究目录内写研究文件，不复制工具、技能或配置，不初始化 Git。'
        f'先用 python3 {cli_path} freeze {study_path} 冻结计划，再执行实验，交付带实际结果和误差图的中文短论文。\n'
        f'按 {ROOT / "checks/contract.md"} 独立复核已登记的结论，用 python3 {cli_path} audit {study_path} 核查，'
        '修复实际核查失败再停。工具只读，禁止读取 examples/ 中的原始解答、其他课题、既有运行及会话记录。'
        '只用研究目录的输入、Python 标准库和 CPU，不联网、不 commit 或 push。'
    )
    (attempt / 'request.txt').write_text(prompt + '\n', encoding='utf-8')
    cmd = ['opencode', 'run', '--archived', '--format', 'json']
    if args.model:
        cmd.extend(['--model', args.model])
    print(f'Running OpenCode once. Local logs and outputs: {attempt}', flush=True)
    with (attempt / 'events.jsonl').open('xb') as log, (attempt / 'stderr.txt').open('xb') as err:
        try:
            # OpenCode 2.3.2 uses PWD to select the project even when cwd is set.
            process = subprocess.run([*cmd, prompt], cwd=ROOT, env={**os.environ, 'PWD': str(ROOT)},
                                     stdout=log, stderr=err, timeout=args.timeout)
        except subprocess.TimeoutExpired:
            sys.exit(f'Time limit reached. Check session/server state and {attempt}; no second request submitted.')
    if process.returncode:
        sys.exit(f'OpenCode exited {process.returncode}; inspect {attempt}')
    # Audit from the checkout rather than relying on the model's reported outcome.
    audit = subprocess.run([sys.executable, ROOT / 'ai4sci.py', 'audit', project], capture_output=True, text=True)
    (attempt / 'audit.json').write_text(audit.stdout, encoding='utf-8')
    if audit.returncode:
        sys.exit(f'Independent audit failed ({audit.returncode}): {audit.stdout}{audit.stderr}')
    result = json.loads(audit.stdout)
    if result['scientific_run'] != 'completed' or not (project / 'research/paper.md').is_file():
        sys.exit('The requested computational study was not completed.')
    print(f'Completed: {project / "research/paper.md"}\nEvidence check: {attempt / "audit.json"}')


if __name__ == '__main__':
    main()
