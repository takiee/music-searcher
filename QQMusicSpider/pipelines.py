# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from QQMusicSpider.items import MusicItem
import json
from scrapy.exceptions import DropItem
import os
import csv


class DuplicatesPipeline(object):
    """
    根据音乐的song_id，对爬取过的音乐进行去重
    """

    def __init__(self):
        self.song_ids = set()

    def process_item(self, item, spider):
        if isinstance(item, MusicItem):
            if item['song_id'] in self.song_ids:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.song_ids.add(item['song_id'])
                return item


class lyricsPipeline(object):
    def process_item(self, item, spider):
        if item['language']==0 or item['language']==2:
            if item['lyric']:
                return item
        else:
            raise DropItem("language item found: %s" % item)



class QqmusicspiderPipeline(object):
    def __init__(self):
        music_path = "music12077"
        self.file = open(music_path, "w", encoding="utf8")


    #在Spider开启时，该方法被调用。
    #通常用于在数据处理之前完成某些初始化工作，如打开文件或者链接数据库
    def process_item(self, item, spider):
        if isinstance(item, MusicItem):
            line = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.file.write(line)
        return item
    #Spider被关闭时，该方法被调用
    #通常用于在数据处理完后，完成某些清理工作，如关闭文件和关闭数据库
    def close_spider(self, spider):
        self.file.close()

class CSVPipeline(object):
    # 保存为csv格式
    def __init__(self):
        # 打开文件，指定方式为写，利用第3个参数把csv写数据时产生的空行消除
        self.f = open("song.csv", "a", newline='',encoding='utf-8')
        # 设置文件第一行的字段名，注意要跟spider传过来的字典key名称相同
        self.fieldnames = ["singer_id","singer_mid","singer_name","song_id","song_mid","song_name","lyric","language","song_url"]
        # 指定文件的写入方式为csv字典写入，参数1为指定具体文件，参数2为指定字段名
        self.writer = csv.DictWriter(self.f, fieldnames=self.fieldnames)
        # 写入第一行字段名，因为只要写入一次，所以文件放在__init__里面
        self.writer.writeheader()

    def process_item(self, item, spider):
        # 写入spider传过来的具体数值
        if item['lyric']:
            self.writer.writerow(item)
        # 写入完返回
            return item

    def close(self, spider):
        self.f.close()



