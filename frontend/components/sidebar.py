import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.markdown("## 🛡️ Brand Shield AI")
        st.markdown("---")
        pages = ["🏠 Home", "🔍 Analyze", "📋 Reports", "📊 Dashboard"]
        for page in pages:
            if st.button(page, use_container_width=True):
                st.session_state["page"] = page
        st.markdown("---")
        st.markdown("**Models Active:**")
        st.success("✅ Google Gemini 1.5 Flash")
        st.success("✅ HuggingFace BART")
        st.info("🔗 [Get Gemini Key](https://aistudio.google.com/app/apikey)")
        st.info("🔗 [Get HF Token](https://huggingface.co/settings/tokens)")
