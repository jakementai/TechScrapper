# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ContentItem(scrapy.Item):
    # define the fields for your item here like:
    forum_title = scrapy.Field()
    main_category = scrapy.Field()
    sub_category = scrapy.Field()
    link = scrapy.Field()
    content = scrapy.Field()

class HistoryItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    
