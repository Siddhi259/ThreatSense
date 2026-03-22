"""
app.py — ThreatSense Web Interface
Emotion-Aware Social Engineering Attack Detection System
Run: streamlit run app.py
"""

import streamlit as st
from main import analyze
from src.logger import get_history, get_stats, clear_log

st.set_page_config(
    page_title="ThreatSense",
    page_icon="🛡",
    layout="centered",
)

st.markdown("""
<style>
.risk-high   { color:#ff4b4b; font-size:26px; font-weight:800; }
.risk-medium { color:#ffa500; font-size:26px; font-weight:800; }
.risk-low    { color:#00c851; font-size:26px; font-weight:800; }
.emotion-tag { display:inline-block; background:#f0f2f6; border-radius:20px;
               padding:4px 12px; margin:3px; font-size:13px; color:#555; }
.emotion-hit { background:#e6f4ea; color:#1a7f37; font-weight:600; }
.ts-header   { font-size:11px; color:#888; letter-spacing:0.08em;
               text-transform:uppercase; margin-bottom:2px; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<p class="ts-header">Cybersecurity · NLP · Machine Learning</p>',
            unsafe_allow_html=True)
st.markdown("## 🛡 ThreatSense")
st.markdown("##### Emotion-Aware Social Engineering Attack Detection System")
st.markdown("*Detecting cyber threats through psychological manipulation patterns*")

tab_scan, tab_batch, tab_history, tab_stats = st.tabs(
    ["🔍 Scan", "📂 Batch", "📜 History", "📊 Stats"]
)

# ── TAB 1: SCAN ───────────────────────────────────────────────────────────────
with tab_scan:
    SAMPLES = {
        "High Risk — Bank Scam":
            "Your bank account is blocked. Act immediately or face legal action.",
        "Medium Risk — Prize Scam":
            "Congratulations! You won a free prize. Claim your reward now immediately!",
        "Low Risk — Normal Message":
            "Meeting postponed to tomorrow. See you then.",
        "High Risk — Government Fraud":
            "URGENT: Government has flagged your account for fraud. Respond now to avoid arrest.",
    }
    col1, col2 = st.columns([3, 1])
    with col2:
        sample_choice = st.selectbox("Load sample", ["— custom —"] + list(SAMPLES.keys()))
    default_text = SAMPLES.get(sample_choice, "") if sample_choice != "— custom —" else ""
    message = st.text_area(
        "Paste message / email / SMS below:",
        value=default_text, height=130,
        placeholder="e.g. Your account has been suspended. Act immediately...",
    )

    if st.button("🔍 Analyze with ThreatSense", type="primary", use_container_width=True):
        if not message.strip():
            st.warning("Please enter a message to analyze.")
        else:
            result = analyze(message)
            level  = result["risk_level"]
            st.divider()
            color_map = {"HIGH": "risk-high", "MEDIUM": "risk-medium", "LOW": "risk-low"}
            emoji_map = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}
            st.markdown(
                f'<div class="{color_map[level]}">'
                f'{emoji_map[level]} {level} RISK &nbsp;|&nbsp; Score: {result["total_score"]}'
                f'</div>', unsafe_allow_html=True)
            st.markdown(f"> {result['explanation']}")

            st.markdown("#### 🧠 Emotion Breakdown")
            tag_html = ""
            for emo, info in result["emotions_detail"].items():
                css = "emotion-tag emotion-hit" if info["detected"] else "emotion-tag"
                kws = f" ({', '.join(info['matched'])})" if info["matched"] else ""
                tag_html += f'<span class="{css}">{emo.capitalize()}{kws}</span>'
            st.markdown(tag_html, unsafe_allow_html=True)

            nonzero = {k: v for k, v in result["breakdown"].items() if v > 0}
            if nonzero:
                st.markdown("#### 📐 Score Breakdown")
                st.bar_chart(nonzero)

            # ML second opinion
            ml = result.get("ml")
            if ml and ml.get("ml_risk_level") not in (None, "N/A"):
                conf = int(ml["ml_confidence"] * 100)
                agree = "✔ Agrees with rule engine" if ml["ml_risk_level"] == level else "⚠ Differs from rule engine"
                st.markdown(f"**🤖 ML Second Opinion:** `{ml['ml_risk_level']}` — {conf}% confidence &nbsp;|&nbsp; {agree}")

            st.markdown("#### 🛡 Recommendation")
            rec_map = {"HIGH": "error", "MEDIUM": "warning", "LOW": "success"}
            getattr(st, rec_map[level])(result["recommendation"])

# ── TAB 2: BATCH ─────────────────────────────────────────────────────────────
with tab_batch:
    st.markdown("### 📂 Batch Analyzer")
    st.markdown("Upload a CSV with one message per row. Optional column 2: expected risk level.")
    uploaded = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded:
        import csv, io
        content = uploaded.read().decode("utf-8")
        reader  = csv.reader(io.StringIO(content))
        rows    = [(r[0].strip().strip('"'), r[1].strip() if len(r) > 1 else "")
                   for r in reader if r and r[0].lower() not in ("message", "msg")]
        st.info(f"Found **{len(rows)}** messages.")
        if st.button("▶ Run ThreatSense Batch Analysis", type="primary"):
            batch_results = []
            prog = st.progress(0)
            for i, (msg, exp) in enumerate(rows):
                r = analyze(msg, save_log=False)
                batch_results.append({
                    "Message":  msg[:60] + ("..." if len(msg) > 60 else ""),
                    "Risk":     r["risk_level"],
                    "Score":    r["total_score"],
                    "Emotions": ", ".join(r["active_emotions"]) or "—",
                    "Expected": exp or "—",
                })
                prog.progress((i + 1) / len(rows))
            st.dataframe(batch_results, use_container_width=True)
            counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
            for b in batch_results:
                counts[b["Risk"]] += 1
            c1, c2, c3 = st.columns(3)
            c1.metric("🔴 HIGH",   counts["HIGH"])
            c2.metric("🟡 MEDIUM", counts["MEDIUM"])
            c3.metric("🟢 LOW",    counts["LOW"])

# ── TAB 3: HISTORY ────────────────────────────────────────────────────────────
with tab_history:
    st.markdown("### 📜 ThreatSense — Analysis History")
    history = get_history()
    if not history:
        st.info("No analyses logged yet. Scan some messages first.")
    else:
        display = []
        for e in reversed(history):
            emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(e["risk_level"], "⬜")
            display.append({
                "ID": e["id"], "Timestamp": e["timestamp"],
                "Risk": f"{emoji} {e['risk_level']}", "Score": e["risk_score"],
                "Emotions": ", ".join(e["active_emotions"]) or "—",
                "Message": e["message"][:70] + ("..." if len(e["message"]) > 70 else ""),
            })
        st.dataframe(display, use_container_width=True)
        if st.button("🗑 Clear History", type="secondary"):
            clear_log()
            st.success("History cleared.")
            st.rerun()

# ── TAB 4: STATS ─────────────────────────────────────────────────────────────
with tab_stats:
    st.markdown("### 📊 ThreatSense — Aggregate Statistics")
    stats = get_stats()
    if stats["total"] == 0:
        st.info("No data yet. Scan some messages to see stats.")
    else:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Scans", stats["total"])
        c2.metric("🔴 HIGH",     stats["by_risk"].get("HIGH",   0))
        c3.metric("🟡 MEDIUM",   stats["by_risk"].get("MEDIUM", 0))
        c4.metric("🟢 LOW",      stats["by_risk"].get("LOW",    0))
        st.metric("Avg Risk Score", stats["avg_score"])
        if stats["top_emotions"]:
            st.markdown("#### Most Detected Emotions")
            st.bar_chart(dict(stats["top_emotions"]))

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.caption("🛡 ThreatSense — Emotion-Aware Social Engineering Attack Detection System | Third Year Project | CSE 2025–2026")
