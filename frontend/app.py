import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Brand Shield AI", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');
:root {
    --red:#C0392B; --red-light:#E74C3C; --red-glow:rgba(192,57,43,0.25);
    --dark-bg:#0F1419; --dark-card:#161D27; --dark-sidebar:#0D1117;
    --border:#1E2A38; --text:#E8EDF2; --muted:#7A8A9A;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 2rem 2.5rem !important; max-width: 100% !important; }
[data-testid="stAppViewContainer"] { background: var(--dark-bg); }
[data-testid="stSidebar"] { background: var(--dark-sidebar) !important; border-right: 1px solid var(--border); }
[data-testid="stSidebar"] .block-container { padding: 0 !important; }

/* Sidebar logo */
.sidebar-logo {
    display:flex; align-items:center; gap:10px;
    padding:20px 20px 14px; border-bottom:1px solid var(--border); margin-bottom:4px;
}
.logo-icon { width:36px;height:36px;background:var(--red);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:18px;box-shadow:0 0 16px var(--red-glow); }
.logo-text { font-family:'Rajdhani',sans-serif;font-size:20px;font-weight:700;color:#fff;letter-spacing:0.5px; }


/* ── Balanced sidebar spacing ── */
[data-testid="stSidebar"] .stButton,
[data-testid="stSidebar"] .stButton > div {
    margin: 0 !important;
    padding: 0 !important;
}
[data-testid="stSidebar"] .element-container {
    margin-bottom: 4px !important;
}
[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
    gap: 4px !important;
}

/* Hide default Streamlit page navigation links */
[data-testid="stSidebarNav"] { display: none !important; }
[data-testid="stSidebarNavItems"] { display: none !important; }
section[data-testid="stSidebar"] ul { display: none !important; }

/* Sidebar nav buttons - no spacing */
[data-testid="stSidebar"] [data-testid="stButton"] {
    margin: 0 !important;
    padding: 0 !important;
}
[data-testid="stSidebar"] [data-testid="stButton"] button {
    background: transparent !important;
    color: #A0B0C0 !important;
    border: none !important;
    border-radius: 8px !important;
    text-align: left !important;
    padding: 11px 18px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    box-shadow: none !important;
    margin: 0 !important;
    width: 100% !important;
    transition: all 0.15s !important;
    line-height: 1.2 !important;
}
[data-testid="stSidebar"] [data-testid="stButton"] button:hover {
    background: rgba(255,255,255,0.06) !important;
    color: #fff !important;
    transform: none !important;
}
/* Remove gap between sidebar elements */
[data-testid="stSidebar"] .stButton { margin-bottom: 0 !important; }
[data-testid="stSidebar"] .element-container { margin-bottom: 0 !important; }
[data-testid="stSidebar"] .stMarkdown { margin-bottom: 0 !important; }

/* Main content buttons */
.main-content [data-testid="stButton"] button,
[data-testid="stMainBlockContainer"] [data-testid="stButton"] button {
    background: var(--red) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 10px 24px !important;
    box-shadow: 0 4px 14px rgba(192,57,43,0.3) !important;
}
[data-testid="stMainBlockContainer"] [data-testid="stButton"] button:hover {
    background: var(--red-light) !important; transform: translateY(-1px) !important;
}

/* Form widgets */
[data-testid="stSelectbox"] label, [data-testid="stTextInput"] label, [data-testid="stTextArea"] label {
    color: #A0B0C0 !important; font-size:12px !important; font-family:'Inter',sans-serif !important;
    text-transform:uppercase; letter-spacing:0.8px;
}
[data-testid="stSelectbox"] > div > div,
[data-testid="stTextInput"] > div > div > input,
[data-testid="stTextArea"] textarea {
    background: #0D1117 !important; border:1px solid var(--border) !important;
    border-radius:8px !important; color:var(--text) !important; font-family:'Inter',sans-serif !important;
}

/* Page header */
.page-header { display:flex;align-items:center;justify-content:space-between;margin-bottom:28px;padding-bottom:20px;border-bottom:1px solid var(--border); }
.page-title { font-family:'Rajdhani',sans-serif;font-size:26px;font-weight:700;color:#fff;letter-spacing:0.5px; }

/* Hero */
.hero-card {
    background:linear-gradient(135deg,#161D27 0%,#1A2332 50%,#0F1922 100%);
    border:1px solid var(--border);border-radius:16px;padding:40px 44px;margin-bottom:24px;position:relative;overflow:hidden;
}
.hero-card::before { content:'';position:absolute;top:-60px;right:-60px;width:300px;height:300px;background:radial-gradient(circle,rgba(192,57,43,0.12) 0%,transparent 70%);border-radius:50%; }
.hero-title { font-family:'Rajdhani',sans-serif;font-size:38px;font-weight:700;color:#fff;line-height:1.2;margin-bottom:16px; }
.hero-title span { color:var(--red-light); }
.hero-desc { font-size:15px;color:#A0B0C0;line-height:1.7;max-width:620px; }

/* Feature grid */
.feature-grid { display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:24px; }
.feature-card { background:var(--dark-card);border:1px solid var(--border);border-radius:12px;padding:24px;transition:border-color 0.2s; }
.feature-card:hover { border-color:var(--red); }
.feature-icon { font-size:28px;margin-bottom:12px; }
.feature-title { font-family:'Rajdhani',sans-serif;font-size:18px;font-weight:700;color:var(--red-light);margin-bottom:6px; }
.feature-desc { font-size:13px;color:var(--muted);line-height:1.5; }

/* Info grid */
.info-grid { display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:24px; }
.info-card { background:var(--dark-card);border:1px solid var(--border);border-radius:12px;padding:28px; }
.info-card-title { font-family:'Rajdhani',sans-serif;font-size:17px;font-weight:700;color:#fff;margin-bottom:16px; }
.info-list { list-style:none;padding:0;margin:0; }
.info-list li { display:flex;align-items:flex-start;gap:10px;padding:8px 0;font-size:13.5px;color:#A8B8C8;border-bottom:1px solid rgba(255,255,255,0.04); }
.info-list li:last-child { border-bottom:none; }
.bullet { color:var(--red);font-size:16px;margin-top:1px; }
.step-list { list-style:none;padding:0;margin:0 0 16px; }
.step-list li { display:flex;align-items:flex-start;gap:14px;padding:10px 0;font-size:13.5px;color:#A8B8C8;border-bottom:1px solid rgba(255,255,255,0.04); }
.step-num { min-width:24px;height:24px;background:rgba(192,57,43,0.2);border:1px solid var(--red);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:var(--red);margin-top:1px; }

/* Verdict */
.verdict-safe { background:rgba(39,174,96,0.12);border:1px solid #27AE60;border-radius:12px;padding:20px 24px; }
.verdict-suspicious { background:rgba(241,196,15,0.10);border:1px solid #F1C40F;border-radius:12px;padding:20px 24px; }
.verdict-impersonation { background:rgba(192,57,43,0.12);border:1px solid var(--red);border-radius:12px;padding:20px 24px; }
.verdict-title { font-family:'Rajdhani',sans-serif;font-size:22px;font-weight:700;margin-bottom:6px; }
.verdict-safe .verdict-title { color:#27AE60; }
.verdict-suspicious .verdict-title { color:#F1C40F; }
.verdict-impersonation .verdict-title { color:var(--red-light); }
.score-grid { display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:16px 0; }
.score-box { background:rgba(255,255,255,0.04);border-radius:10px;padding:16px;text-align:center; }
.score-value { font-family:'Rajdhani',sans-serif;font-size:26px;font-weight:700;color:#fff; }
.score-label { font-size:11px;color:var(--muted);margin-top:2px;text-transform:uppercase;letter-spacing:0.5px; }

/* Reports table */
.rtable { width:100%;border-collapse:collapse; }
.rtable th { background:rgba(255,255,255,0.04);padding:12px 16px;text-align:left;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:1px;color:var(--muted);border-bottom:1px solid var(--border); }
.rtable td { padding:14px 16px;font-size:13.5px;color:var(--text);border-bottom:1px solid rgba(255,255,255,0.04); }
.badge { display:inline-block;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.5px; }
.badge-safe,.badge-low { background:rgba(39,174,96,0.15);color:#27AE60; }
.badge-suspicious,.badge-medium { background:rgba(241,196,15,0.15);color:#F1C40F; }
.badge-impersonation,.badge-high { background:rgba(192,57,43,0.15);color:#E74C3C; }
.badge-critical { background:rgba(142,0,0,0.25);color:#FF4444; }

/* Stats */
.stats-row { display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:24px; }
.stat-card { background:var(--dark-card);border:1px solid var(--border);border-radius:12px;padding:22px; }
.stat-value { font-family:'Rajdhani',sans-serif;font-size:34px;font-weight:700;color:#fff; }
.stat-label { font-size:12px;color:var(--muted);margin-top:4px;text-transform:uppercase;letter-spacing:0.5px; }
.stat-card.danger .stat-value { color:var(--red-light); }
.stat-card.warning .stat-value { color:#F1C40F; }
.stat-card.success .stat-value { color:#27AE60; }

/* Active nav highlight */
.active-nav button { background: rgba(192,57,43,0.15) !important; color: white !important; border-left: 3px solid #C0392B !important; }
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state["page"] = "Home Dashboard"

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="logo-icon">🛡️</div>
        <span class="logo-text">Brand Shield AI</span>
    </div>
    """, unsafe_allow_html=True)

    for icon, label in [("🏠", "Home Dashboard"), ("🔍", "Threat Analysis"), ("📋", "Incident Reports"), ("📊", "Security Insights")]:
        is_active = st.session_state["page"] == label
        style = "background:rgba(192,57,43,0.18);color:white;border-left:3px solid #C0392B;" if is_active else ""
        st.markdown(f'<div style="{style}border-radius:8px;margin:2px 4px;">', unsafe_allow_html=True)
        if st.button(f"{icon}  {label}", key=f"nav_{label}", use_container_width=True):
            st.session_state["page"] = label
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style='margin:20px 8px 0;padding:12px 16px;background:rgba(192,57,43,0.08);border-radius:8px;border:1px solid rgba(192,57,43,0.2);'>
        <div style='font-size:11px;color:#7A8A9A;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;'>Models Active</div>
        <div style='font-size:13px;color:#A8B8C8;margin-bottom:4px;'>✅ Google Gemini Flash</div>
        <div style='font-size:13px;color:#A8B8C8;'>✅ HuggingFace BART</div>
    </div>
    """, unsafe_allow_html=True)

# ── Pages ─────────────────────────────────────────────────────────────────────
page = st.session_state["page"]

# ── HOME ──────────────────────────────────────────────────────────────────────
if page == "Home Dashboard":
    st.markdown("""
    <div class="page-header">
        <div class="page-title">🛡️ Brand Shield AI</div>
        <div style="font-size:13px;color:#7A8A9A;">Multi-Model Detection Platform</div>
    </div>
    <div class="hero-card">
        <div class="hero-title">Detect <span>Brand Impersonation</span><br>with Confidence</div>
        <p class="hero-desc"><strong style="color:#E8EDF2;">Brand Shield AI</strong> is a professional multi-model detection platform designed to identify phishing emails, fake URLs, logo misuse, and brand impersonation attempts in real time using advanced AI models.</p>
    </div>
    <div class="feature-grid">
        <div class="feature-card"><div class="feature-icon">🌐</div><div class="feature-title">AI-Powered</div><div class="feature-desc"><strong>Gemini</strong> + HuggingFace Models in ensemble for maximum accuracy.</div></div>
        <div class="feature-card"><div class="feature-icon">⚡</div><div class="feature-title">Real-Time</div><div class="feature-desc">Fast threat screening with instant verdict and confidence scoring.</div></div>
        <div class="feature-card"><div class="feature-icon">🖥️</div><div class="feature-title">Multi-Modal</div><div class="feature-desc">Text, URL, and Image Detection with full explainability reports.</div></div>
    </div>
    <div class="info-grid">
        <div class="info-card">
            <div class="info-card-title">🎯 What can it detect?</div>
            <ul class="info-list">
                <li><span class="bullet">●</span><div><strong>Phishing emails</strong> impersonating trusted brands, banks, and services</div></li>
                <li><span class="bullet">●</span><div><strong>Malicious URLs</strong> using typosquatting, spoofing, and homograph attacks</div></li>
                <li><span class="bullet">●</span><div><strong>Fake or manipulated logos</strong> and unauthorized brand imagery</div></li>
                <li><span class="bullet">●</span><div><strong>Suspicious multi-modal content</strong> designed to deceive customers</div></li>
            </ul>
        </div>
        <div class="info-card">
            <div class="info-card-title">🚀 Quick Start</div>
            <ol class="step-list">
                <li><div class="step-num">1</div><div>Open the <strong style="color:white">Threat Analysis</strong> page</div></li>
                <li><div class="step-num">2</div><div>Submit email, URL or image content</div></li>
                <li><div class="step-num">3</div><div>Review flagged risk indicators</div></li>
                <li><div class="step-num">4</div><div>Track all findings in Reports and Dashboard</div></li>
            </ol>
        </div>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns([1.2, 1.2])
    with col1:
        if st.button("🔍  Start Analysis", use_container_width=True):
            st.session_state["page"] = "Threat Analysis"; st.rerun()
    with col2:
        if st.button("📋  View Reports", use_container_width=True):
            st.session_state["page"] = "Incident Reports"; st.rerun()

# ── THREAT ANALYSIS ───────────────────────────────────────────────────────────
elif page == "Threat Analysis":
    st.markdown("""
    <div class="page-header">
        <div class="page-title">🔍 Threat Analysis</div>
        <div style="font-size:13px;color:#7A8A9A;">Submit content for brand impersonation detection</div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div style="background:#161D27;border:1px solid #1E2A38;border-radius:14px;padding:28px 32px;max-width:820px;">', unsafe_allow_html=True)
        input_type = st.selectbox("Input Type", ["text", "url", "image"],
            format_func=lambda x: {"text":"📝  Text / Email Content","url":"🔗  URL / Domain","image":"🖼️  Image Description"}[x])
        placeholders = {"text":"Paste suspicious email text here...","url":"https://paypa1-secure.com/verify","image":"Describe the logo or image..."}
        input_content = st.text_area("Content to Analyze", height=160, placeholder=placeholders.get(input_type,""))
        target_brand = st.text_input("Target Brand (optional)", placeholder="e.g. PayPal, Google, Apple")
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🚀  Run Detection"):
        if not input_content.strip():
            st.error("Please provide content to analyze.")
        else:
            with st.spinner("Running multi-model detection..."):
                try:
                    resp = requests.post(f"{BACKEND_URL}/api/detect/", json={
                        "input_type": input_type, "input_content": input_content, "target_brand": target_brand,
                    }, timeout=60)
                    data = resp.json()
                    if data.get("success"):
                        r = data["data"]
                        verdict = r.get("verdict","safe")
                        icons = {"safe":"✅","suspicious":"⚠️","impersonation":"🚨"}
                        labels = {"safe":"SAFE","suspicious":"SUSPICIOUS","impersonation":"IMPERSONATION DETECTED"}
                        c, g, h = r.get("confidence",0), r.get("gemini_score",0), r.get("hf_score",0)
                        st.markdown(f"""
                        <div class="verdict-{verdict}" style="margin-top:20px;">
                            <div class="verdict-title">{icons.get(verdict,'')} {labels.get(verdict,verdict.upper())}</div>
                            <div style="font-size:13px;color:#A8B8C8;margin-top:4px;">{r.get('explanation','')}</div>
                        </div>
                        <div class="score-grid">
                            <div class="score-box"><div class="score-value">{c:.0%}</div><div class="score-label">Ensemble Score</div></div>
                            <div class="score-box"><div class="score-value">{g:.0%}</div><div class="score-label">Gemini Score</div></div>
                            <div class="score-box"><div class="score-value">{h:.0%}</div><div class="score-label">HuggingFace Score</div></div>
                        </div>
                        """, unsafe_allow_html=True)
                        if r.get("red_flags"):
                            flags = "".join([f"<li><span class='bullet'>●</span> {f}</li>" for f in r["red_flags"]])
                            st.markdown(f'<div style="background:#161D27;border:1px solid #1E2A38;border-radius:10px;padding:20px 24px;margin-top:12px;"><div style="font-family:Rajdhani,sans-serif;font-size:15px;font-weight:700;color:#fff;margin-bottom:12px;">🚩 Red Flags</div><ul class="info-list">{flags}</ul></div>', unsafe_allow_html=True)
                    else:
                        st.error(f"API Error: {data.get('errors')}")
                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to backend. Make sure Django is running on port 8000.")
                except Exception as e:
                    st.error(f"Error: {e}")

# ── INCIDENT REPORTS ──────────────────────────────────────────────────────────
elif page == "Incident Reports":
    st.markdown("""
    <div class="page-header">
        <div class="page-title">📋 Incident Reports</div>
        <div style="font-size:13px;color:#7A8A9A;">All detection results and threat records</div>
    </div>
    """, unsafe_allow_html=True)
    try:
        reports = requests.get(f"{BACKEND_URL}/api/reports/", timeout=10).json().get("data", [])
        if not reports:
            st.markdown('<div style="background:#161D27;border:1px solid #1E2A38;border-radius:12px;padding:48px;text-align:center;color:#7A8A9A;"><div style="font-size:36px;margin-bottom:12px;">📭</div><div style="font-size:15px;color:#A0B0C0;">No reports yet — run a detection first!</div></div>', unsafe_allow_html=True)
        else:
            rows = "".join([f'<tr><td>#{r.get("id","")}</td><td>{r.get("detection_input_type","").upper()}</td><td><span class="badge badge-{r.get("detection_verdict","safe")}">{r.get("detection_verdict","").upper()}</span></td><td><span class="badge badge-{r.get("risk_level","low")}">{r.get("risk_level","").upper()}</span></td><td style="color:#7A8A9A;font-size:12px;">{str(r.get("created_at",""))[:16].replace("T"," ")}</td></tr>' for r in reports])
            st.markdown(f'<div style="background:#161D27;border:1px solid #1E2A38;border-radius:12px;overflow:hidden;"><table class="rtable"><thead><tr><th>ID</th><th>Type</th><th>Verdict</th><th>Risk</th><th>Date</th></tr></thead><tbody>{rows}</tbody></table></div>', unsafe_allow_html=True)
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to backend. Make sure Django is running on port 8000.")

# ── SECURITY INSIGHTS ─────────────────────────────────────────────────────────
elif page == "Security Insights":
    st.markdown("""
    <div class="page-header">
        <div class="page-title">📊 Security Insights</div>
        <div style="font-size:13px;color:#7A8A9A;">Detection statistics and threat trends</div>
    </div>
    """, unsafe_allow_html=True)
    try:
        reports = requests.get(f"{BACKEND_URL}/api/reports/", timeout=10).json().get("data", [])
        total = len(reports)
        imp = sum(1 for r in reports if r.get("detection_verdict") == "impersonation")
        sus = sum(1 for r in reports if r.get("detection_verdict") == "suspicious")
        safe = sum(1 for r in reports if r.get("detection_verdict") == "safe")
        st.markdown(f"""
        <div class="stats-row">
            <div class="stat-card"><div class="stat-value">{total}</div><div class="stat-label">Total Scans</div></div>
            <div class="stat-card danger"><div class="stat-value">{imp}</div><div class="stat-label">Impersonations</div></div>
            <div class="stat-card warning"><div class="stat-value">{sus}</div><div class="stat-label">Suspicious</div></div>
            <div class="stat-card success"><div class="stat-value">{safe}</div><div class="stat-label">Safe</div></div>
        </div>
        """, unsafe_allow_html=True)
        if total > 0:
            import plotly.graph_objects as go
            col1, col2 = st.columns(2)
            with col1:
                fig = go.Figure(data=[go.Pie(labels=["Safe","Suspicious","Impersonation"],values=[safe,sus,imp],hole=0.5,marker=dict(colors=["#27AE60","#F1C40F","#C0392B"]))])
                fig.update_layout(title=dict(text="Verdict Distribution",font=dict(color="#E8EDF2",size=15)),paper_bgcolor="#161D27",plot_bgcolor="#161D27",font=dict(color="#A0B0C0"),legend=dict(font=dict(color="#A0B0C0")),margin=dict(t=40,b=20,l=20,r=20))
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                rc = {}
                for r in reports: rc[r.get("risk_level","low")] = rc.get(r.get("risk_level","low"),0)+1
                colors = {"low":"#27AE60","medium":"#F1C40F","high":"#E74C3C","critical":"#FF0000"}
                fig2 = go.Figure(data=[go.Bar(x=list(rc.keys()),y=list(rc.values()),marker_color=[colors.get(k,"#7A8A9A") for k in rc])])
                fig2.update_layout(title=dict(text="Risk Level Breakdown",font=dict(color="#E8EDF2",size=15)),paper_bgcolor="#161D27",plot_bgcolor="#161D27",font=dict(color="#A0B0C0"),margin=dict(t=40,b=20,l=20,r=20),xaxis=dict(gridcolor="#1E2A38"),yaxis=dict(gridcolor="#1E2A38"))
                st.plotly_chart(fig2, use_container_width=True)
        else:
            st.markdown('<div style="background:#161D27;border:1px solid #1E2A38;border-radius:12px;padding:48px;text-align:center;color:#7A8A9A;"><div style="font-size:36px;margin-bottom:12px;">📊</div><div>No data yet — run some detections first!</div></div>', unsafe_allow_html=True)
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to backend. Make sure Django is running on port 8000.")