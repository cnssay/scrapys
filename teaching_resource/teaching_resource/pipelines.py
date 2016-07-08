# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import logging
import os

class TeachingResourcePipeline(object):
    count = 0
    data_dir = os.path.join(os.getcwd(),'data')

    def __init__(self):
        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)

    def process_item(self, item, spider):
        if u'changyan' != spider.name:
            return item

        dir_path = os.path.join(self.data_dir, item["publisher"], item["version"])
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        json_path = os.path.join(dir_path, item["title"]+'.json')
        logging.debug(json_path)

        line = json.dumps(dict(item)) + ',\n'
        with codecs.open(json_path, 'w+', encoding='utf-8') as f_out:
            f_out.write(line.decode("unicode_escape"))

        self.count += 1
        logging.info("total count=" + str(self.count))
        return item
