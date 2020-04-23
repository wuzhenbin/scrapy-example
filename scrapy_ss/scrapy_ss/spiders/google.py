# -*- coding: utf-8 -*-
import scrapy


class GoogleSpider(scrapy.Spider):
    name = 'google'
    allowed_domains = ['www.google.com']
    start_urls = ['https://www.youtube.com/?hl=zh-cn']

    def parse(self, response):
        print(response)
