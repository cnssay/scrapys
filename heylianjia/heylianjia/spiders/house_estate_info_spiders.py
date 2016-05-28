# encoding=utf-8
'''
Created on 2016/2/23

@author: 'ay'
'''

import logging,re,json,os

import scrapy
from scrapy.http import Request
from .. import items


class HouseEstateInfoSpider(scrapy.Spider):
    name = "HouseEstateInfo"
    allowed_domains = ["lianjia.com"]
    base_url = "http://bj.lianjia.com"
    start_urls = [
        "http://bj.lianjia.com/xiaoqu/dongcheng/",
        "http://bj.lianjia.com/xiaoqu/xicheng/",
        "http://bj.lianjia.com/xiaoqu/chaoyang/",
        "http://bj.lianjia.com/xiaoqu/haidian/",
        "http://bj.lianjia.com/xiaoqu/fengtai/",
        "http://bj.lianjia.com/xiaoqu/shijingshan/",
        "http://bj.lianjia.com/xiaoqu/tongzhou/",
        "http://bj.lianjia.com/xiaoqu/changping/",
        "http://bj.lianjia.com/xiaoqu/daxing/",
        "http://bj.lianjia.com/xiaoqu/yizhuangkaifaqu/",
        #"http://bj.lianjia.com/xiaoqu/shunyi/",
        #"http://bj.lianjia.com/xiaoqu/fangshan/",
        #"http://bj.lianjia.com/xiaoqu/mentougou/",
        #"http://bj.lianjia.com/xiaoqu/pinggu/",
        #"http://bj.lianjia.com/xiaoqu/huairou/",
        #"http://bj.lianjia.com/xiaoqu/miyun/",
        #"http://bj.lianjia.com/xiaoqu/yanqing/",
        #"http://bj.lianjia.com/xiaoqu/yanjiao/",
    ]

    process_record = {u'starting_url':u'', u'complete_district':[]}

    def __init__(self):
        pass

    def __del__(self):
        pass

    def parse_1(self,response):
        district_paths = response.selector.xpath('.//dd[@data-index="0"]//div[@class="option-list"]//@href').extract()

        requests = []
        for district in district_paths :
            if district is u'/xiaoqu/' :
                continue
            parse_url = self.base_url + district
            logging.info(parse_url)
            requests.append(Request(parse_url, self.parse_by_district) )

        return requests

    def parse(self, response):
        estate_urls = response.selector.xpath('.//ul[@id="house-lst"]//a[@title]//@href').extract()

        for item in estate_urls :
            yield Request( self.base_url + item , self.parse_estate)

        yield self.parse_next_page(response)

    def parse_next_page(self, response):
        page_data_str =  ''.join(response.selector.xpath('.//div[@class="page-box house-lst-page-box"]//@page-data').extract()).strip()
        page_data = json.loads(page_data_str)
        total_page = int(page_data['totalPage'])
        cur_page = int(page_data['curPage'])
        if cur_page == total_page : #最后一页了
            return None

        #查找下一页地址
        page_url = response.selector.xpath('.//div[@class="page-box house-lst-page-box"]//@page-url').extract()[0]
        next_page_url = page_url.replace(u'{page}', unicode(str(cur_page+1)) )

        self.process_record[u'starting_url'] = self.base_url+next_page_url
        return Request( self.base_url+next_page_url, self.parse)


    def parse_estate(self,response):
        item = items.HouseEstateInfo()

        temp = response.selector.xpath('.//div[@class="fl l-txt"]//a//@href').extract()[2]
        item['district'] = temp.split('/')[2]

        item['name'] = response.selector.xpath('.//div[@class="title fl"]//a[@href="%s"]//text()' % (response.url)).extract()[0]
        item['url'] = response.url

        temp = response.selector.xpath('.//div[@class="res-info fr"]//span[@class="num"]//text()').extract()
        item['avg_price'] = temp[0] if len(temp) > 0 else ''

        temp = response.selector.xpath('.//div[@class="col-2 clearfix"]//span[@class="other"]//text()').extract()

        item['age'] = unicode(filter(str.isdigit,temp[0].encode('utf-8')),'utf-8')
        item['type'] = temp[1] if len(temp) > 1 else ''
        item['wuye_charge'] = unicode(filter(str.isdigit,temp[2].encode('utf-8')),'utf-8') if len(temp) > 2 else ''
        item['wuye_vendor'] = temp[3] if len(temp) > 3 else ''
        item['builder'] = temp[4] if len(temp) > 4 else ''
        item['building_num'] = unicode(filter(str.isdigit,temp[5].encode('utf-8')),'utf-8') if len(temp) > 5 else ''
        item['rongji_rate'] = temp[6] if len(temp) > 6 else ''
        item['house_num'] = temp[7] if len(temp) > 7 else ''
        item['lvhua_rate'] = temp[8] if len(temp) > 8 else ''
        item['school_zone'] = temp[10].strip().replace(' ','').replace('\n', '') if len(temp) > 9 else ''

        temp = response.selector.xpath('.//div[@class="first fl"]//div[@class="next fl"]//p//text()').extract()
        item['increase_desc1'] = ''.join(temp).replace(' ','').replace('\n', '')

        temp = response.selector.xpath('.//div[@class="second fl"]//div[@class="next fl"]//p//text()').extract()
        item['increase_desc2'] = ''.join(temp).replace(' ','').replace('\n', '')

        return item
