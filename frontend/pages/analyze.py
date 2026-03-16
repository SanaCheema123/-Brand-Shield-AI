import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

def render():
    st.markdown('<div class="main-area">', unsafe_allow_html=True)
    st.markdown("""
    <div class="page-header">
        <div class="page-title"><span class="shield">🔍</span> Threat Analysis</div>
        <div style="font-size:13px; color:#7A8A9A;">Submit content for brand impersonation detection</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="analyze-container">', unsafe_allow_html=True)
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<div class="form-section-title">Detection Input</div>', unsafe_allow_html=True)

    input_type = st.selectbox("Input Type", ["text", "url", "image"],
        format_func=lambda x: {"text": "📝  Text / Email Content", "url": "🔗  URL / Domain", "image": "🖼️  Image Description"}[x])

    placeholders = {
        "text": "Paste suspicious email text or message content here...",
        "url": "https://paypa1-secure-login.com/verify",
        "image": "Describe the logo or image — colors, text, style, brand elements..."
    }
    input_content = st.text_area("Content to Analyze", height=160, placeholder=placeholders.get(input_type, ""))
    target_brand = st.text_input("Target Brand (optional)", placeholder="e.g. PayPal, Google, Apple, Bank Al-Habib")

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🚀  Run Detection", use_container_width=False):
        if not input_content.strip():
            st.markdown("""<div style="background:rgba(192,57,43,0.1);border:1px solid #C0392B;border-radius:8px;padding:14px 18px;color:#E74C3C;font-size:14px;">
            ⚠️ Please provide content to analyze.</div>""", unsafe_allow_html=True)
        else:
            with st.spinner("Running multi-model detection..."):
                try:
                    resp = requests.post(f"{BACKEND_URL}/api/detect/", json={
                        "input_type": input_type,
                        "input_content": input_content,
                        "target_brand": target_brand,
                    }, timeout=60)
                    data = resp.json()
                    if data.get("success"):
                        _display_result(data["data"])
                    else:
                        st.error(f"API Error: {data.get('errors')}")
                except requests.exceptions.ConnectionError:
                    st.markdown("""<div style="background:rgba(192,57,43,0.1);border:1px solid #C0392B;border-radius:8px;padding:14px 18px;color:#E74C3C;font-size:14px;">
                    ⚠️ Cannot connect to backend. Make sure Django server is running on port 8000.</div>""", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}")

    st.markdown('</div></div>', unsafe_allow_html=True)


def _display_result(result):
    verdict = result.get("verdict", "safe")
    icons = {"safe": "✅", "suspicious": "⚠️", "impersonation": "🚨"}
    labels = {"safe": "SAFE", "suspicious": "SUSPICIOUS", "impersonation": "IMPERSONATION DETECTED"}

    st.markdown(f"""
    <div class="verdict-{verdict}" style="margin-top:20px;">
        <div class="verdict-title">{icons.get(verdict,'ℹ️')} {labels.get(verdict, verdict.upper())}</div>
        <div style="font-size:13px; color:#A8B8C8; margin-top:4px;">{result.get('explanation','No explanation available.')}</div>
    </div>
    """, unsafe_allow_html=True)

    c = result.get("confidence", 0)
    g = result.get("gemini_score", 0)
    h = result.get("hf_score", 0)
    st.markdown(f"""
    <div class="score-grid" style="margin-top:16px;">
        <div class="score-box">
            <div class="score-value">{c:.0%}</div>
            <div class="score-label">Ensemble Score</div>
        </div>
        <div class="score-box">
            <div class="score-value">{g:.0%}</div>
            <div class="score-label">Gemini Score</div>
        </div>
        <div class="score-box">
            <div class="score-value">{h:.0%}</div>
            <div class="score-label">HuggingFace Score</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    red_flags = result.get("red_flags", [])
    if red_flags:
        flags_html = "".join([f"<li><span class='bullet'>●</span> {f}</li>" for f in red_flags])
        st.markdown(f"""
        <div class="form-card" style="margin-top:16px;">
            <div class="form-section-title">🚩 Red Flags Detected</div>
            <ul class="info-list">{flags_html}</ul>
        </div>
        """, unsafe_allow_html=True)

    rec = result.get("recommendation", "")
    if rec:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.03);border:1px solid #1E2A38;border-radius:10px;padding:16px 20px;margin-top:12px;">
            <div style="font-size:12px;color:#7A8A9A;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Recommendation</div>
            <div style="font-size:14px;color:#A8B8C8;">{rec}</div>
        </div>
        """, unsafe_allow_html=True)