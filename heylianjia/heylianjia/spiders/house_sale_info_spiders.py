# encoding=utf-8
'''
Created on 2016/2/23

@author: 'ay'
'''

import logging,re,json,os

import scrapy
from scrapy.http import Request
from .. import items


class HouseSaleInfoSpider(scrapy.Spider):
    name = "HouseSaleInfo"
    allowed_domains = ["lianjia.com"]
    base_url = "http://bj.lianjia.com"
    start_urls = [
        ##"http://bj.lianjia.com/ershoufang/dongcheng/tf1bp150ep240/",
        ##"http://bj.lianjia.com/ershoufang/xicheng/tf1bp150ep240/",
        ##"http://bj.lianjia.com/ershoufang/chaoyang/tf1bp150ep240/",
        ##"http://bj.lianjia.com/ershoufang/haidian/tf1bp150ep240/",
        ##"http://bj.lianjia.com/ershoufang/fengtai/tf1bp150ep240/",
        ##"http://bj.lianjia.com/ershoufang/shijingshan/tf1bp150ep240/",
        ##"http://bj.lianjia.com/ershoufang/tongzhou/tf1bp150ep240/",
        ##"http://bj.lianjia.com/ershoufang/changping/tf1bp150ep240/",
        ##"http://bj.lianjia.com/ershoufang/daxing/tf1bp150ep240/",
        ##"http://bj.lianjia.com/ershoufang/yizhuangkaifaqu/tf1bp150ep240/",
        "http://bj.lianjia.com/ershoufang/shunyi/tf1bp150ep240/",
        "http://bj.lianjia.com/ershoufang/fangshan/tf1bp150ep240/",
        "http://bj.lianjia.com/ershoufang/mentougou/tf1bp150ep240/",
        "http://bj.lianjia.com/ershoufang/pinggu/tf1bp150ep240/",
        "http://bj.lianjia.com/ershoufang/huairou/tf1bp150ep240/",
        ##"http://bj.lianjia.com/ershoufang/miyun/tf1bp150ep240/",
        ##"http://bj.lianjia.com/ershoufang/yanqing/tf1bp150ep240/", #缺五套
        ##"http://bj.lianjia.com/ershoufang/yanjiao/tf1bp150ep240/",


    ]

    process_record = {u'starting_url':u'', u'complete_district':[]}

    def __init__(self):
        '''
        record_file = open('record_file.json', 'w+')
        json_str = record_file.read()
        if json_str != '' :
            self.process_record = json.loads(json_str)

        if self.process_record[u'starting_url'] != u'' :
            self.start_urls[0] = self.process_record[u'starting_url']
            logging.info(u'starting with url:' + self.process_record[u'starting_url'])
        '''
        pass

    def __del__(self):
        json.dump(self.process_record, self.record_file)
        pass

    def is_in_complete_list(self, url):
        for item in self.process_record[u'complete_district'] :
            if url == item:
                return True

        return False

    def parse(self,response):
        house_info_divs = response.selector.xpath('.//ul[@id="house-lst"]//div[@class="info-panel"]')
        district = response.url.split('/')[4]

        for div in house_info_divs :
            item = items.HouseSaleInfo()
            item['district'] = district
            item['title'] = div.xpath('.//h2//text()').extract()[0]
            item['url'] = div.xpath('.//h2//@href').extract()[0]

            info1 = div.xpath('.//div[@class="where"]//span//text()').extract()
            item['house_estate_url'] = div.xpath('.//a[@class="laisuzhou"]//@href').extract()[0]
            item['house_estate'] = info1[0] if len(info1) > 0 else ''
            item['house_type'] = info1[1][0:-2] if len(info1) > 1 else ''
            item['area'] = info1[2][0:-2] if len(info1) > 2 else ''
            item['direction'] = info1[3] if len(info1) > 3 else ''

            item['zone_url'] = div.xpath('.//div[@class="other"]//a//@href').extract()[0]
            item['zone'] = div.xpath('.//div[@class="other"]//a//text()').extract()[0]
            #不好解析，先留空
            div_text = div.xpath('.//div[@class="con"]//text()').extract()
            item['floor'] = div_text[2] if len(div_text) > 2 else ''
            item['birth'] = div_text[4] if len(div_text) > 4 else ''

            item['tag'] = div.xpath('.//div[@class="chanquan"]//span//text()').extract()

            item['total_price'] = float(div.xpath('.//div[@class="price"]//span//text()').extract()[0])

            p = re.compile(r'\d+')
            match = p.search(div.xpath('.//div[@class="price-pre"]//text()').extract()[0])
            item['unit_price'] = float(match.group())
            yield item

        page_data_str =  ''.join(response.selector.xpath('.//div[@class="list-wrap"]//@page-data').extract()).strip()
        page_data = json.loads(page_data_str)
        total_page = int(page_data['totalPage'])
        cur_page = int(page_data['curPage'])
        if cur_page != total_page : #最后一页了
            #查找下一页地址
            page_url = response.selector.xpath('.//div[@class="list-wrap"]//@page-url').extract()[0]
            next_page_url = page_url.replace(u'{page}', unicode(str(cur_page+1)) )

            self.process_record[u'starting_url'] = self.base_url+next_page_url
            yield Request( self.base_url+next_page_url, self.parse)


    def parse_all(self, response):
        district_list = response.selector.xpath('.//dl[@mod-id="filter-box-d"]//dd//div//a//@href')
        request_pool = []

        for item in district_list :
            if item.extract() == u"/ershoufang/tf1bp150ep250/" : #根目录忽略
                continue

            url = self.base_url+item.extract()
            if self.is_in_complete_list(os.path.dirname(url)) : #如果在已完成链表里面了，就跳过
                continue

            request = Request( url, callback=self.parse_house_list )
            request_pool.append(request)
            #break#for debug

        return request_pool

    def parse_house_list(self, response):
        item = self.parse_item(response)
        yield item

        request = self.parse_next_page(response)

        if request is not None :
            #记录下一个要处理的页面
            self.process_record[u'starting_url'] = request.url
        else:
            self.process_record[u'starting_url'] = u''

        #yield request

    def parse_item(self, response):
        house_info_divs = response.selector.xpath('.//ul[@id="house-lst"]//div[@class="info-panel"]')
        district = response.url.split('/')[4]
        item_pool = []
        #logging.debug(district)

        for div in house_info_divs :
            item = items.HouseSaleInfo()
            item['district'] = district
            item['title'] = div.xpath('.//h2//text()').extract()[0]
            item['url'] = div.xpath('.//h2//@href').extract()[0]

            info1 = div.xpath('.//div[@class="where"]//span//text()').extract()
            item['house_estate_url'] = div.xpath('.//a[@class="laisuzhou"]//@href').extract()[0]
            item['house_estate'] = info1[0] if len(info1) > 0 else ''
            item['house_type'] = info1[1][0:-2] if len(info1) > 1 else ''
            item['area'] = info1[2][0:-2] if len(info1) > 2 else ''
            item['direction'] = info1[3] if len(info1) > 3 else ''

            item['zone_url'] = div.xpath('.//div[@class="other"]//a//@href').extract()[0]
            item['zone'] = div.xpath('.//div[@class="other"]//a//text()').extract()[0]
            #不好解析，先留空
            div_text = div.xpath('.//div[@class="con"]//text()').extract()
            item['floor'] = div_text[2] if len(div_text) > 2 else ''
            item['birth'] = div_text[4] if len(div_text) > 4 else ''

            item['tag'] = div.xpath('.//div[@class="chanquan"]//span//text()').extract()

            item['total_price'] = float(div.xpath('.//div[@class="price"]//span//text()').extract()[0])

            p = re.compile(r'\d+')
            match = p.search(div.xpath('.//div[@class="price-pre"]//text()').extract()[0])
            item['unit_price'] = float(match.group())
            #yield item
            item_pool.append(item)


            #logging.debug(div_text[4])
            #logging.debug(u'小区名称：'+item['house_estate'])
        return item_pool

    def parse_next_page(self, response):
        page_data_str =  ''.join(response.selector.xpath('.//div[@class="list-wrap"]//@page-data').extract()).strip()
        page_data = json.loads(page_data_str)
        total_page = int(page_data['totalPage'])
        cur_page = int(page_data['curPage'])
        if cur_page == total_page : #最后一页了
            return None

        #查找下一页地址
        page_url = response.selector.xpath('.//div[@class="list-wrap"]//@page-url').extract()[0]
        next_page_url = page_url.replace(u'{page}', unicode(str(cur_page+1)) )

        self.process_record[u'starting_url'] = self.base_url+next_page_url
        return Request( self.base_url+next_page_url, self.parse)
