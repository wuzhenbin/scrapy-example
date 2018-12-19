# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field

class sixaingItem(Item):
    # define the fields for your item here like:
    id = Field()
    title = Field()
    thumb = Field()
    time = Field()
    view = Field()
    desc = Field()
    url = Field()
    download_url = Field()

