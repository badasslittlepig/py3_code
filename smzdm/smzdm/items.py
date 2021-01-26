# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SmzdmItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class GoodsItem(scrapy.Item):
    title = scrapy.Field(); #标题
    uri = scrapy.Field(); #跳转链接
