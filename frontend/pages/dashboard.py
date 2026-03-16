import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

def render():
    st.markdown('<div class="main-area">', unsafe_allow_html=True)
    st.markdown("""
    <div class="page-header">
        <div class="page-title"><span class="shield">📊</span> Security Insights</div>
        <div style="font-size:13px; color:#7A8A9A;">Detection statistics and threat trends</div>
    </div>
    """, unsafe_allow_html=True)

    try:
        resp = requests.get(f"{BACKEND_URL}/api/reports/", timeout=10)
        reports = resp.json().get("data", [])

        total = len(reports)
        impersonations = sum(1 for r in reports if r.get("detection_verdict") == "impersonation")
        suspicious = sum(1 for r in reports if r.get("detection_verdict") == "suspicious")
        safe = sum(1 for r in reports if r.get("detection_verdict") == "safe")

        st.markdown(f"""
        <div class="stats-row">
            <div class="stat-card">
                <div class="stat-value">{total}</div>
                <div class="stat-label">Total Scans</div>
            </div>
            <div class="stat-card danger">
                <div class="stat-value">{impersonations}</div>
                <div class="stat-label">Impersonations</div>
            </div>
            <div class="stat-card warning">
                <div class="stat-value">{suspicious}</div>
                <div class="stat-label">Suspicious</div>
            </div>
            <div class="stat-card success">
                <div class="stat-value">{safe}</div>
                <div class="stat-label">Safe</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if total == 0:
            st.markdown("""
            <div style="background:#161D27;border:1px solid #1E2A38;border-radius:12px;padding:48px;text-align:center;color:#7A8A9A;">
                <div style="font-size:36px;margin-bottom:12px;">📊</div>
                <div style="font-size:15px;color:#A0B0C0;">No data yet — run some detections first!</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            try:
                import plotly.graph_objects as go
                col1, col2 = st.columns(2)
                with col1:
                    fig = go.Figure(data=[go.Pie(
                        labels=["Safe", "Suspicious", "Impersonation"],
                        values=[safe, suspicious, impersonations],
                        hole=0.5,
                        marker=dict(colors=["#27AE60", "#F1C40F", "#C0392B"]),
                    )])
                    fig.update_layout(
                        title=dict(text="Verdict Distribution", font=dict(color="#E8EDF2", size=15)),
                        paper_bgcolor="#161D27", plot_bgcolor="#161D27",
                        font=dict(color="#A0B0C0"),
                        legend=dict(font=dict(color="#A0B0C0")),
                        margin=dict(t=40, b=20, l=20, r=20),
                    )
                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    risk_counts = {}
                    for r in reports:
                        risk = r.get("risk_level", "low")
                        risk_counts[risk] = risk_counts.get(risk, 0) + 1
                    colors = {"low": "#27AE60", "medium": "#F1C40F", "high": "#E74C3C", "critical": "#FF0000"}
                    fig2 = go.Figure(data=[go.Bar(
                        x=list(risk_counts.keys()),
                        y=list(risk_counts.values()),
                        marker_color=[colors.get(k, "#7A8A9A") for k in risk_counts.keys()],
                    )])
                    fig2.update_layout(
                        title=dict(text="Risk Level Breakdown", font=dict(color="#E8EDF2", size=15)),
                        paper_bgcolor="#161D27", plot_bgcolor="#161D27",
                        font=dict(color="#A0B0C0"),
                        margin=dict(t=40, b=20, l=20, r=20),
                        xaxis=dict(gridcolor="#1E2A38"),
                        yaxis=dict(gridcolor="#1E2A38"),
                    )
                    st.plotly_chart(fig2, use_container_width=True)
            except ImportError:
                st.info("Install plotly for charts: pip install plotly")

    except requests.exceptions.ConnectionError:
        st.markdown("""<div style="background:rgba(192,57,43,0.1);border:1px solid #C0392B;border-radius:8px;padding:14px 18px;color:#E74C3C;font-size:14px;">
        ⚠️ Cannot connect to backend. Make sure Django server is running on port 8000.</div>""", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error: {e}")

    st.markdown('</div>', unsafe_allow_html=True)