# Module And Libraries Import Field
import scrapy as sp
import pandas as pd
from scrapy.crawler import CrawlerProcess
import datetime
from urllib.parse import urlparse
import time
import re
from twisted.internet import reactor, defer
from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerRunner

# Global Declarations
main_url = 'https://www.flipkart.com/x/p/k?pid='
df_product_id = pd.read_excel("FlipkartPDP_Product_ID.xlsx")
urls,output_data = [],[]
for id in df_product_id['product_id']: urls.append(main_url + id)
df_xpaths = pd.read_excel('xpath_flipkart_pdp.xlsx')
trying_urls = []
main_output_lis = []
Exception_ProductID = []

# Global Function for multiple time use
def parse(response):
        # Removing Previous values from the Sheet
        try: 
            if(len(pd.read_excel("FlipkartPDP_Exception_ProductID.csv"))>0): pd.DataFrame({"Exception_Id":[]}).to_excel("FlipkartPDP_Exception_ProductID.xlsx")
        except: pass
        # Using global variables inside of this function
        global trying_urls,Exception_ProductID,main_output_lis
        pass
        producId = response.url.split(main_url)[1]
        # Created Empty Dictionary for storing Perticular page  data
        temp_dict = {}
        # Global Try Except for Error handling
        try:
                temp_dict.update({"Date": datetime.date.today().strftime("%Y-%m-%d")})
                temp_dict.update({"Week": datetime.datetime.today().weekday()})
                temp_dict.update({"Marketplace": urlparse(response.url).netloc.replace('www.','').replace('.com','').title()})
                temp_dict.update({"Product ID": response.url[response.url.index('pid=')+4:]})
                # Looping for each columns
                for key in range(len(df_xpaths)):
                    if(df_xpaths['name'][key]=='MRP'):
                        val = ''
                        for v in response.xpath((df_xpaths['xpath'][key] + '/text()')).getall(): val += v
                        temp_dict.update({df_xpaths['name'][key] : val if val!='' and val!=None else ''})
                    elif(df_xpaths['name'][key]=='Seller_Offers'): 
                        temp_lis = []
                        for val in response.xpath((df_xpaths['xpath'][key] + '/text()')).getall(): temp_lis.append(val)
                        temp_dict.update({df_xpaths['name'][key] : temp_lis if len(temp_lis)>0 else ''})
                    elif(df_xpaths['name'][key]=='In Stock'):
                        temp_dict.update({df_xpaths['name'][key] : 'Yes' if response.xpath((df_xpaths['xpath'][key] + '/text()')).get()==None else 'No'})
                    elif(df_xpaths['name'][key]=='COD'):
                        temp_dict.update({df_xpaths['name'][key] : 'Yes' if response.xpath((df_xpaths['xpath'][key] + '/text()')).get()!=None else 'No'})
                    elif(df_xpaths['name'][key]=='Offers'):
                        val = response.xpath((df_xpaths['xpath'][key] + '/text()')).getall()
                        temp_dict.update({"No. of Offers": len(val)})
                        temp_dict.update({df_xpaths['name'][key] : [val] if len(val)>0 else [[]]})
                    elif(df_xpaths['name'][key]=='Count of Ratings'):
                        try:
                            val = response.xpath((df_xpaths['xpath'][key] + '/text()')).get()
                            val = val.split("and")
                            temp_dict.update({df_xpaths['name'][key] :  int(re.search(r'\d+', val[0]).group()) if len(val)>0 else ''})
                            temp_dict.update({"Count of Reviews" : int(re.search(r'\d+', val[1]).group()) if len(val)>1 else ''})
                        except: 
                            temp_dict.update({df_xpaths['name'][key] : ''})
                            temp_dict.update({"Reviews" : ''})
                    elif(df_xpaths['name'][key]=='Total Sizes'):
                         val = response.xpath((df_xpaths['xpath'][key] + '/text()')).getall()
                         temp_dict.update({"No of Sizes": len(val)})
                         temp_dict.update({df_xpaths['name'][key] : [val] if len(val)>0 else [[]]})
                    elif(df_xpaths['name'][key]=='Available Sizes'):
                        val = response.xpath((df_xpaths['xpath'][key] + '/text()')).getall()
                        temp_dict.update({"No of Available Sizes": len(val)})
                        temp_dict.update({"Available Sizes": [val] if len(val)>0 else [[]]}) 
                        temp_dict.update({"No of Non-Available Sizes": len([x for x in temp_dict['Total Sizes'][0] if x not in temp_dict['Available Sizes'][0]])})
                        temp_dict.update({"Non-Available Sizes": [[x for x in temp_dict['Total Sizes'][0] if x not in temp_dict['Available Sizes'][0]]]})          
                    elif(df_xpaths['name'][key]=='Available Colors'):
                        val = response.xpath((df_xpaths['xpath'][key])).extract()
                        temp_dict.update({"No of Colors": len(val)})
                    elif(df_xpaths['name'][key]=='No of Images'):
                        val = response.xpath((df_xpaths['xpath'][key])).getall()
                        temp_dict.update({"No of Images": len(val) if len(val)>0 else ''})
                        temp_dict.update({"Product URL": response.url})
                    elif(df_xpaths['name'][key]=='Product Details'):
                        val = response.xpath((df_xpaths['xpath'][key] + '/text()')).getall()
                        temp_dict.update({"Product Details": dict(zip(val[0::2],val[1::2])) if len(val)>0 else ''})
                        try: 
                            temp_dict.update({"Fabric":temp_dict['Product Details']['Fabric'] if(temp_dict['Product Details']['Fabric']!=None) else ''})
                            temp_dict.update({"Bestseller Rank": ''})
                            temp_dict.update({"Rank Detail": ''})
                            temp_dict.update({"Ques": ''})
                        except: temp_dict.update({"Fabric":''})
                    elif(df_xpaths['name'][key]=='Questions_Answers'): pass
                        # val = response.xpath((df_xpaths['xpath'][key] + '/text()')).getall()
                        # temp_dict.update({"Questions_Answers": dict(zip(val[0::2],val[1::2])) if len(val)>0 else ''})
                    elif(df_xpaths['name'][key]=='BuyNow'):
                        temp_dict.update({df_xpaths['name'][key] : 'Yes' if response.xpath((df_xpaths['xpath'][key] + '/text()')).get()!=None else 'No'})
                    else: 
                        val = response.xpath((df_xpaths['xpath'][key] + ('/text()' if df_xpaths['name'][key]!='Image_URL' else ''))).get()
                        temp_dict.update({df_xpaths['name'][key] : val if val!='' and val!=None else ''})
                        # try: temp_dict.update({"Division": temp_dict['Title'].split()[0]})
                        # except: pass
        except: temp_dict.update({df_xpaths['name'][key]: '***'})
        output_data.append(temp_dict)
        # Mandatory Fields
        if(temp_dict['Title']!='' and temp_dict['Brand']!='' and temp_dict['MRP']!='' and
           temp_dict['Title']!='' and temp_dict['Brand']!='' and temp_dict['MRP']!=''):
            main_output_lis.append(temp_dict)
            return temp_dict
        else :  
            Exception_ProductID.append(producId)
            trying_urls.append(response.url)

# Spider Class
class FlipkartpdpSpider(sp.Spider):
    # Global Flow 
    name = 'flipkartpdp'
    allowed_domains = ['flipkart.com']
    main_url = 'https://www.flipkart.com/x/p/k?pid='
    # Reading all Product ID's form the sheet
    df_product_id = pd.read_excel("Product_ID.xlsx")
    urls,output_data = [],[]
    # Genarating URL with concatination of Product ID
    for id in df_product_id['product_id']: urls.append(main_url + id)
    # Reading Input File (xpath file)
    df_xpaths = pd.read_excel('xpath_flipkart_pdp.xlsx')
            
    def start_requests(self):
        # Removing Previous values from the Sheet
        try: 
            if(len(pd.read_excel("FlipkartPDP_Exception_ProductID.csv"))>0): pd.DataFrame({"Exception_Id":[]}).to_excel("FlipkartPDP_Exception_ProductID.xlsx",index=False)
        except: pass
        for url in self.urls[0:5] : yield sp.Request(url, callback=parse)
        # for url in range(10): yield sp.Request(self.urls[url], callback=parse)
 
# Scrapy Crawling Process   
process = CrawlerProcess(settings={'LOG_LEVEL': 'DEBUG',
                                   'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                                   'FEEDS': {"FlipkartPDP_OutputData.csv": {'format': 'csv', 'overwrite': True}}
                                   })
process.crawl(FlipkartpdpSpider)

Exception_ProductID = []

# 3-times Re-Running Process for Skipped URL's 
class TryingSpider(sp.Spider):
  name = 'tryingurl'
  def start_requests(self):
        global trying_urls,Exception_ProductID
        for try_url in trying_urls:
            main_lis_len = len(main_output_lis)
            for looping in range(3):
               if(len(main_output_lis)>main_lis_len):break
               yield sp.Request(try_url, callback=parse)
      
  
# Second Crawller for Re-Running Process                          
again_looping = CrawlerProcess(settings={'LOG_LEVEL': 'DEBUG',
                                   'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                                   'FEEDS': {"FlipkartPDP_Trying_Output.csv": {'format': 'csv', 'overwrite': True}}
                                   })
again_looping.crawl(TryingSpider)

# For Remove ReactModule Error In Scrapy
configure_logging()
runner = CrawlerRunner()
@defer.inlineCallbacks
def crawl():
    yield runner.crawl(FlipkartpdpSpider)
    yield runner.crawl(TryingSpider)
    reactor.stop()
crawl()
reactor.run()

# Filtering Data
original_df = pd.DataFrame(main_output_lis)
output_product_id = list(original_df['Product ID'])
main_exp_id = []
for exp_id in set(Exception_ProductID):
    Exception_ProductID = []
    if exp_id not in output_product_id:
        main_exp_id.append(exp_id)
Exception_Df = pd.DataFrame({"Exception_ProductID":list(set(main_exp_id))}).to_csv("FlipkartPDP_Exception_ProductID.csv")

# Filtering Data
original_df.drop_duplicates(subset='Product ID', keep="last",inplace=True)
original_df['Selling Price'] = original_df['Selling Price'].str.replace("₹",'',regex=True)
original_df['MRP'] = original_df['MRP'].str.replace("₹",'',regex=True)
original_df['Discount %'] = original_df['Discount %'].str.replace('%','',regex=True).str.replace(" off",'',regex=True)
original_df.to_csv("FlipkartPDP_Filtered_Output.csv",index=False)
original_df.to_excel("FlipkartPDP_Filtered_Output.xlsx",index=False)

