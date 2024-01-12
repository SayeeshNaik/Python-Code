import scrapy as sp
import pandas as pd
import datetime
import re
import json
from cleantext import clean
from urllib.parse import urlparse
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests

Pincode = ''
Glob_Exception_ID = []

class AjioPinCodeSpider(sp.Spider):
    custom_settings = {
    #     'DOWNLOAD_DELAY': 1,
    #     'AUTOTHROTTLE_ENABLED': True,
    'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
    }
    
    # Global Flow 
    name = 'ajiopincode'
    main_url = "https://www.ajio.com/p/"
    productId_df = pd.read_excel("Ajio_ProductID.xlsx")
    productId_df['Product_ID'] = main_url + productId_df['Product_ID'].astype(str)
    all_urls = list(productId_df['Product_ID'])
    Pincodes = [581355,581200]
    all_urls = all_urls[306:310]
    # all_urls = ["https://www.ajio.com/p/464589326001"] 
    Exception_ID = []
    
    def start_requests(self):
        for pincode in self.Pincodes:
            for url in self.all_urls: yield sp.Request(url, callback=self.parse, meta={'handle_httpstatus_all': True,'Pincode':pincode}) 
                
        
    def parse(self, response):
        global Pincode,Glob_Exception_ID
        Pincode = str(response.meta['Pincode'])
        page_source = str(response.body)
        start = '''{"wishlist"'''
        end = '''"unRatedProducts":'''
        start_index = page_source.find(start)
        end_index = page_source.find(end)
        product_data = page_source[start_index:end_index+len(end)]
        product_str_data = product_data+'''""}}'''
        product_str_data = clean(product_str_data, no_emoji=True,lower=False)
        product_str_data = product_str_data.replace("\'","'")
        with open('AjioPincode.txt','w') as f:
             f.write(product_str_data)
        try:
            json_data = json.loads(product_str_data)
            json_data = json_data['product']['productDetails']
            product_details = json_data['variantOptions']
            product_details = [{product_code['code']:product_code['scDisplaySize']} for product_code in product_details]
            product_col = ['Product ID','Pincode','Brand','Title','MRP','Selling Price','Discount %']
            temp_dict = {}
            temp_dict.update({"Date": datetime.date.today().strftime("%Y-%m-%d")})
            temp_dict.update({"Week": datetime.datetime.today().weekday()})
            temp_dict.update({"Marketplace": urlparse(response.url).netloc.replace('www.','').replace('.com','').title()})
            temp_dict.update({"Product URL": response.url})
            for key in product_col:
                try:
                    if(key=='Product ID'): val = json_data['baseOptions'][0]['options'][0]['code']
                    elif(key=='Pincode'): val = Pincode
                    elif(key=='Brand'): val = json_data['categories'][0]['code'].replace('-',' ').title()
                    elif(key=='Title'): val = json_data['baseOptions'][0]['options'][0]['modelImage']['altText']
                    elif(key=='MRP'): val = json_data['wasPriceData']['value']
                    elif(key=='Selling Price'): val = json_data['baseOptions'][0]['options'][0]['priceData']['value']
                    elif(key=='Discount %'): val = int(json_data['baseOptions'][0]['options'][0]['priceData']['discountValue'])
                except: val = ''
                temp_dict.update({key: val})
                val = ''
            # Filtering Discount Data
            if(temp_dict['MRP']==temp_dict['Selling Price']): temp_dict['Discount %'] = ''
            temp_delivary_details = {}
            for details in product_details:
                product_code = list(details.keys())[0]
                product_size = list(details.values())[0]
                pinCode_URL = "https://login.web.ajio.com/api/edd/checkDeliveryDetails?productCode={}&postalCode={}&quantity=1&IsExchange=false".format(product_code,Pincode)
                pincode_res = requests.get(pinCode_URL)
                pincode_data = json.loads(pincode_res.content)
                details_val = 'No Service'
                if(pincode_data['codEligible']==True):
                    date = pincode_data['productDetails'][0]['eddUpper']
                    date = date.split('T')[0].split('-')
                    date = list(map(int,date))
                    month = datetime.date(date[0],date[1],date[2]).strftime('%b')
                    details_val = str(date[-1]) + " {}".format(month)
                temp_delivary_details.update({product_size: details_val})
            inStock_val = list(temp_delivary_details.values()).count('No Service')!=len(temp_delivary_details)
            temp_dict.update({'Estimated Delivery Date':temp_delivary_details if inStock_val else "No Service"})
            temp_dict.update({'In Stock': "Yes" if inStock_val else "No"})
            
            return temp_dict
                
        except: 
            Glob_Exception_ID.append(response.url.split(self.main_url)[1].split('?')[0])
            Glob_Exception_ID = list(set(Glob_Exception_ID))
      
process = CrawlerProcess(settings={'LOG_LEVEL': 'DEBUG',
                                   'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                                   'FEEDS': {"AjioPincode_OutputData.csv": {'format': 'csv', 'overwrite': True}}
                                   })
process.crawl(AjioPinCodeSpider)
process.start() 

try:
    main_df = pd.read_csv("AjioPincode_OutputData.csv")
    main_df.to_excel("AjioPincode("+Pincode+")_OutputData.xlsx",index=False)
except: pass

Glob_Exception_ID = pd.DataFrame({'Exception_ID':Glob_Exception_ID})
Glob_Exception_ID.to_excel("AjioPincode("+Pincode+")_Exception_ID.xlsx",index=False)

print("gggggggggg = ",Glob_Exception_ID)