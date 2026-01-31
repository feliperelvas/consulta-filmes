import streamlit as st
from utils import retorna_opcoes_para_busca, traduz_para_portugues, carregar_dados_filme, traduzir_reviews, gerar_analise_cacheada
from components.sidebar import render_sidebar

render_sidebar()

titulo = st.text_input("Digite o nome do filme")

if titulo:
    opcoes = retorna_opcoes_para_busca(titulo)

    if not opcoes:
        st.warning("Nenhum filme encontrado.")
    else:

        labels = ["— Selecione um filme —"] + [
            f"{f['titulo']} ({f['ano']}) — IMDb: {f['imdb_id']}"
            for f in opcoes
        ]

        escolha = st.selectbox(
            "Escolha o filme correto:",
            labels,
            index=0
        )

        if escolha != "— Selecione um filme —":
            filme_escolhido = opcoes[labels.index(escolha) - 1]

            ###

            dados_filme = carregar_dados_filme(filme_escolhido["imdb_id"])

            votos = dados_filme["votos"]
            sinopse = dados_filme["sinopse"]
            rating = dados_filme["rating"]
            reviews = dados_filme["reviews"]
            generos = dados_filme["generos"]

            reviews_traduzidos = traduzir_reviews(reviews)
            
            st.markdown(f"""
            # 🎬 {filme_escolhido['titulo']} ({filme_escolhido['ano']})

            ⭐ **Rating IMDb:** {rating}  
            🗳️ **Número de votos:** {votos}  
            🎞️ **Gêneros:** {traduz_para_portugues(", ".join([genero.get("name") for genero in generos]))}

            ---

            ### 📖 Sinopse
            {traduz_para_portugues(sinopse)}
            """)

            st.divider()

            st.markdown("## 💬 Comentários dos usuários")

            for idx, comentario in enumerate(reviews_traduzidos.values(), start=1):
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
                resumo = gerar_analise_cacheada(filme_escolhido["imdb_id"], reviews)

                with st.container(border=True):
                    st.markdown(resumo)