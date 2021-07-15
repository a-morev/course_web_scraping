# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


def connect_to_db(db_name):
    client = MongoClient('localhost', 27017)
    db = client[db_name]
    return db


class BooksparserPipeline:
    def __init__(self):
        self.mongobase = connect_to_db('books')

    def process_item(self, item, spider):
        if spider.name == 'labirintru':
            pass
        else:
            pass
        collection = self.mongobase[spider.name]
        collection.update_one(item, {'$set': item}, upsert=True)
        return item
