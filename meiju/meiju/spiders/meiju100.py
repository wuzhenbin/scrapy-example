# -*- coding: utf-8 -*-
import scrapy
from meiju.items import Meiju100Item

class Meiju100Spider(scrapy.Spider):
    name = 'meiju100'
    allowed_domains = ['www.meijutt.com/new100.html']
    start_urls = ['https://www.meijutt.com/new100.html']

    def parse(self, response):
        list = response.css('ul.top-list li')
        for block in list:
            item = Meiju100Item()

            title = block.css('h5 a::text').extract_first()
            status = block.css('.state1 font::text').extract_first()
            type = block.css('.mjjq::text').extract_first()
            tv = block.css('.mjtv::text').extract_first()
            last_time = block.css('.lasted-time font::text').extract_first()
            if not last_time:
                last_time = block.css('.lasted-time::text').extract_first()

            item['title'] = title
            item['status'] = status
            item['type'] = type
            item['tv'] = tv
            item['last_time'] = last_time
            yield item

