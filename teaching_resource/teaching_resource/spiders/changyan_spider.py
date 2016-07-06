# coding=utf8
'''
author ay
'''

import scrapy
#from scrapy.http import Request
import logging
from selenium import webdriver
#import datetime
#from .. import items

logging.basicConfig(level=logging.INFO)

def doLogin():
    login_url = 'http://www.changyan.com/sns/index.php?app=public&mod=Login&act=index'
    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
    driver.get(login_url)
    driver.find_element_by_id('username').clear()
    driver.find_element_by_id('username').send_keys('test')

    driver.find_element_by_id('password').clear()
    driver.find_element_by_id('password').send_keys('111111')

    obj = driver.find_elements_by_xpath(r'/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div/ul/li[4]/a[1]')[0]
    obj.click()

    driver.implicitly_wait(30)
    cookies = driver.get_cookies()
    driver.close()
    logging.info(cookies)
    return cookies

class ChangyanSpider(scrapy.Spider):
    name = u"changyan"
    allowed_domains = ["changyan.com"]
    base_url = "http://www.changyan.com"

    start_urls = [
        'http://www.changyan.com/yunres/index.php?m=search&c=resource&a=index&ph=04&s=02&pb=01',
    ]

    def parse(self, response):
        pass

if __name__ == '__main__':
    doLogin()


