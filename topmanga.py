from bs4 import BeautifulSoup as bsp
from datetime import date
import bs4
import requests
import utils
import logging
import csv

logging.basicConfig(filename='myanimelist.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

logging.debug('Get current date')
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
        logging.debug('Create table header')
        table = soup.find("table")
        title_columns = []
        for item in table.find(class_="table-header").contents[:-2]:
            title_columns.append(item.text)
        title_columns.append(bs4.element.NavigableString("Chapters/Volumes"))
        title_columns.append(bs4.element.NavigableString("Published"))
        title_columns.append(bs4.element.NavigableString("Link"))
    except AttributeError:
        logging.info('No more page, exit the program')
        exit()

    rank_list = table.find_all(class_="ranking-list")
    manga_list = []
    for r in rank_list:
        logging.debug('Start add the manga to the list')
        rank_number = r.find(class_="rank ac").text.strip()
        manga_title = r.find(class_="detail").find("h3").text.strip()
        manga_score = r.find(class_="score").text.strip()
        manga_chaps = r.find(class_="detail").find(class_="information").contents[0].text.strip()
        manga_published = r.find(class_="detail").find(class_="information").contents[2].text.strip()
        manga_link = r.find(class_="detail").find(class_="manga_h3").find("a").get("href")
        manga_list.append([rank_number, manga_title, manga_score, manga_chaps, manga_published, manga_link])
        logging.debug('End add the manga to the list')

    mode = "w"
    if page_count > 1:
        mode = "a"
    counter = 0
    with open("rank/manga/myanimelist-top-manga-{}.csv".format(today), mode) as fp:
        writer = csv.writer(fp, delimiter='|')
        if page_count == 1:
            logging.debug('Start write the table header')
            writer.writerow(title_columns)
            logging.debug('End write the table header')
        logging.debug('Start write the rank list')
        writer.writerows(manga_list)
        logging.debug('End write the rank list')



def start():
    utils.clear_console()
    index = 1
    while True:
        get_top_manga_list(index)
        utils.clear_console()
        print(f"{(index) * 50} mangas recorded...")
        index += 1

logging.debug('Start of main function')
if __name__ == '__main__':
    start()
logging.debug('End of main function')
