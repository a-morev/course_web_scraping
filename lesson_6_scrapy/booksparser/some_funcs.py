# Пользовательские функции
def make_link(link, spider_name):
    if spider_name == 'book24ru':
        tmp = link.split('-')
        page_num = str(int(tmp[-1].replace('/', '')) + 1)
        tmp.pop(-1)
        tmp.append(page_num)
        new_link = ''
        li = []
        for t in tmp:
            li.append(t)
            li.append('-')
        li.pop(-1)
        for l in li:
            new_link = new_link + l
        new_link = new_link + '/'
    else:
        tmp = link.split('=')
        page_num = str(int(tmp[-1]) + 1)
        tmp.pop(-1)
        tmp.append(page_num)
        new_link = tmp[0] + '=' + tmp[1]
    return new_link


def current_page_number(link: str, spider_name):
    if spider_name == 'book24ru':
        tmp = link.split('-')
        page_number = int(tmp[-1].replace('/', ''))
    else:
        tmp = link.split('=')
        page_number = int(tmp[-1])
    return page_number
