from bs4 import BeautifulSoup as bsp
import requests


def get_detail():
        base_url = 'https://myanimelist.net'
        url = 'https://myanimelist.net/anime/5114/Fullmetal_Alchemist__Brotherhood'
        page = requests.get(url).content
        soup = bsp(page, 'html.parser')
        main_content = soup.find(attrs={"id": "content"})

        # popularity = main_content.find(class_="numbers popularity").find("strong").text[1:]
        # members = main_content.find(class_="numbers members").find("strong").text.replace(",", "")
        # favorite = [i for i in main_content.find_all(class_="spaceit_pad") if "Favorites:" in i.text][0].find(class_="dark_text").next_sibling.text.strip().replace(",", "")
        # season = main_content.find(class_="information season")
        # season_text = season.text
        # season_link = season.find("a").get("href")
        # studio = main_content.find(class_="information studio author")
        # studio_text = studio.text
        # studio_link = f'{base_url}{studio.find("a").get("href")}'
        # broadcast = [i for i in main_content.find(class_="leftside").find_all(class_="spaceit_pad") if "Broadcast:" in i.text][0].find("span").next_sibling.strip()
        # producers = [i for i in main_content.find(class_="leftside").find_all(class_="spaceit_pad") if "Producers:" in i.text][0].find_all("a")
        # producers = str([i.text for i in producers])
        # licensors = [i for i in main_content.find(class_="leftside").find_all(class_="spaceit_pad") if "Licensors:" in i.text][0].find_all("a")
        # licensors = [i.text for i in licensors]
        # if len(licensors) == 1:
            # licensors = licensors[0]
        # else:
            # licensors = str(licensors)
        # source = [i for i in main_content.find(class_="leftside").find_all(class_="spaceit_pad") if "Source:" in i.text][0].find("span").next_sibling.strip()
        # genres = [i for i in main_content.find(class_="leftside").find_all(class_="spaceit_pad") if "Genres:" in i.text or "Genre:" in i.text][0].find_all("a")
        # genres = str([i.text for i in genres])
        # themes = [i for i in main_content.find(class_="leftside").find_all(class_="spaceit_pad") if "Themes:" in i.text or "Theme:" in i.text][0].find_all("a")
        # themes = [i.text for i in themes]
        # if len(themes) == 1:
            # themes = themes[0]
        # else:
            # themes = str(themes)
        # demographic = [i for i in main_content.find(class_="leftside").find_all(class_="spaceit_pad") if "Demographic:" in i.text][0].find("a").text
        # duration = [i for i in main_content.find(class_="leftside").find_all(class_="spaceit_pad") if "Duration:" in i.text][0].find("span").next_sibling.strip()
        # rating = [i for i in main_content.find(class_="leftside").find_all(class_="spaceit_pad") if "Rating:" in i.text][0].find("span").next_sibling.strip()
        related_anime = main_content.find(class_="anime_detail_related_anime")
        trs = related_anime.find_all("tr")
        adaptation = [item for item in trs if "Adaptation:" in item.text][0].find("a").get("href")
        adaptation = base_url + adaptation

        print(adaptation)


def start():
        get_detail()


if __name__ == "__main__":
    start()
