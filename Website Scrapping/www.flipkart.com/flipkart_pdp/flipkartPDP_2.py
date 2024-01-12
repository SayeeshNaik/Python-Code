import scrapy as sp
import pandas as pd
from scrapy.crawler import CrawlerProcess
import datetime
from urllib.parse import urlparse
import time
import re

class FlipkartpdpSpider(sp.Spider):
    # custom_settings = {
    #     'DOWNLOAD_DELAY': 2,  # minimum download delay
    #     # 'AUTOTHROTTLE_ENABLED': True,
    # }
    
    # Global Flow 
    name = 'flipkartpdp_2'
    allowed_domains = ['flipkart.com']
    main_url = 'https://www.flipkart.com/x/p/k?pid='
    exp_id = pd.read_excel("FlipkartPDP_Exception_ProductID.xlsx")
    urls,output_data,Exception_ProductId = [],[],[]
    for id in exp_id: urls.append(main_url + id)
    df_xpaths = pd.read_excel('xpath_flipkart_pdp.xlsx')
    print("uuuuuuuuuuu = ",urls)
    delay_count = 0
        
    def __init__(self):    
        self.Exception_ProductId = []
        
    def start_requests(self):
        try: 
            if(len(pd.read_excel("FlipkartPDP_Exception_ProductID.xlsx"))>0): pd.DataFrame({"Exception_Id":[]}).to_excel("FlipkartPDP_Exception_ProductID.xlsx")
        except: pass
        # for url in self.urls : yield sp.Request(url, callback=self.parse)
        # for url in range(5): yield sp.Request(self.urls[url], callback=self.parse) if self.urls[url]!="https://www.flipkart.com/x/p/k?pid=FABEEP7FH7XPVBV4" else 0
        

    def parse(self, response):
        pass
        temp_dict = {}
        
        try:
                temp_dict.update({"Date": datetime.date.today().strftime("%d-%m-%Y")})
                temp_dict.update({"Week": datetime.datetime.today().weekday()})
                temp_dict.update({"Marketplace": urlparse(response.url).netloc.replace('www.','').replace('.com','').title()})
                temp_dict.update({"Product ID": response.url[response.url.index('pid=')+4:]})
               
                for key in range(len(self.df_xpaths)):
                    if(self.df_xpaths['name'][key]=='MRP'):
                        val = ''
                        for v in response.xpath((self.df_xpaths['xpath'][key] + '/text()')).getall(): val += v
                        temp_dict.update({self.df_xpaths['name'][key] : val if val!='' and val!=None else 'None'})
                    elif(self.df_xpaths['name'][key]=='Seller_Offers'): 
                        temp_lis = []
                        for val in response.xpath((self.df_xpaths['xpath'][key] + '/text()')).getall(): temp_lis.append(val)
                        temp_dict.update({self.df_xpaths['name'][key] : temp_lis if len(temp_lis)>0 else 'None'})
                    elif(self.df_xpaths['name'][key]=='In Stock'):
                        temp_dict.update({self.df_xpaths['name'][key] : 'In Stock' if response.xpath((self.df_xpaths['xpath'][key] + '/text()')).get()==None else 'Out Of Stock'})
                    elif(self.df_xpaths['name'][key]=='COD'):
                        temp_dict.update({self.df_xpaths['name'][key] : 'Yes' if response.xpath((self.df_xpaths['xpath'][key] + '/text()')).get()!=None else 'No'})
                    elif(self.df_xpaths['name'][key]=='Offers'):
                        val = response.xpath((self.df_xpaths['xpath'][key] + '/text()')).getall()
                        temp_dict.update({"No. of Offers": len(val)})
                        temp_dict.update({self.df_xpaths['name'][key] : [val] if len(val)>0 else "Not Available"})
                    elif(self.df_xpaths['name'][key]=='Count of Ratings'):
                        try:
                            val = response.xpath((self.df_xpaths['xpath'][key] + '/text()')).get()
                            val = val.split("and")
                            temp_dict.update({self.df_xpaths['name'][key] :  int(re.search(r'\d+', val[0]).group()) if len(val)>0 else "Not Available"})
                            temp_dict.update({"Count of Reviews" : int(re.search(r'\d+', val[1]).group()) if len(val)>1 else "Not Available"})
                        except: 
                            temp_dict.update({self.df_xpaths['name'][key] : "Not Available"})
                            temp_dict.update({"Reviews" : "Not Available"})
                    elif(self.df_xpaths['name'][key]=='Total Sizes'):
                         val = response.xpath((self.df_xpaths['xpath'][key] + '/text()')).getall()
                         temp_dict.update({"No of Sizes": len(val)})
                         temp_dict.update({self.df_xpaths['name'][key] : [val] if len(val)>0 else "Not Available"})
                    elif(self.df_xpaths['name'][key]=='Available Sizes'):
                        val = response.xpath((self.df_xpaths['xpath'][key] + '/text()')).getall()
                        temp_dict.update({"No of Available Sizes": len(val)})
                        temp_dict.update({"Available Sizes": [val] if len(val)>0 else "Not Available"}) 
                        temp_dict.update({"No of Non-Available Sizes": len([x for x in temp_dict['Total Sizes'][0] if x not in temp_dict['Available Sizes'][0]])})
                        temp_dict.update({"Non-Available Sizes": [[x for x in temp_dict['Total Sizes'][0] if x not in temp_dict['Available Sizes'][0]]]})          
                    elif(self.df_xpaths['name'][key]=='Available Colors'):
                        val = response.xpath((self.df_xpaths['xpath'][key])).extract()
                        temp_dict.update({"No of Colors": len(val)})
                        temp_dict.update({"No of Images": [val] if len(val)>0 else "Not Available"})
                        temp_dict.update({"Product URL": response.url})
                    elif(self.df_xpaths['name'][key]=='Product Details'):
                        val = response.xpath((self.df_xpaths['xpath'][key] + '/text()')).getall()
                        temp_dict.update({"Product Details": dict(zip(val[0::2],val[1::2])) if len(val)>0 else "Not Available"})
                        try: 
                            temp_dict.update({"Fabric":temp_dict['Product Details']['Fabric'] if(temp_dict['Product Details']['Fabric']!=None) else "Not Available"})
                            temp_dict.update({"Bestseller Rank": ''})
                        except: temp_dict.update({"Fabric":"Not Available"})
                    elif(self.df_xpaths['name'][key]=='Questions_Answers'): pass
                        # val = response.xpath((self.df_xpaths['xpath'][key] + '/text()')).getall()
                        # temp_dict.update({"Questions_Answers": dict(zip(val[0::2],val[1::2])) if len(val)>0 else "Not Available"})
                    elif(self.df_xpaths['name'][key]=='BuyNow'):
                        temp_dict.update({self.df_xpaths['name'][key] : 'Yes' if response.xpath((self.df_xpaths['xpath'][key] + '/text()')).get()!=None else 'No'})
                    else: 
                        val = response.xpath((self.df_xpaths['xpath'][key] + ('/text()' if self.df_xpaths['name'][key]!='Image_URL' else ''))).get()
                        temp_dict.update({self.df_xpaths['name'][key] : val if val!='' and val!=None else 'Not Available'})
                        try: temp_dict.update({"Division": temp_dict['Title'].split()[0]})
                        except: pass
        except: temp_dict.update({self.df_xpaths['name'][key]: '***'})
        self.output_data.append(temp_dict)
        return temp_dict if temp_dict['Title']!='Not Available' else  self.Exception_Id(response.url[response.url.index('pid=')+4:])
    
    def Exception_Id(self,Exp_Id):
        self.Exception_ProductId.append(Exp_Id)
        pd.DataFrame({"Exception_Id":self.Exception_ProductId}).to_excel("FlipkartPDP_Exception_ProductID.xlsx")
        
process = CrawlerProcess(settings={'LOG_LEVEL': 'DEBUG',
                                   'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                                   'FEEDS': {"FlipkartPDP_OutputData.csv": {'format': 'csv', 'overwrite': True}}
                                   })
process.crawl(FlipkartpdpSpider)
process.start()

# Storing Data
df = pd.read_csv('FlipkartPDP_OutputData.csv')
df.to_excel("FlipkartPDP_OutputData.xlsx", index=False)

# Filtering Data
original_df = pd.read_excel("FlipkartPDP_OutputData.xlsx")
original_df['Selling Price'] = original_df['Selling Price'].str.replace("₹",'')
original_df['MRP'] = original_df['MRP'].str.replace("₹",'')
original_df['Discount %'] = original_df['Discount %'].str.replace('%','').str.replace('off','')
filtered_df = original_df.to_excel("FlipkartPDP_Filtered_Output.xlsx",index=False)

