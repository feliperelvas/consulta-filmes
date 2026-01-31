import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.markdown("## 🔐 Configurações")

        api_key = st.text_input(
            "Informe sua API Key do Gemini",
            type="password",
            help="Sua chave não será armazenada"
        )

        if api_key:
            st.session_state["api_key"] = api_key

        if st.session_state.get("api_key"):
            st.success("API Key configurada")
        else:
            st.warning("API Key não configurada")
