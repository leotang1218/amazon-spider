# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    title = scrapy.Field()
    rating = scrapy.Field()
    rating_count = scrapy.Field()
    src_price = scrapy.Field()
    now_price = scrapy.Field()
    fin_price = scrapy.Field()
    asin = scrapy.Field()
    detail_url = scrapy.Field()
    thumbnail_url = scrapy.Field()
    variant = scrapy.Field()  # 变体数量
    first_rank = scrapy.Field()  # 第一类排名
    second_rank = scrapy.Field()  # 第二类排名
    third_rank = scrapy.Field()  # 第三类排名
    keyword = scrapy.Field()
