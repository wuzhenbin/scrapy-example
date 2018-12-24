# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from urllib.parse import quote
from scrapyseleniumtest.items import ProductItem


class CyzoneSpider(Spider):
    name = 'cyzone'
    allowed_domains = ['www.cyzone.cn/']
    base_url = 'http://www.cyzone.cn/search/index/search?wd='

    def start_requests(self):
        for keyword in self.settings.get('KEYWORDS'):
            url = '{}{}'.format(self.base_url, quote(keyword)) 
            yield Request(url=url, callback=self.parse, meta={'page': 1}, dont_filter=True)
                

    def parse(self, response):
        lis = response.css('.list-inner .article-item')
        for item in lis: 
            title = item.css('.item-desc::text').extract_first()
            print(title,'title')


