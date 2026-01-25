import requests
from bs4 import BeautifulSoup

class IMDB:
    def __init__(self, title):
        self.__title = title
        self.__headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
        }
        self.__data = None

    def __fetch_data(self):
        if self.__data is None:
            url = f"https://api.imdbapi.dev/titles/{self.__title}"
            response = requests.get(url, headers=self.__headers)
            response.raise_for_status()
            self.__data = response.json()

    def getReviews(self) -> dict:
        url_base = f'https://www.imdb.com/pt/title/{self.__title}/reviews/?spoilers=EXCLUDE&sort=review_volume%2Cdesc'
        resposta = requests.get(url_base, headers=self.__headers)
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
        return resultado

    def getRating(self) -> float:
        self.__fetch_data()
        return self.__data.get("rating", {}).get("aggregateRating")

    def getNome(self) -> float:
        self.__fetch_data()
        return self.__data.get("primaryTitle", {})

    def getAno(self) -> float:
        self.__fetch_data()
        return self.__data.get("startYear", {})
    
    def getSinopse(self) -> float:
        self.__fetch_data()
        return self.__data.get("plot", {})

    def getnumeroVotos(self) -> float:
        self.__fetch_data()
        return self.__data.get("rating", {}).get("voteCount")


if __name__ == "__main__":
    titulo = "tt27543632"
    empregada = IMDB(title=titulo)
    ano = empregada.getAno()
    print(ano)
    votos = empregada.getnumeroVotos()
    print(votos)
    comentarios = empregada.getReviews()
    print(comentarios)