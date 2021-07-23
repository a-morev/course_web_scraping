# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstagramParserItem(scrapy.Item):
    # define the fields for your item here like:
    user_link = scrapy.Field()
    user_id = scrapy.Field()
    fullname = scrapy.Field()
    user_photo_link = scrapy.Field()
    user_data = scrapy.Field()
    # Количество комментариев от пользователя распарсенному пользователю
    comments_number = scrapy.Field()
    # Пользователь, посты которого рассматривали и искали комментаторов
    parsed_user = scrapy.Field()
    _id = scrapy.Field()
