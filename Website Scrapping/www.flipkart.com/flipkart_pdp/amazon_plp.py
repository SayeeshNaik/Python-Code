import scrapy as sp
import pandas as pd
from scrapy.crawler import CrawlerProcess

class FlipkartpdpSpider(sp.Spider):
    name = 'amazonplp'
    all_products = ['mobile','tv','laptop']
    main_xpaths_df = pd.read_excel("xpath_amazon_plp.xlsx")
    xpaths_df = dict(zip(main_xpaths_df['fields'],main_xpaths_df['xpath']))
    main_div_xpath = '('+xpaths_df['main_div']+')'
    del xpaths_df['main_div']
    output_data = []
    
    def start_requests(self):
        try:
          if(len(self.output_data)>0): self.output_data = []
        except: pass
       
        num_of_page = 50
        for product_name in self.all_products:
            base_url = "https://www.amazon.in/s?k="+product_name+"&page="
            for pagination in range(num_of_page): yield sp.Request(base_url+str(pagination), callback=self.parse)
    
    def parse(self, response):
        len_main_div = len(response.xpath(self.main_div_xpath).getall())
        data_lis = []
        for i in range(1,len_main_div+1):
            temp_dict = {}
            for key_name in self.xpaths_df:
                try:
                    product_xpath = self.main_div_xpath + str([i]) + self.xpaths_df[key_name]
                    if(key_name=='MRP'):
                        val = response.xpath(product_xpath + '/text()').getall()
                        temp_dict.update({key_name: val[1]})
                    elif(key_name=='DETAILS'):pass
                    elif(key_name=="IMG_URL"):
                        val = response.xpath(product_xpath).get()
                        temp_dict.update({key_name: val})
                    else:
                        val = response.xpath(product_xpath +  '/text()').get()
                        temp_dict.update({key_name: val if val!=None and val!='' else "None"})
                        temp_dict.update({"Base_URL": response.url})
                except: temp_dict.update({key_name: "***"})
            data_lis.append(temp_dict)
        self.output_data += data_lis
        pd.DataFrame(self.output_data).to_excel("AmazonPLP_OutputData.xlsx")
        return data_lis    
     
process = CrawlerProcess(settings={'LOG_LEVEL': 'DEBUG',
                                   'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                                   'FEEDS': {"AmazonPLP_OutputData.csv": {'format': 'csv', 'overwrite': True}}
                                   })
process.crawl(FlipkartpdpSpider)
process.start()