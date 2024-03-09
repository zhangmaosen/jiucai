import scrapy
import json
import os
import hydra
from omegaconf import DictConfig, OmegaConf

from hydra import compose, initialize

class ReportSummarySpider(scrapy.Spider):
    name = "report_summary"
    allowed_domains = ["dfcfw.com"]
    start_urls = ["http://dfcfw.com/"]

    url = 'https://data.eastmoney.com/report/zw_industry.jshtml'

    report_lists_file = 'reports_lists.txt' 
    file = None
    #report_lists_file = 'sample_lists.json' 
    path_no = 1
    pdf_cnt = 0
    pdf_per_path = 100

    def config_app(self) -> None:
        initialize(version_base=None, config_path="conf", job_name="test_app")
        cfg = compose(config_name="crawl_report_summary")
        print(OmegaConf.to_yaml(cfg))
        self.report_lists_file = cfg["urls_file_name"] if "urls_file_name" in cfg.keys() else self.report_lists_file

        
        #self.file =  open(self.lists_file_name, mode = 'r', encoding='utf8')

    def start_requests(self):
        self.config_app()
        os.makedirs(f'./summary/{self.path_no}', exist_ok=True)
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
        para = response.url.split('?')[-1]
        file_name = para.split('=')[-1] + ".html"

        self.logger.info('Saving Summary %s', file_name)
        if self.pdf_cnt < self.pdf_per_path:
            self.pdf_cnt += 1
        else:
            self.path_no += 1
            self.pdf_cnt = 0
            os.mkdir(f'./summary/{self.path_no}')

        p_path = "./summary/" + str(self.path_no) + '/' + file_name
        with open(p_path, 'wb') as file:
            file.write(response.body)
    
