from bs4 import BeautifulSoup as bsp
from datetime import date
import bs4
import requests
import os

def clearConsole():
    command = "clear"
    if os.name in ("nt", "dos"):
        command = "cls"
    os.system(command)

def write_to_file(page, rank_list, rank_number, manga_title, manga_score, manga_chaps, manga_published, title_columns):
    mode = "w"
    if page > 1:
        mode = "a"
    counter = 0
    today = date.today().strftime("%b-%d-%Y")
    with open("manga/myanimelist-top-manga-{}.csv".format(today), mode) as fp:
        if page == 1:
            for t in title_columns:
                if counter == len(title_columns) - 1:
                    fp.write(t.text)
                else:
                    fp.write(t.text + ',')
                counter += 1
            fp.write('\n')
        for i in range(len(rank_list)):
            fp.write(rank_number[i] + ',')
            fp.write(manga_title[i] + ',')
            fp.write(manga_score[i] + ',' )
            fp.write(manga_chaps[i] + ',')
            fp.write(manga_published[i] + '\n')
        fp.close()

def get_top_manga_list(page_count):
    url = "https://myanimelist.net/topmanga.php"
    if page_count > 1:
        url = url + "?limit={}".format(50 * (page_count - 1))

    r = requests.get(url)
    page = r.content

    soup = bsp(page, 'html.parser')
    try:
        table = soup.find("table")
        title_columns = table.find(class_="table-header").contents[:-2]
        title_columns.append(bs4.element.NavigableString("Chapters/Volumes"))
        title_columns.append(bs4.element.NavigableString("Published"))
    except AttributeError:
        exit()

    rank_list = table.find_all(class_="ranking-list")
    rank_number = []
    manga_title = []
    manga_score = []
    manga_chaps = []
    manga_published = []
    for r in rank_list:
        rank_number.append(r.find(class_="rank ac").text.strip())
        manga_title.append(r.find(class_="detail").find("h3").text.strip())
        manga_score.append(r.find(class_="score").text.strip())
        manga_chaps.append(r.find(class_="detail").find(class_="information").contents[0].text.strip())
        manga_published.append(r.find(class_="detail").find(class_="information").contents[2].text.strip())

    write_to_file(page_count, rank_list, rank_number, manga_title, manga_score, manga_chaps, manga_published, title_columns)

if __name__ == '__main__':
    clearConsole()
    index = 1
    while True:
        get_top_manga_list(index)
        clearConsole()
        print(f"{(index) * 50} mangas recorded...")
        index += 1
