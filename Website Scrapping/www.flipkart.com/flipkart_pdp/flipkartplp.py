import scrapy as sp
import pandas as pd
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlparse
from bs4 import BeautifulSoup

class FlipkartpdpSpider(sp.Spider):
    name = 'flipkartplp'
    main_url = 'https://www.flipkart.com/search?q=mobile&page='
    main_xpaths_df = pd.read_excel("xpath_flipkart_plp.xlsx")
    xpaths_df = dict(zip(main_xpaths_df['fields'],main_xpaths_df['xpath']))
    main_div_xpath = '('+xpaths_df['main_div']+')'
    del xpaths_df['main_div']
    output_data = []
    
    def start_requests(self):
        try:
          if(len(self.output_data)>0): self.output_data = []
        except: pass
        for i in range(3): yield sp.Request(self.main_url+str(i), callback=self.parse) 

    def parse(self, response):
        len_main_div = len(response.xpath(self.main_div_xpath).getall())
        data_lis = []
        for i in range(1,len_main_div+1):
            temp_dict = {}
            for k in self.xpaths_df:
                try:
                    product_xpath = self.main_div_xpath + str([i]) + self.xpaths_df[k]
                    if(k=='MRP'):
                        val = response.xpath(product_xpath + '/text()').getall()
                        mrp = ''
                        for v in val: mrp+=v
                        temp_dict.update({k: mrp})
                    elif(k=='DETAILS'):pass
                    elif(k=="IMG_URL"):
                        val = response.xpath(product_xpath).get()
                        temp_dict.update({k: val})
                    else:
                        val = response.xpath(product_xpath +  '/text()').get()
                        temp_dict.update({k: val if val!=None and val!='' else "None"})
                except: temp_dict.update({k: "***"})
            data_lis.append(temp_dict)
        self.output_data += data_lis
        pd.DataFrame(self.output_data).to_excel("FlipkartPLP_OutputData.xlsx",index=False)
        return data_lis    
     
process = CrawlerProcess(settings={'LOG_LEVEL': 'DEBUG',
                                   'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                                   'FEEDS': {"Flipkart_OutputData.csv": {'format': 'csv', 'overwrite': True}}
                                   })
process.crawl(FlipkartpdpSpider)
process.start()