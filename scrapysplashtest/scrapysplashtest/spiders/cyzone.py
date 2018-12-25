# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from urllib.parse import quote
from scrapy_splash import SplashRequest

class CyzoneSpider(Spider):
    name = 'cyzone'
    allowed_domains = ['http://www.cyzone.cn']
    base_url = 'http://www.cyzone.cn/search/index/search?wd='

    def start_requests(self):
        keyword = self.settings.get('KEYWORD')
        url = self.base_url + quote(keyword)

        yield SplashRequest(
            url, 
            callback=self.parse, 
            endpoint='render.html',
            args={
                'page': 1, 
                'wait': 2
            }
        )

    def parse(self, response):
        lis = response.css('.list-inner .article-item')
        for item in lis: 
            title = item.css('.item-desc::text').extract_first()
            print(title,'title')

