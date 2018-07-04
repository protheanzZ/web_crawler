from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from jianshu_zhuanti.items import JianshuZhuantiItem


class jianshu_zhuanti(CrawlSpider):
    name = 'jianshu_zhuanti'
    start_urls = ['http://www.jianshu.com/recommendations/collections?page=1&order_by=hot']

    def parse(self, response):
        item = JianshuZhuantiItem()
        selector = Selector(response)
        infos = selector.xpath('//div[@class="col-xs-8"]')
        for info in infos:
            try:
                name = info.xpath('div/a[1]/h4/text()').extract()[0]
                content = info.xpath('div/a[1]/p/text()').extract()[0]
                article = info.xpath('div/div/a/text()').extract()[0]
                fans = info.xpath('div/div/text()').extract()[0]

                item['name'] = name
                item['content'] = content
                item['article'] = article
                item['fans'] = fans

                yield item

            except IndexError:
                pass

        urls = ['http://www.jianshu.com/recommendations/collections?page={}&order_hot'.format(str(i))
                for i in range(2, 37)]

        for url in urls:
            yield Request(url, callback=self.parse)


