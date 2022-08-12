import threading

import topanime
import topmanga
import anime_recommendation
import manga_recommendation

if __name__ == '__main__':
     anime = threading.Thread(target=topanime.start)
     anime_rec = threading.Thread(target=anime_recommendation.start)
     manga = threading.Thread(target=topmanga.start)
     manga_rec = threading.Thread(target=manga_recommendation.start)
     anime.start()
     anime.join()
     manga.start()
     manga.join()
     anime_rec.start()
     anime_rec.join()
     manga_rec.start()
     manga_rec.join()
     print("Task completed")
