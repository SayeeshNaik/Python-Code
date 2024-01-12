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
from selenium import webdriver
from scrapy.http import HtmlResponse
import requests
import urllib.parse

main_url = "https://www.ajio.com/"
exception_id = []
exception_url = []
trying_url = []
main_output_data = []
input1 = []
input2 = []

class AjioplpSpider(sp.Spider):
    # Global Flow 
    name = 'Ajio_PLP'
    
    main_url = "https://www.ajio.com/" 
    all_keywords=[]
    df = pd.read_excel("Batch_3600-3800.xlsx")
    listings = list(df['Product_list'])

    for i in listings:
        for page_num in range(1):
            all_keywords.append(main_url+f"api/search?fields=SITE&currentPage={page_num}&pageSize=45&format=json&query="+str(i)+"Arelevance&sortBy=relevance&text="+str(i))

    for url in all_keywords:
        response = requests.get(url)
        index = response.text.find('products')
        if index != -1:
            parsed_url = urllib.parse.urlparse(url)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            text = query_params.get('text')
            input1.append(text)
        
        else:
            parsed_url = urllib.parse.urlparse(url)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            text = query_params.get('text')
            input2.append(text)
        
    Product_list1 = pd.DataFrame(input1)
    product_list2 = pd.DataFrame(input2)

    Product_list1.to_excel("Product_list1_actual.xlsx",header=['Item Code'],index=False)
    product_list2.to_excel("Product_list2.xlsx",header=['Item Code'],index=False)
    
    df = pd.read_excel(
        "Product_list2.xlsx", sheet_name="Sheet1")
    listings1 = list(df["Item Code"])
    df = pd.read_excel(
        "Product_list1_actual.xlsxl", sheet_name="Sheet1")
    listings2 = list(df["Item Code"])
    all_urls = []
    if listings1:
        for i in listings1:
            for page_num in range(0,5):
                all_urls.append(main_url+f"api/search?fields=SITE&currentPage={page_num}&pageSize=45&format=json&query="+str(i)+"&gridColumns=3&advfilter=true&platform=Desktop&is_ads_enable_plp=false&is_ads_enable_slp=")
    Exception_product_name=[]
    for i in listings2:
        for page_num in range(0,5):
                all_urls.append(main_url+f"api/search?fields=SITE&currentPage={page_num}&pageSize=45&format=json&query="+str(i)+"Arelevance&sortBy=relevance&text="+str(i))
    # for i in listings:
    #     for page_num in range(0,5):
    #         all.urls.append(main_url+"api/search?fields=SITE&currentPage="+str(page_num)+"&pageSize=45&format=json&query={0}&sortBy=relevance&gridColumns=3&advfilter=true&platform=Desktop&is_ads_enable_plp=false&is_ads_enable_slp=false&showAdsOnNextPage=false&segmentIds=".format(str(i)))
    def start_requests(self):
        pass
        
        for url in self.all_urls:
            yield sp.Request(url=url,callback=self.parse)        
        
    def parse(self, response):
        main_page = str(response.body)
        main_page = main_page.replace("}'","}").replace("b'","")
        
        json_string = main_page
        json_string = clean(json_string,no_emoji=True,lower=False)
        try:
         json_data = json.loads(json_string)
         json_data_new = json_data['products']
        except:
            json_data_new=[]
        with open('Ajioplp.txt','w') as f:
            f.write(json_string)
                
        product_col=["freeTextSearch","fnlColorVariantData","name","price","wasPriceData","url","offerPrice","discountPercent","images"]
        required_col=["Keyword","Brand","Title","Price","MRP","Product URL", "Offer Price", "Discount", "Image URL"]
        required_Dict = dict(zip(product_col,required_col))
        Data_lis=[]
        for product in json_data_new:
            temp_dict={}
            temp_dict.update({"Date": datetime.date.today().strftime("%d-%m-%Y")})
            temp_dict.update({"Week": datetime.datetime.today().weekday()})
            temp_dict.update({"Marketplace": urlparse(response.url).netloc.replace('www.','').replace('.com','').title()})
            temp_dict.update({"Is Sponsored":'nan'})
            temp_dict.update({"Deal Text":'nan'})
            temp_dict.update({"Platform Sponsored":'nan'})
            temp_dict.update({"Delivery Text":'nan'})
            temp_dict.update({"Total Reviews":0})
            temp_dict.update({"Offers":'nan'})
            temp_dict.update({"Availability":'NaN'})
            temp_dict.update({"Base URL":response.url})
            temp_dict.update({"Tags":'nan'})
            temp_dict.update({"Is Sponsered ":'nan'})
            temp_dict.update({"Platform Sponsered ":'nan'})
            
            temp_dict.update({"Available Size":'nan'})
            temp_dict.update({"Deal Text ":'nan'})
            temp_dict.update({"mrp1":'nan'})
            temp_dict.update({"price1":'nan'})
            
            
            for col in product_col:
                try:
                    if col =='freeTextSearch':
                        val = json_data[col]
                        
                except:val='nan'
                temp_dict.update({col:val})
                
                try:
                    if col == 'fnlColorVariantData':
                        val = product[col]['brandName']
                except:val = 'nan'
                temp_dict.update({col:val})
                
                try:
                    if col == 'name':
                        val=product[col]
                except:val='nan'
                temp_dict.update({col: val})
                try:
                     if col == 'price':
                        val = product[col]['value']
                except:val='0'
                temp_dict.update({col: val})
                
                try:
                     if col == 'wasPriceData':
                        val = product[col]['value']
                except:val='0'
                temp_dict.update({col: val})
                
                try:
                    if col == 'images':
                        val = product[col][0]['url']

                except:val="URL Not Found"
                temp_dict.update({col:val})
                try:
                     if col =='offerPrice':
                         val = product[col]['value']
                except:val='0'
                          
                try:
                     if col == 'discountPercent':
                         val = product[col]
                except:val='0'
                
                try:
                     if col == 'url':
                         val = product[col]
                         val = self.main_url + val
                         val = val.replace('//','/')
                         
                except:val='nan'
                temp_dict.update({col: val})
            for old_col_name in required_Dict:
                temp_dict[required_Dict[old_col_name]] = temp_dict.pop(old_col_name)
            Data_lis.append(temp_dict)      
        self.Exception_product_name.append(response.url) if(len(Data_lis)==0) else 0
        
        pd.DataFrame({"Exception_Product_Name_":self.Exception_product_name}).to_excel("Ajio_Exception_Product_Name_Batch_3600-3800.xlsx",index=False)
          
        return Data_lis    
      
process = CrawlerProcess(settings={'LOG_LEVEL': 'DEBUG',
                                   'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                                   'FEEDS': {"AjioPLP_Data.csv": {'format': 'csv', 'overwrite': True}}
                                   })
process.crawl(AjioplpSpider)
process.start() 

try:
    main_df = pd.read_csv("AjioPLP_Data.csv")
    
except: pass

# Postprocessing 
df = pd.read_csv("AjioPLP_Data.csv")
df['Discount'] = df['Discount'].str.replace("%"," ")
df['Discount'] = df['Discount'].str.replace("off"," ")
df['Keyword'] = df['Keyword'].replace('Arelevance', '', regex=True)
df.sort_values(by='Keyword', inplace=True)
df['Rank'] = 1
prev_keyword = None

for index, row in df.iterrows():
    if row['Keyword'] !=prev_keyword:
        count=1
    else:
        count+=1
    df.at[index,'Rank']=count
    prev_keyword=row['Keyword']
    
df.to_csv("AjioPLP_Data_Batch_3600-3800.csv")
