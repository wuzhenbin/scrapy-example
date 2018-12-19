# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from movie.items import sixaingItem

class SixiangSpider(Spider):
    name = 'sixiang'
    allowed_domains = ['www.ibtbb.com']
    start_urls = ['http://www.ibtbb.com']

    def parse_detail(self, response):
        id = response.url.replace('http://www.ibtbb.com/','').replace('.html','')
        download_url = response.css('.entry-content a[href*=dl_id]::attr(href)').extract_first()
        item = sixaingItem()
        item['id'] = id
        item['download_url'] = download_url
        yield item

    # 分类列表
    def parse_nav_url(self, response):
        lis = response.css('.post-grid .post')
        for item in lis:
            title = item.css('h2 a::text').extract_first()
            id = item.css('h2 a::attr(href)').re_first('http://www.ibtbb.com/(.*).html')
            url = item.css('h2 a::attr(href)').extract_first()
            thumb = item.css('.entry-thumb img::attr(src)').extract_first()
            time = item.css('.entry-meta .date::text').extract_first()
            view = item.css('.entry-meta .meta-view::text').extract_first()
            desc = item.css('.entry-excerpt p::text').extract_first() 

            item = sixaingItem()
            item['title'] = title
            item['id'] = id
            item['url'] = url
            item['thumb'] = thumb
            item['time'] = time
            item['view'] = view
            item['desc'] = desc

            yield item
            yield Request(url, callback=self.parse_detail)

    # 获取分类地址
    def parse(self, response):
        # nav_lis = response.css('#nav li')
        # # 去掉第一个和最后一个
        # nav_lis.pop(0)
        # nav_lis.pop()
        # for item in nav_lis:
        #     url = item.css('a::attr(href)').extract_first()
        #     yield Request(url, callback=self.parse_nav_url)

        yield Request('http://www.ibtbb.com/720p', callback=self.parse_nav_url)
