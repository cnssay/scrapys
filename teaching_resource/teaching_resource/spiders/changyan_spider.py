# coding=utf8
'''
author ay
'''

import scrapy
from scrapy_splash import SplashRequest
import logging
import json
import os
import re
from .. import items

#logging.basicConfig(level=logging.INFO)

def doLogin(cache = True):
    cookies = ''
    cached_cookies_file_name = 'cookies.json'
    if cache is True and os.path.exists(cached_cookies_file_name):
        cookies_json = open(cached_cookies_file_name, 'r').read()
        logging.info(cookies_json)
        if len(cookies_json) != 0:
            cookies = json.loads(cookies_json)
            return cookies

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
    logging.info('get direct cookies')

    json.dump(cookies, open(cached_cookies_file_name, 'w+'))
    return cookies

class ChangyanSpider(scrapy.Spider):
    name = u"changyan"
    allowed_domains = ["changyan.com"]
    base_url = "http://www.changyan.com"

    start_urls = [
        'http://www.changyan.com/yunres/index.php?m=search&c=resource&a=index&ph=04&s=02&pb=01', #人教版
#        'http://www.changyan.com/yunres/index.php?m=search&c=resource&a=index&ph=04&s=02&pb=19', #北师大版
#        'http://www.changyan.com/yunres/index.php?m=search&c=resource&a=index&ph=04&s=02&pb=30', #沪科版
#        'http://www.changyan.com/yunres/index.php?m=search&c=resource&a=index&ph=04&s=02&pb=34', #湘教版
#        'http://www.changyan.com/yunres/index.php?m=search&c=resource&a=index&ph=04&s=02&pb=41', #华东师大版
#        'http://www.changyan.com/yunres/index.php?m=search&c=resource&a=index&ph=04&s=02&pb=42', #冀教版
#        'http://www.changyan.com/yunres/index.php?m=search&c=resource&a=index&ph=04&s=02&pb=44'  #浙教版
    ]

    data_dir = os.path.join(os.getcwd(),'data')

    count = 1
    current_page = 1

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5}, dont_filter=True)

    def parse(self, response):

        # parse current page's items
        #yield SplashRequest(response.url, self.parse_items, args={'wait': 1}, dont_filter=True)

        urls = response.selector.xpath("//./a[@class='list-item-book']/@href").extract()

        for url in urls :
            yield SplashRequest(self.base_url+url, self.parse_items, args={'wait': 1}, dont_filter=True)


    def parse_items(self, response):
        '''
        version_str = response.selector.xpath("//./a[@class='list-item-book current']/text()").extract()[0]
        logging.debug(version_str)
        '''
        publisher = response.selector.xpath("//./a[@class='list-item-publisher current']/text()").extract()[0]
        version = response.selector.xpath("//./a[@class='list-item-book current']/text()").extract()[0]

        item_nodes = response.selector.xpath("//./li[@class='clearfix']/h2/a")

        #parse detailed page
        for item_node in item_nodes :
            resource_id = item_node.xpath("@data-value").extract()[0]
            url = item_node.xpath("@href").extract()[0]

            if self.is_analyzed(publisher, version, resource_id) :
                #logging.debug("thie item has analyzed: %s / %s / %s " % (publisher, version, resource_id) )
                continue
            yield SplashRequest(self.base_url+url, self.parse_detailed, args={'wait':0.5})

        next_page_element = response.selector.xpath(u"//./a[text()='下一页']")
        if len(next_page_element) == 0:
            logging.info("last page!")
            return

        #try to obtain next page items
        current_page_element = response.selector.xpath("//./a[@class='current']/text()").extract()
        logging.info("current page counter:" + current_page_element[0])

        next_page = int(current_page_element[0]) + 1
        logging.info("next page counter:" + str(next_page))

        script = u"""
        function main(splash)
            splash:go("%s")
            splash:wait(0.5)
            splash:runjs("searchapp.search('%d')")
            splash:wait(0.5)
            return splash:html()
        end
        """ % (response.url, next_page)

        #logging.info(script)

        self.current_page += 1
        yield SplashRequest(response.url, self.parse_items, args={'wait':1, 'lua_source':script}, endpoint='execute',dont_filter=True)

    def parse_detailed(self,response):

        item = items.TeachingResourceItem()

        item["version"] = response.selector.xpath("//./div[@class='bread_title fl']/a[last()]/text()").extract()[0]
        item["publisher"] = response.selector.xpath("//./div[@class='bread_title fl']/a[last()-1]/text()").extract()[0]
        item["title"] = response.selector.xpath("//./div[@class='bread_title fl']/span/text()").extract()[0]
        item["resource_id"] = response.selector.xpath("//./input[@id='resid']/@value").extract()[0]
        resources_urls = []
        while True:
            resources_urls = response.selector.xpath("//./a[@class='zy_load']/@data_url").extract()
            if len(resources_urls) != 0 :
                break

            node = response.xpath("//./script[@src='/yunres/Public/Search/js/timeLine.js']/following::*[1]").extract()
            if len(node) != 0 :
                js = node[0]
                ret = re.search(r'previewurl = (?P<resource>[^;]*)', js)
                if ret is not None :
                    '''
                    the format of url may be http://download.cycore.cn/e/files/e21f5969ae5b479b9d20d91d74d684d7_doc.swf,
                    or http://download.cycore.cn/c/files/ca8eeff2ba7540139145fbde0bfdaa74_ppt.swf,
                    we can turn the swf into ppt or world format.
                    '''
                    url = ret.group('resource')
                    logging.debug( 'swf url='+url)
                    if url.find('_') != -1 :
                        url = url.replace('_', '.')[0:-5].strip("'")
                        logging.debug( 'formated swf url='+url)
                    else:
                        url = url.strip("'")
                        logging.debug(r'it is a actual swf file, no need for be formated')

                    resources_urls.append(url)
                    break

            imgs = response.selector.xpath("//./div[@id='documentViewer']/img/@src").extract()
            if len(imgs) != 0 :
                resources_urls = imgs
                break

            logging.warning("unknown detailed page:" + response.url)
            return

        item["resource_link"] = resources_urls
        return item

    def is_analyzed(self, publisher, version, resource_id):
        dir_path = os.path.join(self.data_dir, publisher, version)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        json_path = os.path.join(dir_path, resource_id +'.json')
        return os.path.isfile(json_path)


if __name__ == '__main__':
    #coockies = doLogin()
    pass

