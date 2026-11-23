# 独立复核：均匀网格求积的误差阶

**判定：可以交付。** 由未参与实验和写稿的复核者独立重算；四条登记结论均获支持，无阻塞项。正式实验已完成，试跑和正式命令均退出 0。

## 精确复算

复核不调用原实验程序，而用 Python 标准库 `Fraction` 根据整数平方和求取精确估计。由 $\sum_{i=0}^{n-1}i^2=(n-1)n(2n-1)/6$，得左端点估计 $Q_L=(n-1)n(2n-1)/(6n^3)$；再按端点权重关系得到梯形估计 $Q_T=Q_L+1/(2n)$。分别减去真值 $I=1/3$，与原始数据逐行比较。

| 方法 | 精确 $E(128)$ | 精确 $E(256)$ | 精确误差比 | 复算经验阶 | CSV 经验阶 |
|---|---:|---:|---:|---:|---:|
| 复合梯形 | 1/98304 | 1/393216 | 4 | 2 | 1.9999999999921272 |
| 左端点矩形 | 383/98304 | 767/393216 | 1532/767 | 0.9981178144220237 | 0.9981178144220304 |

在全部十二个方法与网格组合上，估计值和误差与精确复算相符；梯形误差均为正，左端点误差均为负。以 CSV 的浮点误差和浮点解析式重算，最大偏差依次为 `1.8648277366750676e-17` 和 `2.0816681711721685e-17`，与 `consistency.csv` 一致。另将 CSV 误差的十进制文本当作精确分数求残差，两种方法的最大值均为约 `1.85333e-17`；这是不同的计算口径，均通过冻结容差 `1e-14`。

## 逐条核对

| 登记项 | 判定 | 依据 |
|---|---|---|
| C1 / K1 | 支持 | [梯形笔记](../inputs/trapezoid-note.md)第 5 行给出原函数和解析参考值 1/3。 |
| C2 / K2 | 支持 | [原始 CSV](results.csv)第 7 行的带符号误差为 `+2.5431315104351704e-6`；末次经验阶符合二阶阈值，论文显示精度准确。 |
| C3 / K3 | 支持 | 同一 CSV 第 13 行的带符号误差为 `-0.0019505818684895648`；末次经验阶符合一阶阈值，论文显示精度准确。 |
| C4 / K4 | 支持 | [全网格对照](consistency.csv)两行的最大偏差和符号标志均由复算确认，论文显示的 `1.865e-17` 与 `2.082e-17` 舍入正确。 |

冻结计划摘要与 `plan.sha256` 一致。`run.json` 的试跑值为梯形 `0.375`、左端点 `0.125`，符号符合预期；两组的被积函数、区间、网格和参考值匹配。图中的六个横坐标和十二个数据点与从 CSV 重算到两位小数的坐标一致，向左表示网格加密。摘要所述的误差下降及两组降幅差异在所测网格上成立；论文未把结果外推到其他函数或更细的舍入主导区间。冻结摘要核实的是计划字节一致性，不是独立时间戳。

## 本地审计

实际执行 `python3 .ai4sci-kit/ai4sci.py audit .`，退出码 `0`。结果：

```json
{"claims": {"C1": "supported", "C2": "supported", "C3": "supported", "C4": "supported"}, "deliverability": "ready", "error_count": 0, "errors": [], "incomplete": [], "incomplete_count": 0, "run": "complete", "scientific_run": "completed"}
```

审计核对证据和交付结构；前述闭式复算单独核对科学结论。

## 复算命令

复核者从项目根目录执行以下两条只读命令，均退出 0。第一条打印逐点闭式估计、误差、收敛阶与图的预期坐标，供对照原始文件；第二条单独重算全网格最大偏差和符号。

```sh
python3 - <<'PY'
import csv, json, math, hashlib
from fractions import Fraction as F
from pathlib import Path
root=Path('.')
plan_bytes=Path('research/plan.json').read_bytes()
print('PLAN_SHA256',hashlib.sha256(plan_bytes).hexdigest(),Path('research/plan.sha256').read_text().strip())
rows=list(csv.DictReader(open('research/results.csv',newline='',encoding='utf-8')))
cons=list(csv.DictReader(open('research/consistency.csv',newline='',encoding='utf-8')))
ns=[8,16,32,64,128,256]
I=F(1,3)
all_exact={}
for method in ('trapezoid','left'):
    print('\nMETHOD',method)
    exact_errors=[]
    for n in ns:
        # closed-form integer sum of squares; no call to experiment implementation
        S=F((n-1)*n*(2*n-1),6)
        q_left=S/F(n**3)
        q=q_left + (F(1,2*n) if method=='trapezoid' else 0)
        e=q-I
        exact_errors.append(e)
        row=next(r for r in rows if r['method']==method and int(r['n'])==n)
        stored_e=F(row['signed_error'])
        stored_q=F(row['estimate'])
        pred=F(1,6*n*n) if method=='trapezoid' else F(1,6*n*n)-F(1,2*n)
        residual=abs(stored_e-pred)
        print('n=%d exact_Q=%s exact_e=%s csv_Q=%s csv_e=%s exact_resid_csv_e=%s float_resid=%.17g sign=%s' % (n,q,e,row['estimate'],row['signed_error'],residual,float(residual), 'match' if (stored_e>0)==(pred>0) else 'MISMATCH'))
    ratio=abs(exact_errors[-2]/exact_errors[-1])
    p=math.log2(float(ratio))
    cr=next(r for r in cons if r['method']==method)
    csv_p=float(next(r for r in rows if r['method']==method and int(r['n'])==256)['order'])
    print('EXACT_FINAL_ERRORS',exact_errors[-2],exact_errors[-1],'RATIO',ratio,'FINAL_P',repr(p),'CSV_P',repr(csv_p),'K4_CSV_FLOAT',cr)
    print('max exact rational CSV signed-error residual=',max(abs(F(r['signed_error'])-(F(1,6*int(r['n'])**2) if method=='trapezoid' else F(1,6*int(r['n'])**2)-F(1,2*int(r['n'])))) for r in rows if r['method']==method))
# independent plotted coordinate audit from formula in plot_errors
left,right,top,bottom=105,745,115,430
lo_x=math.log2(1/256)-.25; hi_x=math.log2(1/8)+.25
for n in ns:
 h=1/n
 x=left+(math.log2(h)-lo_x)*(right-left)/(hi_x-lo_x)
 print('SVG_X n=%d expected=%.2f' % (n,x))
for method in ('trapezoid','left'):
 for r in (x for x in rows if x['method']==method):
  err=abs(F(r['signed_error']))
  ylog=math.log10(float(err)); lo_y=math.floor(min(math.log10(float(abs(F(x['signed_error'])))) for x in rows)); hi_y=math.ceil(max(math.log10(float(abs(F(x['signed_error'])))) for x in rows))
  y=bottom-(ylog-lo_y)*(bottom-top)/(hi_y-lo_y)
  print('SVG_Y',method,r['n'],'expected=%.2f'%y)
PY
```

```sh
python3 - <<'PY'
import csv
from fractions import Fraction as F
rows=list(csv.DictReader(open('research/results.csv',newline='')))
for m in ('trapezoid','left'):
    rs=[r for r in rows if r['method']==m]
    ds=[]; exact=[]; signs=[]
    for r in rs:
        n=int(r['n']); csv_e=float(r['signed_error'])
        theory=1/(6*n**2)
        if m=='left': theory-=1/(2*n)
        ds.append(abs(csv_e-theory))
        exact.append(abs(F(r['signed_error'])-
            (F(1,6*n*n) if m=='trapezoid' else F(1,6*n*n)-F(1,2*n))))
        signs.append((csv_e>0)==(theory>0))
    print(m, 'float_max=',repr(max(ds)),
          'exact_csv_decimal_max=',repr(float(max(exact))),
          'signs=',all(signs))
PY
```
