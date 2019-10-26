# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XimalayaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Siye_list(scrapy.Item):
    xi_list=scrapy.Field()
    # xi_name=scrapy.Field()
    # xi_username=scrapy.Field()
    # xi_url=scrapy.Field()
class Ya_list(scrapy.Item):
    title=scrapy.Field()
    ya_list=scrapy.Field()
    # ya_name=scrapy.Field()
    # ya_url=scrapy.Field()
