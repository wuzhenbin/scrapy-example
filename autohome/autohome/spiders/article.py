# -*- coding: utf-8 -*-
import scrapy
from autohome.items import articleItem

class ArticleSpider(scrapy.Spider):
    name = 'article'
    allowed_domains = ['autohome.com.cn']
    start_urls = ['https://www.autohome.com.cn/all/1/#liststart']

    def parse(self, response):
        lis = response.css('.article li')
        for item in lis:
            block = articleItem()
            block['title'] = item.css('h3::text').extract_first()
            block['link'] = 'https:{}'.format(item.css('a::attr(href)').extract_first()) 
            yield block
