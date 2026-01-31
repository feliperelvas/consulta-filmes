import requests
from bs4 import BeautifulSoup
import re

class CinemaScraper:
    def __init__(self, cinema_url):
        self.__cinema_url = cinema_url
        self.__headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/140.0.0.0 Safari/537.36"
            )
        }
        self.__lista_filmes = []

    def fetch_html(self):
        r = requests.get(self.__cinema_url, headers=self.__headers)
        r.raise_for_status()
        return r.text

    def getFilmesCinesystemIlha(self):
        html = self.fetch_html()
        soup = BeautifulSoup(html, "html.parser")

        retorno = soup.find("div", id="retorno_filmes")
        if not retorno:
            return

        filmes = retorno.find_all(
            "div",
            class_="col-md-10 m-0-auto",
            recursive=False
        )

        for filme in filmes:
            nome_tag = filme.select_one(".cinema-filme-title")
            if not nome_tag:
                continue

            nome = nome_tag.get_text(strip=True)

            texto = filme.get_text(" ", strip=True)
            duracao_match = re.search(r"(\d+)\s*min", texto)
            duracao = int(duracao_match.group(1)) if duracao_match else None

            sessoes = []

            for link in filme.find_all("a", href=True):
                horario = link.get_text(strip=True)
                url = link["href"]

                tipo = "Normal"
                tipo_tag = link.find_previous("span", class_="label-filme1")
                if tipo_tag:
                    tipo = tipo_tag.get_text(strip=True)

                sessoes.append({
                    "horario": horario,
                    "tipo": tipo,
                    "link": url
                })

            self.__lista_filmes.append({
                "nome": nome,
                "duracao_min": duracao,
                "sessoes": sessoes
            })
        
        return self.__lista_filmes

if __name__ == "__main__":
    url = "https://ilhaplaza.com.br/cinema/"
    cinema = CinemaScraper(url)
    lista = cinema.getFilmesCinesystemIlha()
    print(lista)