import re
from urllib.parse import urljoin
from scrapy.http import HtmlResponse


def parse_search_results(response):
    page = 1
    keyword = 'messerset mit block schwarz'

    search_products = response.xpath('//div[@data-component-type="s-search-result"]')
    for product in search_products:
        # print(product)
        asin = product.xpath("@data-asin").get()
        relative_url = product.xpath('.//a[@class="a-link-normal s-no-outline"]/@href').get()
        whole_url = urljoin("https://www.amazon.de/", relative_url)
        title = product.xpath(".//span[@class='a-size-base-plus a-color-base a-text-normal']/text()").get()
        src_price = product.xpath(".//span[@class='a-price a-text-price']/span[@aria-hidden='true']/text()").get()
        now_price_xp = product.xpath(".//span[@class='a-price']/span[@class='a-offscreen']/text()").get()
        now_price = re.sub(r'\s+', '', now_price_xp)
        rating_xp = product.xpath(".//i[@class='a-icon a-icon-star-small a-star-small-4 aok-align-bottom' or @class='a-icon a-icon-star-small a-star-small-4-5 aok-align-bottom']/span[@class='a-icon-alt']/text()").get()
        if title == "Klarstein Kitano - Messer-Set, Messerblock, 8-teilig, Präzisionsklingen, Rostfreier Edelstahl, Holzblock, Schwarz":
            print(f"rating: {rating_xp}")
        rating = "" if not rating_xp else rating_xp.split(" ")[0].replace(',', '.')
        rating_count = product.xpath(".//span[@class='a-size-base s-underline-text']/text()").get()
        rating_count = 0 if not rating_count else rating_count.replace(",", "")
        thumbnail_url = product.xpath(".//div[@class='a-section aok-relative s-image-square-aspect']/img[@class='s-image']/@src").get()

        detail = {
            "keyword": keyword,
            "asin": asin,
            "url": whole_url,
            "ad": True if "/slredirect/" in whole_url else False,
            "title": title,
            "price": src_price,
            "real_price": now_price,
            "rating": rating,
            "rating_count": rating_count,
            "thumbnail_url": thumbnail_url,
        }
        if title == "Gerlach Deco Black Messerblock Messerset Küchenmesserset 5 Messer aus Edelstahl Buchenholz Küchenmesser im Block Kochmesser Brotmesser Gemüsemesser Küche Küchenutensilien Küchenzubehör, Schwarz":
            print(detail)
    #     yield detail

    # if page != 1:
    #     return
    # available_pages = response.xpath(
    #     '//*[contains(@class, "s-pagination-item")][not(has-class("s-pagination-separator"))]/text()'
    # ).getall()
    #
    # last_page = available_pages[-1]
    # print("最大页数：", last_page)
    # for page_num in range(2, int(last_page)):
    #     amazon_search_url = f'https://www.amazon.com/s?k={keyword}&page={page_num}'
    #     yield scrapy.Request(url=amazon_search_url, callback=self.parse_search_results,
    #                          meta={'keyword': keyword, 'page': page_num})


if __name__ == '__main__':
    url = 'http://www.example.com'

    with open("../test.html", "r", encoding='utf-8') as rf:
        content = rf.read()
        response = HtmlResponse(url=url, body=content, encoding='utf-8')
        parse_search_results(response)
