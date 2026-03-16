import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

def render():
    st.markdown('<div class="main-area">', unsafe_allow_html=True)
    st.markdown("""
    <div class="page-header">
        <div class="page-title"><span class="shield">📋</span> Incident Reports</div>
        <div style="font-size:13px; color:#7A8A9A;">All detection results and threat records</div>
    </div>
    """, unsafe_allow_html=True)

    try:
        resp = requests.get(f"{BACKEND_URL}/api/reports/", timeout=10)
        data = resp.json()
        reports = data.get("data", [])

        if not reports:
            st.markdown("""
            <div style="background:#161D27;border:1px solid #1E2A38;border-radius:12px;padding:48px;text-align:center;color:#7A8A9A;">
                <div style="font-size:36px;margin-bottom:12px;">📭</div>
                <div style="font-size:16px;color:#A0B0C0;margin-bottom:6px;">No reports yet</div>
                <div style="font-size:13px;">Run a detection in Threat Analysis to see results here.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            rows = ""
            for r in reports:
                v = r.get("detection_verdict", "safe")
                risk = r.get("risk_level", "low")
                created = r.get("created_at", "")[:16].replace("T", " ")
                rows += f"""
                <tr>
                    <td>#{r.get('id','')}</td>
                    <td>{r.get('detection_input_type','').upper()}</td>
                    <td><span class="badge badge-{v}">{v.upper()}</span></td>
                    <td><span class="badge badge-{risk}">{risk.upper()}</span></td>
                    <td style="color:#7A8A9A;font-size:12px;">{created}</td>
                </tr>"""

            st.markdown(f"""
            <div style="background:#161D27;border:1px solid #1E2A38;border-radius:12px;overflow:hidden;">
                <table class="report-table">
                    <thead>
                        <tr>
                            <th>ID</th><th>Type</th><th>Verdict</th><th>Risk</th><th>Date</th>
                        </tr>
                    </thead>
                    <tbody>{rows}</tbody>
                </table>
            </div>
            """, unsafe_allow_html=True)

    except requests.exceptions.ConnectionError:
        st.markdown("""<div style="background:rgba(192,57,43,0.1);border:1px solid #C0392B;border-radius:8px;padding:14px 18px;color:#E74C3C;font-size:14px;">
        ⚠️ Cannot connect to backend. Make sure Django server is running on port 8000.</div>""", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error: {e}")

    st.markdown('</div>', unsafe_allow_html=True)