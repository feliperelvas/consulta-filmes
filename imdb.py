import requests
from bs4 import BeautifulSoup

url = 'https://www.imdb.com/pt/title/tt27543632/reviews/?spoilers=EXCLUDE&sort=review_volume%2Cdesc'
# url = 'https://www.imdb.com/pt/title/tt31050594/reviews/?spoilers=EXCLUDE&sort=review_volume%2Cdesc'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
}

resposta = requests.get(url, headers=headers)

soup = BeautifulSoup(resposta.text, "html.parser")

resultado = {}

articles = soup.find_all(
    "article",
    class_="sc-bb1e1e59-1 gtpcFu user-review-item"
)

for idx, article in enumerate(articles, start=1):

    # 🔹 TÍTULO
    titulo = None
    h3 = article.select_one(
        "div.ipc-list-card__content h3.ipc-title__text"
    )
    if h3:
        titulo = h3.get_text(strip=True)

    # 🔹 MENSAGEM (CORRETO AGORA)
    mensagem = None
    mensagem_div = article.select_one(
        "div.ipc-overflowText--listCard "
        "div.ipc-html-content-inner-div"
    )
    if mensagem_div:
        mensagem = mensagem_div.get_text(
            separator="\n",
            strip=True
        )

    resultado[f"comentario_{idx:02d}"] = {
        "titulo": titulo,
        "mensagem": mensagem
    }