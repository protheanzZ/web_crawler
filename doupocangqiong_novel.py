# -*- coding: utf-8 -*-

import requests
import re
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
}

f = open('doupo.txt', 'a+')


def get_info(url):
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        contents = re.findall('<p>(.*?)</p>', res.content.decode("utf-8"), re.S)
        for content in contents:
            content = content.replace('&rdquo;', '')
            content = content.replace('&ldquo;', '')
            content = content.replace('&hellip', '')
            f.write(content+'\n')

    else:
        pass


if __name__ == '__main__':
    done = 1
    urls = ['http://www.doupoxs.com/doupocangqiong/%s.html' % i for i in range(2, 1665)]
    for url in urls:
        get_info(url)
        time.sleep(1)
        print('done!',done)
        done += 1

f.close()

