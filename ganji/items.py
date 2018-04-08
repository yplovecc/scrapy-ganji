# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GanjiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    e164 = scrapy.Field()
    company = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    pubdate = scrapy.Field()
    insertime = scrapy.Field()
