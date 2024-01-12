import scrapy as sp
import pandas as pd
import datetime
from requests_html import HTMLSession
import re
import json
from cleantext import clean
from urllib.parse import urlparse
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor, defer
from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerRunner
from selenium import webdriver
from selenium.webdriver.common.by import By

main_url = "https://www.myntra.com/"
# productId_df = pd.read_excel("MyntraPDP_ProductID.xlsx")
productId_df = pd.read_excel("MyntraPDP_ProductID(abhi).xlsx")
productId_df['Product_ID'] = main_url + productId_df['Product_ID'].astype(str)
all_urls = productId_df['Product_ID']
all_urls = all_urls[0:1]
# all_urls = ['https://www.myntra.com/18974370']
# all_urls = ["https://www.myntra.com/18974370"]
# all_urls = ["https://www.myntra.com/18652620"]
# all_urls = ['https://www.myntra.com/111456']  # outof stock

# productId_df = pd.read_excel("MyntraPDP_Exception_URL.xlsx")
# productId_df['Exception_URL'] = main_url + productId_df['Exception_URL'].astype(str)
# all_urls = productId_df['Exception_URL']
# all_urls = ['https://www.myntra.com/10787892?bm-verify=AAQAAAAG_____yId4NgL8VUyamBSRFY6ENX5oFyDxMtRye7fmeTWwRGX20hw7ojhOZwIwR9Em5Z6VxUWktx8uxSY0xx4nILBkOamvz4cYi7EWE4YZT4Z6a3VI-_Ww6fvbRwgkLxhtMotIP6wURu1EQ0EOJYx4LCNQT0MXLwkMGYLNl8pNKmNkXqMDhSgMP6x2AKHeBXD5TqaE0pjBAGS5xyEYVPW0nndwpd7IDIbsGOx6ZdF2yRFgg']
# all_urls=['https://www.myntra.com/10787900?bm-verify=AAQAAAAG_____8a0DOhULbzQvq3zeelMSmNnIuPc-x9r9iCndd458j2ORWlNKNMIncELnn7FTJ3r4xhHBlH6syRcpSGVBY9zs76BCFSzBMajsklrvRz-wH_tYcwVpZWNuCGBgr_Ii-swtkbI8Z7D3o6PHwf3fOAu80FEVICTwp7JKT-dJrNsWZQqAS6BuKeJKlvb5ptA7UhhPCbLHTpfnXmYyEIfH2XILOWlT8EJ4qIxXdOGH0a6zA']
exception_id = []
Exception_URL = []
trying_url = []
all_output_lis = []



def parse(response):
    parent_page = str(response.body)
    main_page = str(response.body)
    start_string = '{"pdpData'
    json_start = main_page.find(start_string)
    main_page = main_page[json_start:]
    ending = main_page.find("</script>")
    json_string = main_page[0:ending].replace( "\\\\", "")
    json_data_str=clean(json_string, no_emoji=True,lower=False)
    removing_str = json_data_str.find(',"bundledSkus":')
    json_data_str = json_data_str[0:removing_str]+'}}'
    with open('myntrapdp.txt','w') as f:
            f.write(json_data_str)
    start_offers_str = main_page.find('{"android"')
    start_division = parent_page.find('"itemListElement":')+len('"itemListElement":')
    json_division_str = parent_page[start_division:]
    end_division = json_division_str.find("]")+1
    json_division_str =  json_division_str[:end_division]
    json_division_str = clean(json_division_str,no_emoji=True,lower=False)
    try:
        json_data = json.loads(json_data_str)
        json_data = json_data['pdpData']
        try:json_division = json.loads(json_division_str)
        except: pass
        product_col = ['Product ID', 'Brand', 'Title', 'MRP', 'Selling Price', 'Discount %','Product Ratings', 'Category','Sub Category','Division','Product Type', 'No of Total Sizes',
                        'Total Sizes', 'No of Available Sizes', 'Available Sizes', 'No of Non Available Sizes', 'Non Available Sizes', 
                        'Product Details', 'Fabric', 'No of Offers', 'Total Offers', 'No of Images','Image URL','In Stock','Count of Ratings',
                        'Count of Reviews','Seller URl']
        temp_dict = {}
        temp_dict.update({"Date": datetime.date.today().strftime("%Y-%m-%d")})
        temp_dict.update({"Week": datetime.datetime.today().weekday()})
        temp_dict.update({"Marketplace": urlparse(response.url).netloc.replace('www.','').replace('.com','').title()})
        temp_dict.update({"Product URL": response.url})
        
        for key in product_col:
            try:
                if(key=='Product ID'): val = json_data['id']
                elif(key=='Brand'): val = json_data['brand']['name'].title()
                elif(key=='Title'): val = json_data['name'].replace(json_data['brand']['name']+' ',"").title()
                elif(key=='MRP'): val = json_data['mrp']
                elif(key=='Selling Price'): val = json_data['sizes'][0]['sizeSellerData'][0]['discountedPrice']
                elif(key=='Discount %'): val = json_data['discounts'][1]['discountPercent']
                elif(key=='Product Ratings'): val = round(json_data['ratings']['averageRating'],1)
                elif(key=='Category'): val = json_division[0]['item']['name']
                elif(key=='Sub Category'): val = json_division[2]['item']['name']
                elif(key=='Division'): val = json_division[1]['item']['name']
                elif(key=='Product Type'): val = json_division[3]['item']['name']
                elif(key=='No of Total Sizes'): val = len([size['label'] for size in json_data['sizes']])
                elif(key=='Total Sizes'): val = [[size['label'] for size in json_data['sizes']]]
                elif(key=='No of Available Sizes'): val = len([size['label'] for size in json_data['sizes'] if size['available']==True])
                elif(key=='Available Sizes'): val = [[size['label'] for size in json_data['sizes'] if size['available']==True]]
                elif(key=='No of Non Available Sizes'): val = len([size['label'] for size in json_data['sizes'] if size['available']==False])
                elif(key=='Non Available Sizes'): val = [[size['label'] for size in json_data['sizes'] if size['available']==False]]     
                elif(key=='Product Details'): val = json_data['articleAttributes']
                elif(key=='Fabric'): val = json_data['articleAttributes']['Fabric']
                elif(key=='No of Offers'): val = len([offer['title'] for offer in json_data['offers']])
                elif(key=='Total Offers'): val = [json_data['serviceability']['descriptors']]
                elif(key=='No of Images'): val = len(json_data['media']['albums'][0]['images'])
                elif(key=='Image URL'): val = json_data['media']['albums'][0]['images'][0]['imageURL'].replace('u002F','/')
                elif(key=='In Stock'): val = "Yes" if json_data['flags']['outOfStock']==False else "No"
                elif(key=='Count of Ratings'): val = json_data['ratings']['totalCount']
                elif(key=='Count of Reviews'): val = json_data['ratings']['ratingInfo']['reviewsCount']
                elif(key=='Seller URl'): val = json_data['sellers'][0]['sellerName']
                   
            except: val = ''
            temp_dict.update({key: val})
            val = ''
        not_available_col = ['Current_Size','No of Colors', 'Total Colors','Bestseller Rank',
                                'Rank Detail','Ques','COD','Description']
        for empty_col in not_available_col: temp_dict.update({empty_col: ''})
            
            
        # Filtration 
        try: temp_dict['Product Ratings'] = round(temp_dict['Product Ratings'],1)
        except: pass
        
     
        print("**********************************")

        
        all_output_lis.append(temp_dict)
        return temp_dict

    except: Exception_URL.append(response.url)

    

class MyntrapdpSpider(sp.Spider):
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'AUTOTHROTTLE_ENABLED': True,
    }
    
    # Global Flow 
    name = 'myntra'
    
    def start_requests(self):
        pass
        for url in all_urls:
          yield sp.Request(url,callback=parse)        
        
   

      
process = CrawlerProcess(settings={'LOG_LEVEL': 'DEBUG',
                                   'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                                   'FEEDS': {"MyntraPDP_Data.csv": {'format': 'csv', 'overwrite': True}}
                                   })
process.crawl(MyntrapdpSpider)
process.start() 

try:
  last_df = pd.read_csv("MyntraPDP_Data.csv")
  last_df.to_excel("MyntraPDP_Data.xlsx",index=False)
except: pass

print("eeeeeeeeeeeeeeee = ",Exception_URL)


# Exception_URL = ["https://www.myntra.com/10341699"]
# class TryingSpider(sp.Spider):
#   name = 'tryingurl'
#   def start_requests(self):
#         global Exception_URL
#         for try_url in Exception_URL:
#             main_lis_len = len(all_output_lis)
#             for looping in range(3):
#                if(len(all_output_lis)>main_lis_len):break
#                yield sp.Request(try_url, callback=parse)

# again_looping = CrawlerProcess(settings={'LOG_LEVEL': 'DEBUG',
#                                    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
#                                    'FEEDS': {"MyntraPDP_Trying_Output.csv": {'format': 'csv', 'overwrite': True}}
#                                    })
# again_looping.crawl(TryingSpider)

# configure_logging()
# runner = CrawlerRunner()
# @defer.inlineCallbacks
# def crawl():
#     yield runner.crawl(MyntrapdpSpider)
#     yield runner.crawl(TryingSpider)
#     reactor.stop()
# crawl()
# reactor.run()




Exception_URL_df = pd.DataFrame({'Exception_URL':Exception_URL})
Exception_URL_df.to_excel("MyntraPDP_Exception_URL.xlsx",index=False)
