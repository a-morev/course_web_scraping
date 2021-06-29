"""
Зарегистрироваться на https://openweathermap.org/api и написать функцию, которая получает погоду
в данный момент для города, название которого получается через input. https://openweathermap.org/current
"""
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()


class Weather:
    def __init__(self, appid):
        self._appid = appid

    def get_by_city_name(self, city_name):
        params = {
            'q': city_name,
            'appid': self._appid
        }
        url = 'https://api.openweathermap.org/data/2.5/weather'
        resp = requests.get(url, params=params)
        return resp.json()

    @staticmethod
    def save_to_file(data):
        with open('city_weather.json', 'w', encoding='utf-8') as f:
            json.dump(data, f)


if __name__ == '__main__':
    appid = os.getenv('APPID', None)
    weather = Weather(appid)
    object_json = weather.get_by_city_name(input('Enter the name of the city in English: '))
    # print(object_json)
    weather.save_to_file(object_json)
