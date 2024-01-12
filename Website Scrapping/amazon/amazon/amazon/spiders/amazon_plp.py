
import numpy as np
import pandas as pd
import scrapy as sp
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
# from IPython.display import HTML, display
import re
import time

df = pd.read_excel("C:/Users/User/Scrapy Websites/amazon/amazon/amazon/spiders/Product ID.xlsx", sheet_name='Amazon')
listings = list(df["Item Code"])

df = pd.read_excel("C:/Users/User/Scrapy Websites/amazon/amazon/amazon/spiders/Amazon xpaths file.xlsx", index_col=0)
df.dropna(inplace=True)
xpaths = {}
for i in df.index.values:
    temp = {i: df.loc[i]["xpaths"]}
    xpaths.update(temp)

print("ASINs:", listings)
print("XPATHs - ")
print(xpaths, "/n")


class AmazonPlpSpider(sp.Spider):
    name = 'amazon_plp'
    custom_settings = {
        'DOWNLOAD_DELAY': 2,  # minimum download delay
        'AUTOTHROTTLE_ENABLED': True,
    }
    

    def start_requests(self):
                # d = data = {
                # "authority":" m.media-amazon.com",
                # "method": "GET",
                # "path": "/images/G/01/AUIClients/AmazonUIFont-amazonember_rgit-9cc1bb64eb270135f1adf3a4881c2ee5e7c37be5._V2_.woff2",
                # "scheme": "https",
                # "accept":" */*",
                # "accept-encoding": "gzip, deflate, br",
                # "accept-language": "en-US,en;q=0.9",
                # "origin": "https://images-eu.ssl-images-amazon.com",
                # "referer": "https://images-eu.ssl-images-amazon.com/",
                # "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
                # "sec-ch-ua-mobile": "?0",
                # "sec-ch-ua-platform": "Windows",
                # "sec-fetch-dest": "font",
                # "sec-fetch-mode": "cors",
                # "sec-fetch-site": "cross-site",
                # "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 S,afari/537.36"
                # }
                
    #     for i in listings:
            
    #         URL2 = "https://www.amazon.in/dp/{0}?th=1&psc=1".format(i)
    #         # print("URL OF A PRODUCT:", URL2,"\n")
    #         # print("URL FORMAT:", url.format(i))
    
            # for i in listings:
            #     myUrl = "https://www.amazon.in/dp/" + i + "?th=1&psc=1"
            #     print("myurl = ",myUrl)
            #     time.sleep(1)
                yield sp.Request("https://www.amazon.in/AKAAS-Sleeve-Formal-White-Shirt_L/dp/B07547YK2J/ref=sr_1_1?crid=3V830F1OLTC48&keywords=shits&qid=1673421903&sprefix=shit%2Caps%2C362&sr=8-1", callback=self.parse)

    def parse(self, response):
            print("dfdfdfdf")
        # print("RESPONSE URL FORMAT IN PARSE FUNCTION:", response.url)
        # for i in listings:
            print("kkkkkkkkkkk = ",response.body)
            # time.sleep(2)
            txt = response.xpath("//span[@id='productTitle']/text()").get()
            # a = response.xpath('//*[@id="appContainer"]/div[2]/div/div/div[2]/div/div[3]/div/div[1]/div[1]/text()').getall()
            # b = response.xpath('//*[@id="appContainer"]/div[2]/div/div/div[2]/div/div[3]/div/div[1]/div[1]/text()').get()
            print('coooooooooo = ',txt)
            # print(a)
            # print(b)
        #     URL2 = "https://www.amazon.in/dp/{0}?th=1&psc=1".format(i)
        #     # print("URL OF A PRODUCT:", URL2,"\n")
        #     # print("URL FORMAT:", url.format(i))
        # # URL = response.url+"?th=1&psc=1"
        #     print("rrrrrrrrrrrrr = ",response)
        #     print("7777777777777= ",response.url)
        #     td = {}
        #     asin = re.findall('B0.{8}', URL2)[0]

            # print(f"ASIN: {asin} ; URL: {URL}")
            # td['ASIN'] = asin
            # td['URL'] = URL
            # for key in xpaths.keys():
            
            #         path = xpaths[key]+'/text()'
            #         try:
            #             value = response.xpath(path).extract()
            #             print("============== = ", xpaths[key],value)
            #         except:
            #             value = "NOT GIVEN"
            #         # print(f"{key}: {value}")
            #             print("NNNNNNNNNNNNNNNN")
            #         td[key] = value
                
            # print('************* = ',td)
            
            print("ggggggggggggggggggggggggggggggg")
            
            yield {"data":txt}


process = CrawlerProcess(settings={'LOG_LEVEL': 'DEBUG',
                                   'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                                   'FEEDS': {"scrap_out.csv": {'format': 'csv', 'overwrite': True}}
                                   })
process.crawl(AmazonPlpSpider)
process.start()
df = pd.read_csv('scrap_out.csv')
df.to_excel("scrap_df.xlsx", index=False)
















# df = pd.read_csv('scrap_out.csv')
# df.to_excel("scrap_df.xlsx", index=False)


# allowed_domains = ['www.amazon.com']
# csv_file_path="E:/Dhiomics/Scrapping/TMRW/PDP/Input/Demo.xlsx"
# df= pd.read_excel(csv_file_path, sheet_name='Amazon')
# # start_urls = ['https://www.amazon.com/s?k=shirts&crid=V4WQRA9IT1WY&sprefix=shir%2Caps%2C343&ref=nb_sb_noss_2']
# main_data = []
# print("DF = ",df[0])
# start_urls = []
# product={}
# custom_settings = {
#     'DOWNLOAD_DELAY': 0.5 # 2 seconds of delay
#     }

# for i in df[0]:
#     start_urls.append("https://www.amazon.in//dp/" + str(i) + "?th=1&psc=1")
# print("Start URLs = ",len(start_urls))

# def parse(self, response):
#     # global start_urls
#     # print("self123 = ",self.start_urls)
#     for i in self.start_urls:
#         productid=i[26:36]
#         title = response.xpath("//span[@id='productTitle']/text()").get()
#         price = response.css('.a-offscreen::text').get()
#         image_url = response.css('.a-dynamic-image::attr(src)').get()
#         # description = response.xpath('//div[@id="productDescription"]/p/span/text()').get()
#         self.product = {
#         'title': title,
#         'price': price,
#         'image_url': image_url,
#         'productid':productid
#         # 'description': description
#                     }

#     self.main_data.append(self.product)
#     # print('Main_Df = ',self.main_data)
#     output_data = pd.DataFrame(self.main_data)
#     print("OUt = ",output_data)

# # Return the product details
#     yield output_data.to_csv("C:/Users/kpava/OneDrive/Desktop/OuputData.csv")
