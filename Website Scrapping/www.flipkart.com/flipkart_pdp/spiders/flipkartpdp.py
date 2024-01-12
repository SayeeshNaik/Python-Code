import numpy as np
import pandas as pd
import scrapy as sp
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
# from IPython.display import HTML, display
import re
import time

class FlipkartpdpSpider(sp.Spider):
    name = 'flipkartpdp'
    allowed_domains = ['flipkart.com']
    custom_settings = {
        # 'DOWNLOAD_DELAY': 2,
        'AUTOTHROTTLE_ENABLED': True,
    }
    
    # Main URL 
    main_url = 'https://www.flipkart.com/vtexx-men-solid-casual-multicolor-shirt/p/itm25789d7c73ff6?pid='
    df_product_id = pd.read_excel("product.xlsx")
    urls,output_data = [],[]
    for id in df_product_id['product_id']: urls.append(main_url + id)
    df_xpaths = pd.read_excel('xpaths.xlsx')
    
    def start_requests(self):
        for url in self.urls: yield sp.Request(url, callback=self.parse)
        
    id_index = 0
    def parse(self, response):
        pass
        temp_dict = {}
        try:
                temp_dict.update({"product_id":self.df_product_id['product_id'][self.id_index]})
                self.id_index += 1
                for i in range(len(self.df_xpaths)):
                    if(self.df_xpaths['name'][i]=='main_price'):
                        val = ''
                        for v in response.xpath((self.df_xpaths['xpath'][i] + '/text()')).getall(): val += v
                        temp_dict.update({self.df_xpaths['name'][i] : val if val!='' and val!=None else '***'})
                    else: 
                        val = response.xpath((self.df_xpaths['xpath'][i] + '/text()')).get()
                        temp_dict.update({self.df_xpaths['name'][i] : val if val!='' and val!=None else '***'})
        except: temp_dict.update({self.df_xpaths['name'][i]: '***'})
        self.output_data.append(temp_dict)
        if(len(self.output_data)==len(self.df_product_id)):
            try:
                df_output = pd.DataFrame(self.output_data)
                df_output.to_excel('OutputData.xlsx')
            except:
                pass
                
        yield {"outputData ":self.output_data}
        
