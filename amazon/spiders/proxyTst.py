# -*- coding: utf-8 -*-
import configparser
import re

import scrapy
from urllib.parse import urljoin


# messerset mit block schwarz
from scrapy.utils.spider import logger


class ProxyTstSpider(scrapy.Spider):

    name = "proxy"

    allowed_domains = ['test.com']
    start_urls = ['http://httpbin.org/ip']  # 修改start_url，默认会返回request的IP

    def parse(self, response):
        print(response.text)
