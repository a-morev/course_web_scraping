# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class InstagramParserPipeline:
    def process_item(self, item, spider):
        # если юзер попал в список, значит у него есть минимум один коммент
        item['comments_number'] = 1
        client = MongoClient('localhost', 27017)
        db = client['instagram']
        users_collection = db.users
        # если юзера нет в бд - добавлем, если есть - увеличиваем comment_number На 1
        if users_collection.count_documents({'user_id': item['user_id']}) == 0:
            users_collection.insert_one(item)
            print()
        else:
            users_collection.update_one({'user_id': item['user_id']}, {'$inc': {'comments_number': 1}})
        return item
