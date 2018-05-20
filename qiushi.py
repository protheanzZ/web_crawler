import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
}

info_lists = []


def judgment_sex(class_name):
    if class_name == 'womenIcon':
        return '女'
    else:
        return '男'


def get_info(url):
    res = requests.get(url, headers=headers)
    ids = re.findall('<h2>(.*?)</h2>', res.text, re.S)
    