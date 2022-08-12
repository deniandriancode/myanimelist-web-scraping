from bs4 import BeautifulSoup as bsp
from datetime import datetime
import requests
import utils

today = datetime.now().strftime("%b-%d-%Y_%H:%M")

def get_rec(page_num):
    url = "https://myanimelist.net/recommendations.php?s=recentrecs&t=anime"
    mode = "w"
    if page_num > 1:
        url += "&show={}".format((page_num - 1) * 100)
        mode = "a"

    response = None
    while response is None:
        try:
            response = requests.get(url)
        except OSError:
            continue
    
    page = response.content

    soup = bsp(page, 'html.parser')

    try:
        rec_content = soup.find(id="content")
        rec_pair = rec_content.find_all(class_="spaceit borderClass")
    except:
        exit()
    title_columns = ["If You Like", "Then You Might Like", "Description"]
    rec_if_like_arr = []
    rec_might_like_arr = []
    description_rec_arr = []

    for i in range(len(rec_pair)):
        rec_pair_table = rec_pair[i].find("table")
        rec_if_like_arr.append(rec_pair_table.find_all("td")[0].find_all("a")[1].text)
        rec_might_like_arr.append(rec_pair_table.find_all("td")[1].find_all("a")[1].text)
        description_rec_arr.append(rec_pair_table.parent.find(class_="recommendations-user-recs-text").text.strip().replace("\r", " ").replace("\n", " "))


    with open("recommendation/anime/myanimelist-anime-recommendation-{}.csv".format(today), mode) as fp:
        if mode == "w":
            counter = 0
            for title in title_columns:
                if counter < len(title_columns) - 1:
                    fp.write(title + "|")
                    counter += 1
                else:
                    fp.write(title + "\n")
        for i in range(len(rec_pair)):
            fp.write(rec_if_like_arr[i] + "|")
            fp.write(rec_might_like_arr[i] + "|")
            fp.write(description_rec_arr[i] + "\n")
        fp.close()

def start():
    utils.clear_console()
    for i in range(1,201):
        get_rec(i)
        utils.clear_console()
        print("{} anime recommendations recorded...".format(i * 100))
        i += 1
