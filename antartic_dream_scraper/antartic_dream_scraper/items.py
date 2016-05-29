# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TripItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    begin_date = scrapy.Field()
    end_date = scrapy.Field()
    duration = scrapy.Field()
    ship = scrapy.Field()
    capability = scrapy.Field()
    route_map = scrapy.Field()
    type = scrapy.Field()
    url = scrapy.Field()
    departure_addr = scrapy.Field()
    arrival_addr = scrapy.Field()
    price_info = scrapy.Field()
