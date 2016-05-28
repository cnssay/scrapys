# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
import logging

class PolarCruisesPipeline(object):
    def open_spider(self, spider):
        self.json_file = codecs.open("porlar_cruises.json", 'w+', encoding='utf-8')
        self.json_file.write('[\n')
        self.count = 0

    def close_spider(self, spider):
        self.json_file.write(']')
        self.json_file.flush()
        self.json_file.close()
        logging.info('total count=' + str(self.count))

    def process_item(self, item, spider):
        if u'polarcruises' != spider.name :
            return item
        line = json.dumps(dict(item)) + ',\n'
        self.json_file.write(line.decode("unicode_escape"))
        self.count += 1

        logging.debug('total count=' + str(self.count))
        return item
