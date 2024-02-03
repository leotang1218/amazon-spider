# -*- coding: utf-8 -*-
import configparser
import re

import scrapy
from urllib.parse import urljoin


# messerset mit block schwarz
from scrapy.utils.spider import logger


class AmazonSearchSpider(scrapy.Spider):

    name = "amazon_search"

    def __init__(self, keyword: list, **kwargs: any):
        config = configparser.ConfigParser()
        # 读取配置文件
        config.read('./scrapy.cfg', encoding='utf8')
        self.cfg = config
        self.keyword = keyword
        self.domain = self.cfg["0Domain"]["using_domain"]
        logger.info(self.domain)
        super().__init__(**kwargs)

    def start_requests(self):
        amazon_search_url = f'https://{self.domain}/s?k={self.keyword}&page=1'
        yield scrapy.Request(url=amazon_search_url, callback=self.parse_search_results,
                             meta={'keyword': self.keyword, 'page': 1})

    def parse_search_results(self, response):
        page = response.meta['page']
        keyword = response.meta['keyword']

        search_products = response.xpath('//div[@data-component-type="s-search-result"]')
        for product in search_products:
            asin = product.xpath("@data-asin").get()
            relative_url = product.xpath('.//a[@class="a-link-normal s-no-outline"]/@href').get()
            whole_url = urljoin(f"https://{self.domain}/", relative_url)
            title = product.xpath(".//span[@class='a-size-base-plus a-color-base a-text-normal']/text()").get()
            src_price = product.xpath(".//span[@class='a-price a-text-price']/span[@aria-hidden='true']/text()").get()
            now_price_xp = product.xpath(".//span[@class='a-price']/span[@class='a-offscreen']/text()").get()
            now_price = re.sub(r'\s+', '', now_price_xp)
            rating_xp = product.xpath(".//i[@class='a-icon a-icon-star-small a-star-small-4 aok-align-bottom' or @class='a-icon a-icon-star-small a-star-small-4-5 aok-align-bottom']/span[@class='a-icon-alt']/text()").get()
            rating = "" if not rating_xp else rating_xp.split(" ")[0].replace(',', '.')
            rating_count = product.xpath(".//span[@class='a-size-base s-underline-text']/text()").get()
            rating_count = 0 if not rating_count else  rating_count.replace(",", "")
            thumbnail_url = product.xpath(".//div[@class='a-section aok-relative s-image-square-aspect']/img[@class='s-image']/@src").get()

            detail = {
                "keyword": keyword,
                "asin": asin,
                "url": whole_url,
                "ad": True if "/slredirect/" in whole_url else False,
                "title": title,
                "src_price": src_price,
                "now_price": now_price,
                "rating": rating,
                "rating_count": rating_count,
                "thumbnail_url": thumbnail_url,
            }
            # logger.info(f"产品项：{detail}")
            yield detail

        if page != 1:
            return
        # available_pages = response.xpath(
        #     '//*[contains(@class, "s-pagination-item")][not(has-class("s-pagination-separator"))]/text()'
        # ).getall()
        #
        # last_page = available_pages[-1]
        # logger.info("最大页数：%s", last_page)
        # for page_num in range(2, int(last_page)):
        #     amazon_search_url = f'https://{self.domain}/s?k={keyword}&page={page_num}'
        #     yield scrapy.Request(url=amazon_search_url, callback=self.parse_search_results,
        #                          meta={'keyword': keyword, 'page': page_num})
