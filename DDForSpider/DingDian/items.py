# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class bookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	name = scrapy.Field()
	chapterNew = scrapy.Field()
	author = scrapy.Field()
	charNum = scrapy.Field()
	updateTime = scrapy.Field()
	isEnd = scrapy.Field()
	id = scrapy.Field()
	type = scrapy.Field()
	

class chapterItem(scrapy.Item):
	chapterName = scrapy.Field()
	chapterNum = scrapy.Field()
	content = scrapy.Field()
	type = scrapy.Field()
	id = scrapy.Field()
