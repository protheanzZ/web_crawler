from multiprocessing import Pool
from page_spider import get_info
from page_spider import tongcheng_url
from page_spider import tongcheng_info

db_urls = [item['url'] for item in tongcheng_url.find()]
db_infos = [item['url'] for item in tongcheng_info.find()]
x = set(db_urls)
y = set(db_infos)

rest_urls = x-y
print('begin!')
if __name__ == '__main__':
    pool = Pool(processes=12)
    pool.map(get_info, rest_urls)