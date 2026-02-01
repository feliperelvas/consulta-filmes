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
- **Recomenda filme do dia** → o que assistir hoje no seu cinema de preferência

👈 Selecione uma página no menu lateral.
""")
