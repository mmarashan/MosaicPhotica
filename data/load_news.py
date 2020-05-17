import json
from typing import List

from GoogleNews import GoogleNews


class News:
    def __init__(self, link: str, text: str, image_url: str):
        self.link = link
        self.text = text
        self.image_url = image_url

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self)


def load_news() -> List[News]:
    googlenews: GoogleNews = GoogleNews(lang='ru', period='d')
    googlenews.search(" ")
    search_result = []
    for p in range(1, 3):
        googlenews.getpage(p)
        result = googlenews.result()
        for r in result:
            search_result.append(r)
        googlenews.clear()

    news_list = []
    for n in search_result:
        new = News(n['link'], n['desc'], "")
        if str(n['img']).startswith("http"):
            new.image_url = n['img']
        news_list.append(new)
    print("Return {}: {}".format(len(news_list), news_list))

load_news()
