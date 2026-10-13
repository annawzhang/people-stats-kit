"""生成 docs/index.html 报告。"""

from __future__ import annotations

from html import escape


def _pct(x: float | None, digits: int = 1) -> str:
    if x is None:
        return "—"
    return f"{x * 100:.{digits}f}%"


def _num(x: float | None, digits: int = 3) -> str:
    if x is None:
        return "—"
    return f"{x:.{digits}f}"


def render(ctx: dict) -> str:
    ab = ctx["ab_test"]
    ss = ctx["sample_size"]
    funnel = ctx["funnel"]
    surv = ctx["survival"]
    cal = ctx["calibration"]
    brier = ctx["brier"]

    funnel_rows = "".join(
        f"<tr><td>{escape(r['name'])}</td><td class='num'>{r['n']}</td>"
        f"<td class='num'>{_pct(r['rate'])}</td>"
        f"<td class='num'>{'—' if not r['ci'] else _pct(r['ci'][0]) + ' – ' + _pct(r['ci'][1])}</td></tr>"
        for r in funnel
    )
    cal_rows = "".join(
        f"<tr><td>{escape(b['label'])}</td><td class='num'>{b['n']}</td>"
        f"<td class='num'>{_pct(b['mean_score'])}</td>"
        f"<td class='num'>{_pct(b['rate'])}</td>"
        f"<td class='num'>{_pct(b['gap']) if b.get('gap') is not None else '—'}</td></tr>"
        for b in cal
    )
    sig = "显著" if ab["p_value"] < 0.05 else "不显著"
    med = surv["median"]
    med_s = "—" if med is None else f"{med:.1f} 天"

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>People Stats Kit · 人力量化报告</title>
<style>
:root {{ --text:#0f172a; --muted:#64748b; --border:#e2e8f0; --accent:#0f766e; --bg:#f8fafc; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;
  background:var(--bg); color:var(--text); font-size:14px; line-height:1.6; }}
.wrap {{ max-width:980px; margin:0 auto; padding:28px 20px 60px; }}
h1 {{ font-size:1.6rem; margin:0 0 6px; }}
h2 {{ font-size:1.05rem; margin:28px 0 10px; border-left:4px solid var(--accent); padding-left:10px; }}
.muted {{ color:var(--muted); font-size:0.86rem; }}
.badge {{ display:inline-block; background:#fef3c7; color:#92400e; border-radius:999px; padding:2px 10px; font-size:0.75rem; }}
.grid {{ display:grid; gap:12px; grid-template-columns:repeat(4,1fr); margin:16px 0; }}
@media (max-width:800px) {{ .grid {{ grid-template-columns:1fr 1fr; }} }}
.card {{ background:#fff; border:1px solid var(--border); border-radius:12px; padding:14px; }}
.card .lbl {{ color:var(--muted); font-size:0.78rem; }}
.card .val {{ font-size:1.45rem; font-weight:700; margin-top:4px; }}
table {{ width:100%; border-collapse:collapse; background:#fff; border:1px solid var(--border); border-radius:12px; overflow:hidden; }}
th, td {{ padding:8px 10px; border-bottom:1px solid var(--border); text-align:left; }}
th {{ color:var(--muted); font-weight:600; font-size:0.8rem; background:#fff; }}
td.num, th.num {{ text-align:right; font-variant-numeric:tabular-nums; }}
.note {{ background:#f0fdfa; border:1px solid #99f6e4; border-radius:10px; padding:12px 14px; font-size:0.86rem; margin-top:10px; }}
code {{ background:#f1f5f9; padding:1px 5px; border-radius:4px; font-size:0.84rem; }}
</style>
</head>
<body>
<div class="wrap">
  <div class="badge">虚构数据 · 对齐公开作品口径</div>
  <h1>People Stats Kit · 人力量化报告</h1>
  <p class="muted">把统计学方法落到招聘漏斗、人才触达 AB、Offer 周期与评分校准。纯 Python 标准库，可复现。</p>

  <div class="grid">
    <div class="card"><div class="lbl">触达 AB 结论</div><div class="val">{sig}</div><div class="muted">p = {_num(ab['p_value'], 4)}</div></div>
    <div class="card"><div class="lbl">回复率提升</div><div class="val">{_pct(ab['lift'])}</div><div class="muted">{_pct(ab['rate_a'])} → {_pct(ab['rate_b'])}</div></div>
    <div class="card"><div class="lbl">开实验每组至少</div><div class="val">{ss['n_per_group']}</div><div class="muted">α={ss['alpha']} · 功效 {ss['power']:.0%}</div></div>
    <div class="card"><div class="lbl">入职中位周期</div><div class="val">{med_s}</div><div class="muted">Kaplan–Meier</div></div>
  </div>

  <h2>1. 触达文案 AB · 双比例 z 检验</h2>
  <p class="muted">场景对齐人才评估模型：对照组标准跟进 vs 实验组按 S+/S/A 分层跟进。混合样本不参与对比的排他逻辑见
    <a href="https://github.com/annawzhang/explainable-talent-scoring">explainable-talent-scoring</a>。</p>
  <table>
    <thead><tr><th>组</th><th class="num">触达</th><th class="num">回复</th><th class="num">回复率</th></tr></thead>
    <tbody>
      <tr><td>{escape(ctx['ab_labels']['a'])}</td><td class="num">{ab['n_a']}</td><td class="num">{ab['success_a']}</td><td class="num">{_pct(ab['rate_a'])}</td></tr>
      <tr><td>{escape(ctx['ab_labels']['b'])}</td><td class="num">{ab['n_b']}</td><td class="num">{ab['success_b']}</td><td class="num">{_pct(ab['rate_b'])}</td></tr>
    </tbody>
  </table>
  <div class="note">z = {_num(ab['z'], 3)}，双侧 p = {_num(ab['p_value'], 4)}。相对提升 {_pct(ab['lift'])}。
  若要在开跑前规划样本量：从 {_pct(ss['p1'])} 做到 {_pct(ss['p2'])}，每组约需 <strong>{ss['n_per_group']}</strong> 人。</div>

  <h2>2. 招聘漏斗 · 转化率 Wilson 置信区间</h2>
  <p class="muted">阶段名对齐 <a href="https://github.com/annawzhang/hiring-copilot">hiring-copilot</a>。看点估计不够，还要看区间是否重叠。</p>
  <table>
    <thead><tr><th>阶段</th><th class="num">人数</th><th class="num">上一步转化</th><th class="num">95% Wilson CI</th></tr></thead>
    <tbody>{funnel_rows}</tbody>
  </table>

  <h2>3. 招聘周期 · Kaplan–Meier</h2>
  <p class="muted">终点=入职；仍在 Offer / 观察未完记为删失。中位生存时间（一半人已入职）= <strong>{med_s}</strong>。</p>
  <div class="note">曲线点数 {len(surv['curve'])}；事件 {surv['n_events']} / 观察 {surv['n']}。
  对应作品里 Offer 停留超时、接受率偏低时，先看周期分布再拍 SLA。</div>

  <h2>4. 初筛分校准 · 预测 vs 现场面通过</h2>
  <p class="muted">分数映射到 0–1，分档对齐初筛「0–39 / 40–59 / ≥60」。gap = 真实通过率 − 平均预测分。</p>
  <table>
    <thead><tr><th>分档</th><th class="num">人数</th><th class="num">平均预测</th><th class="num">真实通过率</th><th class="num">gap</th></tr></thead>
    <tbody>{cal_rows}</tbody>
  </table>
  <div class="note">Brier score = {_num(brier, 4)}（越小越好）。高分档通过率应高于低分档，否则回头检查评分卡——与 hiring-copilot 分析页同一问题。</div>

  <p class="muted" style="margin-top:28px">本地：<code>python3 run.py</code> · 测试：<code>python3 -m unittest discover -s tests -v</code></p>
</div>
</body>
</html>
"""
