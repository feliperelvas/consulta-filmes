# 🎬 Consulta de Filmes com IA — Streamlit App

Este projeto é uma aplicação interativa desenvolvida em **Streamlit** que combina **web scraping**, **APIs de filmes (TMDB / IMDb)** e **Inteligência Artificial (Gemini)** para ajudar o usuário a:

- Buscar informações detalhadas sobre filmes
- Ler resumos críticos gerados por IA a partir de avaliações do público
- Ver filmes em cartaz em um cinema específico no dia atual
- Receber uma **recomendação inteligente** sobre qual filme assistir hoje

---

## 🚀 Funcionalidades

### 📌 Página 1 — Busca por Filme
- Busca de filmes pelo nome (português ou inglês)
- Correspondência automática com o IMDb (`ttXXXX`)
- Exibição de:
  - Título
  - Ano
  - Gêneros
  - Sinopse (traduzida)
  - Rating IMDb
  - Número de votos
- Scraping dos comentários de usuários do IMDb
- Tradução automática dos comentários
- **Resumo crítico gerado por IA** com base nas avaliações

---

### 🎟️ Página 2 — Recomenda filme do dia
- Scraping dos filmes **em cartaz hoje** a partir do site oficial do cinema
- Exibição de:
  - Nome do filme
  - Duração
  - Sessões disponíveis
  - Tipo da sessão (2D / 3D)
  - Link direto para compra de ingresso
- Para cada filme em cartaz:
  - Busca automática no TMDB
  - Correspondência com IMDb
  - Coleta de avaliações
  - Resumo crítico gerado por IA
- **Recomendação final por IA**, indicando:
  - O melhor filme para assistir hoje
  - Justificativa
  - Alternativas relevantes

---

## 🧠 Inteligência Artificial

O projeto utiliza a **API do Google Gemini**, com a chave fornecida pelo próprio usuário via interface.

A IA é usada em dois níveis:
1. **Resumo individual de filmes**, com base em avaliações do público.
2. **Decisão final**, comparando todos os filmes em cartaz e sugerindo o melhor.

Nenhuma API Key é armazenada.

---

## 🧰 Tecnologias Utilizadas

- **Python 3.10+**
- **Streamlit**
- **BeautifulSoup**
- **TMDB API**
- **IMDB Api (imdbapi.dev)**
- **Google Gemini API**
- **Deep Translator**

---

## 🔗 URLs para conseguir os tokens das APIs utilizadas

- Token do TMDB: https://www.themoviedb.org/settings/api
- Token do Gemini: https://aistudio.google.com/api-keys

---

## 📁 Estrutura do Projeto

```
.
├── 0_Home.py                         # Página inicial (Home)
├── pages/
│   └── 1_Busca_por_filme.py          # Traz informações do filme procurado
│   └── 2_Recomenda_filme_do_dia.py   # Traz a recomendação de filme via IA para o cinema escolhido
├── utils.py                          # Funções auxiliares (APIs, IA, tradução, cache)
├── imdb.py                           # Classe de scraping do IMDb
├── cinema_scraper.py                 # Scraper de cinema (filmes em cartaz)
├── components/
│   └── sidebar.py                    # Sidebar compartilhada (configurações)
├── .env                              # Variáveis de ambiente
├── .env.example                      # Exemplo das variáveis de ambiente
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🧪 Observações Importantes

- O projeto utiliza cache inteligente (st.cache_data) para:
    - Evitar chamadas repetidas à API
    - Reduzir custo de IA
    - Melhorar performance
- O estado da aplicação é gerenciado com st.session_state, garantindo:
    - Persistência de dados entre cliques
    - UX estável
- O scraping é feito apenas para uso educacional e demonstrativo.
- Foi utilizada a API do Gemini visto que ela possui um free tier.

---

## 📈 Possíveis Evoluções

- Suporte a múltiplos cinemas.
- Filtro por gênero ou horário.
- Sistema de recomendação baseado em perfil do usuário.
- Histórico de filmes analisados.
- Suporte a mais de um modelo de IA.

---

## 👨‍💻 Autor

Desenvolvido por Felipe Relvas.