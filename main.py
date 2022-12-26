import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from feedgen.feed import FeedGenerator
import pytz

cover_news_url = "https://cover-corp.com/news"

html_text = requests.get(cover_news_url).text
soup = BeautifulSoup(html_text, "html.parser")

fg = FeedGenerator()
fg.id(cover_news_url)
fg.title("NEWS | カバー株式会社")
fg.subtitle("カバーからの最新情報をお届けします。")
fg.link(href=cover_news_url, rel="alternate")
fg.language("ja")

for elem in reversed(soup.find_all(href=re.compile("/news/detail/"))):

    news_url = "https://cover-corp.com" + elem.attrs["href"]
    news_title = elem.select("h4")[0].text
    news_image_url = "https://cover-corp.com" + elem.select("div")[1].select("img")[0]["src"]
    news_date_string = elem.select("p")[0].text
    news_dt = datetime.strptime(news_date_string, "%Y.%m.%d")
    jst_timezone = pytz.timezone("Asia/Tokyo")
    news_dt_in_jst = jst_timezone.localize(news_dt)

    fe = fg.add_entry()
    fe.id(news_url)
    fe.link(href=news_url)
    fe.title(news_title)
    fe.enclosure(news_image_url, 0, "image/jpeg")
    fe.pubDate(news_dt_in_jst)
    

atomfeed = fg.atom_str(pretty=True)
rssfeed  = fg.rss_str(pretty=True)

fg.atom_file('public/atom.xml')
fg.rss_file('public/rss.xml')