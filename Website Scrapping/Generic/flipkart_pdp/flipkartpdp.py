import scrapy as sp
import pandas as pd
import json
from scrapy.crawler import CrawlerProcess

class FlipkartpdpSpider(sp.Spider):
    custom_settings = {
        # 'DOWNLOAD_DELAY': 1,  # minimum download delay
        # 'AUTOTHROTTLE_ENABLED': True,
    }
    # Global Flow 
    name = 'flipkartpdp'
    allowed_domains = ['flipkart.com']
    main_url = 'https://www.flipkart.com/vtexx-men-solid-casual-multicolor-shirt/p/itm25789d7c73ff6?pid='
    df_product_id = pd.read_excel("Product_ID.xlsx")
    urls,output_data = [],[]
    for id in df_product_id['product_id']: urls.append(main_url + id)
    df_xpaths = pd.read_excel('xpaths.xlsx')
    
    def start_requests(self):
        # for url in self.urls: yield sp.Request(url, callback=self.parse)
        for i in range(100): yield sp.Request(self.urls[i], callback=self.parse)
        
    id_index = 0
    def parse(self, response):
        pass
        temp_dict = {}
        try:
                temp_dict.update({"Product_ID":self.df_product_id['product_id'][self.id_index]})
                self.id_index += 1
                for i in range(len(self.df_xpaths)):
                    if(self.df_xpaths['name'][i]=='Main_Price'):
                        val = ''
                        for v in response.xpath((self.df_xpaths['xpath'][i] + '/text()')).getall(): val += v
                        temp_dict.update({self.df_xpaths['name'][i] : val if val!='' and val!=None else 'None'})
                    elif(self.df_xpaths['name'][i]=='Seller_Offers'): 
                        temp_lis = []
                        for val in response.xpath((self.df_xpaths['xpath'][i] + '/text()')).getall(): temp_lis.append(val)
                        temp_dict.update({self.df_xpaths['name'][i] : temp_lis if len(temp_lis)>0 else 'None'})
                    else: 
                        val = response.xpath((self.df_xpaths['xpath'][i] + '/text()')).get()
                        temp_dict.update({self.df_xpaths['name'][i] : val if val!='' and val!=None else 'None'})
        except: temp_dict.update({self.df_xpaths['name'][i]: '***'})
        self.output_data.append(temp_dict)
        return temp_dict 
    # if temp_dict['Product_Name']!='None' else {}
        
process = CrawlerProcess(settings={'LOG_LEVEL': 'DEBUG',
                                   'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                                   'FEEDS': {"OutputDataCSV.csv": {'format': 'csv', 'overwrite': True}}
                                   })
process.crawl(FlipkartpdpSpider)
process.start()

df = pd.read_csv('OutputDataCSV.csv')
df.to_excel("OutputDataExcell.xlsx", index=False)