import requests
from lxml import etree
import time
import pymongo

client = pymongo.MongoClient('localhost', 27017)
db = client['crawler']
tongcheng_url = db['tongcheng_url']
tongcheng_info = db['tongcheng_info']

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'connection': 'keep-alive'
}

channel_list = '''
http://cd.58.com/shouji/
http://cd.58.com/tongxunyw/
http://cd.58.com/danche/
http://cd.58.com/diandongche/
http://cd.58.com/fzixingche/
http://cd.58.com/sanlunche/
http://cd.58.com/peijianzhuangbei/
http://cd.58.com/diannao/
http://cd.58.com/bijiben/
http://cd.58.com/pbdn/
http://cd.58.com/diannaopeijian/
http://cd.58.com/zhoubianshebei/
http://cd.58.com/shuma/
http://cd.58.com/shumaxiangji/
http://cd.58.com/mpsanmpsi/
http://cd.58.com/youxiji/
http://cd.58.com/ershoukongtiao/
http://cd.58.com/dianshiji/
http://cd.58.com/xiyiji/
http://cd.58.com/bingxiang/
http://cd.58.com/jiadian/
http://cd.58.com/binggui/
http://cd.58.com/chuang/
http://cd.58.com/ershoujiaju/
http://cd.58.com/yingyou/
http://cd.58.com/yingeryongpin/
http://cd.58.com/muyingweiyang/
http://cd.58.com/muyingtongchuang/
http://cd.58.com/yunfuyongpin/
http://cd.58.com/fushi/
http://cd.58.com/nanzhuang/
http://cd.58.com/fsxiemao/
http://cd.58.com/xiangbao/
http://cd.58.com/meirong/
http://cd.58.com/yishu/
http://cd.58.com/shufahuihua/
http://cd.58.com/zhubaoshipin/
http://cd.58.com/yuqi/
http://cd.58.com/tushu/
http://cd.58.com/tushubook/
http://cd.58.com/wenti/
http://cd.58.com/yundongfushi/
http://cd.58.com/jianshenqixie/
http://cd.58.com/huju/
http://cd.58.com/qiulei/
http://cd.58.com/yueqi/
http://cd.58.com/kaquan/
http://cd.58.com/bangongshebei/
http://cd.58.com/diannaohaocai/
http://cd.58.com/bangongjiaju/
http://cd.58.com/ershoushebei/
http://cd.58.com/chengren/
http://cd.58.com/nvyongpin/
http://cd.58.com/qinglvqingqu/
http://cd.58.com/qingquneiyi/
http://cd.58.com/chengren/
http://cd.58.com/xiaoyuan/
http://cd.58.com/ershouqiugou/
http://cd.58.com/tiaozao/

'''


def get_links(channel, pages):
    list_view = '{}pn{}/'.format(channel, str(pages))
    try:
        html = requests.get(list_view, headers=headers)
        time.sleep(2)
        selector = etree.HTML(html.text)
        if selector.xpath('//tr'):
            infos = selector.xpath('//tr')
            for info in infos:
                if info.xpath('td[2]/a/@href'):
                    url = info.xpath('td[2]/a/@href')[0]
                    tongcheng_url.insert_one({'url': url})
                else:
                    pass
        else:
            pass
    except requests.exceptions.ConnectionError:
        pass


def get_info(url):
    if url == '#':
        print('invalid url!')
        return False
    url_update = url
    if not url.startswith('http:'):
        url_update = 'http:' + url
        
    html = None
    try:
        html = requests.get(url_update, headers=headers)
    except requests.exceptions.ConnectionError:
        print('connect refused!')
        return False
    selector = etree.HTML(html.text)
    try:
        title = selector.xpath('//h1/text()')[0]
        if selector.xpath('//span[@class="price_now"]/i/text()'):
            price = selector.xpath('//span[@class="price_now"]/i/text()')[0]
        else:
            price = '无'
        if selector.xpath('//div[@class="palce_li"]/span/i/text()'):
            area = selector.xpath('//div[@class="palce_li"]/span/i/text()')[0]
        else:
            area = '无'
        view = selector.xpath('//p/span[1]/text()')[0]
        if selector.xpath('//p/span[2]/text()'):
            want = selector.xpath('//p/span[2]/text()')[0]
        else:
            want = '无'
        info = {
            'title': title,
            'price': price,
            'area': area,
            'view': view,
            'want': want,
            'url': url
        }
        tongcheng_info.insert_one(info)
        print(info)
    except IndexError:
        pass

