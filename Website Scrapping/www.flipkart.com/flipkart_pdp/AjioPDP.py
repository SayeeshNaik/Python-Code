# Module And Libraries Import Field
import scrapy as sp
import pandas as pd
import datetime
import re
import json
from cleantext import clean
from urllib.parse import urlparse
from scrapy.crawler import CrawlerProcess

# Global Declarations (outside of Class)
main_url = "https://www.ajio.com"
Glob_Exception_ID = []
Glob_Exception_URL = []
trying_url = []

class MyntrapdpSpider(sp.Spider):
    # Settings for Avaid Server Over-Load 
    # custom_settings = {
    #     'DOWNLOAD_DELAY': 1, # For Giving 1s Delay for Each Requests
    #     'AUTOTHROTTLE_ENABLED': True,
    # }
    
    # Global Flow 
    name = 'ajiopdp'
    main_url = "https://www.ajio.com/p/"
    # Reading Product ID sheet
    productId_df = pd.read_excel("Ajio_ProductID.xlsx")
    # Adding URL to the Product ID
    productId_df['Product_ID'] = main_url + productId_df['Product_ID'].astype(str)
    # Listing All URL's with combination of Product ID
    all_urls = list(productId_df['Product_ID'])
    
    # For Calling Parse Fuction Loop Wise    
    def start_requests(self):
        # Reamoving Previous values from Sheet
        try: 
            if(len(pd.read_excel("AjioPDP_Exception_ID.csv"))>0): pd.DataFrame({"Exception_Id":[]}).to_excel("AjioPDP_Exception_ID.xlsx")
        except: pass
        # Looping Parse Function
        for url in self.all_urls: yield sp.Request(url, callback=self.parse, meta={'handle_httpstatus_all': True})        
        
    def parse(self, response):
        # Getting Dynamic Page Source
        page_source = str(response.body)
        # Using String Index and slicing for Json conversion
        start = '''{"wishlist"'''
        end = '''"unRatedProducts":'''
        start_index = page_source.find(start)
        end_index = page_source.find(end)
        product_data = page_source[start_index:end_index+len(end)]
        product_str_data = product_data+'''""}}'''
        # Reamoving Unwanted Characters from the Json String
        product_str_data = clean(product_str_data, no_emoji=True,lower=False)
        product_str_data = product_str_data.replace("\'","'")
        # Storing Json String as TXT file for Our Reference
        with open('AjioPDP.txt','w') as f:
             f.write(product_str_data)
        try:
            # Converting Json String format to Perfect Json
            json_data = json.loads(product_str_data)
            json_main_data = json_data['product']
            json_data = json_data['product']['productDetails']
        
            # Columns Name list for Output Data
            product_col = ['Product ID', 'Brand', 'Title', 'MRP', 'Selling Price', 'Discount %', 'Division','Category', 'Sub-Category', 'No of Sizes',
                        'Total Sizes', 'No of Available Sizes', 'Aavailable Sizes', 'No of Non-Available Sizes', 'Non-Available Sizes', 
                        'No. of Offers', 'Offers','Product Details','Fabric', 'No of Colors', 'Total Colors', 'No of Images','Image URL','Seller URL',
                        'In Stock']
            
            # Empty Dict for storing  each page data 
            temp_dict = {}
            temp_dict.update({"Date": datetime.date.today().strftime("%Y-%m-%d")})
            temp_dict.update({"Week": datetime.datetime.today().weekday()})
            temp_dict.update({"Marketplace": urlparse(response.url).netloc.replace('www.','').replace('.com','').title()})
            temp_dict.update({"Product URL": response.url})
            # Looping for get Each columns at a time
            for key in product_col:
                # Global Try Except for Error Handling
                try:
                    # These all conditions to get perticular  data from the Json 
                    if(key=='Product ID'): val = json_data['baseOptions'][0]['options'][0]['code']
                    elif(key=='Brand'): val = json_data['categories'][0]['code'].replace('-',' ').title()
                    elif(key=='Title'): val = json_data['baseOptions'][0]['options'][0]['modelImage']['altText']
                    elif(key=='MRP'): val = json_data['wasPriceData']['value']
                    elif(key=='Selling Price'): val = json_data['baseOptions'][0]['options'][0]['priceData']['value']
                    elif(key=='Discount %'): val = json_data['baseOptions'][0]['options'][0]['priceData']['discountValue']
                    elif(key=='Division'): val = json_data['rilfnlBreadCrumbList']['rilfnlBreadCrumb'][0]['name']
                    elif(key=='Category'): val = json_data['rilfnlBreadCrumbList']['rilfnlBreadCrumb'][1]['name']
                    elif(key=='Sub-Category'): val = json_data['rilfnlBreadCrumbList']['rilfnlBreadCrumb'][2]['name']
                    elif(key=='No of Sizes'): val = len([data['scDisplaySize'] for data in json_data['variantOptions']])
                    elif(key=='Total Sizes'): val = [[data['scDisplaySize'] for data in json_data['variantOptions']]]
                    elif(key=='No of Available Sizes'): 
                        val = []
                        for size in json_data['variantOptions']: 
                            if(size['stock']['stockLevelStatus']=='inStock'): val.append(size['scDisplaySize'])
                        val = len(val)
                    elif(key=='Aavailable Sizes'):
                        val = []
                        for size in json_data['variantOptions']: 
                            if(size['stock']['stockLevelStatus']=='inStock'): val.append(size['scDisplaySize'])
                        val = [val]
                    elif(key=='No of Non-Available Sizes'): 
                        val = []
                        for size in json_data['variantOptions']: 
                            if(size['stock']['stockLevelStatus']=='inStock'): val.append(size['scDisplaySize'])
                        val = len(val)
                    elif(key=='Non-Available Sizes'):
                        val = []
                        for size in json_data['variantOptions']: 
                            if(size['stock']['stockLevelStatus']=='inStock'): val.append(size['scDisplaySize'])
                        val = [val]
                    elif(key=='No. of Offers'): val = len([offers for offers in json_data['potentialPromotions']])
                    elif(key=='Offers'): 
                        val = {}
                        [val.update({offers['title'].replace('<br>',''):offers['description'][:offers['description'].find('<a')]})for offers in json_data['potentialPromotions']]
                    elif(key=='Product Details'):
                        val = {}
                        [val.update({detail['name']: detail['featureValues'][0]['value']}) for detail in json_data['featureData']]
                    elif(key=='Fabric'): val = temp_dict['Product Details']['Fabric Detail']
                    elif(key=='No of Colors'): val = len([colors['color'] for colors in json_data['baseOptions'][0]['options']])
                    elif(key=='Total Colors'): val = [[colors['color'] for colors in json_data['baseOptions'][0]['options']]]
                    elif(key=='No of Images'): val = len([image['url'] for image in json_data['images'] if(image['format']=='cartIcon')])
                    elif(key=='Image URL'): val = json_data['baseOptions'][0]['options'][0]['modelImage']['url']
                    elif(key=='Seller URL'): val = main_url + json_data['fnlColorVariantData']['categoryUrl']
                    elif(key=='In Stock'): val = "Yes" if json_data['baseOptions'][0]['options'][0]['stock']['stockLevelStatus']=='inStock' else "No"
              
                except: val = ''
                # Dynamically Storing Each Key, Value pair and storing to the perticular Dictionary
                temp_dict.update({key: val})
                val = ''
            
            # Not present in the page (But these all columns  also required)
            not_available_col = ['Product Rating','Count of Ratings','Count of Reviews','Current_Size','Bestseller Rank',
                                 'Rank Detail','Ques','COD','Product Type','Description']
            # Storing value as empty (non available columns)
            for empty_col in not_available_col: temp_dict.update({empty_col: ''})
            # Filtering Data
            if(temp_dict['MRP']==temp_dict['Selling Price']): temp_dict['Discount %'] = ''
            # Mandatory Fields
            if(temp_dict['Title']!='' and temp_dict['MRP']!=''): return temp_dict
            else: Glob_Exception_ID.append(response.url.split(self.main_url)[1].split('?')[0])
        except: Glob_Exception_ID.append(response.url.split(self.main_url)[1].split('?')[0])
     
# Settings for Running Crawller 
process = CrawlerProcess(settings={'LOG_LEVEL': 'DEBUG',
                                   'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                                   'FEEDS': {"AjioPDP_OutputData.csv": {'format': 'csv', 'overwrite': True}} # For Storing Parse Return Data
                                   })
process.crawl(MyntrapdpSpider)
process.start() 

# For converting CSV format to XLSX
try:
    main_df = pd.read_csv("AjioPDP_OutputData.csv")
    main_df.to_excel("AjioPDP_OutputData.xlsx",index=False)
except: pass
# Storing Exception ID's to the perticulr sheet
Exception_Id_df = pd.DataFrame({'Exception_ID':Glob_Exception_ID})
Exception_Id_df.to_excel('AjioPDP_Exception_ID.xlsx',index=False)