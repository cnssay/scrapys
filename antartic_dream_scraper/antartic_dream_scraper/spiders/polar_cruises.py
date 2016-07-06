# coding=utf8
'''
author ay
'''

import scrapy
from scrapy.http import Request
import logging
import datetime
from .. import items
import re

class PolarCruises(scrapy.Spider):
    name = u"polarcruises"
    allowed_domains = ["polarcruises.com"]
    base_url = "http://www.polarcruises.com"
    start_urls = [
        "http://www.polarcruises.com/antarctica/ships/luxury-expedition-ships",
        "http://www.polarcruises.com/antarctica/ships/expedition-ships",
        "http://www.polarcruises.com/antarctica/ships/ross-sea-east-antarctica-ships-and-specialty-trips",
    ]

    limit_count = -3
    count = 0
    def __init__(self):
        pass

    def closed(self, reason):
        logging.info("parse count=" + str(self.count))
        pass

    def parse(self, response):
        '''
        '''
        elements = response.selector.xpath('.//div[@class="field-items"]/div/a/@href')

        #target =  u
        for element in elements:
            detail_url = self.base_url + element.extract()
            #if target != detail_url:
            #    continue

            yield Request( detail_url, self.parse_ship_page)

    def match_price(self, response):
        price_dict = {}

        tr_elements = response.selector.xpath('.//div[@class="rates-table-wrapper"]//tbody/tr')
        col_names = response.selector.xpath('.//div[@class="rates-table-wrapper"]/table[1]//div[@class="cabin-title"]/text()').extract()

        for tr in tr_elements:
            date_raw = tr.xpath('.//td/div[@class="rates-table-date"]/a/text()').extract()[0]

            prices = tr.xpath('.//td[@data-price]/@data-price').extract()
            if len(prices) > len(col_names):
                logging.warn("count of price is larger then cols' !")
                logging.info(prices)
                logging.info(col_names)
                price_dict[date_raw] = ''
                continue
            prices_info = ''
            for index in range(len(prices)):
                prices_info += u"%s = %s |" % (col_names[index].strip(), prices[index].strip())

            price_dict[date_raw] = prices_info
        return price_dict

    def parse_ship_page(self, response):
        '''
        @url http://www.polarcruises.com/antarctica/ships/luxury-expedition-ships/national-geographic-explorer
        @returns items 0 0
        '''
        elements = response.selector.xpath('.//div[@id="ship-tours-box-wrapper"]/div/div/div/a')

        ship_type = response.selector.xpath('.//div[@class="breadcrumb"]/a/text()').extract()[2]

        price_dict = self.match_price(response)
        logging.info(price_dict)

        self.count += 1
        #logging.info("ship type=" + ship_type)
        #logging.info("element count=" + str(len(elements)))
        logging.info(response.url)
        for element in elements:
            trip_url = self.base_url + element.xpath('.//@href').extract()[0]

            item = items.TripItem()
            item["url"] = trip_url
            item["type"] = ship_type

            date_raw = element.xpath('.//text()').extract()[0]
            begin, end, duration = self.parse_date(date_raw)

            item["begin_date"] = begin.strftime('%Y/%m/%d')
            item["end_date"] = end.strftime('%Y/%m/%d')
            item["duration"] = duration

            item["price_info"] = price_dict[date_raw] if price_dict.has_key(date_raw) else u''

            logging.info(trip_url)

            request = Request(trip_url, self.parse_trip_page, dont_filter=True)
            request.meta['item'] = item
            yield request

    def parse_date(self, date_raw):
        try:
            # example: date_raw = u'Oct 30 -  Nov 20, 2016 (22 days)'
            temp = date_raw.split(',')  # [u'Oct 30 -  Nov 20', u' 2016 (22 days)']
            temp1 = temp[1].strip().split(' ') # [u'2016', u'(22', u'days)']
            end_date_str = temp[0].split('-')[1].strip() # Oct 30
            end_year_str = temp1[0]
            duration_str = temp1[1][1:]

            temp_datetime = datetime.datetime.strptime(end_date_str, r"%b %d")
            end_date = datetime.date(int(end_year_str), temp_datetime.month, temp_datetime.day)
            duration = int(duration_str)
            begin_date = end_date - datetime.timedelta(days=duration)

            return begin_date, end_date, duration
        except:
            logging.warn("parse date error! date=" + date_raw)
            nop = datetime.date(2000,1,1)
            return nop, nop, 0

    def split_trip_summay(self, text):
        words = text.strip().split(' ')
        for index in range(len(words)):
            if words[index] in [u'—', u'–', u'-']:
                return ' '.join(words[index+1:])
        logging.warn(" cannot parse trip summary, text=" + text)
        return ''

    def parse_trip_page(self, response):
        '''
        '''

        item = response.meta['item']

        title = response.selector.xpath('.//h1[@id="page-title"]/text()').extract()[0]
        item["title"] = title.strip()

        ship = response.selector.xpath(".//div[@class='node-teaser-title']/text()").extract()[0]
        item["ship"] = ship

        capability = response.selector.xpath('.//div[@class="passenger-count"]/text()').extract()
        item["capability"] = '' if len(capability) == 0 else capability[0].split(' ')[0]

        temp = response.selector.xpath('.//div[@class="itinerary-text"]/p/img/@src').extract()
        item["route_map"] = '' if len(temp) == 0 else self.base_url + temp[0]

        trip_summaries = response.selector.xpath('.//div[@id="itinerary-details-wrapper"]/div/h3/a/text()').extract()

        p = re.compile(r'\sday[s]*\s',re.I)
        for summary in trip_summaries :
            if p.search(summary) is not None :
                departure_addr = self.split_trip_summay(summary)
                break

        for summary in reversed(trip_summaries) :
            if p.search(summary) is not None :
                arrival_addr = self.split_trip_summay(summary)
                break

        item["departure_addr"] = departure_addr
        item["arrival_addr"] = arrival_addr

        return item




