# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


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
