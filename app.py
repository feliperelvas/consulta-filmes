import streamlit as st
from utils import retorna_opcoes_para_busca
from imdb import IMDB

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

        # st.success(f"Você escolheu: {filme_escolhido['titulo']}")
        # st.write(f"IMDb ID: `{filme_escolhido['imdb_id']}`")

        ###

        ClasseFilme = IMDB(title=filme_escolhido['imdb_id'])

        votos = ClasseFilme.getnumeroVotos()
        sinopse = ClasseFilme.getSinopse()
        rating = ClasseFilme.getRating()
        reviews = ClasseFilme.getReviews()
        
        st.markdown(f"""
        # 🎬 {filme_escolhido['titulo']} ({filme_escolhido['ano']})

        ⭐ **Rating IMDb:** {rating}  
        🗳️ **Número de votos:** {votos}

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


