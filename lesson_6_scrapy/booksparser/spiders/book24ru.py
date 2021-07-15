import scrapy
from scrapy.http import HtmlResponse
from lesson_6_scrapy.booksparser.items import BooksparserItem

from lesson_6_scrapy.booksparser.some_funcs import make_link, current_page_number


class Book24ruSpider(scrapy.Spider):
    name = 'book24ru'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/catalog/detskie-knigi-1159/']

    def parse(self, response: HtmlResponse):
        # ограничение по количеству перебираемых страниц - без этого ограничения - это СЛИШКОМ долго
        max_page_number = 10
        # для стартовой страницы формируем ссылку на следующую страницу не так как для остальных
        if response.url in self.start_urls:
            next_page = response.url + 'page-2/'
        else:
            next_page = make_link(response.url, self.name)
        # проверка условия на номер текущей страницы
        if response.xpath("//div[@class='product-list__item']").extract() and current_page_number(response.url,
                                                                                                  self.name) <= \
                max_page_number or response.url in self.start_urls:
            yield response.follow(next_page, callback=self.parse)

        books = response.xpath(
            "//div[@class='product-card__content']//a[contains(@class,'product-card__name')]/@href").extract()
        for link in books:
            link = 'https://book24.ru' + link
            yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        book_title = response.xpath("//h1[@class='item-detail__title']/text()").extract_first()
        book_authors = list(response.xpath("//a[@itemprop='author']/text()").extract())
        book_link = response.url
        book_price = response.xpath("//div[@class='item-actions__price-old']/text()").extract_first()
        try:
            book_sale_price = response.xpath("//b[@itemprop='price']/text()").extract_first() + response.xpath(
                "//div[@class='item-actions__price']/text()").extract_first()
        except:
            book_sale_price = None
        item = BooksparserItem(title=book_title, authors=book_authors, link=book_link, price=book_price,
                               sale_price=book_sale_price)
        yield item
