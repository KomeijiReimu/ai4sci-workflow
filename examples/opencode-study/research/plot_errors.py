"""Draw the study's log-log error plot from results.csv using the standard library."""

import csv
import math
from pathlib import Path


def main():
    research = Path("research")
    styles = {
        "trapezoid": ("复合梯形法", "#165b96", "circle", "none"),
        "left": ("左端点矩形法", "#a14013", "rect", "7 5"),
    }
    points = {method: [] for method in styles}
    with (research / "results.csv").open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            points[row["method"]].append((int(row["n"]), float(row["h"]), float(row["abs_error"])))

    x_ticks = sorted({(n, h) for series in points.values() for n, h, _ in series}, key=lambda tick: tick[1])
    lo_x, hi_x = math.log2(x_ticks[0][1]) - 0.25, math.log2(x_ticks[-1][1]) + 0.25
    log_errors = [math.log10(error) for series in points.values() for _, _, error in series]
    lo_y, hi_y = math.floor(min(log_errors)), math.ceil(max(log_errors))
    left, right, top, bottom = 105, 745, 115, 430

    def x_pos(h):
        return left + (math.log2(h) - lo_x) * (right - left) / (hi_x - lo_x)

    def y_pos(log_error):
        return bottom - (log_error - lo_y) * (bottom - top) / (hi_y - lo_y)

    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="780" height="515" viewBox="0 0 780 515" '
        'xml:lang="zh-CN" role="img" aria-labelledby="title desc">',
        '<title id="title">均匀网格求积的绝对误差</title>',
        '<desc id="desc">双对数坐标，比较复合梯形法与左端点矩形法，每条曲线有六个网格点。</desc>',
        '<rect width="780" height="515" fill="#fff"/>',
        '<g fill="#17242f" font-family="Noto Sans CJK SC, Source Han Sans SC, Microsoft YaHei, '
        'PingFang SC, WenQuanYi Zen Hei, sans-serif" font-size="15">',
        '<text x="390" y="37" text-anchor="middle" font-size="23" font-weight="bold">'
        '均匀网格求积的绝对误差</text>',
        '<text x="390" y="63" text-anchor="middle">f(x) = x²，积分区间 [0,1]，双对数坐标</text>',
    ]
    for n, h in x_ticks:
        x = x_pos(h)
        svg.extend([
            f'<path d="M{x:.2f} {top} V{bottom}" stroke="#e1e7ec"/>',
            f'<text x="{x:.2f}" y="{bottom + 25}" text-anchor="middle">1/{n}</text>',
        ])
    superscripts = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
    for exponent in range(lo_y, hi_y + 1):
        y = y_pos(exponent)
        svg.extend([
            f'<path d="M{left} {y:.2f} H{right}" stroke="#e1e7ec"/>',
            f'<text x="{left - 11}" y="{y + 5:.2f}" text-anchor="end">'
            f'10{str(exponent).translate(superscripts)}</text>',
        ])
    svg.extend([
        f'<path d="M{left} {top} V{bottom} H{right}" fill="none" stroke="#17242f"/>',
        '<text x="425" y="492" text-anchor="middle">网格步长 h = 1/n（对数刻度）</text>',
        '<text x="31" y="273" transform="rotate(-90 31 273)" text-anchor="middle">'
        '绝对误差 |Q − I|（对数刻度）</text>',
    ])
    for (method, (label, color, marker, dash)), legend_x in zip(styles.items(), (235, 425)):
        coords = [(x_pos(h), y_pos(math.log10(error))) for _, h, error in points[method]]
        vertices = " ".join(f"{x:.2f},{y:.2f}" for x, y in coords)
        svg.extend([
            f'<g id="{method}">',
            f'<polyline points="{vertices}" fill="none" stroke="{color}" stroke-width="2.5" '
            f'stroke-dasharray="{dash}"/>',
            f'<path d="M{legend_x} 88 h32" stroke="{color}" stroke-width="2.5" stroke-dasharray="{dash}"/>',
            f'<text x="{legend_x + 42}" y="93">{label}</text>',
        ])
        for x, y in coords + [(legend_x + 16, 88)]:
            if marker == "circle":
                shape = f'<circle cx="{x:.2f}" cy="{y:.2f}" r="4.5"'
            else:
                shape = f'<rect x="{x - 4:.2f}" y="{y - 4:.2f}" width="8" height="8"'
            svg.append(f'{shape} fill="#fff" stroke="{color}" stroke-width="2"/>')
        svg.append('</g>')
    svg.extend(['</g>', '</svg>'])
    (research / "error.svg").write_text("\n".join(svg) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
