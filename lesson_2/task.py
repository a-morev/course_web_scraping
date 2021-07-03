"""
Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы получаем
должность) с сайтов Superjob(по желанию) и HH(обязательно). Приложение должно анализировать несколько страниц сайта
(также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
1. Наименование вакансии.
2. Предлагаемую зарплату (отдельно минимальную и максимальную).
3. Ссылку на саму вакансию.
4. Сайт, откуда собрана вакансия.
По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение). Структура должна быть
одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью dataFrame через pandas.
Сохраните в json либо csv.
"""
import requests
from bs4 import BeautifulSoup as bs
import time
import json
import pandas as pd


class HHru:

    def __init__(self, job, region):
        self.work = job
        self.url_main = f'https://{region}.hh.ru'
        self.info_all = []
        self.soup = None
        self.url_search = f'/search/vacancy?clusters=true&enable_snippets=true' \
                          f'&text={job}&L_save_area=true&area=2019&showClusters=true'

    def get_page(self):
        time.sleep(2)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.106 Safari/537.36 '
        }
        try:
            resp = requests.get(self.url_main + self.url_search, headers=headers)
            if resp.status_code == 200:
                # with open('hh_text.txt', 'w') as f:
                #     f.write(resp.text)
                return resp
        except Exception as err:
            return err

    def get_page_info(self, text_page):
        if not isinstance(text_page, str):
            return 'bad html'

        self.soup = bs(text_page, "html.parser")
        vacancy = self.soup.find_all(attrs={'class': 'vacancy-serp-item'})
        for line in vacancy:
            line_info = {}
            soup_line = bs(str(line), "html.parser")
            name_1 = soup_line.find(attrs={'class': 'bloko-link', 'data-qa': 'vacancy-serp__vacancy-title'})
            line_info.update({'name': name_1.text})
            line_info.update({'href': name_1.attrs['href']})
            line_info.update({'name': name_1.text})
            price = soup_line.find(attrs={'class': 'bloko-section-header-3 bloko-section-header-3_lite',
                                          'data-qa': 'vacancy-serp__vacancy-compensation'})
            if price is None:
                price_b = 0
                price_e = 0
            else:
                price_t = price.text.replace('\u202f', '')
                if price_t.count('от') > 0:
                    price_b = int(price_t[3:price_t.rfind(' ', 5)])
                    price_e = 0

                if price_t.count('–') > 0:
                    l_price = price_t.split(' ')
                    price_b = int(l_price[0])
                    price_e = int(l_price[2])

                if price_t.count('до') > 0:
                    price_b = 0
                    price_e = int(price_t[3:price_t.rfind(' ', 5)])

                line_info.update({'price_begin': price_b})
                line_info.update({'price_end': price_e})

            self.info_all.append(line_info)

    def next_page(self):
        next_button = self.soup.find(attrs={'class': 'bloko-button', 'data-qa': 'pager-next'})
        if next_button is not None:
            self.url_search = next_button.attrs['href']
            return True
        else:
            return False

    def save_to_json_file(self):
        with open('data_file.json', 'w', encoding='UTF-8') as f:
            json.dump(self.info_all, f, indent=2, ensure_ascii=False)

    def save_to_csv_file(self):
        df = pd.DataFrame.from_records(self.info_all)
        df.to_csv("data_file.csv", index=False)


if __name__ == '__main__':
    job = input('Enter the title of the work: ')
    region = 'tomsk'
    hh = HHru(job, region)

    i_0 = True
    i = 0
    while True:
        i += 1
        print(f'iteracion {i}')

        hh_page = hh.get_page()
        hh.get_page_info(hh_page.text)
        next_page = hh.next_page()
        if not next_page:
            break

    hh.save_to_json_file()
    hh.save_to_csv_file()
