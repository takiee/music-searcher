# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QqmusicspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class MusicItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    singer_id = scrapy.Field()#1
    singer_mid = scrapy.Field()#2
    singer_name = scrapy.Field()#3
    song_id = scrapy.Field()#4
    song_mid = scrapy.Field()#5
    song_name = scrapy.Field()#6
    lyric = scrapy.Field()#7
    language = scrapy.Field()#8
    song_url = scrapy.Field()#9

    # subtitle = scrapy.Field()

    # song_time_public = scrapy.Field()

    # album_name = scrapy.Field()

    # song_type = scrapy.Field()
    # hot_comments = scrapy.Field()

    # company = scrapy.Field()