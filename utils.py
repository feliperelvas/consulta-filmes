import requests
import os
from dotenv import load_dotenv
import streamlit as st
from google import genai
from google.genai import types
from deep_translator import GoogleTranslator
from imdb import IMDB

load_dotenv()

TMDB_KEY = os.getenv("TMDB_TOKEN")

@st.cache_data(ttl=3600, show_spinner=False)
def retorna_opcoes_para_busca(titulo, max_results=5):
    search_url = "https://api.themoviedb.org/3/search/movie"
    r = requests.get(search_url, params={
        "api_key": TMDB_KEY,
        "language": "pt-BR",
        "query": titulo
    }).json()

    filmes = []

    for filme in r.get("results", [])[:max_results]:
        tmdb_id = filme["id"]

        ext_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/external_ids"
        ext = requests.get(ext_url, params={
            "api_key": TMDB_KEY
        }).json()

        filmes.append({
            "titulo": filme.get("title"),
            "titulo_original": filme.get("original_title"),
            "ano": filme.get("release_date", "")[:4],
            "tmdb_id": tmdb_id,
            "imdb_id": ext.get("imdb_id"),
            "popularidade": filme.get("popularity", 0)
        })

    return filmes

def preparar_reviews_para_ia(reviews, max_reviews=5, max_chars=600):
    textos = []

    for comentario in list(reviews.values())[:max_reviews]:
        texto = comentario.get("mensagem", "")
        texto = texto[:max_chars]
        textos.append(texto)

    return textos

def formatar_comentarios(lista_textos):
    resultado = []

    for i, texto in enumerate(lista_textos, start=1):
        resultado.append(
            f"<comentario{i:02d}> {texto} </comentario{i:02d}>"
        )

    return "\n".join(resultado)

def gerar_resumo_ia(reviews):
    api_key = st.session_state.get("api_key")
    if not api_key:
        return "API key não informada."
    
    client = genai.Client()

    prompt_sistema = """
    Você é um crítico de cinema profissional.

    Com base nos comentários de usuários abaixo, gere um resumo crítico do filme contendo:

    1. Avaliação geral do público
    2. Principais pontos positivos
    3. Principais pontos negativos
    4. Tom geral (ex: empolgante, morno, decepcionante)
    5. Um parágrafo final resumindo a experiência

    Seja imparcial, claro e conciso.
    Não cite comentários individuais.
    Escreva em português.
    Lembre-se sempre de pontuar e pular linhas para deixar bem indicado seus comentários do título do parágrafo.
    """

    lista_reviews = preparar_reviews_para_ia(reviews=reviews)

    prompt_comentarios = formatar_comentarios(lista_textos=lista_reviews)

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        config=types.GenerateContentConfig(
            system_instruction=prompt_sistema),
        contents=prompt_comentarios
    )

    return response.text

def traduz_para_portugues(texto):
    return GoogleTranslator(source='auto', target='portuguese').translate(texto)

@st.cache_data(show_spinner="Buscando informações do filme...")
def carregar_dados_filme(imdb_id):
    filme = IMDB(title=imdb_id)

    return {
        "votos": filme.getnumeroVotos(),
        "sinopse": filme.getSinopse(),
        "rating": filme.getRating(),
        "reviews": filme.getReviews(),
        "generos": filme.getGenero(),
    }

@st.cache_data(show_spinner="Traduzindo comentários...")
def traduzir_reviews(reviews):
    return {
        k: {
            "titulo": traduz_para_portugues(v.get("titulo", "Sem título")),
            "mensagem": traduz_para_portugues(v.get("mensagem", ""))
        }
        for k, v in list(reviews.items())[:5]
    }

@st.cache_data(show_spinner="Gerando análise com IA...")
def gerar_analise_cacheada(imdb_id, reviews):
    return gerar_resumo_ia(reviews)