from bs4 import BeautifulSoup as bsp
from datetime import date, datetime
import bs4
import utils
import requests
import logging
import csv

logging.basicConfig(filename='myanimelist.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

logging.debug('Get current date')
today = date.today().strftime("%b-%d-%Y")

def get_anime_review(page):
    mode = 'w'
    url = 'https://myanimelist.net/reviews.php?t=manga'
    if page != 1:
        url = url + '&p={}'.format(page)
        mode = 'a'

    response = None
    logging.debug('Fetching page')
    while response is None:
        try:
            response = requests.get(url)
        except OSError:
            logging.info('Page cannot be fetched, refetch')
            continue

    soup = bsp(response.content, 'html.parser')

    main_content = soup.find(id='content')
    
    review_header = ['Manga Title', 'Manga Link', 'User', 'User Link', 'Review Status', 'Additional Flag', 'Review', 'Reviewer\'s Rating']
    review_elements = main_content.find_all(class_='review-element')
    manga_review = []

    for review in review_elements:
        try:
            logging.debug('Write review to a file')
            anime_title = review.find(class_='titleblock').a.text
            anime_link = review.find(class_='titleblock').a.get('href')
            mal_user = review.find(class_='username').a.text
            mal_user_link = review.find(class_='username').a.get('href')
            review_status = review.find(class_='tags').find_all(class_='tag')[0].text
            additional_flag = utils.get_additional_flag(review)
            review_content = review.find(class_='text').text.strip().replace("\r", "").replace("\n", "")
            reviewer_rating = review.find(class_='rating').find(class_='num').text
            manga_review.append([anime_title, anime_link, mal_user, mal_user_link, review_status, additional_flag, review_content, reviewer_rating])
        except Exception:
            logging.info('Review cannot be written, continue the next review')
            continue

    with open('review/manga/manga-review-%s.csv'% today, mode) as fp:
        writer = csv.writer(fp, delimiter='|')
        if mode == 'w':
            writer.writerow(review_header)
        writer.writerows(manga_review)
            
def start():
    utils.clear_console()
    for i in range(400):
        get_anime_review(i+1)
        utils.clear_console()
        print("{} manga reviews recorded..".format(50 * (i+1)))
        
logging.debug('Main function START')
if __name__ == '__main__':
    start()
logging.debug('Main function END')
