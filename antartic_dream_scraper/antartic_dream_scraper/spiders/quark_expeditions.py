# coding=utf8
'''
author: ay

'''

import scrapy

class QuarkExpeditions(scrapy.Spider):
    name = "QuarkExpeditionsSpider"
    allowed_domains = ["quarkexpeditions.com"]
    base_url = "http://www.quarkexpeditions.com"
    start_urls = [
        "",
    ]

    def __init__(self):
        pass

    def __del__(self):
        pass

    def parse(self, response):
        pass




