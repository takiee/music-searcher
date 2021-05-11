from pymongo import MongoClient
import csv

# 1.连接本地数据库服务
connection = MongoClient('localhost')
# 2.连接本地数据库 demo。没有会创建
db = connection.song
# 3.创建集合
collection=db.song
# 根据情况清空所有数据
collection.remove(None)

# 4.打开外部文件
with open('D:\大三上\学习\信息检索\信息检索课程设计\QQMusicSpider-master\song.csv', 'r', encoding='utf-8')as csvfile:
    # 调用csv中的DictReader函数直接获取数据为字典形式
    reader = csv.DictReader(csvfile)
    # 创建一个counts计数一下 看自己一共添加了了多少条数据
    counts = 0
    for each in reader:
        # 将数据中需要转换类型的数据转换类型。原本全是字符串（string）。
        collection.insert(each)
        counts += 1
    print('成功添加了' + str(counts) + '条数据 ')
