# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SplashScrapyAmazonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    fit_type = scrapy.Field()
    fit_id = scrapy.Field()
    color_name = scrapy.Field()
    color_id = scrapy.Field()
    size_name = scrapy.Field()
    size_id = scrapy.Field()
    content = scrapy.Field()
    image = scrapy.Field()
