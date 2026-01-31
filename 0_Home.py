import streamlit as st
from components.sidebar import render_sidebar

render_sidebar()

st.set_page_config(
    page_title="🎬 Recomendador de Filmes",
    layout="wide"
)

st.title("🎥 Bem-vindo ao Recomendador de Filmes")

st.markdown("""
Use o menu à esquerda para navegar:

- **Busca por filme** → informações detalhadas + análise por IA  
- **Cinema do dia** → o que assistir hoje (em breve)

👈 Selecione uma página no menu lateral.
""")
