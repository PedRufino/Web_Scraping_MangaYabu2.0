from bs4 import BeautifulSoup
from io import BytesIO
from folder import save_path
from time import sleep
from tqdm import tqdm
from PIL import Image
import requests
import json
import re
import os

headers = {
    "authority": "mangayabu.top",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh-CN;q=0.5,zh;q=0.4",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
}

try:
    with open('config.json', 'r') as folder:
        config = json.load(folder)
        path = config['path']
except (FileNotFoundError, json.decoder.JSONDecodeError):
    save_path()

class FindManga:
    def __init__(self):
        self.response = requests.get(
            "https://mangayabu.top/api/show3.php", headers=headers
        )
        soup = BeautifulSoup(self.response.text, "html.parser").text
        self.json_manga = json.loads(soup)
        pass

    # pega o nome que foi inserido na variavel e tranforma em slug:
    # Ex: 'Solo Leveling' -> 'solo-leveling'
    def cria_slug(self, slug_manga):
        slug_manga = slug_manga.strip()
        slug_manga = re.sub(r"\s+", "-", slug_manga)
        slug_manga = re.sub(r"'", "-", slug_manga)
        slug_manga = re.sub(r"[^\w\s-]", "", slug_manga)
        self.slug_manga = slug_manga.lower()
        pass

    def title_path(self, title_folder):
        title_folder = title_folder.strip()
        title_folder = re.sub(r"[^\w\s-]", "", title_folder)
        self.title_folder = title_folder
        pass

    # Busca na api e traz o manga digitado
    def search_manga_title(self):
        mg_title = None
        for item_list in self.json_manga:
            if self.slug_manga == item_list["slug"]:
                mg_title = item_list["slug"]
                self.title_path(title_folder=item_list["title"])
        if mg_title == None:
            return "Mangá não encontrado!!"
        else:
            return mg_title

    # Inicia uma pesquisa na API e retorna uma lista com 10 mangás que foram encontrados de acordo com o que foi digitado
    # Ex: 'Solo' -> ['Solo Leveling', 'Solo Leveling (Novel)', 'Solo Necromancer', ...]
    def find_manga(self, title):
        title = title.lower().strip()
        results = []
        for manga in self.json_manga:
            if title in manga["title"].lower():
                results.append(manga["title"])
        if not results:
            return "Mangá não encontrado!!"
        elif len(results) > 10:
            return "Muitos resultados, seja mais específicos"
        # Cria uma tabela com os mangás encontrados
        while True:
            print("-" * 50)
            for i, result in enumerate(results, start=1):
                print(f" {i} - {result}")
            print("-" * 50)
            choice = input("Digite o número do manga escolhido:\n>>> ")
            if choice.isdigit() and 0 < int(choice) <= len(results):
                slug_manga = results[int(choice) - 1]
                self.cria_slug(slug_manga)
                break
            else:
                os.system("cls")
                print("Escolha um número válido")
                sleep(1)
                os.system("cls")


class ChapterAndPage:
    def __init__(self):
        self.mg = FindManga()

    def find_and_create_slug(self, **kwargs):
        if kwargs.get("title"):
            self.mg.find_manga(kwargs["title"])
        elif kwargs.get("slug_manga"):
            self.mg.cria_slug(kwargs["slug_manga"])
        self.response = requests.get(
            f"https://mangayabu.top/manga/{self.mg.search_manga_title()}/",
            headers=headers,
        )
        self.soup = BeautifulSoup(self.response.text, "html.parser")

    def choice_chapter(self, **kwargs):
        # Traz json de capitulos
        manga_info = self.soup.find("script", {"id": "manga-info"}).text
        self.json_chapter = json.loads(manga_info)["allposts"]
        self.link_chapter = []
        os.makedirs(f"{path}/{self.mg.title_folder}", exist_ok=True)
        # cria uma lista com os links dos capitulos desejados
        if len(kwargs) == 2:
            for chapter in self.json_chapter[::-1]:
                for num_cap in range(int(kwargs["start"]), int(kwargs["end"]) + 1):
                    if chapter["num"] == str(num_cap).zfill(2):
                        self.link_chapter.append(
                            {
                                "cap": chapter["num"],
                                "link": chapter["chapters"][0]["id"],
                            }
                        )
        # Traz apenas 1 link do capítulo desejado
        elif len(kwargs) == 1:
            for chapter in self.json_chapter[::-1]:
                if chapter["num"] == str(kwargs["num"]).zfill(2):
                    self.link_chapter.append(
                        {"cap": chapter["num"], "link": chapter["chapters"][0]["id"]}
                    )
        # Tratativa de erro caso tenha mais de 2 itens no kwargs
        else:
            os.system("cls")
            print("Foi encontrado mais de 2 itens na lista")
            print("")
            print("Para baixar mais de um capítulo, siga o exemplo do início")
            sleep(1)
            os.system("cls")
        return "Busca Realizada com Sucesso"

    # Faz o download das paginas e salva no PDF
    def image_downloader(self):
        for link in tqdm(self.link_chapter):
            response = requests.get(link["link"], headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            list_link = soup.find("div", {"class": "section table-of-contents"})("img")
            x = 0
            for link_page in list_link:
                lk_pg = requests.get(link_page["src"], headers=headers)
                file_image = Image.open(BytesIO(lk_pg.content))
                os.makedirs(f"{path}/{self.mg.title_folder}/capitulo-{link['cap']}", exist_ok=True)
                file_image.convert("RGB").save(f'{path}/{self.mg.title_folder}/capitulo-{link["cap"]}/Pagina-{x:02d}.jpg')
                x += 1
            # imagens[0].save(
            #     f"{path}/{self.mg.title_folder}/Capítulo-{link['cap']}.pdf",
            #     save_all=True,
            #     append_images=imagens[1:],
            # )
        pass
