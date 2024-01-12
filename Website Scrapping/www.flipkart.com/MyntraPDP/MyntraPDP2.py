import scrapy as sp
import pandas as pd
import datetime
from requests_html import HTMLSession
import re
import json
from cleantext import clean
from urllib.parse import urlparse
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from selenium.webdriver.common.by import By

main_url = "https://www.myntra.com/"
exception_id = []
exception_url = []
trying_url = []

class MyntrapdpSpider(sp.Spider):
    
    # Global Flow 
    name = 'myntra'
    main_url = "https://www.myntra.com/"
    productId_df = pd.read_excel("MyntraPDP_ProductID.xlsx")
    productId_df['Product_ID'] = main_url + productId_df['Product_ID'].astype(str)
    all_urls = productId_df['Product_ID']
    all_urls = ["https://www.myntra.com/18974370"]
    # all_urls = ["https://www.myntra.com/18652620"]
  
    
    def start_requests(self):
        pass
        for url in self.all_urls:
          yield sp.Request(url,callback=self.parse)        
        
    def parse(self, response):
        main_page = str(response.body)
        start_string = '{"pdpData'
        json_start = main_page.find(start_string)
        main_page = main_page[json_start:]
        ending = main_page.find("</script>")
        json_string = main_page[0:ending].replace( "\\\\", "")
        json_data=clean(json_string, no_emoji=True)
        json_data = json.loads(json_data)
        with open('myntrapdp.txt','w') as f:
            f.write(json_string)
        json_data = json_data['pdpdata']
        logical_df = {'Product ID':json_data['id'],'Brand':json_data['brand']['name'],'Title':json_data['name'],'MRP': json_data['price']['mrp'],
                      'Selling Price':json_data['price']['discounted'],'Discount %':json_data['discounts'][0]['discountpercent'],'Product Ratings':json_data['ratings']['averagerating'],
                      'Total Sizes':json_data['sizes'],'In Stock':json_data['flags']} 
        
        temp_dict = {}
        for key in logical_df:
            try:
                if(key=='Title'):
                    val = logical_df[key]
                    if(type(val)==str): val = val.title()
                    if temp_dict['Brand'] in val: val = val.replace(temp_dict['Brand'],'')
                 
                elif(key=='Total Sizes'):
                    
                    val = logical_df[key]
                    available_sizes = []
                    non_available_sizes = []
                    for size_dict in val:
                        if(size_dict['available']==True):
                            available_sizes.append(size_dict['label'])
                        else: non_available_sizes.append(size_dict['label'])
                    total_sizes = available_sizes+non_available_sizes
                    temp_dict.update({'No of Total Sizes': len(total_sizes),'Total Sizes': [total_sizes]})
                    temp_dict.update({'No Available Sizes':len(available_sizes),'Available Sizes':[available_sizes]})
                    temp_dict.update({'No Non Available Sizes':len(non_available_sizes),'Non Available Sizes':[non_available_sizes]})
                # elif(key=='In Stock'):
                #     val = logical_df[key]
                #     temp_dict({key: 'In Stock' if val==False else 'Out Of Stock'})
                else:
                    val = logical_df[key]
            except: val = ''
            if(key!='Total Sizes' and key!='In Stock'):
                temp_dict.update({key:val.title() if type(val)==str else val})
        
        # Filtration 
        temp_dict['Product Ratings'] = round(temp_dict['Product Ratings'],1)

       
        return temp_dict

      
process = CrawlerProcess(settings={'LOG_LEVEL': 'DEBUG',
                                   'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                                   'FEEDS': {"MyntraPDP_Data.csv": {'format': 'csv', 'overwrite': True}}
                                   })
process.crawl(MyntrapdpSpider)
process.start() 

main_df = pd.read_csv("MyntraPDP_Data.csv")
main_df.to_excel("MyntraPDP_Data.xlsx",index=False)
