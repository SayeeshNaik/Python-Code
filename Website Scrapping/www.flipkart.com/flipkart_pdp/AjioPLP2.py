import scrapy as sp
import pandas as pd
import datetime
import time
import re
import json
from cleantext import clean
from urllib.parse import urlparse
from scrapy.crawler import CrawlerProcess

main_url = "https://www.myntra.com/"
exception_id = []
exception_url = []
trying_url = []
main_output_data = []

class AjioPLPSpider(sp.Spider):
    # custom_settings = {
    #     'DOWNLOAD_DELAY': 2 # 2 seconds of delay
    #     }
    
    # Global Flow 
    name = 'myntraplp'
    main_url = "https://www.ajio.com/"
    keyname = ['men tshirt']
    all_urls = ''
    def start_requests(self):
        pass
        for page_num in range(1,2):
            for url in self.all_urls:
                url = url+'?p={}'.format(page_num)
                yield sp.Request(url,callback=self.parse)        
        
    def parse(self, response):
       
        return {}
        

      
process = CrawlerProcess(settings={'LOG_LEVEL': 'DEBUG',
                                   'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                                   'FEEDS': {"MyntraPLP_Data.csv": {'format': 'csv', 'overwrite': True}}
                                   })
process.crawl(AjioPLPSpider)
process.start() 

try:
    main_df = pd.read_csv("MyntraPLP_Data.csv")
    main_df.to_excel("MyntraPLP_Data.xlsx",index=False)
except: pass