import requests
from lxml import etree
import pymongo
from multiprocessing import Pool
import re


client = pymongo.MongoClient('localhost', 27017)
db = client['crawler']
jianshu_homepage = db['jianshu_homepage']

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}

codes = {}


def get_jianshu_info(url):
    html = requests.get(url, headers=headers)

    selector = etree.HTML(html.text)
    infos = selector.xpath('//ul[@class="note-list"]/li')
    code = re.findall('.*?page=(.*?)$', url)[0]
    if code not in codes:
        print(code)
        codes[code] = 1
    else:
        codes[code] += 1
    for info in infos:
        try:
            author = info.xpath('div/div/a/text()')[0]
            title = info.xpath('div/a/text()')[0]
            content = info.xpath('div/p/text()')[0].strip()
            comment = info.xpath('div/div/a[2]/text()')[1].strip()
            like = info.xpath('div/div/span/text()')[0].strip()

            data = {
                'author': author,
                'title': title,
                'content': content,
                'comment': comment,
                'like': like
            }
            jianshu_homepage.insert_one(data)
        except IndexError:
            pass


if __name__ == '__main__':
    urls = ['https://www.jianshu.com/c/bDHhpK?order_by=added_at&page={}'.format(str(i)) for i in range(1, 10001)]
    pool = Pool(processes=12)
    pool.map(get_jianshu_info, urls)