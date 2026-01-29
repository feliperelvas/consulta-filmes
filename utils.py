import requests
import os
from dotenv import load_dotenv
import streamlit as st

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