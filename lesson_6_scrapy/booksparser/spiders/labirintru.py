import scrapy
from scrapy.http import HtmlResponse
from lesson_6_scrapy.booksparser.items import BooksparserItem

from lesson_6_scrapy.booksparser.some_funcs import make_link, current_page_number


class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/genres/2038/?page=1']

    def parse(self, response: HtmlResponse):
        # Добавлено ограничение на число перебираемых страниц
        max_page_number = 10
        next_page = make_link(response.url, self.name)
        # Проверка на номер страницы
        if response.xpath(
                "//div[@class='pagination-next']/a[@class='pagination-next__text']").extract() and current_page_number(
            response.url, self.name) <= max_page_number:
            yield response.follow(next_page, callback=self.parse)
        books_links = response.xpath(
            "//div[contains(@data-title,'Детская художественная литература') and @class = 'products-row ']//a[@class ="
            " 'product-title-link']/@href").extract()
        for link in books_links:
            link = 'https://www.labirint.ru' + link
            yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        # print(response.url)
        book_title = response.xpath("//h1/text()").extract_first()
        book_authors = list(response.xpath("//div[@class = 'authors']/ a[@data-event-label='author']/text()").extract())
        book_link = response.url
        book_price = response.xpath("//span[@class='buying-priceold-val-number']/text()").extract_first()
        book_sale_price = response.xpath("//span[@class='buying-pricenew-val-number']/text()").extract_first()
        item = BooksparserItem(title=book_title, authors=book_authors, link=book_link, price=book_price,
                               sale_price=book_sale_price)
        yield item
