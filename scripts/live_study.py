"""Run the credentialed OpenCode acceptance task in a new, retained study directory."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PROMPT = ('用 ai4sci 完成一个微型中文计算研究：仅从 inputs/ 两份笔记选一个可用均匀网格实验检验的误差问题。'
          '先冻结研究计划，执行实验，交付带实际结果和误差图的中文短论文；独立复核已登记的结论。'
          '按本地安装的 .ai4sci-kit/checks/contract.md 和 .ai4sci-kit/ai4sci.py audit . 交付，'
          '修复实际核查失败再停，不改工具。只用本目录资料、Python 标准库、CPU。不要联网、读其他课题、commit 或 push。')


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('directory', type=Path, help='new directory; failed and successful attempts are retained')
    cli.add_argument('--model', help='OpenCode provider/model (default: configured model)')
    cli.add_argument('--timeout', type=int, default=1200, help='wall time in seconds')
    args = cli.parse_args()
    if args.timeout <= 0:
        cli.error('--timeout must be positive')
    if not shutil.which('git') or not shutil.which('opencode'):
        cli.error('Git and OpenCode must be on PATH')
    attempt = args.directory.resolve()
    if attempt.exists():
        cli.error(f'already exists: {attempt}; inspect the original attempt before starting another')
    attempt.mkdir(mode=0o700, parents=True)
    project = attempt / 'study'
    project.mkdir()
    subprocess.run(['git', 'init', '-q', str(project)], check=True)
    subprocess.run([sys.executable, ROOT / 'ai4sci.py', 'init', project], check=True)
    inputs = project / 'inputs'
    inputs.mkdir()
    for note in ['trapezoid-note.md', 'left-note.md']:
        shutil.copy2(ROOT / 'examples/quadrature/research' / note, inputs / note)
    (attempt / 'request.txt').write_text(PROMPT + '\n', encoding='utf-8')
    cmd = ['opencode', 'run', '--archived', '--format', 'json']
    if args.model:
        cmd.extend(['--model', args.model])
    print(f'Running OpenCode once. Local logs and outputs: {attempt}', flush=True)
    with (attempt / 'events.jsonl').open('xb') as log, (attempt / 'stderr.txt').open('xb') as err:
        try:
            process = subprocess.run([*cmd, PROMPT], cwd=project, stdout=log, stderr=err, timeout=args.timeout)
        except subprocess.TimeoutExpired:
            sys.exit(f'Time limit reached. Check session/server state and {attempt}; no second request submitted.')
    if process.returncode:
        sys.exit(f'OpenCode exited {process.returncode}; inspect {attempt}')
    # Use the independent checkout, not a verifier the study's agent could have edited.
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
