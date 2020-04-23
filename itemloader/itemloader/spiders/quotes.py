# -*- coding: utf-8 -*-
import scrapy
from itemloader.items import quoteItem
from itemloader.loaders import quoteLoader

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['127.0.0.1:8080']
    start_urls = ['http://127.0.0.1:8080/Quotes%20to%20Scrape.htm/']

    def parse(self, response):
        quotes = response.css('.quote')
        for quote in quotes:
            loader = quoteLoader(item=quoteItem(), selector=quote)
            loader.add_css('text', '.text::text')
            loader.add_css('author', '.author::text')
            loader.add_css('tags', '.tag::text')
            yield loader.load_item()



