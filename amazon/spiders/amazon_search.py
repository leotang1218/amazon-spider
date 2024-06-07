# -*- coding: utf-8 -*-
import configparser
import re
from urllib.parse import urljoin

import scrapy

from scrapy.utils.spider import logger

from amazon.utils import now_ts


class AmazonSearchSpider(scrapy.Spider):

    name = "amazon_search"

    def __init__(self, keyword: list, **kwargs: any):
        config = configparser.ConfigParser()
        # 读取配置文件
        config.read('./scrapy.cfg', encoding='utf8')
        self.cfg = config
        self.keyword = keyword
        self.ts = now_ts()
        self.domain = self.cfg["0Domain"]["using_domain"]
        logger.info(self.domain)
        super().__init__(**kwargs)

    def start_requests(self):
        page = 1
        amazon_search_url = f'https://{self.domain}/s?k={self.keyword}&page={page}&qid={self.ts}&ref=sr_pg_{page}'
        yield scrapy.Request(url=amazon_search_url, callback=self.parse_search_results,
                             meta={'keyword': self.keyword, 'page': page})

    def parse_search_results(self, response):
        page = response.meta['page']
        keyword = response.meta['keyword']
        logger.info(f"正抓取第 {page} 数据")

        search_products = response.xpath('//div[@data-component-type="s-search-result"]')
        for product in search_products[:1]:
            asin = product.xpath("@data-asin").get()
            detail_url = product.xpath('.//a[@class="a-link-normal s-no-outline"]/@href').get()
            title = product.xpath(".//span[@class='a-size-medium a-color-base a-text-normal']/text()").get()
            src_price_str = product.xpath(
                ".//span[@class='a-price a-text-price']/span[@aria-hidden='true']/text()").get()
            if src_price_str:
                src_price = round(float(str(src_price_str)[1:].replace(",", "")), 2)
            else:
                src_price = 0.0
            now_price_str = product.xpath(".//span[@class='a-price']/span[@class='a-offscreen']/text()").get()
            if now_price_str:
                now_price = round(float(str(now_price_str)[1:].replace(",", "")), 2)
            else:
                now_price = 0.0
            coupon_str = product.xpath(
                ".//span[@class='s-coupon-unclipped']/span[@class='a-size-base s-highlighted-text-padding aok-inline-block s-coupon-highlight-color']/text()").get()
            fin_price = now_price
            if coupon_str:
                if "$" in coupon_str:
                    coupon = float(str(coupon_str).replace("Save $", ''))
                    fin_price = round(float(now_price) - coupon, 2)
                elif "%" in coupon_str:
                    coupon = float(str(coupon_str).replace("Save", '').replace("%", ''))
                    fin_price = round(float(now_price) * ((100 - coupon) * 0.01), 2)
            rating_str = product.xpath(
                ".//a[@class='a-popover-trigger a-declarative']/i/span[@class='a-icon-alt']/text()").get()
            rating = "" if not rating_str else rating_str.split(" ")[0].replace(',', '.')
            rating_count_str = product.xpath(".//span[@class='a-size-base s-underline-text']/text()").get()
            rating_count = 0 if not rating_count_str else int(rating_count_str.replace(",", ""))
            thumbnail_url = product.xpath(
                ".//div[@class='aok-relative']/span/a/div[@class='a-section aok-relative s-image-fixed-height']/img[@class='s-image s-image-optimized-rendering']/@src").get()

            item = {
                "title": title,
                "rating": rating,
                "rating_count": rating_count,
                "src_price": src_price,
                "now_price": now_price,
                "fin_price": fin_price,
                "asin": asin,
                "detail_url": detail_url,
                "thumbnail_url": thumbnail_url,
                "variant": 0,   # todo
                "first_rank": "",
                "second_rank": "",
                "third_rank": "",
                "keyword": keyword,
            }

            yield item  # 如果不需要详情，这里就可以返回数据了
            # if detail_url:
            #     whole_url = urljoin(f"https://{self.domain}/", detail_url)
            #     logger.info(f"fetch detail url: {whole_url}")
            #     request = scrapy.Request(url=whole_url, callback=self.parse_detail)
            #     request.meta['item'] = item  # 将item传递给下一个页面的回调
            #     yield request
            # else:
            #     yield item

        available_pages = response.xpath(
            '//*[contains(@class, "s-pagination-item")][not(has-class("s-pagination-separator"))]/text()'
        ).getall()

        last_page = available_pages[-1]
        if last_page == "Next":
            return
        logger.info(f"现在页数：{page}, 最大页数：{last_page}")
        # 如果当前页大于等于最大页就结束了
        if page < int(last_page):
            next_page = page + 1
            amazon_search_url = f'https://{self.domain}/s?k={keyword}&page={next_page}&qid={self.ts}&ref=sr_pg_{next_page}'
            yield scrapy.Request(url=amazon_search_url, callback=self.parse_search_results,
                                 meta={'keyword': keyword, 'page': next_page})

    @staticmethod
    def _fetch_rank(s):
        pattern = r"#([\d,]+)"

        match = re.search(pattern, s)
        if match:
            number = match.group(1)
            return number
        return 0

    def parse_detail(self, response):
        item = response.meta['item']
        # 抓取详情页数据并合并
        # asin = response.xpath("//th[text()=' ASIN ']/following-sibling::*/text()").get()
        # if asin:
        #     asin = asin.strip()
        sell_rank_xp = response.xpath("//th[text()=' Best Sellers Rank ']/following-sibling::td[1]")
        sell_rank_list = sell_rank_xp.xpath("span/span")
        _sell_rank_list = []
        for sell_rank in sell_rank_list:
            rank = self._fetch_rank(str(sell_rank))
            cate = sell_rank.xpath("a/text()").get()
            if cate:
                cate = cate.replace("&amp;", "&")
                match = re.search(r"in\s(.+)", cate)
                if match:
                    cate = match.group(1)
            rank_str = f"{rank} in {cate}"
            _sell_rank_list.append(rank_str)

        first_rank = ''
        second_rank = ''
        third_rank = ''
        for i, rank in enumerate(_sell_rank_list):
            if i == 0:
                first_rank = rank
            if i == 1:
                second_rank = rank
            if i == 2:
                third_rank = rank

        var_parent = response.xpath(
            '//ul[@class="a-unordered-list a-nostyle a-button-list a-declarative a-button-toggle-group a-horizontal a-spacing-top-micro swatches swatchesSquare imageSwatches"]/li')
        variant = 1
        if len(var_parent) > 0:
            variant = len(var_parent)

        item['variant'] = variant
        item['first_rank'] = first_rank
        item['second_rank'] = second_rank
        item['third_rank'] = third_rank

        yield item