# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


import pdb; pdb.set_trace()  # XXX BREAKPOINT
class HouseRentInfo(scrapy.Item):
    district = scrapy.Field() # 行政区
    title = scrapy.Field() # 标题
    url = scrapy.Field() # 链接

    house_estate = scrapy.Field() # 小区名
    house_estate_url = scrapy.Field() # 小区链接

    zone = scrapy.Field() # 地区，比行政区范围要小
    zone_url = scrapy.Field() # 地区链接

    house_type = scrapy.Field() # 户型
    area = scrapy.Field() # 面积
    direction = scrapy.Field() # 朝向

    floor = scrapy.Field() # 所在楼层
    birth = scrapy.Field() # 何时建成

    tag = scrapy.Field() # 标签，地铁，随时看房等信息

    rent = scrapy.Field() # 租金


class HouseSaleInfo(scrapy.Item):
    district = scrapy.Field() # 行政区
    title = scrapy.Field() # 标题
    url = scrapy.Field() # 链接

    house_estate = scrapy.Field() # 小区名
    house_estate_url = scrapy.Field() # 小区链接

    zone = scrapy.Field() # 地区，比行政区范围要小
    zone_url = scrapy.Field() # 地区链接

    house_type = scrapy.Field() # 户型
    area = scrapy.Field() # 面积
    direction = scrapy.Field() # 朝向

    floor = scrapy.Field() # 所在楼层
    birth = scrapy.Field() # 何时建成

    tag = scrapy.Field() # 标签，地铁，是否满五年

    total_price = scrapy.Field() # 总价
    unit_price = scrapy.Field() # 单价

class HouseEstateInfo(scrapy.Item):
    district = scrapy.Field() # 行政区
    name = scrapy.Field() # 小区名
    url = scrapy.Field() # 链接

    avg_price = scrapy.Field() # 均价

    age = scrapy.Field()  #建筑年代
    type = scrapy.Field() #建筑类型
    wuye_charge = scrapy.Field() #物业费用
    wuye_vendor = scrapy.Field() #物业公司
    builder = scrapy.Field() #开发商
    building_num = scrapy.Field() #楼栋总数
    rongji_rate = scrapy.Field() #容积率
    house_num = scrapy.Field() #房屋总数
    lvhua_rate = scrapy.Field() #绿化率
    school_zone = scrapy.Field() #所属学区

    increase_desc1 = scrapy.Field() #上涨简介1
    increase_desc2 = scrapy.Field() #上涨简介2

