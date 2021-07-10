"""
1) Написать приложение, которое собирает основные новости с сайтов news.mail.ru, lenta.ru,
yandex.news.
Для парсинга использовать xpath. Структура данных должна содержать:
- название источника,
- наименование новости,
- ссылку на новость,
- дата публикации
*Нельзя использовать BeautifulSoup
2) Сложить все новости в БД(Mongo); без дубликатов, с обновлениями
"""
import requests
from lxml import html

from pymongo import MongoClient
import time
from datetime import datetime
from datetime import timedelta

from lesson_4.mongo import MongoCollectionProcessor


class News:
    def __init__(self):
        self.info_list = []
        self.main_url = ''
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                          '(KHTML, like Gecko) Chrome/91.0.4472.123 Safari/537.36'
        }


class Mail(News):
    def __init__(self):
        super().__init__()
        self.main_url = 'https://news.mail.ru/'

    def get_news(self):
        req = requests.get(self.main_url, headers=self.headers)

        dom = html.fromstring(req.text)

        """распарсим блоки дневных новостей"""

        xpath_for_item = '//body/div[@class ="layout"]/div[@data-module="TrackBlocks"]/div[@class ="block"]' \
                         '/div[@class ="wrapper"]//table[@class ="daynews__inner"]' \
                         '//td[@class ="daynews__main" or @class ="daynews__items"]' \
                         '/div[contains(@class, "daynews__item")]/a'
        items = dom.xpath(xpath_for_item)
        for item in items:
            info = {}
            info['source'] = 'news.mail.ru'
            info['href'] = item.xpath(".//@href")[0]
            xpath_item_name = './/span/text()'
            info['name'] = item.xpath(xpath_item_name)[0].replace('\xa0', ' ')
            info['date'] = self._get_date(info['href'])
            self.info_list.append(info)

        """распарсим остальные новости"""

        xpath_for_item = '//body/div[@class="layout"]/div[@data-module="TrackBlocks"]/div[@class="block"]' \
                         '/div[@class="wrapper"]//li[@class="list__item"]'
        items = dom.xpath(xpath_for_item)
        for item in items:
            info = {}
            info['source'] = 'news.mail.ru'
            info['href'] = item.xpath(".//@href")[0]
            xpath_item_name = './/a/text()'
            info['name'] = item.xpath(xpath_item_name)[0].replace('\xa0', ' ')
            info['date'] = self._get_date(info['href'])
            self.info_list.append(info)

    @staticmethod
    def _get_date(url):
        time.sleep(2)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                          '(KHTML, like Gecko) Chrome/91.0.4472.123 Safari/537.36'
        }
        req = requests.get(url, headers=headers)
        dom = html.fromstring(req.text)
        items = dom.xpath('//span[@class="note"]/span[@datetime]')
        date_ = datetime.strptime(items[0].xpath('./@datetime')[0][:-6], '%Y-%m-%dT%H:%M:%S')
        return str(date_)


class Lenta(News):
    def __init__(self):
        super().__init__()
        self.main_url = 'https://lenta.ru/'

    def get_news(self):
        req = requests.get(self.main_url, headers=self.headers)
        dom = html.fromstring(req.text)
        items = dom.xpath('//body/div[@id="root"]//section[contains(@class, "b-top7-for-main")]'
                          '//div[contains(@class, "item")]//a[contains(@href, "news")]')
        month_ru = (['января', 'Jan'],
                    ['февраля', 'Feb'],
                    ['марта', 'Mar'],
                    ['апреля', 'Apr'],
                    ['мая', 'May'],
                    ['июня', 'Jun'],
                    ['июля', 'Jul'],
                    ['августа', 'Aug'],
                    ['сентября', 'Sep'],
                    ['октября', 'Oct'],
                    ['ноября', 'Nov'],
                    ['декабря', 'Dec'])

        for item in items[1:]:
            info = {}
            info['source'] = 'lenta.ru'
            info['href'] = self.main_url + item.xpath("./@href")[0]
            info['name'] = item.xpath('./text()')[0].replace('\xa0', ' ')
            date_ = str(item.xpath('.//time/@datetime')[0]).strip()
            for ru_, en_ in month_ru:
                if date_.count(ru_) > 0:
                    date_ = date_.replace(ru_, en_)
                    break

            info['date'] = str(datetime.strptime(date_, '%H:%M, %d %b %Y'))
            self.info_list.append(info)


class Yandex(News):
    def __init__(self):
        super().__init__()
        self.main_url = 'https://yandex.ru/news/'

    def get_news(self):
        req = requests.get(self.main_url, headers=self.headers)
        dom = html.fromstring(req.text)
        items = dom.xpath('//body/div[@id]/div/div/div/div[1]//div[contains(@class,"mg-grid__col_xs")]'
                          '/article/div[contains(@class,"mg-card")]//a/h2/..')
        '//span[contains(@class,"_time")]'
        currentdate = datetime.today()
        day_b = currentdate.combine(currentdate.date(), currentdate.min.time())
        for item in items:
            info = {}
            info['source'] = 'yandex.ru'
            info['href'] = item.xpath("./@href")[0]
            info['name'] = item.xpath('.//h2/text()')[0].replace('\xa0', ' ')
            time = str(item.xpath('./../../../..//span[contains(@class,"_time")]/text()')[0])
            try:
                h_and_m = list(map(int, time.split(':')))
                info['date'] = str(day_b + timedelta(hours=h_and_m[0], minutes=h_and_m[0]))
            except Exception:
                info['date'] = time
            self.info_list.append(info)


if __name__ == '__main__':
    with MongoClient('localhost:27017') as client:
        db = client['news']
        collection = db['day_news']

        mongo = MongoCollectionProcessor(collection)

        mail_news = Mail()
        mail_news.get_news()

        # заполнение данных
        mongo.write_mongo(mail_news.info_list, no_check=False)

        lenta_news = Lenta()
        lenta_news.get_news()

        # заполнение данных
        mongo.write_mongo(lenta_news.info_list, no_check=False)

        yandex_news = Yandex()
        yandex_news.get_news()

        # заполнение данных
        mongo.write_mongo(yandex_news.info_list, no_check=False)

        # полная выгрузка
        result = mongo.query_mongo({})
        mongo.result_output(result)
