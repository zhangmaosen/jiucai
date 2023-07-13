import scrapy
import json
import os

class ReportDetailSpider(scrapy.Spider):
    name = "report_detail"
    allowed_domains = ["dfcfw.com"]
    start_urls = ["http://dfcfw.com/"]

    url = 'https://data.eastmoney.com/report/zw_industry.jshtml'

    report_lists_file = 'reports_lists.txt' #'sample_lists.json' #

    path_no = 1
    pdf_cnt = 0
    pdf_per_path = 100

    def start_requests(self):
        os.mkdir(f'./pdf/{self.path_no}')
        with open(self.report_lists_file, mode='r', encoding='utf8') as file:
            while True:
                line = file.readline()
                if not line :
                    break

                data = json.loads(line)
                size = data["size"]
                data = data["data"]

                for i in range(0, size):
                    infor_code = data[i]["infoCode"]
                    print(f"infor_code is {infor_code}")
                    yield  scrapy.FormRequest(url=self.url, 
                                        formdata={'infocode':infor_code}, method='GET')
                

    def parse(self, response):
        h = response.css('.pdf-link').xpath("@href").get()
        print(f"pdf href is {h}")
        yield scrapy.Request(h, callback=self.save_pdf)
        pass
    
    def save_pdf(self, response):
        path = response.url.split('/')[-1]
        file_name = path.split('?')[-1]
        self.logger.info('Saving PDF %s', file_name)
        if self.pdf_cnt < self.pdf_per_path:
            self.pdf_cnt += 1
        else:
            self.path_no += 1
            self.pdf_cnt = 0
            os.mkdir(f'./pdf/{self.path_no}')

        p_path = "./pdf/" + str(self.path_no) + '/' + file_name
        with open(p_path, 'wb') as file:
            file.write(response.body)