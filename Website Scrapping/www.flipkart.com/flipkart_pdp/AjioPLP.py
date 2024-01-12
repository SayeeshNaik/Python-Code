import scrapy as sp
import pandas as pd
import datetime
import time
import re
import json
from cleantext import clean
from urllib.parse import urlparse
from scrapy.crawler import CrawlerProcess

main_url = "https://www.myntra.com/"
exception_id = []
exception_url = []
trying_url = []
main_output_data = []

class MyntraplpSpider(sp.Spider):
    custom_settings = {
        'DOWNLOAD_DELAY': 2 # 2 seconds of delay
        }
    
    # Global Flow 
    name = 'ajioplp'
    main_url = "https://www.ajio.com/"
    all_urls = ["https://www.ajio.com/search/men%20t%20shirt"]  
    # all_urls = ["https://www.ajio.com/search/?text=women%20dress"]
    def start_requests(self):
        pass
        # for page_num in range(1,2):
        for url in self.all_urls:
                # url = url+'?p={}'.format(page_num)
            yield sp.Request(url,callback=self.parse)        
        
    def parse(self, response):
        main_page = str(response.body)
        keyword = response.url.split('/')[-1].title()
        start_string = '{"wishlist":'
        json_start = main_page.find(start_string)
        main_page = main_page[json_start:]
        ending = main_page.find("</script>")
        json_string = main_page[0:ending].replace( "\\\\", "")
        json_string = json_string.replace("\'","")
        str_en = json_string.encode("ascii", "ignore")
        str_de = str_en.decode()
        str_de = str_de.replace("\'","")
        json_string = str_de
       
        json_string = json_string.replace("\s","s").replace("\ ","")
        json_format_start = json_string.find('"entities":')+len('"entities":')
        json_string = json_string[json_format_start:]
        json_format_end = json_string.find(',"gridColumns"')
        json_string = json_string[:json_format_end]
        json_string = json_string.replace('"{','{').replace('}"','}')
        json_string=clean(json_string, no_emoji=True,lower=False)
        json_data = json.loads(json_string)
        with open('AjioPLP.txt','w') as f:
            f.write(json_string)
            
        product_col = ['url','name','wasPriceData','price','discountPercent','images']
        renamed_col = ['Product ID','Title','MRP','Selling Price','Discount %','Image URL']
        rename_col_dict = dict(zip(product_col,renamed_col))
        Data_lis = []
        for product in json_data:
            temp_dict = {}
            temp_dict.update({"Date": datetime.date.today().strftime("%d-%m-%Y")})
            temp_dict.update({"Week": datetime.datetime.today().weekday()})
            temp_dict.update({"Marketplace": urlparse(response.url).netloc.replace('www.','').replace('.com','').title()})
            temp_dict.update({'Page URL': response.url})
            temp_dict.update({'Key Name': keyword})
            for col in product_col:
                try:
                    val = json_data[product][col]
                    if(col=='url'): 
                        val = val.split('/')[-1]
                    if(col=='waspricedata' or col=='price'): val = val['value']
                    if(col=='images'): val = val[0]['url']
                    # if(col=='images'): val = val[0]['url']
                   
                except: val = ''
                temp_dict.update({col: val})
                if(col=='url'):temp_dict.update({'Product URL':self.main_url+'p/'+temp_dict['url']})
            for old_col in rename_col_dict:
                temp_dict[rename_col_dict[old_col]] = temp_dict.pop(old_col)
            Data_lis.append(temp_dict)

        return Data_lis
        

      
process = CrawlerProcess(settings={'LOG_LEVEL': 'DEBUG',
                                   'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                                   'FEEDS': {"AjioPLP.csv": {'format': 'csv', 'overwrite': True}}
                                   })
process.crawl(MyntraplpSpider)
process.start() 

try:
    main_df = pd.read_csv("AjioPLP.csv")
    main_df.to_excel("AjioPLP.xlsx",index=False)
except: pass