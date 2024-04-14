from typing import Iterable
import scrapy
import pandas as pd
from trafilatura import fetch_url, extract
from langchain_community.llms import Ollama

from langchain.prompts import PromptTemplate

from langchain.chains import LLMChain

class StockNewsSpider(scrapy.Spider):
    name = "stock_news"
    #allowed_domains = ["*"]
    start_urls = ["https://vip.stock.finance.sina.com.cn/corp/go.php/vCB_AllNewsStock/symbol/{c}.phtml"]
    stock_info_files = ['/home/userroot/dev/jiucai/crawl/tushare/300index.parquet']
    #['/home/userroot/dev/jiucai/crawl/tushare/sse_stock_info.parquet',
                        #'/home/userroot/dev/jiucai/crawl/tushare/sz_stocks_info.parquet']
    custom_settings = {
		'FEEDS': { 'data/stock_news.jsonl': { 'format': 'jsonl','overwrite': True}}
		}
    llm = Ollama(model="deepseek-llm:latest", timeout=360,num_predict=500,temperature=0, keep_alive = -1) #keep_alive=-1,
    # S = "<|im_start|>"
    # E = "<|im_end|>"
    # System_Message = "你是一个专业的财经新闻编辑，严格按照新闻内容进行采编。回答的时候直接给出内容，不要给建议，不要提问。"
    # #Q = "需要从下面的文字中提取关键信息\n\n{text_input}"
    # Q = "需要从下面的文字中提取关键的事实和判断\n{text_input}"

    # template = f"{S}system\n{System_Message}{E}\n" + f"{S}问题\n{Q}{E}\n" + f"{S}回答\n"

    # fact_extraction_prompt = PromptTemplate(
    #     input_variables=["text_input"],
    #     template=template
    # )
    # fact_extraction_chain = LLMChain(llm=llm, prompt=fact_extraction_prompt)

    def parse_list(self, response):
        #print('parse url start!')
        code = response.meta['code']

        date_list = [t.replace("\xa0", " ").strip() for t in response.css('.datelist ul::text').getall() if len(t.replace("\xa0", " ").strip())>1]
        url_list = response.css('.datelist ul a::attr(href)').getall()
        title_list = response.css('.datelist ul a')

        news_df = pd.DataFrame({'date':date_list, 'url':url_list, 'title':title_list})
        for idx, news in news_df.iterrows():
        # selector = response.css('.datelist ul a')[0]
            title = news['title'].css('::text').get()
            yield scrapy.Request(url=news['url'], callback=self.parse, meta={'title':title, 'date':news['date'],'code':code})
        next_pager = response.css('.datelist~ div a')
        for pager in next_pager:
            text = pager.css('::text').get()
            if text == '下一页':
                url = pager.css('::attr(href)').get()
                yield scrapy.Request(url=url,callback=self.parse_list,meta={'code':code})
    
    def parse(self, response):
        title = response.meta['title']
        #print(f'parse_content-----------------------------------------{title}')
        #yield scrapy.Request(url=, callback=self.parse_list)
        #date = response.css('.date::text').get()
        content = extract(response.text)
        #key_note = self.fact_extraction_chain.invoke(content)['text']

        #print(f'----content：{content}--------key_note：{key_note}-------------')
        #yield {'date':response.meta['date'],'code':response.meta['code'],'key_note':key_note,'content':content, 'title':response.meta['title']}
        yield {'date':response.meta['date'],'code':response.meta['code'],'content':content, 'title':response.meta['title']}


    def start_requests(self) :
        
        for file in self.stock_info_files:
            df = pd.read_parquet(file)
            df[['code','exchange']] = df['con_code'].str.split('.', expand=True)
            df['exchange'] = df['exchange'].apply(lambda x: x.lower())
            code = df[['exchange','code']].apply(''.join, axis=1)
            for c in code.values:
                url = self.start_urls[0].format(c=c)
                yield scrapy.Request(url, callback=self.parse_list, meta={'code':c})
                #break
            #break
        #return super().start_requests()