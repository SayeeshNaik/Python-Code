

import numpy as np
import pandas as pd
import scrapy as sp
from scrapy.crawler import CrawlerProcess
import datetime
# from scrapy.utils.project import get_project_settings
# from IPython.display import HTML, display
import re
import time

main_output_df = pd.DataFrame()

class AmazonPlpSpider(sp.Spider):
    name = 'amazon_plp'
    # custom_settings = {
    #     'DOWNLOAD_DELAY': 2,  # minimum download delay
    #     'AUTOTHROTTLE_ENABLED': True,
    # }
    
    df = pd.read_excel("AmazonPDP_ID.xlsx", sheet_name='Amazon')
    listings = list(df["Item Code"])

    df = pd.read_excel("xpath_amazon_pdp.xlsx", index_col=0)
    df.dropna(inplace=True)
    xpaths = {}
    for i in df.index.values:
        temp = {i: df.loc[i]["xpaths"]}
        xpaths.update(temp)
        
    print("xxxxxxx = ",xpaths)

    print("ASINs:", len(listings))
    # print("XPATHs - ")
    # print(xpaths, "/n")

    json_list = []
    output_data = []
    exp_lis = []

    def start_requests(self):

        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
        # }
 
        num_pages = 50
        
        try:
            exp_df = pd.read_excel("Exp_ID.xlsx")
            exp_df = exp_df['Exp_ID']
            exp_lis = []
            for id in exp_df: exp_lis.append(id)   
            last_output_df = pd.read_excel("AmazonPDP_AllData.xlsx") 
            print("kkkkkkkkkkkkkkkkkkkk = ",len(last_output_df))
            
            if(len(exp_lis)>0):
                for product_ID in exp_lis:
                    myurl = '''https://www.amazon.in/dp/{0}?th=1&psc=1'''.format(str(product_ID))
                    yield sp.Request(url=myurl, callback=self.parse)
                try:
                    recent_output_df = pd.read_excel("AmazonPDP_OutputData.xlsx")
                    main_output_df = pd.concat([last_output_df,recent_output_df])
                    len_output_df = pd.read_excel("AmazonPDP_AllData.xlsx")
                    # if(len_output_df<=num_pages):
                    main_output_df.to_excel("AmazonPDP_AllData.xlsx",index=False)
                except: pass
                
            else:
                print("SSSSSSSSSSSSTTTTTTTTTTTTTOOOOOOOOOOOOOPPPPPPPPPPPPPPPPP")
            
                # empty_df = pd.read_excel("AmazonPDP_AllData.xlsx")
                # empty_df.drop(empty_df.index,inplace=True)
                
                for i in self.listings[0:num_pages]:                        
                    myurl = '''https://www.amazon.in/dp/{0}?th=1&psc=1'''.format(str(i))
                    yield sp.Request(url=myurl, callback=self.parse)
                    
        except: 
            
             for i in self.listings[0:num_pages]:                        
                myurl = '''https://www.amazon.in/dp/{0}?th=1&psc=1'''.format(
                    str(i))
                yield sp.Request(url=myurl, callback=self.parse)
                
                
        # *************************************************************************************
                            
            # exp_df = pd.read_excel("Exp_ID.xlsx")
            # exp_df = exp_df['Exp_ID']
            # exp_lis = []
            # for id in exp_df: exp_lis.append(id)
            # print('eeeeeeee =',exp_lis)
            # for i in exp_lis:
            #     myurl = '''https://www.amazon.in/dp/{0}?th=1&psc=1'''.format(
            #     str(i))
            #     yield sp.Request(url=myurl, callback=self.parse)
        
                
        # for i in self.listings[0:num_pages]:                        
        #         myurl = '''https://www.amazon.in/dp/{0}?th=1&psc=1'''.format(
        #             str(i))
        #         yield sp.Request(url=myurl, callback=self.parse)

    def parse(self, response):
        product_id = response.url.split('https://www.amazon.in/dp/')[1].split('?')[0]
                
        temp_dict = {}
        for k in self.xpaths:
            temp_dict.update({"Base_URL": response.url})
            temp_dict.update({"Product_ID": product_id})
            val = response.xpath(self.xpaths[k]).get()
            temp_dict.update({k: val})
        
        pd.DataFrame({"Exp_ID":self.exp_lis}).to_excel("Exp_ID.xlsx",index=False)
        try:
                if(temp_dict['TITLE']==None): 
                    self.exp_lis.append(product_id)
                    self.exp_lis = list(set(self.exp_lis))
                else: 
                    self.output_data += [temp_dict]
                    return temp_dict
        except: 
             self.output_data += [temp_dict]
        
        print("EEEEEEEEEEEEEEEEE  =  ",self.exp_lis)
        
process = CrawlerProcess(settings={'LOG_LEVEL': 'DEBUG',
                                'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                                'FEEDS': {"AmazonPDP_OutputData.csv": {'format': 'csv', 'overwrite': True}}
                                })

process.crawl(AmazonPlpSpider)
process.start()

df = pd.read_csv('AmazonPDP_OutputData.csv')
df.to_excel("AmazonPDP_OutputData.xlsx", index=False)
Del_df = pd.read_excel("AmazonPDP_AllData.xlsx")
if(len(Del_df)==0):
    df.to_excel("AmazonPDP_AllData.xlsx",index=False)

# Del_df.drop(Del_df.index, inplace=True)


