# music-searcher
音乐搜索引擎：可从歌手、歌曲名字、歌词三个角度进行搜索
## 总体框架设计

![image](https://user-images.githubusercontent.com/83262562/117762770-548a0980-b25c-11eb-8f2f-d7e190e0121f.png)
## 爬虫部分
### 爬虫思路
先在[QQ音乐的歌手页面](https://y.qq.com/portal/singer_list.html)爬取指定数量的歌手，然后根据歌手的id获取每一个歌手的歌曲列表信息，在根据歌曲id获得歌曲的歌词。
## 数据库设计
爬虫获得的数据不适合使用关系型数据库存储，因此在下载配置非关系型数据库Mongo之后，将保存的csv文件中的数据写入Mongo数据库中。

![image](https://user-images.githubusercontent.com/83262562/117762961-9a46d200-b25c-11eb-8437-ad7d05663526.png)
## 搜素引擎模块
基于Whoosh框架：Whoosh模块是一个纯Python的全文搜索库，能够快速开发个性化搜索引擎。whoosh可以为自由格式或结构化文本编制索引，然后根据简单或复杂的搜索条件快速查找匹配的文档。Whoosh模块使用jieba分词来进行中文分词，使用Okapi BM25F计算相似度评分并排序。Whoosh的重要行为都不是硬编码的。文本索引、每个字段中每个术语存储的信息级别、搜索查询的解析、允许的查询类型、评分算法等都是可定制、可替换和可扩展的。此外，由于Whoosh是纯Python实现的，因此可以在Python能运行的任何地方运行，而不需要编译器。
### 定义索引的schema
创建 Schema 对象时，使用关键字参数将字段名映射为字段类型。字段列表及其类型定义了要索引的内容和可搜索的内容。whoosh附带了一些非常有用的预定义字段类型：
-	whoosh.fields.ID：只将字段的整个值作为单个的单元进行索引，应用于song_url字段的存储
-	whoosh.fields.TEXT：用于正文文本,索引文本并存储术语位置，以允许短语搜索
-	whoosh.fields.STORED：设置为True意味着索引的值随结果一起返回
```py
schema = Schema(singer_name=TEXT(stored=True),
                song_name=TEXT(stored=True, analyzer=ChineseAnalyzer()),
                song_url=ID(stored=True),
                lyric=TEXT(stored=True, analyzer=ChineseAnalyzer()))
 ```
 
### 建立索引
创建索引目录，并清除索引的当前内容。使用`writer(`) 方法通过 Index 对象返回 `IndexWriter`对象，用于下一步将文档添加到索引到中。索引编写器的 `add_document(**kwargs)` 方法接受字段名映射到值的关键字参数，最后调用`commit()`，`IndexWriter` 将添加的文档保存到索引。
```py
writer = ix.writer()
with open('.\song.csv', 'r', encoding='utf-8')as f:
    reader = csv.reader(f)
    header_row = next(reader)
    for song in reader:
        singer_name=song[2]
        song_name=song[5]
        lyric=song[6]
        song_url=song[8]
        writer.add_document(singer_name=singer_name,song_name=song_name,song_url=song_url,lyric=lyric)
writer.commit()
```

## 搜索查询
定义Query类，Query类中包含`Search()`和`Search_lyric()`两个函数，用于搜索以及针对歌词的搜索。`Search()`需要给定搜索的类别和内容，限制最多搜索到2000个结果；`Search_lyric()`针对单词的搜索，将Search得到的结果根据查询词进行高亮显示。
```py
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
            res.update(highlight=high_part[i])
            alist.append(res)
        return alist
```
## 结果展示
  网页基于Django框架实现
  
  ![image](https://user-images.githubusercontent.com/83262562/117763393-51dbe400-b25d-11eb-94b0-d534908c9803.png)
![image](https://user-images.githubusercontent.com/83262562/117763403-556f6b00-b25d-11eb-8f79-7812efeee649.png)

