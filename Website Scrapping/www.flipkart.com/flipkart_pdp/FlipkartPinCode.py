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
from scrapy.utils.response import open_in_browser
import webbrowser

class FlipkartpdpSpider(sp.Spider):
    # Global Flow 
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    name = 'flipkartpdp'
    main_url = 'https://www.flipkart.com/x/p/k?pid='
    df_product_id = pd.read_excel("Product_ID.xlsx")
    urls,output_data = [],[]
    for id in df_product_id['product_id']: urls.append(main_url + id)
    df_xpaths = pd.read_excel('xpath_flipkart_pdp.xlsx')
            
    def start_requests(self):
        try: 
            if(len(pd.read_excel("FlipkartPDP_Exception_ProductID.csv"))>0): pd.DataFrame({"Exception_Id":[]}).to_excel("FlipkartPDP_Exception_ProductID.xlsx",index=False)
        except: pass
        # for url in self.urls : yield sp.Request(url, callback=self.parse)
        for url in range(5): yield sp.Request(self.urls[url], callback=self.parse)
        
    def parse(self,response):
        print("uuuuuuuuuuu = ",response.url)
        pin = response.xpath("//div[@class='_12cXX4']//span//text()").getall()
        val = response.xpath("//div[@class='_3XINqE']//span/text()").getall()
        print("ppppppppppppp = ",pin)
        print("vvvvvvvvvvvvv = ",val)
        # open_in_browser(response)
        
        return {}
 
# Scrapy Crawling Process   
process = CrawlerProcess(settings={'LOG_LEVEL': 'DEBUG',
                                   'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                                   'FEEDS': {"FlipkartPinCode.csv": {'format': 'csv', 'overwrite': True}}
                                   })
process.crawl(FlipkartpdpSpider)
process.start()
