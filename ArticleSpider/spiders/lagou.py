# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ArticleSpider.items import LagouJobItemLoader, LagouJobItem
from ArticleSpider.utils.common import get_md5
from datetime import datetime

# shut down and s=restart
'''
scrapy crawl lagou -s JOBDIR=job_info/001
control c shut down
scrapy crawl lagou -s JOBDIR=job_info/001 restart
start another one
scrapy crawl lagou -s JOBDIR=job_info/002

'''

class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['http://www.lagou.com/']

    headers = {
        "HOST": "www.laogu.com",
        "Referer": "https://www.lagou.com",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
    }
    rules = (
        Rule(LinkExtractor(allow=("zhaopin/.*",)), follow=True),
        Rule(LinkExtractor(allow=("gongsi/j\d+.html",)), follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),
    )


    def parse_job(self, response):
        print("start")
        print(response.css('body::text'))
        item_loader = LagouJobItemLoader(item=LagouJobItem(), response=response)
        item_loader.add_css("title", ".job-name::attr(title)")
        item_loader.add_value("url", "response.url")
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("salary", ".job_request .salary::text")
        item_loader.add_xpath("job_city", "/html/body/div[2]/div/div[1]/dd/p[1]/span[2]/text()")
        item_loader.add_xpath("work_years", "/html/body/div[2]/div/div[1]/dd/p[1]/span[3]/text()")
        item_loader.add_xpath("degree_need", "/html/body/div[2]/div/div[1]/dd/p[1]/span[4]/text()")
        item_loader.add_xpath("job_type", "/html/body/div[2]/div/div[1]/dd/p[1]/span[5]/text()")
        item_loader.add_css("tags", ".position-label li::text")
        item_loader.add_css("publish_time", ".publish_time::text")
        item_loader.add_css("job_advantage", ".job-advantage::text")
        item_loader.add_css("job_desc", ".job-detail::text")
        item_loader.add_css("job_addr", ".work_addr")
        item_loader.add_css("company_name", "#job_company dt a img::attr(alt)")
        item_loader.add_css("company_url", "#job_company dt a::attr(href)")
        item_loader.add_value("crawl_time", datetime.now())

        job_item = item_loader.load_item()
        # print(item_loader)

        return job_item
