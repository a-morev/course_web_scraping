# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib

import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes


class LeroymerlinparserPipeline:
    def process_item(self, item, spider):
        return item


class LeroymerlinparserPhotosPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except TypeError as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    # разложим картинки по папкам - название папки будет содержать кусок url-адреса item'а
    def file_path(self, request, response=None, info=None, *, item=None):
        my_dir = item['link'].split('/')
        my_dir = my_dir[-2]
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'full/{my_dir}/{image_guid}.jpg'
