from bs4 import BeautifulSoup as bsp
from datetime import date
import requests
import csv

def get_anime_link(page_count):
        url = "https://myanimelist.net/topanime.php"
        if page_count > 1:
                url = url + "?limit={}".format(50 * (page_count - 1))

        response = None
        while response is None:
                try:
                        response = requests.get(url)
                except OSError:
                        continue
                        
        page = response.content

        soup = bsp(page, 'html.parser')
        try:
                table = soup.find("table")
        except AttributeError:
                return

        rank_list = table.find_all(class_="ranking-list")
        link_list = []
        for r in rank_list:
                anime_link = r.find(class_="detail").find(class_="anime_ranking_h3").find("a").get("href")
                link_list.append([anime_link])

        mode = "w"
        if page_count > 1:
                mode = "a"
        counter = 0
        with open("animelink.csv", mode, newline='') as fp:
                writer = csv.writer(fp, delimiter='|')
                writer.writerows(link_list)


def start():
        index = 1
        while True:
                get_anime_link(index)
                print(f"{(index) * 50} anime links recorded...")
                index += 1


if __name__ == "__main__":
        start()
