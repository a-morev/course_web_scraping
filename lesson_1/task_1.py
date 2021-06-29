"""
Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
сохранить JSON-вывод в файле *.json; написать функцию, возвращающую список репозиториев.
"""
import json

import requests


def get_repo(username: str):
    url = f'https://api.github.com/users/{username}/repos'
    req_repo = requests.get(url)
    if req_repo.status_code == 200:
        user_repos = req_repo.json()
        return [i["name"] for i in user_repos]
    else:
        print('Error!')


if __name__ == '__main__':
    with open('repos.json', 'w', encoding='utf-8') as f:
        json.dump(get_repo('a-morev'), f)
    print('Записано в json в файл ')
