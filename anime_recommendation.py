from bs4 import BeautifulSoup as bsp
from datetime import datetime
import requests
import utils
import logging
import csv

logging.basicConfig(filename='myanimelist.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

logging.debug('Get current time')
today = datetime.now().strftime("%b-%d-%Y_%H:%M")

def get_rec(page_num):
    url = "https://myanimelist.net/recommendations.php?s=recentrecs&t=anime"
    mode = "w"
    if page_num > 1:
        url += "&show={}".format((page_num - 1) * 100)
        mode = "a"

    response = None
    logging.debug("Getting the page")
    while response is None:
        try:
            response = requests.get(url)
        except OSError:
            continue
    logging.debug("Finished getting the page")
    
    page = response.content

    soup = bsp(page, 'html.parser')

    try:
        logging.debug('Get recommendation pair')
        rec_content = soup.find(id="content")
        rec_pair = rec_content.find_all(class_="spaceit borderClass")
    except Exception:
        logging.info('Cannot find recommendation pair')
        exit()
    title_columns = ["If You Like", "Then You Might Like", "Description", "User", "User Link"]
    anime_recommendation = []

    logging.debug("Start extract data")
    for i in range(len(rec_pair)):
        rec_pair_table = rec_pair[i].find("table")
        rec_if_like = rec_pair_table.find_all("td")[0].find_all("a")[1].text
        rec_might_like = rec_pair_table.find_all("td")[1].find_all("a")[1].text
        description_rec = rec_pair_table.parent.find(class_="recommendations-user-recs-text").text.strip().replace("\r", " ").replace("\n", " ").replace("\"", "")
        mal_user = rec_pair[i].find(class_="lightLink spaceit").find_all("a")[1].text
        mal_user_link = "https://myanimelist.net" + rec_pair[i].find(class_="lightLink spaceit").find_all("a")[1].get("href")
        anime_recommendation.append([rec_if_like, rec_might_like, description_rec, mal_user, mal_user_link])

    logging.debug("End extract data")

    with open("recommendation/anime/myanimelist-anime-recommendation-{}.csv".format(today), mode) as fp:
        writer = csv.writer(fp, delimiter='|')
        if mode == 'w':
            logging.debug("Start write table header")
            writer.writerow(title_columns)
            logging.debug("End write table header")
        logging.debug("Start write anime recommendation")
        writer.writerows(anime_recommendation)
        logging.debug("End write anime recommendation")

def start():
    utils.clear_console()
    for i in range(1,201):
        get_rec(i)
        utils.clear_console()
        print("{} anime recommendations recorded...".format(i * 100))
        i += 1

logging.debug('Main function START')
if __name__ == '__main__':
    start()
logging.debug('Main function END')

# add reviewer name and link
