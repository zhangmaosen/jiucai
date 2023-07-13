import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import json
import urllib.parse
import os
import threading

class CompanySurveyDetailsSpider(CrawlSpider):
    page_num = 0
    page_size = 1000
    path = ''
    content_list = []
    name = "company_survey_details"
    allowed_domains = ["eastmoney.com"]
    file_name = 'survey_lists/survey_lists.txt'
    #https://data.eastmoney.com/jgdy/dyxx/000729,2023-07-07.html
    #url = 'https://data.eastmoney.com/jgdy/dyxx/'
    #
    url = '''https://datacenter-web.eastmoney.com/api/data/v1/get?reportName=RPT_ORG_SURVEY&columns=SECUCODE%2CSECURITY_CODE%2CSECURITY_NAME_ABBR%2CNOTICE_DATE%2CRECEIVE_START_DATE%2CRECEIVE_END_DATE%2CRECEIVE_OBJECT%2CRECEIVE_PLACE%2CRECEIVE_WAY_EXPLAIN%2CINVESTIGATORS%2CRECEPTIONIST%2CNUM%2CCONTENT%2CORG_TYPE&quoteColumns=&source=WEB&client=WEB&sortColumns=NUMBERNEW&sortTypes=1'''
    def start_requests(self):
        path = "survey_contents/"
        # Check whether the specified path exists or not
        isExist = os.path.exists(path)
        if not isExist:
        # Create a new directory because it does not exist
            os.makedirs(path)

        self.path = path

        with open(self.file_name, mode='r',encoding='utf8') as file:
            while True:
                line = file.readline()
                if not line :
                    break
                
                j_data = json.loads(line)
                
                surveys = j_data['result']['data']

                for i in surveys:
                    code = i['SECURITY_CODE']
                    date = i['RECEIVE_START_DATE'].split(' ')[0]

                    #print(f'code is {code}, data is {date}')
                    params = str(code) + ','+str(date)+'.html'

                    
                    code = "(SECURITY_CODE=" +"\""+str(code)+ "\")"
                    date = "(RECEIVE_START_DATE=" + "\'" + str(date) + "\')"
                    filter = '(IS_SOURCE="1")' + code + date

                    filter = urllib.parse.quote(filter)
                    url = self.url + '&filter=' + filter
                    #print(f'filter is {filter}')
                    #print(f'url is {url}')

                    yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        content_data = (response.body).decode(encoding='UTF-8',errors='strict')
        self.content_list.append(content_data)
        ending = hash(response.url) % 25
        with open(self.path + 'survey_contents_' +str(ending)+'.txt', mode = 'a+', encoding='utf8') as file:
            file.writelines(content_data + '\n')
            #print(content_data)
        

