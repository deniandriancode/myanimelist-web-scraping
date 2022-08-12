from bs4 import BeautifulSoup as bsp
from datetime import date
import bs4
import requests
import utils

today = date.today().strftime("%b-%d-%Y")

def get_top_manga_list(page_count):
    url = "https://myanimelist.net/topmanga.php"
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
        title_columns = table.find(class_="table-header").contents[:-2]
        title_columns.append(bs4.element.NavigableString("Chapters/Volumes"))
        title_columns.append(bs4.element.NavigableString("Published"))
        title_columns.append(bs4.element.NavigableString("Link"))
    except AttributeError:
        exit()

    rank_list = table.find_all(class_="ranking-list")
    manga_list = []
    for r in rank_list:
        rank_number = r.find(class_="rank ac").text.strip()
        manga_title = r.find(class_="detail").find("h3").text.strip()
        manga_score = r.find(class_="score").text.strip()
        manga_chaps = r.find(class_="detail").find(class_="information").contents[0].text.strip()
        manga_published = r.find(class_="detail").find(class_="information").contents[2].text.strip()
        manga_link = r.find(class_="detail").find(class_="manga_h3").find("a").get("href")
        manga_list.append("{},{},{},{},{},{}\n".format(rank_number, manga_title, manga_score, manga_chaps, manga_published, manga_link))

    mode = "w"
    if page_count > 1:
        mode = "a"
    counter = 0
    with open("manga/myanimelist-top-manga-{}.csv".format(today), mode) as fp:
        if page_count == 1:
            for t in title_columns:
                if counter == len(title_columns) - 1:
                    fp.write(t.text)
                else:
                    fp.write(t.text + ',')
                counter += 1
            fp.write('\n')
        for i in range(len(rank_list)):
            fp.write(manga_list[i])
        fp.close()

def start():
    utils.clear_console()
    index = 1
    while True:
        get_top_manga_list(index)
        utils.clear_console()
        print(f"{(index) * 50} mangas recorded...")
        index += 1

