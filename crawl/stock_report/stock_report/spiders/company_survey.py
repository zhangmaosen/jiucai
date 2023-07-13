import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import requests
import json
import os

class CompanySurveySpider(CrawlSpider):
    path = ''
    _page_num = 1
    total_page_size = 0
    page_size = 50
    name = "company_survey"
    allowed_domains = ["eastmoney.com"]
    start_urls = ["http://eastmoney.com/"]
    url = 'https://datacenter-web.eastmoney.com/api/data/v1/get?sortColumns=NOTICE_DATE%2CSUM%2CRECEIVE_START_DATE%2CSECURITY_CODE&sortTypes=-1%2C-1%2C-1%2C1&reportName=RPT_ORG_SURVEYNEW&columns=SECUCODE%2CSECURITY_CODE%2CSECURITY_NAME_ABBR%2CNOTICE_DATE%2CRECEIVE_START_DATE%2CRECEIVE_PLACE%2CRECEIVE_WAY_EXPLAIN%2CRECEPTIONIST%2CSUM&quoteColumns=f2~01~SECURITY_CODE~CLOSE_PRICE%2Cf3~01~SECURITY_CODE~CHANGE_RATE&quoteType=0&source=WEB&client=WEB&filter=(NUMBERNEW%3D%221%22)(IS_SOURCE%3D%221%22)(RECEIVE_START_DATE%3E%272020-07-09%27)'


    def start_requests(self):


        path = "survey_lists/"
        # Check whether the specified path exists or not
        isExist = os.path.exists(path)
        if not isExist:

        # Create a new directory because it does not exist
            os.makedirs(path)
        
        self.path = path
        print("The survey lists data path is created!")


        r_url = self.url 
        payload = {'pageSize': str(self.page_size), 
                                           'pageNumber':str(self._page_num)}
        r = requests.get(r_url, params=payload)
        data = (r.text) #.decode(encodin='utf8')
        data = json.loads(data)
        print(f'data is ' + str(data['result']['pages']))

        self.total_page_size = data['result']['pages']

        for self._page_num in range(1, self.total_page_size+1):
            from requests.models import PreparedRequest
            url = self.url
            params = {'pageSize':str(self.page_size),'pageNumber':str(self._page_num)}
            req = PreparedRequest()
            req.prepare_url(url, params)
            
            url = req.url

            print(f'get url {url}')
            
            yield scrapy.Request(url=url, callback=self.parse)
        

    def parse(self, response):
        lists_data = (response.body).decode(encoding='UTF-8',errors='strict')
        with open(self.path + 'survey_lists.txt', mode = 'a+', encoding='utf8') as file:
            file.writelines(lists_data + '\n')
            print(lists_data)

