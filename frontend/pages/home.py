import streamlit as st

def render():
    st.markdown('<div class="main-area">', unsafe_allow_html=True)

    # Header
    st.markdown("""
    <div class="page-header">
        <div class="page-title">
            <span class="shield">🛡️</span> Brand Shield AI
        </div>
        <div style="font-size:13px; color:#7A8A9A;">Multi-Model Detection Platform</div>
    </div>
    """, unsafe_allow_html=True)

    # Hero
    st.markdown("""
    <div class="hero-card">
        <div class="hero-title">Detect <span>Brand Impersonation</span><br>with Confidence</div>
        <p class="hero-desc">
            <strong style="color:#E8EDF2;">Brand Shield AI</strong> is a professional multi-model detection platform
            designed to identify phishing emails, fake URLs, logo misuse, and brand impersonation attempts
            in real time using advanced AI models.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Feature cards
    st.markdown("""
    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-icon">🌐</div>
            <div class="feature-title">AI-Powered</div>
            <div class="feature-desc"><strong>Gemini</strong> + HuggingFace Models running in ensemble for maximum accuracy.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Real-Time</div>
            <div class="feature-desc">Fast threat screening with instant verdict and confidence scoring.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🖥️</div>
            <div class="feature-title">Multi-Modal</div>
            <div class="feature-desc">Text, URL, and Image Detection with explainability reports.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Info grid
    st.markdown("""
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
            <div class="btn-row">
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🔍  Start Analysis", use_container_width=True):
            st.session_state["page"] = "Threat Analysis"
            st.rerun()
    with col2:
        if st.button("📋  View Reports", use_container_width=True):
            st.session_state["page"] = "Incident Reports"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)