import scrapy
import requests
import json

class ReportSpider(scrapy.Spider):
    name = "report"
    allowed_domains = ["data.eastmoney.com"]
    url = 'https://reportapi.eastmoney.com/report/list?cb=datatable1140573&industryCode=*&pageSize=50&industry=*&rating=*&ratingChange=*&beginTime=2021-06-19&endTime=2023-06-19&pageNo=3&fields=&qType=1&orgCode=&rcode=&p=3&pageNum=3&pageNumber=3&_=1687161492598'
    start_urls = ["http://data.eastmoney.com/"]
    page_size = 50
    begin_time = '2022-06-01'
    end_time = '2023-06-01'
    page_no = 1
    qtype = 1

    hits = 0

    total_page = None

    def start_requests(self):

        r_url = 'https://reportapi.eastmoney.com/report/list'
        payload = {'pageSize': str(self.page_size), 
                                           'beginTime':str(self.begin_time),
                                           'endTime':str(self.end_time),
                                           'pageNo':str(self.page_no),
                                           'qType':str(self.qtype)}
        r = requests.get(r_url, params=payload)
        data = (r.text) #.decode(encodin='utf8')
        data = json.loads(data)
        self.hits = data["hits"]
        print(f"hits is {self.hits}")

        total_pages = self.hits // self.page_size + 1
        print(f"total_pages is {total_pages}")

        for self.page_no in range(1, total_pages + 1):
            yield scrapy.FormRequest(url=r_url, 
                                    formdata={'pageSize': str(self.page_size), 
                                            'beginTime':str(self.begin_time),
                                            'endTime':str(self.end_time),
                                            'pageNo':str(self.page_no),
                                            'qType':str(self.qtype)}, method='GET')


        # urls = [
        #     'https://reportapi.eastmoney.com/report/list?cb=datatable1140573&industryCode=*&pageSize=50&industry=*&rating=*&ratingChange=*&beginTime=2021-06-19&endTime=2023-06-19'
        # ]
        # for url in urls:
        #     yield scrapy.Request(url=url, callback=self.parse)
    def parse(self, response):
        report_data = (response.body).decode(encoding='UTF-8',errors='strict')
        with open('reports_lists.txt', mode = 'a+', encoding='utf8') as file:
            file.writelines(report_data + '\n')
            #print(report_data)