from bs4 import BeautifulSoup as bsp
from datetime import date
import bs4
import requests
import utils
import logging

logging.basicConfig(filename='myanimelist.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

logging.debug('Get current date')
today = date.today().strftime("%b-%d-%Y")

def get_top_anime_list(page_count):
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
        logging.debug('Create table header')
        table = soup.find("table")
        title_columns = table.find(class_="table-header").contents[:-2]
        title_columns.append(bs4.element.NavigableString("Episodes"))
        title_columns.append(bs4.element.NavigableString("Airing"))
        title_columns.append(bs4.element.NavigableString("Link"))
    except AttributeError:
        logging.info('No more page, exit the program')
        exit()

    rank_list = table.find_all(class_="ranking-list")
    anime_list = []
    for r in rank_list:
        logging.debug('Start add the anime to the list')
        rank_number = r.find(class_="rank ac").text.strip()
        anime_title = r.find(class_="detail").find("h3").text.strip()
        anime_score = r.find(class_="score").text.strip()
        anime_episodes = r.find(class_="detail").find(class_="information").contents[0].text.strip()
        anime_airing = r.find(class_="detail").find(class_="information").contents[2].text.strip()
        anime_link = r.find(class_="detail").find(class_="anime_ranking_h3").find("a").get("href")
        anime_list.append("{},{},{},{},{},{}\n".format(rank_number, anime_title, anime_score, anime_episodes, anime_airing, anime_link))
        logging.debug('End add the anime to the list')

    mode = "w"
    if page_count > 1:
        mode = "a"
    counter = 0
    with open("anime/myanimelist-top-anime-{}.csv".format(today), mode) as fp:
        if page_count == 1:
            for t in title_columns:
                logging.debug('Start write the table header')
                if counter == len(title_columns) - 1:
                    fp.write(t.text)
                else:
                    fp.write(t.text + ',')
                counter += 1
                logging.debug('End write the table header')
            fp.write('\n')
        for i in range(len(rank_list)):
            logging.debug('Start write the rank list')
            fp.write(anime_list[i])
            logging.debug('End write the rank list')
        fp.close()

logging.debug('Start of main function')
def start():
    utils.clear_console()
    index = 1
    while True:
        get_top_anime_list(index)
        utils.clear_console()
        print(f"{(index) * 50} animes recorded...")
        index += 1

logging.debug('End of main function')

