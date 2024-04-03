import scrapy


class StockMorningSpider(scrapy.Spider):
    name = "stock_morning"
    allowed_domains = ["eastmoney.com"]
    start_urls = ["https://stock.eastmoney.com/a/czpnc_1.html"]


    def start_requests(self):
        urls = [
            "https://quotes.toscrape.com/page/1/",
            "https://quotes.toscrape.com/page/2/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self, response):
        pass
