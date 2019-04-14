# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ArticleSpider.items import TopshopItem, TopshopItemLoader
from ArticleSpider.utils.common import get_md5
from datetime import datetime

class TopshopSpider(CrawlSpider):
    name = 'topshop'
    allowed_domains = ['us.topshop.com']
    start_urls = ['http://us.topshop.com/']

    headers = {
        "HOST": "us.topshop.com",
        "Referer": "http://us.topshop.com/",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
    }

    rules = (
        Rule(LinkExtractor(allow=r'http://us.topshop.com/en/tsus/product/\d*'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item_loader = TopshopItemLoader(item=TopshopItem(), response=response)
        item_loader.add_css("id", ".product_code span::text")
        item_loader.add_css("title", "h1")
        item_loader.add_value("url", "response.url")
        item_loader.add_value("front_image_url", ".product_hero__image a::attr(href)")
        item_loader.add_css("brand", "")
        item_loader.add_css("website", "")
        item_loader.add_css("category", "")
        item_loader.add_css("price", "product_price::text")
        item_loader.add_css("tags", "product_colour span::text")
        item_loader.add_css("desc", "#productInfo p::text")
        item_loader.add_value("crawl_time", datetime.now())


        topshop_item = item_loader.load_item()
        # print(item_loader)

        return topshop_item
