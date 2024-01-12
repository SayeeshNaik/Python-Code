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
    # custom_settings = {
    #     'DOWNLOAD_DELAY': 2 # 2 seconds of delay
    #     }
    
    # Global Flow 
    name = 'myntraplp'
    main_url = "https://www.myntra.com/"
    # all_urls = ["https://www.myntra.com/men-shirt"]  
    all_urls = ["https://www.myntra.com/men's dress new style"]
    def start_requests(self):
        pass
        for page_num in range(1,2):
            for url in self.all_urls:
                url = url+'?p={}'.format(page_num)
                yield sp.Request(url,callback=self.parse)        
        
    def parse(self, response):
        main_page = str(response.body)
        keyword = response.url.split(self.main_url)[1].split('?')[0].title()
        start_string = ' {"searchData":'
        json_start = main_page.find(start_string)
        main_page = main_page[json_start:]
        ending = main_page.find("</script>")
        json_string = main_page[0:ending].replace( "\\\\", "")
        json_data=clean(json_string, no_emoji=True,lower=False)
        json_data = json.loads(json_data)
        
        with open('myntraplp.txt','w') as f:
            f.write(json_string)
        json_data = json_data['searchData']['results']['products']
        
        product_col = ['productId','category','brand','additionalInfo','mrp','price','discountDisplayLabel','rating','ratingCount','searchImage','sizes','gender']  
        renamed_col = ['Product ID','Category','Brand','Title','MRP','Selling Price','Discount %','Rating','Count Of Rating','Image URL','Available Sizes','Division']
        rename_col_dict = dict(zip(product_col,renamed_col))
        Data_lis = []
        for product in json_data:
            temp_dict = {}
            temp_dict.update({"Date": datetime.date.today().strftime("%d-%m-%Y")})
            temp_dict.update({"Week": datetime.datetime.today().weekday()})
            temp_dict.update({"Marketplace": urlparse(response.url).netloc.replace('www.','').replace('.com','').title()})
            for col in product_col:
                try:
                    val = product[col]
                    val = val.title() if(type(val)==str and col!='searchImage') else val
                    try: 
                        temp_dict.update({'Product URL': self.main_url + str(temp_dict['productid'])})
                        temp_dict.update({'Keyword': keyword})
                    except: pass
                    if(col=='discountdisplaylabel'):
                        val = re.findall(r'\d+', val)[0]
                        val = str(val) + ' Off' if int(val)>100 else val 
                    if(col=='rating'): val = str(format(val, ".2f"))[:-1]
                    if(col=='sizes'): val = [[val]]
                    if(col=='searchImage'): val= val.replace('u002F','/').replace('http','https')
                except: val = ''
                temp_dict.update({col: val})
            
            for old_col in rename_col_dict:
                temp_dict[rename_col_dict[old_col]] = temp_dict.pop(old_col)
            Data_lis.append(temp_dict)

        return Data_lis
        

      
process = CrawlerProcess(settings={'LOG_LEVEL': 'DEBUG',
                                   'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                                   'FEEDS': {"MyntraPLP_Data.csv": {'format': 'csv', 'overwrite': True}}
                                   })
process.crawl(MyntraplpSpider)
process.start() 

try:
    main_df = pd.read_csv("MyntraPLP_Data.csv")
    main_df.to_excel("MyntraPLP_Data.xlsx",index=False)
except: pass