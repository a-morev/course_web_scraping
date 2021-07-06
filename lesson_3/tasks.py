"""
1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
записывающую собранные вакансии в созданную БД.
2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше
введённой суммы.
3.* Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.
"""
import json
import logging
from pymongo import MongoClient


class Mongo:

    def __init__(self, collection):
        self._collection = collection
        logging.basicConfig(filename="log_mongo.log", level=logging.INFO)

    def write_mongo(self, data, no_check=True, **kwargs):
        if no_check:
            if type(data) == list:
                """
                process the data in a loop
                """
                self._collection.insertMany(data)

            elif type(data) == dict:
                self._collection.insertOne(data)
        else:
            try:
                self._collection.create_index(kwargs['colum'], unique=kwargs['unique'], dropDups=kwargs['dropDups'])
            finally:
                for line in json_data:
                    try:
                        self._collection.insert_one(line)
                    except Exception as err:
                        logging.error(f'Dublicate save: {err}')

    def drop_mongo(self, filter_: dict):
        self._collection.drop(filter_)

    @staticmethod
    def query_mongo(filter_):
        return collection.find(filter_)

    @staticmethod
    def result_output(result):
        for line in result:
            print(line)


if __name__ == '__main__':
    # используем данные парсинга из предыдущего урока lesson-2
    with open('data_file.json', encoding='UTF-8') as f:
        json_data = json.load(f)

    with MongoClient('localhost:27017') as client:
        db = client['hh']
        collection = db['vacancy']

        mongo = Mongo(collection)
        # удаление данных
        # mongo.drop_mongo({})

        # заполнение данных
        mongo.write_mongo(json_data, no_check=False, colum=[('href', 1)], unique=True, dropDups=True)

        # полная выгрузка
        result = mongo.query_mongo({})
        mongo.result_output(result)
        # выводит на экран вакансии с заработной платой больше введённой суммы
        result = mongo.query_mongo({'price_begin': {'$gte': 15000}})
        mongo.result_output(result)
        # использование одновременно мин/макс зарплаты
        result = mongo.query_mongo({'$and': [{'price_begin': {'$gte': 15000}}, {'price_end': {'$lte': 100000}}]})
        mongo.result_output(result)
        # вариант null
        result = mongo.query_mongo({'$or': [{'price_begin': None}, {'price_end': None}]})
        mongo.result_output(result)
