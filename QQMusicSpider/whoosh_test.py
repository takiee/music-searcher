# -*- coding: utf-8 -*-
import os
from whoosh.index import create_in
from whoosh.fields import *
from jieba.analyse import ChineseAnalyzer
import csv
from whoosh.qparser import QueryParser
import whoosh.highlight
import whoosh.index as index
import pandas as pd
'''
创建索引
'''
# 创建schema, stored为True表示能够被检索
schema = Schema(singer_name=TEXT(stored=True),
                song_name=TEXT(stored=True, analyzer=ChineseAnalyzer()),
                song_url=ID(stored=True),
                lyric=TEXT(stored=True, analyzer=ChineseAnalyzer()))

# # 存储schema信息至indexdir目录
# indexdir = 'indexdir_final/'
# if not os.path.exists(indexdir):
#     os.mkdir(indexdir)
# ix = create_in(indexdir, schema)
#
# writer = ix.writer()
# with open('D:\大三上\学习\信息检索\信息检索课程设计\QQMusicSpider-master\song.csv', 'r', encoding='utf-8')as f:
#     reader = csv.reader(f)
#     header_row = next(reader)
#     for song in reader:
#         singer_name=song[2]
#         song_name=song[5]
#         lyric=song[6]
#         song_url=song[8]
#         writer.add_document(singer_name=singer_name,song_name=song_name,song_url=song_url,lyric=lyric)
# writer.commit()

'''
搜索查询
'''
# ix = index.open_dir("indexdir")
# searcher = ix.searcher()
# results = searcher.find("singer_name", "陈奕迅",limit=None)
# # results = searcher.find("song_name", "女孩")
# print('一共发现%d份文档。' % len(results))
# for i in range(len(results)):
#     print(results[i])

from whoosh.index import open_dir


class Query:
    def __init__(self):
        self.ix = index.open_dir("../QQMusicSpider/indexdir_final")
        self.searcher = self.ix.searcher()

    def Search(self, category,content):
        ix = self.ix
        searcher = self.searcher
        qp = QueryParser(category, schema=schema)
        q = qp.parse(content)
        results = searcher.search(q, limit=2000)
        print('一共发现%d份文档。' % len(results))
        return results


    def Search_lyric(self,content):
        category='lyric'
        results=self.Search(category,content)
        high_part = list(range(len(results)))
        print('一共发现%d份文档。' % len(results))
        alist = []
        for i in range(len(results)):
            res = dict((results[i]))
            high_part[i] = results[i].highlights(category)
            # print(high_part[i])
            res.update(highlight=high_part[i])
            # print(res)
            alist.append(res)
        return alist

# qtest=Query()
# results=qtest.Search_lyric('看海天一色')
# # print("\\n")
# print(results)
# # print(type(results.filter(results)))
