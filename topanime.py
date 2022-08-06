from bs4 import BeautifulSoup as bsp
from datetime import date
import bs4
import requests
import utils

today = date.today().strftime("%b-%d-%Y")

def write_to_file(page, rank_list, rank_number, anime_title, anime_score, anime_episodes, anime_airing, title_columns):
    mode = "w"
    if page > 1:
        mode = "a"
    counter = 0
    with open("anime/myanimelist-top-anime-{}.csv".format(today), mode) as fp:
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
            fp.write(anime_title[i] + ',')
            fp.write(anime_score[i] + ',' )
            fp.write(anime_episodes[i] + ',')
            fp.write(anime_airing[i] + '\n')
        fp.close()

def get_top_anime_list(page_count):
    url = "https://myanimelist.net/topanime.php"
    if page_count > 1:
        url = url + "?limit={}".format(50 * (page_count - 1))

    r = requests.get(url)
    page = r.content

    soup = bsp(page, 'html.parser')
    try:
        table = soup.find("table")
        title_columns = table.find(class_="table-header").contents[:-2]
        title_columns.append(bs4.element.NavigableString("Episodes"))
        title_columns.append(bs4.element.NavigableString("Airing"))
    except AttributeError:
        exit()

    rank_list = table.find_all(class_="ranking-list")
    rank_number = []
    anime_title = []
    anime_score = []
    anime_episodes = []
    anime_airing = []
    for r in rank_list:
        rank_number.append(r.find(class_="rank ac").text.strip())
        anime_title.append(r.find(class_="detail").find("h3").text.strip())
        anime_score.append(r.find(class_="score").text.strip())
        anime_episodes.append(r.find(class_="detail").find(class_="information").contents[0].text.strip())
        anime_airing.append(r.find(class_="detail").find(class_="information").contents[2].text.strip())

    write_to_file(page_count, rank_list, rank_number, anime_title, anime_score, anime_episodes, anime_airing, title_columns)

def start():
    utils.clearConsole()
    index = 1
    while True:
        get_top_anime_list(index)
        utils.clearConsole()
        print(f"{(index) * 50} animes recorded...")
        index += 1

if __name__ == '__main__':
    start()
