import requests
import re

url = 'https://accounts.douban.com/login'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}

params = {
    'source': 'None',
    'redir': 'https://www.douban.com',
    'form_email': '18096381532',
    'form_password': '19960505',
    'login': '登录'
}

html = requests.post(url, data=params, headers=headers)

print(html.text)

print(re.search('prothean', html.text))

print(html.status_code)