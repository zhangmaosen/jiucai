import scrapy
import json

class FinNewsSpider(scrapy.Spider):
    name = "fin_news"
    allowed_domains = ["eastmoney.com"]
    start_urls = ["https://np-listapi.eastmoney.com/comm/web/getNewsByColumns?client=web&biz=web_news_col&column=1207&order=1&needInteractData=0&page_index={page_index}&page_size=20&req_trace=171&fields=code,showTime,title,mediaName,summary,image,url,uniqueUrl,Np_dst&types=1,20"]
    detail_news_url = "https://finance.eastmoney.com/a/{nid}.html"
    max_page_id = 18
    custom_settings = {
		'FEEDS': { 'data/news.jsonl': { 'format': 'jsonl',}}
		}
    def parse(self, response):
        for ele in response.css("#ContentBody p"):
            all_text = ''.join(ele.css("*::text").getall())
            if len(all_text) > 0:
                yield {'news' :''.join(ele.css("*::text").getall()),
                       'url': response.url}


    def parse_news(self, response):
        json_content = json.loads((response.body).decode(encoding='UTF-8',errors='strict'))
        for news in json_content['data']['list']:
            detail_url = self.detail_news_url.format(nid=news['code'])
            yield scrapy.Request(detail_url, callback=self.parse)

    def start_requests(self):
        for i in range(1,self.max_page_id+1):
            for url in self.start_urls:
                url_need = url.format(page_index = i)
                yield scrapy.Request(url_need, callback=self.parse_news)
                # json_content = json.loads((response.body).decode(encoding='UTF-8',errors='strict'))
                # for news in json_content['data']['list']:
                #     detail_url = self.detail_news_url.format(nid=news['code'])
                #     yield scrapy.Request(detail_url, callback=self.parse)

    
