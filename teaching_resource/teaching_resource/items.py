# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TeachingResourceItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    resource_link = scrapy.Field()
    version = scrapy.Field()
    publisher = scrapy.Field()
    resource_id = scrapy.Field()
    pass
