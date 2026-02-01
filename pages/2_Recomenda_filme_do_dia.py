import streamlit as st
from cinema_scraper import CinemaScraper

from utils import gerar_resumo_filme_em_cartaz, gerar_recomendacao_final

from components.sidebar import render_sidebar

# -------------------------
# CONSTANTES
# -------------------------
URL_ILHAPLAZA = "https://ilhaplaza.com.br/cinema/"

# -------------------------
# Configuração da página
# -------------------------
st.set_page_config(
    page_title="🎟️ Cinema do Dia",
    layout="wide"
)

render_sidebar()

if "filmes_em_cartaz" not in st.session_state:
    st.session_state["filmes_em_cartaz"] = None

if "resumos_filmes" not in st.session_state:
    st.session_state["resumos_filmes"] = None

if "recomendacao_final" not in st.session_state:
    st.session_state["recomendacao_final"] = None

if "gerar_analise" not in st.session_state:
    st.session_state["gerar_analise"] = False

# -------------------------
# Cabeçalho
# -------------------------
st.title("🎟️ Cinema do Dia")
st.caption(
    "Veja os filmes em cartaz hoje e descubra qual a IA recomenda assistir."
)


# -------------------------
# Seleção do cinema
# -------------------------
ilha_plaza = CinemaScraper(cinema_url=URL_ILHAPLAZA)
with st.container(border=True):
    st.subheader("🎬 Cinema")

    cinema = st.selectbox(
        "Escolha o cinema",
        [
            "Cinemark Ilha Plaza",
            # depois você adiciona outros
        ]
    )

    buscar_filmes = st.button(
        "📽️ Ver filmes em cartaz hoje",
        use_container_width=True
    )


# -------------------------
# Scraping dos filmes
# -------------------------
if buscar_filmes:

    with st.spinner("Buscando filmes em cartaz..."):
        filmes_em_cartaz = ilha_plaza.getFilmesCinesystemIlha()

    if not filmes_em_cartaz:
        st.warning("Nenhum filme encontrado para hoje.")
        st.stop()
    
    st.session_state["filmes_em_cartaz"] = filmes_em_cartaz

# -------------------------
# Carrega filmes em cartaz
# -------------------------
if st.session_state.get("filmes_em_cartaz"):

    st.subheader("📽️ Filmes em cartaz hoje")

    for filme in st.session_state["filmes_em_cartaz"]:
        with st.expander(f"🎬 {filme['nome']} ({filme['duracao_min']} min)"):
            for sessao in filme["sessoes"]:
                tipo = "🌐 3D" if sessao["tipo"] == "3D" else "🎞️ 2D"

                col1, col2, col3 = st.columns([1, 1, 2])
                col1.write(f"🕒 {sessao['horario']}")
                col2.write(f"🎥 {tipo}")
                col3.markdown(f"[🎟️ Comprar ingresso]({sessao['link']})")


# -------------------------
# IA — botão explícito
# -------------------------
if st.session_state.get("filmes_em_cartaz"):
    st.divider()

    with st.container(border=True):
        st.subheader("🤖 Recomendação por Inteligência Artificial")
        st.caption(
            "A IA analisa avaliações do público para todos os filmes "
            "em cartaz hoje e indica a melhor escolha."
        )

        st.session_state["gerar_analise"] = st.button(
            "🤖 Gerar recomendação do dia",
            use_container_width=True,
            disabled=not st.session_state.get("api_key") or st.session_state["gerar_analise"],
            help="Informe sua API Key na barra lateral para ativar esta funcionalidade."
            if not st.session_state.get("api_key")
            else None
        )

# -------------------------
# Pipeline completo
# -------------------------
if st.session_state["gerar_analise"]:

    with st.spinner("Analisando filmes e gerando recomendação..."):

        resumos_filmes = []

        for filme in st.session_state["filmes_em_cartaz"]:
            resumo = gerar_resumo_filme_em_cartaz(filme)
            if resumo:
                resumos_filmes.append(resumo)

        recomendacao = gerar_recomendacao_final(resumos_filmes)

        st.session_state["resumos_filmes"] = resumos_filmes
        st.session_state["recomendacao_final"] = recomendacao
        st.session_state["gerar_analise"] = False

# -------------------------
# Mostrar resumos individuais
# -------------------------
if st.session_state.get("resumos_filmes"):
    st.subheader("📝 Resumo dos filmes em cartaz")

    for filme in st.session_state["resumos_filmes"]:
        with st.expander(f"🎬 {filme['titulo']}"):
            st.markdown(filme["resumo"])
            st.caption(
                f"Duração: {filme['duracao_min']} min | "
                f"Horários: {', '.join(filme['horarios'])}"
            )


# -------------------------
# IA FINAL — recomendação
# -------------------------
st.divider()

if st.session_state.get("recomendacao_final"):
    with st.container(border=True):
        st.markdown("## 🎯 Recomendação da IA")
        st.markdown(st.session_state["recomendacao_final"])
