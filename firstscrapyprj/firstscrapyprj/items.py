# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FirstscrapyprjItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    author = scrapy.Field()
    text_quote = scrapy.Field()
    tags = scrapy.Field()
    
class GermanYellowPageItem(scrapy.Item):
    # структура данных немецких желтых страниц
    name_firm = scrapy.Field()
    term = scrapy.Field()
    telephone = scrapy.Field()
    url = scrapy.Field()
    fax = scrapy.Field()
    lat = scrapy.Field() # долгота
    lon = scrapy.Field() # широта
    postalcode = street = scrapy.Field()
    hnr = scrapy.Field()
    city = scrapy.Field()
    email = scrapy.Field()
    rating = scrapy.Field()
    search_request = scrapy.Field()
    


