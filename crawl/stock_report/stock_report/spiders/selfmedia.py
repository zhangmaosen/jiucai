import scrapy


class SelfmediaSpider(scrapy.Spider):
    name = "selfmedia"
    allowed_domains = ["eastmoney.com"]
    start_urls = ["http://eastmoney.com/"]

    
    def parse(self, response):
        pass
