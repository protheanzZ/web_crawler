import requests
from lxml import etree
import re
import pymongo
import time

client = pymongo.MongoClient('localhost', 27017)
mydb = client['mydb']
musictop = mydb['musictop_review']

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}


def get_url_music(url):
    html = requests.get(url, headers=headers)
    selector = etree.HTML(html.text)
    music_hrefs = selector.xpath('//a[@class="nbg"]/@href')
    for music_href in music_hrefs:
        get_music_info(music_href)


def get_music_info(url):
    html = requests.get(url, headers=headers)
    selector = etree.HTML(html.text)
    name = selector.xpath('//div[@id = "wrapper"]/h1/span/text()')[0]
    artist = re.findall('表演者:.*?>(.*?)</a>', html.text, re.S)[0]
    style = re.findall('流派:</span>&nbsp;(.*?)<br />', html.text, re.S)
    try:
        style = style[0].strip()
    except Exception:
        style = '未知'
    time = re.findall('<span class="pl">发行时间:</span>&nbsp;(.*?)<br />', html.text, re.S)[0].strip()
    publisher = re.findall(' <span class="pl">出版者:</span>&nbsp;(.*?)<br />', html.text, re.S)
    try:
        publisher = publisher[0].strip()
    except Exception:
        publisher = '未知'
    score = selector.xpath('//*[@id="interest_sectl"]/div/div[2]/strong/text()')[0]
    print(name, artist, style, time, publisher, score)
    info = {
        'name': name,
        'artist': artist,
        'style': style,
        'time': time,
        'publisher': publisher,
        'score': score
    }
    musictop.insert_one(info)


if __name__ == '__main__':
    urls = ['http://music.douban.com/top250?start={}'.format(str(i)) for i in range(0, 250, 25)]
    for url in urls:
        get_url_music(url)
        time.sleep(2)