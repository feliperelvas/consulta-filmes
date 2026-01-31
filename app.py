import streamlit as st
from utils import retorna_opcoes_para_busca, gerar_resumo_ia
from imdb import IMDB

with st.sidebar:
    st.markdown("## 🔐 Configurações")
    api_key = st.text_input(
        "Informe sua API Key do Gemini",
        type="password",
        help="Sua chave não será armazenada"
    )

if api_key:
    st.session_state["api_key"] = api_key

titulo = st.text_input("Digite o nome do filme")

if titulo:
    opcoes = retorna_opcoes_para_busca(titulo)

    if not opcoes:
        st.warning("Nenhum filme encontrado.")
    else:
        labels = [
            f"{f['titulo']} ({f['ano']}) — IMDb: {f['imdb_id']}"
            for f in opcoes
        ]

        escolha = st.selectbox("Escolha o filme correto:", labels)

        filme_escolhido = opcoes[labels.index(escolha)]

        ###

        ClasseFilme = IMDB(title=filme_escolhido['imdb_id'])

        votos = ClasseFilme.getnumeroVotos()
        sinopse = ClasseFilme.getSinopse()
        rating = ClasseFilme.getRating()
        reviews = ClasseFilme.getReviews()
        generos = ClasseFilme.getGenero()
        
        st.markdown(f"""
        # 🎬 {filme_escolhido['titulo']} ({filme_escolhido['ano']})

        ⭐ **Rating IMDb:** {rating}  
        🗳️ **Número de votos:** {votos}  
        🎞️ **Gêneros:** {", ".join([genero.get("name") for genero in generos])}

        ---

        ### 📖 Sinopse
        {sinopse}

        ---
        """)

        st.markdown("## 💬 Comentários dos usuários")

        for idx, comentario in enumerate(reviews.values(), start=1):
            titulo = comentario.get("titulo", "Sem título")
            mensagem = comentario.get("mensagem", "")

            with st.expander(f"📝 {idx:02d}. {titulo}"):
                st.markdown(mensagem)
            
            if idx == 5: break

        st.divider()

        with st.container(border=True):
            st.subheader("Análise por Inteligência Artificial")
            st.caption(
                "A IA analisa as avaliações do público e gera um resumo crítico "
                "destacando padrões, pontos positivos e negativos."
            )

            # Espaço visual
            st.write("")

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                gerar_analise = st.button(
                    "Gerar análise",
                    use_container_width=True,
                    disabled=not st.session_state.get("api_key"),
                    help="Informe sua API Key na barra lateral para ativar esta funcionalidade."
                    if not st.session_state.get("api_key")
                    else "Clique para gerar a análise com IA"
                )

        if gerar_analise:
            with st.spinner("Analisando avaliações com IA..."):
                resumo = gerar_resumo_ia(reviews)

            with st.container(border=True):
                st.markdown(resumo)