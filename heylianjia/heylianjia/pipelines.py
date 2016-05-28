# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json,os
import codecs


class HouseSaleInfoPipeline(object):
    def __init__(self):
        self.file = None
        self.current_district = u''
        self.file_pool = {}
        #self.file.write(u'[\n')
        pass

    def __del__(self):
        #self.file.write(u']')
        pass

    def process_item(self, item, spider):
        if u'HouseSaleInfo' != spider.name :
            return item

        if item['district'] not in self.file_pool:
            file_name = item['district']+u'.json'
            self.file_pool[item['district']] = codecs.open( os.path.join(u'json_data', file_name), 'w+', encoding='utf-8')

        ofile = self.file_pool[item['district']]

        line = json.dumps(dict(item)) + '\n'
        ofile.write(line.decode("unicode_escape"))

        return item

class HouseRentInfoPipeline(object):
    def __init__(self):
        self.file = None
        self.current_district = u''
        self.file_pool = {}
        #self.file.write(u'[\n')
        pass

    def __del__(self):
        #self.file.write(u']')
        pass

    def process_item(self, item, spider):
        if u'HouseRentInfo' != spider.name :
            return item

        if item['district'] not in self.file_pool:
            file_name = item['district']+u'.json'
            self.file_pool[item['district']] = codecs.open( os.path.join(u'rent_json_data', file_name), 'w+', encoding='utf-8')

        ofile = self.file_pool[item['district']]


        line = json.dumps(dict(item)) + '\n'
        ofile.write(line.decode("unicode_escape"))

        return item

class HouseEstateInfoPipeline(object):
    def __init__(self):
        self.file = None
        self.current_district = u''

        self.file_pool = {}
        pass

    def __del__(self):
        pass

    def process_item(self, item, spider):
        if u'HouseEstateInfo' != spider.name :
            return item

        if item['district'] not in self.file_pool:
            file_name = item['district']+u'.json'
            self.file_pool[item['district']] = codecs.open( os.path.join(u'house_estate_json_data', file_name), 'w+', encoding='utf-8')

        ofile = self.file_pool[item['district']]

        line = json.dumps(dict(item)) + '\n'
        ofile.write(line.decode("unicode_escape"))

        pass