import requests
import re
import pymysql
import time
from lxml import etree
import numpy.random

conn = pymysql.connect(host='localhost', user='root', passwd='123456', db='crawler', charset='utf8')
cur = conn.cursor()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}


def get_movie_url(url):
    html = requests.get(url, headers=headers)
    print(html.status_code)
    selector = etree.HTML(html.text)
    movie_hrefs = selector.xpath('//div[@class="pic"]/a/@href')
    for movie_href in movie_hrefs:
        get_movie_info(movie_href)


def get_movie_info(url):
    html = requests.get(url, headers=headers)
    selector = etree.HTML(html.text)
    try:
        name = selector.xpath('//h1/span[1]/text()')[0]
        director = selector.xpath('//div[@id="info"]/span[1]/span[2]/a/text()')[0]
        actors = selector.xpath('//div[@id="info"]/span[3]/span[2]')[0]
        actor = actors.xpath('string(.)')
        style = re.findall('<span property="v:genre">(.*?)</span>', html.text, re.S)[0]
        country = re.findall('<span class="pl">制片国家/地区:</span> (.*?)<br/>', html.text, re.S)[0]
        release_time = re.findall('上映日期:</span> .*?>(.*?)</span>', html.text, re.S)[0]
        runtime = re.findall('片长:</span>.*?>(.*?)</span>', html.text, re.S)[0]
        score = selector.xpath('//strong[@class="ll rating_num"]/text()')[0]
        cur.execute("""
            insert into doubanmovie (name,director, actor, style, country, release_time, runtime, score)
            values(%s,%s,%s,%s,%s,%s,%s,%s)
        """, (str(name), str(director), str(actor), str(style), str(country), str(release_time),
              str(runtime), str(score)))
        print(name, director, actor, '\n', style, country, release_time, runtime, score)
    except IndexError:
        print(url)
        pass


if __name__ == '__main__':
    urls = ['http://movie.douban.com/top250?start={}'.format(str(i)) for i in range(0, 250, 25)]
    for url in urls:
        get_movie_url(url)
        time.sleep(numpy.random.rand()*10)
    conn.commit()
