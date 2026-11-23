"""Run the credentialed OpenCode acceptance task in a new, retained study directory."""
import argparse
import csv
import json
import math
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
MESHES = (8, 16, 32, 64, 128, 256)
METHODS = ('trapezoid', 'left')
ORDER_COLUMNS = ('order', 'observed_order')
ORDER_ATOL = 1e-5
LIMITS = ('Fixed quadrature benchmark only: the two signed-error series, their marked final-grid values, '
          'reported order/observed_order cells and relative plotted positions were targeted. Other '
          'columns (including unrecognized rate aliases), numerical '
          'roles in prose and scientific interpretation are not assessed. Commands are not replayed; '
          'review presence is not reviewer authentication or publication endorsement.')


def study_file(project, base, name):
    path = (base / name).resolve()
    if Path(name).is_absolute() or not path.is_relative_to(project) or not path.is_file():
        raise ValueError(f'Expected project-local file: {name}')
    return path


def check_study(project):
    """Task-specific checks after the general manifest/claim audit has passed."""
    research = project / 'research'
    paper = (research / 'paper.md').read_text(encoding='utf-8')
    run = json.loads((research / 'run.json').read_text(encoding='utf-8'))
    claims = json.loads((research / 'claims.json').read_text(encoding='utf-8'))['claims']
    for field in ('command', 'plot_command'):
        command = run.get(field)
        if not isinstance(command, str):
            raise ValueError(f'Missing {field}: python3 <project-local script.py>')
        argv = shlex.split(command)
        if len(argv) < 2 or argv[0] != 'python3' or not argv[1].endswith('.py'):
            raise ValueError(f'Expected {field}: python3 <project-local script.py>')
        script = study_file(project, project, argv[1])
        if not script.read_text(encoding='utf-8').strip():
            raise ValueError(f'Empty script: {script}')

    # Exact uniform-mesh biases from the supplied notes, not the submitted experiment.
    expected = {(m, n): 1 / (6*n*n) - (1 / (2*n) if m == 'left' else 0)
                for m in METHODS for n in MESHES}
    tables = set()
    for method in METHODS:
        matches = [e for c in claims for e in c['evidence'] if e['kind'] == 'number' and e['column'] == 'signed_error'
                   and e['key'].get('method') == method and e['key'].get('n') == str(MESHES[-1])
                   and math.isclose(float(e['value']), expected[method, MESHES[-1]], rel_tol=1e-5)]
        if not matches:
            raise ValueError(f'Missing accurate marked final-grid signed error for {method}')
        tables.update(e['path'] for e in matches)
    if len(tables) != 1:
        raise ValueError('Expected one common measured table for both methods')
    table_name = tables.pop()
    table = study_file(project, project, table_name)
    errors = {}
    with table.open(encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        if not {'method', 'n', 'signed_error'}.issubset(headers):
            raise ValueError('Measured CSV requires method,n,signed_error headers')
        orders = {col: {} for col in ORDER_COLUMNS if col in headers}
        for row in reader:
            key = row['method'], int(row['n'])
            value = float(row['signed_error'])
            if key not in expected or key in errors or not math.isclose(value, expected[key], rel_tol=0, abs_tol=1e-14):
                raise ValueError(f'Unexpected, duplicate or inaccurate mesh error: {key}')
            errors[key] = value
            for col, cells in orders.items():
                if row[col] != '':
                    cells[key] = float(row[col])
    if errors.keys() != expected.keys():
        raise ValueError('Measured table is missing formal meshes')
    # Recompute from the checked *measurements* by key, independent of CSV row order.
    rates = {(m, n): math.log2(abs(errors[m, n//2] / errors[m, n])) for m in METHODS for n in MESHES[1:]}
    rate_checks = {col: {'cells': len(cells), 'marked_bindings': 0} for col, cells in orders.items()}
    for col, cells in orders.items():
        for key, value in cells.items():
            if key not in rates or not math.isclose(value, rates[key], rel_tol=0, abs_tol=ORDER_ATOL):
                raise ValueError(f'Inaccurate or undefined reported doubling rate: {col} {key}')
    for c in claims:
        for e in c['evidence']:
            if e['kind'] == 'number' and e['column'] in ORDER_COLUMNS:
                col = e['column']
                key = e['key'].get('method'), int(e['key'].get('n', '0'))
                if (e['path'] != table_name or key not in orders.get(col, {})
                        or not math.isclose(float(e['value']), rates[key], rel_tol=0, abs_tol=ORDER_ATOL)):
                    raise ValueError(f'Unverified marked doubling rate in {c["id"]}: {col} {key}')
                rate_checks[col]['marked_bindings'] += 1

    outputs = {study_file(project, project, s) for s in run['outputs']}
    figures = set()
    for bracketed, plain in re.findall(r'!\[[^\]\n]*\]\((?:<([^>\n]+)>|([^\s()]+))\)', paper):
        name = bracketed or plain
        if Path(name).suffix.lower() == '.svg':
            figures.add(study_file(project, research, name))
    if len(figures & outputs) != 1:
        raise ValueError('Expected one Markdown-embedded SVG figure declared in run outputs')
    figure = (figures & outputs).pop()
    svg = ET.parse(figure).getroot()
    ns = '{http://www.w3.org/2000/svg}'
    if svg.tag != ns + 'svg':
        raise ValueError('Expected an SVG drawing')
    points = {}
    for method in METHODS:
        series = [p for group in svg.iter() if group.get('id') == method for p in group.iter(ns + 'polyline')]
        if len(series) != 1:
            raise ValueError(f'Expected one plotted polyline for {method}')
        coords = [float(v) for v in re.split(r'[\s,]+', series[0].get('points', '').strip())]
        if len(coords) != 2*len(MESHES) or not all(map(math.isfinite, coords)):
            raise ValueError(f'Expected one plotted point per mesh for {method}')
        points.update(zip(((method, n) for n in MESHES), zip(coords[::2], coords[1::2])))

    # Origin, scale and canvas size are free; both curves must use the same log axes.
    x0, x1 = points['trapezoid', MESHES[0]][0], points['trapezoid', MESHES[-1]][0]
    low, high = min(expected, key=lambda k: abs(expected[k])), max(expected, key=lambda k: abs(expected[k]))
    y0, y1 = points[low][1], points[high][1]
    if abs(x1-x0) < 20 or y0-y1 < 20:
        raise ValueError('Missing usable plot extent for mesh and absolute error')
    for key, (x, y) in points.items():
        px = x0 + (x1-x0) * math.log2(key[1]/MESHES[0]) / math.log2(MESHES[-1]/MESHES[0])
        py = y0 + (y1-y0) * math.log(abs(expected[key]/expected[low])) / math.log(abs(expected[high]/expected[low]))
        if abs(x-px) > 1 or abs(y-py) > 1:
            raise ValueError(f'Plotted point disagrees with numerical error series: {key}')

    review = study_file(project, research, 'review.md').read_text(encoding='utf-8')
    if not review.strip():
        raise ValueError('Empty review artifact: research/review.md')
    return {'figure': str(figure.relative_to(project)), 'measured_table': str(table.relative_to(project)),
            'checked_mesh_errors': len(errors), 'checked_doubling_rates': sum(len(cells) for cells in orders.values()),
            'rate_columns': rate_checks, 'order_atol': ORDER_ATOL,
            'review': {'path': 'research/review.md', 'status': 'present, not assessed'}}


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
        f'研究目录是 {project}；用此目录 inputs/ 的两份笔记检验一个固定问题：'
        '积分 x² 于 [0,1]，比较复合梯形与左端点法的网格加密误差。'
        '只在研究目录内写研究文件，不复制工具、技能或配置，不初始化 Git。'
        f'先用 python3 {cli_path} freeze {study_path} 冻结计划，再执行实验，交付带实际结果和误差图的中文短论文。\n'
        '本验收题的接口（不适用于其他课题）：正式面板数 n=8,16,32,64,128,256。直接做两种求积；'
        '闭式公式只作独立对照，不生成观测。任意命名的一张 CSV 必含 method,n,signed_error；'
        'method 取 trapezoid 或 left，signed_error 为实测估计减 1/3，每种方法每个 n 恰好一行，'
        '保存完整精度（绝对容差 1e-14）。论文分别登记 n=256 的带符号误差（至少六位有效数字），'
        '用 method 和 n 定位对应 signed_error。若报告经验收敛阶，用同一 CSV 的 order 或 observed_order 列；'
        '在细网格 n 行记 log2(|E(n/2)/E(n)|)，无前一网格或未报告则留空。论文用 method 和 n 定位该列的单元格；'
        f'表值和登记值的绝对容差均为 {ORDER_ATOL}。\n'
        '论文用 ![说明](相对路径.svg) 内嵌一张实测绝对误差双对数 SVG 图（含空格的路径用尖括号）。'
        '共用横轴 n 或 1/n，纵轴为绝对误差；每条 SVG polyline 或其父组的 id 为对应 method。'
        'points 为按 n 递增排列的六个绘图区坐标，直接写坐标，不用坐标变换，宽、高跨度至少 20 个单位。'
        'run.json 的 outputs 同时登记 CSV 和 SVG；command、plot_command 分别给出从研究根目录重算数据、'
        '重画图的实际 python3 项目内脚本.py 命令（可同一个脚本）。\n'
        f'按 {ROOT / "checks/contract.md"} 请另一复核者对照决定性结论、原始单元格和图，独立复算；'
        '在 research/review.md 记录核查方法、结果及分歧。只有自查则如实注明，不冒称独立或盲审。'
        '按 handoff 模板保留简短的 research/handoff.md。'
        f'用 python3 {cli_path} audit {study_path} 核查，'
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
    try:
        if result['scientific_run'] != 'completed' or result['deliverability'] != 'ready':
            raise ValueError('The requested computational study was not completed.')
        quality = {'result': 'pass', **check_study(project), 'limits': LIMITS}
    except (ValueError, KeyError, TypeError, OSError, ET.ParseError, csv.Error) as error:
        quality = {'result': 'fail', 'reason': str(error), 'limits': LIMITS}
    quality['benchmark'] = 'Uniform-mesh quadrature of x² on [0,1]: trapezoid and left endpoints'
    (attempt / 'quality.json').write_text(json.dumps(quality, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if quality['result'] != 'pass':
        sys.exit(f'Benchmark failed: {quality["reason"]}; inspect {attempt}; no second request submitted.')
    print(f'Fixed numerical benchmark passed: {project / "research/paper.md"}\nEvidence check: {attempt / "audit.json"}'
          f'\nBenchmark check: {attempt / "quality.json"}\n{LIMITS}')


if __name__ == '__main__':
    main()
