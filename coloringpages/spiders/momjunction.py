import scrapy
from itemloaders import ItemLoader
from scrapy import Request
from scrapy.http import Response

from ..items import ColoringPagesItem


class MomjunctionSpider(scrapy.Spider):
    name = 'momjunction'
    allowed_domains = ['www.momjunction.com']
    start_urls = ['https://www.momjunction.com/coloring-pics/']


    def parse(self, response):
        for category in response.css(".cat-item"):
            yield Request(category.css("a::attr(href)").get(), self.parse_category)

    def parse_category(self, response):
        color_items = response.css(".color-cat")
        for color_item in color_items:
            title = color_item.css("img::attr(title)").get()
            yield response.follow(
                color_item.css("a::attr(href)").get(),
                meta={"category": title},
                callback=self.parse_category_item
            )

    def parse_category_item(self, response: Response):
        return response.follow(
            response.css(".color-cat a::attr(href)").get(),
            callback=self.parse_images,
            meta={"category": response.meta.get("category")}
        )

    def parse_images(self, response):
        loader = ItemLoader(item=ColoringPagesItem(), selector=response, response=response)
        loader.add_value("category", response.meta.get("category"))
        loader.add_css("image_urls", "#slideshow .nopin.coloringwide.size-full::attr(src)")
        yield loader.load_item()
