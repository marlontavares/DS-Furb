# -*- coding: utf-8 -*-
import scrapy
import re


class BooksToscrapeComSpider(scrapy.Spider):
    name = 'books.toscrape.com'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        for book in response.css('.product_pod'):
            link = book.css('h3 a::attr(href)').get()
            yield scrapy.Request(response.urljoin(link), callback=self.parse_book)
        url = response.css('.pager .next a::attr(href)').get()
        if url:
           yield response.follow(url)

    def parse_book(self, book):
        name = book.css('h1::text').get()
        price = book.css('.price_color::text').get().replace('£', '')
        stars = book.css('.star-rating')[0].xpath("@class").extract()[0].replace('star-rating ', '')
        quantity = book.xpath('//table[@class="table table-striped"]/tr[6]/td/text()').extract_first()
        category = book.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").extract_first()
        list = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5}
        yield {'name': name,
               'price': float(price),
               'stars': list[stars.lower()],
               'quantity': int(re.sub("[^0-9]", "", quantity)),
               'category': category}

    # def parse(self, response):
    #     for book in response.css('.product_pod'):
    #         link = book.css('h3 a::attr(href)').get()
    #         name = book.css('h3 a::attr(title)').get()
    #         price = book.css('.price_color::text')[0].get().replace('£', '')
    #         stars = book.css('.star-rating')[0].xpath("@class").extract()[0].replace('star-rating ', '')
    #         list = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5}
    #         yield {'name': name,
    #                'price': float(price),
    #                'stars': list[stars.lower()],
    #                'link': link}
    #     url = response.css('.pager .next a::attr(href)').get()  
    #    # if url:
    #       #  yield response.follow(url)
