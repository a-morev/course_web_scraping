"""
Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и
сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
Логин тестового ящика: study.ai_172@mail.ru
Пароль тестового ящика: NextPassword172!
"""

from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient

driver = webdriver.Chrome()
driver.get('https://mail.ru/')

# авторизация
login = driver.find_element_by_name("login")
login.send_keys('study.ai_172')
button = driver.find_element_by_xpath("//button[@data-testid='enter-password']")
button.click()

time.sleep(1)
pswd = driver.find_element_by_name("password")
pswd.send_keys('NextPassword172!')

button = driver.find_element_by_xpath("//button[@data-testid='login-to-mail']")
button.click()

# сбор ссылок писем
time.sleep(3)
mail_elems = driver.find_elements_by_class_name('js-tooltip-direction_letter-bottom')
hrefs = [el.get_attribute('href') for el in mail_elems]
links = set(hrefs)
len_check = len(links)

while True:
    actions = ActionChains(driver)
    actions.move_to_element(mail_elems[-1])
    actions.perform()
    time.sleep(4)
    mail_elems = driver.find_elements_by_class_name('js-tooltip-direction_letter-bottom')
    hrefs = [el.get_attribute('href') for el in mail_elems]
    links.update(set(hrefs))
    if len_check == len(links):
        break
    len_check = len(links)

# сбор данных по ссылкам
mails = []
for link in links:
    mail_data = {}
    driver.get(link)
    time.sleep(2)

    mail_data['from'] = driver.find_element_by_class_name('letter-contact').get_attribute('title')
    mail_data['date'] = driver.find_element_by_class_name('letter__date').text
    mail_data['title'] = driver.find_element_by_xpath('//h2').text
    mail_data['text'] = driver.find_element_by_class_name('letter-body').text
    mail_data['link'] = link

    mails.append(mail_data)

# добавление в базу
client = MongoClient('localhost', 27017)

db = client['mails']
main_coll = db.main_coll

for el in mails:
    main_coll.update_one({'link': el.get('link')}, {'$set': el}, upsert=True)

print(f'Писем в базе: {main_coll.count_documents({})}')
