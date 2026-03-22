"""
src/report_generator.py — ThreatSense
Generates self-contained HTML reports for single analyses or batch sessions.

Usage:
  from src.report_generator import generate_single_report, generate_batch_report
  path = generate_single_report(message, result)
  path = generate_batch_report(results_list)
"""

import os
from datetime import datetime

REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "reports")


def _ensure_dir():
    os.makedirs(REPORTS_DIR, exist_ok=True)


def _risk_color(level):
    return {"HIGH": "#e53e3e", "MEDIUM": "#dd6b20", "LOW": "#38a169"}.get(level, "#718096")


def _risk_bg(level):
    return {"HIGH": "#fff5f5", "MEDIUM": "#fffaf0", "LOW": "#f0fff4"}.get(level, "#f7fafc")


def generate_single_report(message: str, result: dict, output_path: str = None) -> str:
    """Generate a ThreatSense single-message HTML analysis report."""
    _ensure_dir()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ts_slug   = datetime.now().strftime("%Y%m%d_%H%M%S")
    level     = result["risk_level"]
    score     = result["total_score"]
    color     = _risk_color(level)
    bg        = _risk_bg(level)

    badges_html = ""
    for emo, info in result.get("emotions_detail", {}).items():
        if info["detected"]:
            kws = ", ".join(info["matched"])
            badges_html += (f'<span class="badge badge-hit">'
                            f'{emo.capitalize()} <small>({kws})</small></span>')
        else:
            badges_html += f'<span class="badge">{emo.capitalize()}</span>'

    bars_html = ""
    for emo, pts in result.get("breakdown", {}).items():
        pct    = min(pts * 8, 100)
        bcolor = color if pts > 0 else "#cbd5e0"
        bars_html += f"""
        <div class="bar-row">
          <span class="bar-label">{emo.capitalize()}</span>
          <div class="bar-track"><div class="bar-fill" style="width:{pct}%;background:{bcolor}"></div></div>
          <span class="bar-pts">{pts}</span>
        </div>"""

    ml = result.get("ml") or {}
    ml_html = ""
    if ml.get("ml_risk_level") not in (None, "N/A", ""):
        conf    = int(ml.get("ml_confidence", 0) * 100)
        ml_lvl  = ml.get("ml_risk_level", "—")
        ml_col  = _risk_color(ml_lvl)
        agree   = "✔ Agrees with rule engine" if ml_lvl == level else "⚠ Differs"
        probs   = ml.get("probabilities", {})
        prob_rows = "".join(f'<tr><td>{k}</td><td>{int(v*100)}%</td></tr>'
                            for k, v in probs.items())
        ml_html = f"""
        <div class="section">
          <h3>🤖 ThreatSense ML Second Opinion</h3>
          <p><strong style="color:{ml_col}">{ml_lvl}</strong>
             &nbsp;—&nbsp; Confidence: <strong>{conf}%</strong>
             &nbsp;|&nbsp; {agree}</p>
          <table class="prob-table">
            <tr><th>Class</th><th>Probability</th></tr>{prob_rows}
          </table>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>ThreatSense — Analysis Report — {timestamp}</title>
<style>
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{ font-family:'Segoe UI',Arial,sans-serif; background:#f7fafc;
        color:#2d3748; padding:30px; }}
.card {{ background:#fff; border-radius:12px; padding:28px;
         max-width:780px; margin:0 auto;
         box-shadow:0 2px 12px rgba(0,0,0,.08); }}
.header {{ border-bottom:3px solid {color}; padding-bottom:16px; margin-bottom:20px; }}
.header h1 {{ font-size:22px; color:#1a202c; }}
.header .brand {{ font-size:13px; color:{color}; font-weight:700;
                   letter-spacing:0.08em; text-transform:uppercase; }}
.header p {{ color:#718096; font-size:13px; margin-top:4px; }}
.risk-pill {{ display:inline-block; background:{bg}; color:{color};
              border:2px solid {color}; border-radius:30px;
              padding:8px 22px; font-size:20px; font-weight:800;
              margin:14px 0; }}
.section {{ margin-top:22px; }}
.section h3 {{ font-size:15px; color:#4a5568; margin-bottom:10px; }}
.message-box {{ background:#edf2f7; border-left:4px solid {color};
                padding:12px 16px; border-radius:6px; font-size:14px;
                line-height:1.6; word-break:break-word; }}
.badge {{ display:inline-block; background:#edf2f7; color:#718096;
          border-radius:20px; padding:4px 12px; margin:3px; font-size:13px; }}
.badge-hit {{ background:#e6f4ea; color:#276749; font-weight:600; }}
.bar-row {{ display:flex; align-items:center; gap:10px; margin:5px 0; }}
.bar-label {{ width:90px; font-size:13px; color:#4a5568; }}
.bar-track {{ flex:1; background:#edf2f7; border-radius:4px; height:14px; overflow:hidden; }}
.bar-fill {{ height:100%; border-radius:4px; }}
.bar-pts {{ width:24px; text-align:right; font-size:13px; font-weight:600; }}
.recommendation {{ background:{bg}; border:1px solid {color};
                   border-radius:8px; padding:14px 16px; font-size:14px;
                   margin-top:10px; line-height:1.6; }}
.prob-table {{ border-collapse:collapse; font-size:13px; margin-top:8px; }}
.prob-table th,.prob-table td {{ border:1px solid #e2e8f0; padding:5px 14px; }}
.prob-table th {{ background:#f7fafc; }}
.footer {{ text-align:center; color:#a0aec0; font-size:12px; margin-top:26px; }}
</style>
</head>
<body>
<div class="card">
  <div class="header">
    <div class="brand">🛡 ThreatSense</div>
    <h1>Social Engineering Threat Analysis Report</h1>
    <p>Generated: {timestamp} &nbsp;|&nbsp; Emotion-Aware Attack Detection</p>
  </div>
  <div class="section">
    <h3>📩 Analyzed Message</h3>
    <div class="message-box">{message}</div>
  </div>
  <div class="section">
    <div class="risk-pill">
      {"🔴" if level=="HIGH" else "🟡" if level=="MEDIUM" else "🟢"}
      {level} RISK &nbsp;|&nbsp; Score: {score}
    </div>
    <p style="color:#718096;font-size:14px;margin-top:6px">{result.get('explanation','')}</p>
  </div>
  <div class="section">
    <h3>🧠 Emotion Detection</h3>
    {badges_html}
  </div>
  <div class="section">
    <h3>📐 Score Breakdown</h3>
    {bars_html}
  </div>
  {ml_html}
  <div class="section">
    <h3>🛡 Recommendation</h3>
    <div class="recommendation">{result.get('recommendation','')}</div>
  </div>
  <div class="footer">🛡 ThreatSense — Emotion-Aware Social Engineering Attack Detection System</div>
</div>
</body>
</html>"""

    if output_path is None:
        output_path = os.path.join(REPORTS_DIR, f"threatsense_report_{ts_slug}.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    return output_path


def generate_batch_report(results: list, output_path: str = None) -> str:
    """Generate a ThreatSense HTML batch summary report."""
    _ensure_dir()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ts_slug   = datetime.now().strftime("%Y%m%d_%H%M%S")
    counts    = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    rows      = ""

    for i, r in enumerate(results, 1):
        level  = r.get("risk_level", "LOW")
        score  = r.get("risk_score", r.get("total_score", 0))
        emoji  = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(level, "⬜")
        color  = _risk_color(level)
        counts[level] += 1
        msg    = r.get("message", "")[:80]
        emos   = r.get("active_emotions", "")
        rows  += f"""<tr>
          <td>{i}</td>
          <td style="max-width:360px;word-break:break-word">{msg}{"..." if len(r.get("message",""))>80 else ""}</td>
          <td><strong style="color:{color}">{emoji} {level}</strong></td>
          <td>{score}</td>
          <td>{emos if isinstance(emos,str) else ", ".join(emos)}</td>
        </tr>"""

    total = len(results)
    html  = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>ThreatSense — Batch Report — {timestamp}</title>
<style>
body {{ font-family:'Segoe UI',Arial,sans-serif; background:#f7fafc; color:#2d3748; padding:30px; }}
.card {{ background:#fff; border-radius:12px; padding:28px; max-width:960px; margin:0 auto;
         box-shadow:0 2px 12px rgba(0,0,0,.08); }}
.brand {{ font-size:12px; color:#0E7490; font-weight:700; letter-spacing:0.08em;
           text-transform:uppercase; margin-bottom:4px; }}
h1 {{ font-size:22px; color:#1a202c; border-bottom:3px solid #0E7490;
      padding-bottom:12px; margin-bottom:18px; }}
.summary {{ display:flex; gap:20px; margin-bottom:24px; flex-wrap:wrap; }}
.stat {{ background:#f7fafc; border-radius:10px; padding:14px 24px; text-align:center; min-width:120px; }}
.stat .n {{ font-size:32px; font-weight:800; }}
.stat .l {{ font-size:13px; color:#718096; }}
table {{ border-collapse:collapse; width:100%; font-size:13px; }}
th,td {{ border:1px solid #e2e8f0; padding:8px 12px; text-align:left; }}
th {{ background:#edf2f7; font-weight:600; }}
.footer {{ text-align:center; color:#a0aec0; font-size:12px; margin-top:24px; }}
</style>
</head>
<body>
<div class="card">
  <div class="brand">🛡 ThreatSense</div>
  <h1>Batch Analysis Report</h1>
  <p style="color:#718096;font-size:13px;margin-bottom:18px">Generated: {timestamp} | Total: {total}</p>
  <div class="summary">
    <div class="stat"><div class="n">{total}</div><div class="l">Total</div></div>
    <div class="stat"><div class="n" style="color:#e53e3e">{counts["HIGH"]}</div><div class="l">🔴 HIGH</div></div>
    <div class="stat"><div class="n" style="color:#dd6b20">{counts["MEDIUM"]}</div><div class="l">🟡 MEDIUM</div></div>
    <div class="stat"><div class="n" style="color:#38a169">{counts["LOW"]}</div><div class="l">🟢 LOW</div></div>
  </div>
  <table>
    <tr><th>#</th><th>Message</th><th>Risk</th><th>Score</th><th>Emotions</th></tr>
    {rows}
  </table>
  <div class="footer">🛡 ThreatSense — Emotion-Aware Social Engineering Attack Detection System</div>
</div>
</body>
</html>"""

    if output_path is None:
        output_path = os.path.join(REPORTS_DIR, f"threatsense_batch_{ts_slug}.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    return output_path
