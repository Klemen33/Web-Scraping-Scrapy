# import scrapy
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor

from time import sleep
from scrapy import Spider
from scrapy.http.request import Request
from selenium import webdriver
from scrapy.selector import Selector
from selenium.common.exceptions import NoSuchElementException



# class BooksSpider(CrawlSpider):
#     name = 'books'
#     allowed_domains = ['books.toscrape.com']
    # start_urls = ['http://books.toscrape.com/']

    # rules = (Rule(LinkExtractor(deny_domains=('google.com')), callback='parse_page', follow=False),)

    # def parse_page(self, response):
    #     yield {'URL': response.url}

class BooksSpider(Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']

    def start_requests(self):
        self.driver = webdriver.Chrome('F:\z Self Learn\Scrapy\chromedriver')
        self.driver.get('http://books.toscrape.com')

        sel = Selector(text=self.driver.page_source)
        books = sel.xpath('//h3/a/@href').extract()

        for book in books:
            url = 'http://books.toscrape.com/' + book
            yield Request(url, callback=self.parse_book)

        # return super().start_requests()

        while True:
            try:
                next_page = self.driver.find_element_by_xpath('//a[text()="next"]')
                sleep(5)
                self.logger.info('Sleeping for 5 seconds.')
                next_page.click()

                sel = Selector(text=self.driver.page_source)
                books = sel.xpath('//h3/a/@href').extract()

                for book in books:
                    url = 'http://books.toscrape.com/catalogue/' + book
                    yield Request(url, callback=self.parse_book)

            except NoSuchElementException:
                self.logger.info('No more pages to load.')
                self.driver.quit()
                break

    def parse_book(self, response):
        pass