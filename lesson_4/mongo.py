"""
Запись всех результатов в БД Mongo
"""

import logging


class MongoCollectionProcessor:

    def __init__(self, collect):
        self._collection = collect
        logging.basicConfig(filename="log_mongo.log", level=logging.INFO)

    def write_mongo(self, data, no_check=True):

        if no_check:
            if type(data) == list:
                """
                process the data in a loop
                """
                self._collection.insert_many(data)

            elif type(data) == dict:
                self._collection.insert_one(data)
        else:
            # первый вариант с индексацией
            # try:
            #     self._collection.create_index(kwargs['colum'], unique=kwargs['unique'], dropDups=kwargs['dropDups'])
            # finally:
            #     for line in data:
            #         try:
            #             self._collection.insert_one(line)
            #         except Exception as err:
            #             logging.error(f'Dublicate save: {err}')

            # второй вариант как вы и сказали переделал с upsert
            for line in data:
                try:
                    self._collection.update_many({'href': {'$eq': line['href']}}, {'$set': line}, upsert=True)
                except Exception as err:
                    logging.error(f'Dublicate save: {err}')

    def drop_mongo(self, filter_: dict):
        self._collection.drop(filter_)

    def query_mongo(self, filter_):
        return self._collection.find(filter_)

    def result_output(self, result):
        for line in result:
            print(line)
