from bs4 import BeautifulSoup as bsp
import requests
import csv

src = open("animelink.csv", "r")

def get_detail(page):
        mode = "w"
        if page > 1:
                mode = "a"
        base_url = 'https://myanimelist.net'
        url = src.readline()
        page = requests.get(url).content
        soup = bsp(page, 'html.parser')
        main_content = soup.find(attrs={"id": "content"})

        popularity = main_content.find(class_="numbers popularity").find("strong").text[1:]
        members = main_content.find(class_="numbers members").find("strong").text.replace(",", "")
        favorite = [i for i in main_content.find_all(class_="spaceit_pad") if "Favorites:" in i.text][0].find(class_="dark_text").next_sibling.text.strip().replace(",", "")
        season = main_content.find(class_="information season")
        try:
                season_text = season.text
                season_link = season.find("a").get("href")
        except Exception:
                season_text = "-"
                season_link = "-"
        studio = main_content.find(class_="information studio author")
        studio_text = studio.text
        studio_link = f'{base_url}{studio.find("a").get("href")}'
        try:
                broadcast = [i for i in main_content.find(class_="leftside").find_all(class_="spaceit_pad") if "Broadcast:" in i.text][0].find("span").next_sibling.strip()
        except Exception:
                broadcast = "-"
        producers = [i for i in main_content.find(class_="leftside").find_all(class_="spaceit_pad") if "Producers:" in i.text][0].find_all("a")
        producers = str([i.text for i in producers])
        licensors = [i for i in main_content.find(class_="leftside").find_all(class_="spaceit_pad") if "Licensors:" in i.text][0].find_all("a")
        licensors = [i.text for i in licensors]
        if len(licensors) == 1:
            licensors = licensors[0]
        else:
            licensors = str(licensors)
        source = [i for i in main_content.find(class_="leftside").find_all(class_="spaceit_pad") if "Source:" in i.text][0].find("span").next_sibling.strip()
        genres = [i for i in main_content.find(class_="leftside").find_all(class_="spaceit_pad") if "Genres:" in i.text or "Genre:" in i.text][0].find_all("a")
        genres = str([i.text for i in genres])
        themes = [i for i in main_content.find(class_="leftside").find_all(class_="spaceit_pad") if "Themes:" in i.text or "Theme:" in i.text][0].find_all("a")
        themes = [i.text for i in themes]
        if len(themes) == 1:
            themes = themes[0]
        else:
            themes = str(themes)
            
        try:
                demographic = [i for i in main_content.find(class_="leftside").find_all(class_="spaceit_pad") if "Demographic:" in i.text][0].find("a").text
        except Exception:
                demographic = "-"
        duration = [i for i in main_content.find(class_="leftside").find_all(class_="spaceit_pad") if "Duration:" in i.text][0].find("span").next_sibling.strip()
        rating = [i for i in main_content.find(class_="leftside").find_all(class_="spaceit_pad") if "Rating:" in i.text][0].find("span").next_sibling.strip()
        # related_anime = main_content.find(class_="anime_detail_related_anime")
        # trs = related_anime.find_all("tr")
        # adaptation = [item for item in trs if "Adaptation:" in item.text][0].find("a").get("href")
        # adaptation = base_url + adaptation

        title_columns = ["Popularity", "Members", "Favorite", "Season", "Season Link", "Studio", "Studio Link", "Broadcast", "Producers", "Licensors", "Source", "Genres", "Themes", "Demographic", "Duration", "Rating"]
        anime_detail_contents = [popularity, members, favorite, season_text, season_link, studio_text, studio_link, broadcast, producers, licensors, source, genres, themes, demographic, duration, rating]

        with open("animedetail.csv", mode) as fp:
                writer = csv.writer(fp, delimiter="|")
                if mode == "w":
                        writer.writerow(title_columns)
                writer.writerow(anime_detail_contents)
        
        

def start():        
        page = 1
        lines = 0
        with open("animelink.csv", "r") as fp:
                for count, line in enumerate(fp):
                        pass
                lines = count + 1
        while page <= lines:
                get_detail(page)
                print(f"{page} iteration finished")
                page += 1


if __name__ == "__main__":
        start()
    
src.close()
