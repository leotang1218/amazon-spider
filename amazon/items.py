# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    keyword = scrapy.Field()
    asin = scrapy.Field()
    url = scrapy.Field()
    ad = scrapy.Field()
    title = scrapy.Field()
    src_price = scrapy.Field()
    now_price = scrapy.Field()
    rating = scrapy.Field()
    rating_count = scrapy.Field()
    thumbnail_url = scrapy.Field()
