

目标是 https://www.meijutt.com/new100.html 
我们要爬取的是最近更新100条美剧的数据 字段包括 美剧名 状态 小分类 电视台 更新时间
听起来简单吧 控制住自己想用requests来爬取的冲动。

在进行项目实战之前
我们先来简单了解下 scrapy的运行过程
先来介绍几个主角： 
spider items pipelines setting
具体含义的话等理解用途自然就明白了 这几个主角在scrapy生成的文件都能找到
首先spisers里的parse是我们的入口 我们将在这里完成数据解析的功能 数据解析完我们交给 item, 
item是做啥的呢，术语叫做'结构化数据' item对象是种简单的容器，保存了爬取到得数据。 
其提供了 类似于词典(dictionary-like)的API以及用于声明可用字段的简单语法。
我们可以理解为 item是将我们爬取到的数据进行封装，以便于其他模块使用。
当item在spider中被收集之后，它将会被传递到pipeline，一些组件会按照一定的顺序执行对item的处理。 
pipelines就是我们自己定义的中间件，可以实现所有我们爬取后进行的操作
pipeline经常进行一下一些操作： 
1清理HTML数据 
2验证爬取的数据(检查item包含某些字段) 
3查重(并丢弃) 
4将爬取结果保存到数据库中
5保存文件
6下载图片等等

接下来我们沿着这个思路进行， go~

scrapy startproject meiju
cd meiju
scrapy genspider meiju100 www.meijutt.com/new100.html


<!-- 解析部分 -->
接下来将我们的目标数据解析出来
打开浏览器 调出控制台
我们发现一个class名为'top-list'的ul标签 所有列表都在这个ul的li标签里面

进入shell命令
scrapy shell www.meijutt.com/new100.html
response 嗯 状态200 请求正常
我们用css选择器将它选出来 然后针对每一条li寻找到我们想要的数据
list = response.css('ul.top-list li')
for block in list:
    title = block.css('h5 a::text').extract_first()
    status = block.css('.state1 font::text').extract_first()
    type = block.css('.mjjq::text').extract_first()
    tv = block.css('.mjtv::text').extract_first()
    last_time = block.css('.lasted-time font::text').extract_first()
    print(title, status, type, tv, last_time)

'''
凡妮莎海辛第三季 第11集 科幻,奇幻,动作,剧情 Syfy 2018-12-18
黑色童话第一季 第7集 惊悚,悬疑,奇幻 FX 2018-12-18
黑霹雳第二季 第9集 科幻,动作 CW 2018-12-18
家的港湾第六季 第6集 爱情,剧情 Showcase 2018-12-18
联邦调查局第一季 第10集 罪案,剧情 CBS 2018-12-18
我爱露西第四季 第30集 歌舞,家庭,喜剧 CBS 2018-12-18
战神金刚：传奇的保护神第八季 第2集 科幻,喜剧,动画,动作,冒险 Netflix 2018-12-18
古战场传奇第四季 第7集 爱情,奇幻,历史 Starz 2018-12-18
穿越者第三季 第2集 科幻,动作,剧情 Netflix 2018-12-18
天佑吾王第一季 第16集 剧情 其他 2018-12-18
少女从军记第四季 第8集 战争,剧情 BBC 2018-12-18
德国83年第二季 第5集 惊悚,历史,剧情 Amazon-Prime None
清道夫第六季 第8集 罪案,剧情 Showtime None
法律与秩序第十五季 第1集 罪案,悬疑,剧情 NBC None
鲁保罗变装皇后秀.众婊季第四季 第1集 真人秀 其他 None
爆笑超市第四季 第9集 喜剧 NBC None
逃离丹尼莫拉第一季 第5集 迷你剧,罪案,悬疑 Showtime None
....
'''
关于选择器的用法将在另一篇文章进行 现在我们成功将数据拿到了，当然了，只是调试层面
接下来打开在spiders文件夹里meiju100.py scrapy已经为我们写好了初步的代码
注意稍微改下代码 start_urls改成我们的目标网址 不是http 最后面的斜杠也要去掉 如下
'''
# -*- coding: utf-8 -*-
import scrapy


class Meiju100Spider(scrapy.Spider):
    name = 'meiju100'
    allowed_domains = ['www.meijutt.com/new100.html']
    start_urls = ['https://www.meijutt.com/new100.html']

    def parse(self, response):
        pass
'''
在parse里面把我们调试成功的代码加进去 并且尝试打印出来
'''
# -*- coding: utf-8 -*-
import scrapy


class Meiju100Spider(scrapy.Spider):
    name = 'meiju100'
    allowed_domains = ['www.meijutt.com/new100.html']
    start_urls = ['https://www.meijutt.com/new100.html']

    def parse(self, response):
        list = response.css('ul.top-list li')
        for block in list:
            title = block.css('h5 a::text').extract_first()
            status = block.css('.state1 font::text').extract_first()
            type = block.css('.mjjq::text').extract_first()
            tv = block.css('.mjtv::text').extract_first()
            last_time = block.css('.lasted-time font::text').extract_first()
            print(title,status,type,tv,last_time)
'''
继续刚才的命令行 exit()退出shell调试 走起 scrapy crawl meiju100
成功的话返回我们刚在调试所返回的列表
接下来我们把刚才成功爬取到的数据保存到数据库 
找到items.py 先定义好我们要存的数据
'''
import scrapy

class Meiju100Item(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    status = scrapy.Field()
    type = scrapy.Field()
    tv = scrapy.Field()
    last_time = scrapy.Field()
'''
定义好items以后回到spiser文件里头 引入刚定义的item 实例化items 配好每一个数据
最后将item yield出去

import scrapy
from meiju.items import Meiju100Item

class Meiju100Spider(scrapy.Spider):
    name = 'meiju100'
    allowed_domains = ['www.meijutt.com/new100.html']
    start_urls = ['https://www.meijutt.com/new100.html']

    def parse(self, response):
        list = response.css('ul.top-list li')
        for block in list:
            item = Meiju100Item()

            title = block.css('h5 a::text').extract_first()
            status = block.css('.state1 font::text').extract_first()
            type = block.css('.mjjq::text').extract_first()
            tv = block.css('.mjtv::text').extract_first()
            last_time = block.css('.lasted-time font::text').extract_first()
            if not last_time:
                last_time = block.css('.lasted-time::text').extract_first()

            item['title'] = title
            item['status'] = status
            item['type'] = type
            item['tv'] = tv
            item['last_time'] = last_time
            yield item
走起 scrapy crawl meiju100
可以看到 我们爬取的数据被结构化显示出来了 

最后到存储阶段了
我们将写好一个 pipelines 来保存这些数据 拿mysql做参考例子
这里使用的是 mysql的orm框架 sqlalchemy 
账号信息存储在setting文件里面
'''
# mysql
MYSQL_URL = 'localhost:3306'
MYSQL_USER = 'root'
MYSQL_PASS = '****'
MYSQL_DATABASE = 'meiju'

'''
关于 pipelines以及数据库将在我的另外的文章做叙述 
这个我们大概理解下功能即可 pipelines的执行顺序分别是
from_crawler # 我们在这里读取mysql在setting设置的相关账号信息
__init__  # 我们在这里初始化mysql的连接数据
open_spider # 开始进行爬取
process_item # 二次处理数据 这里我们没这个需求
close_spider # 关闭spider进行的操作 这里我们不操作

pipelines写好以后还需要在setting里面做相关配置 找到setting.py里面的ITEM_PIPELINES 取消注释
这里我们定义2个ITEM_PIPELINES MeijuPipeline是默认的 我们没做任何操作
数字越小 优先级越高 范围1-1000
ITEM_PIPELINES = {
    'meiju.pipelines.MeijuPipeline': 300,
    'meiju.pipelines.SqlalchemyPipeline': 400
}
此例子的sqlalchemy需要在mysql里面提前建好表 不然会报错
'''
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Meiju(Base):
    __tablename__ = 'meiju100'
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    status = Column(String(30))
    type = Column(String(20))
    tv = Column(String(20))
    last_time = Column(String(50))


class Meiju100Pipeline(object):
    def process_item(self, item, spider):
        return item

class SqlalchemyPipeline(object):
	def __init__(self, mysql_url, mysql_user, mysql_pass, mysql_database):
		engine = create_engine('mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(mysql_user,
																				 mysql_pass,
																				 mysql_url,
																				 mysql_database))
		Session = sessionmaker(bind=engine)
		self.session = Session()

	def getItem(self, item):
		return Meiju(
			title=item['title'],
			status=item['status'],
			type=item['type'],
			tv=item['tv'],
			last_time=item['last_time'],
		)

	def add_all(self, list):
		self.session.add_all([self.getItem(item) for item in list])
		self.session.commit()

	def add_one(self, item):
		new_obj = Meiju(
			title=item['title'],
			status=item['status'],
			type=item['type'],
			tv=item['tv'],
			last_time=item['last_time'],
		)
		self.session.add(new_obj)
		self.session.commit()
		return new_obj

	@classmethod
	def from_crawler(cls, crawler):
		return cls(
			mysql_url = crawler.settings.get('MYSQL_URL'),
			mysql_user = crawler.settings.get('MYSQL_USER'),
			mysql_pass = crawler.settings.get('MYSQL_PASS'),
		 	mysql_database = crawler.settings.get('MYSQL_DATABASE')
		)

	def process_item(self, item, spider):
		self.add_one(item)
		return item
'''
至此 我们成功将数据爬进mysql里面