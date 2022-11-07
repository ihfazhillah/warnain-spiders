import scrapy
from itemloaders import ItemLoader
from scrapy import Request

from ..items import ColoringPagesItem


class IheartcraftythingsSpider(scrapy.Spider):
    name = 'iheartcraftythings'
    allowed_domains = ['iheartcraftythings.com']
    start_urls = ['https://iheartcraftythings.com/coloring-for-toddlers-coloring-pages.html']

    def parse(self, response):
        next_url = response.css(".g1-nav-single-next>a::attr(href)").get()
        prev_url = response.css(".g1-nav-single-prev>a::attr(href)").get()
        if next_url and "coloring" in next_url:
            yield Request(next_url)
        if prev_url and "coloring" in prev_url:
            yield Request(prev_url)

        loader = ItemLoader(item=ColoringPagesItem(), selector=response)
        loader.add_css("category", ".entry-title::text")
        loader.add_css("image_urls", ".entry-content img.lazyload.size-full::attr(data-src)")
        yield loader.load_item()

