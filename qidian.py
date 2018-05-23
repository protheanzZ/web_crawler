import xlwt
import requests
from lxml import etree
import time
import re

all_info_list = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
}


def get_info(url):
    html = requests.get(url, headers=headers)
    selector = etree.HTML(html.text)
    infos = selector.xpath('//ul[@class="all-img-list cf"]/li')

    for info in infos:
        title = info.xpath('div[2]/h4/a/text()')[0]
        author = info.xpath('div[2]/p[1]/a[1]/text()')[0]
        style_1 = info.xpath('div[2]/p[1]/a[2]/text()')[0]
        style_2 = info.xpath('div[2]/p[1]/a[3]/text()')[0]
        style = style_1 + '·' +style_2
        complete = info.xpath('div[2]/p[1]/span/text()')[0]
        introduce = info.xpath('div[2]/p[2]/text()')[0].strip()
        # 动态
        # word = info.xpath('div[2]/p[3]/span/text()')[0]
        info_list = [title, author, style, complete, introduce]
        all_info_list.append(info_list)
    time.sleep(1)


if __name__ == '__main__':
    urls = ['https://www.qidian.com/all?page=%s' % i for i in range(1, 50)]  # 注意xls文件最多65535行，更多行需要openpyxl库
    for url in urls:
        get_info(url)
        page = re.search('\d*?$', url)
        print('page', page.group(), 'has crawled!')

    header = ['title', 'author', 'style', 'complete', 'introduce']

    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('Sheet1')
    for h in range(len(header)):
        sheet.write(0, h, header[h])

    i = 1
    for data_list in all_info_list:
        j = 0
        for data in data_list:
            sheet.write(i, j, data)
            j += 1
        i += 1

    book.save('novels_qidian.xls')
