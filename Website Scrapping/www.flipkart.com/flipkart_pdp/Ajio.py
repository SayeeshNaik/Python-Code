import scrapy as sp
import pandas as pd
import datetime
import re
from urllib.parse import urlparse
from scrapy.crawler import CrawlerProcess


class AjiopdpSpider(sp.Spider):
    # custom_settings = {
    #     # 'DOWNLOAD_DELAY': 1,  # minimum download delay
    #     # 'AUTOTHROTTLE_ENABLED': True,
    # }
    # Global Flow 
    name = 'ajio'
    main_url = 'https://www.ajio.com/p/'
    productId_df = pd.read_excel("Ajio_ProductID.xlsx")
    productId_df['ProductId'] = main_url + productId_df['ProductId'].astype(str)
    all_urls = productId_df['ProductId']
    Exceception_Id = []
    logical_df = {
    'Title' : '{"altText":',
    'Brand' : '{"brandName":',
    'MRP' : '","formattedValue',
    'Discount %': ',"discountPercent"',
    "Total Sizes": '"scDisplaySize":',
    'Product Details': '"comparable":true,"featureValues":[{"value":"',
    }
        
    def start_requests(self):
        for url in self.all_urls:
          yield sp.Request(url,callback=self.parse)        
        
    def parse(self, response):
        page = str(response.body)
        start_ind = page.index('{"wishlist":{}')
        end_ind = page.index('"unRatedProducts":""}}')+22
        data = page[start_ind:end_ind]
        productId = response.url.split('/p/')[1]
        temp_dict = {}
        
        try:
            temp_dict.update({"Date": datetime.date.today().strftime("%d-%m-%Y")})
            temp_dict.update({"Week": datetime.datetime.today().weekday()})
            temp_dict.update({"Marketplace": urlparse(response.url).netloc.replace('www.','').replace('.com','').title()})
            temp_dict.update({"Product_Id": productId})
            temp_dict.update({"Product URL": response.url})
            for key in self.logical_df:
                logic = self.logical_df[key]
                l = data.count(logic)
                if(key=='MRP'):  
                    amount_lis=[m.start() for m in re.finditer(logic, data)]
                    val1 = list(map(int, re.findall(r'\d+', data[amount_lis[0]:amount_lis[0]+40])))
                    val1=int(''.join(map(str,val1[0:len(val1)-1])))
                    val2 = list(map(str, re.findall(r'\d+', data[amount_lis[1]:amount_lis[1]+40])))
                    val2=int(''.join(map(str,val2[0:len(val2)-1])))
                    if(val1>val2):temp_dict.update({key: val1})
                    else: temp_dict.update({key: val2})
                    if(val1<val2):temp_dict.update({'Selling Price': val1})
                    else: temp_dict.update({'Selling Price': val2})
                # elif(key=='Discount %'):
                #     val = data[data.find(logic):data.find(logic)+200].split(':')[1].split(',')[0]
                #     print("DDDDDDDDDDDDDDDD = ",type(temp_dict['MRP']),type(temp_dict['Selling Price']),val)
                #     if(temp_dict['MRP']!=temp_dict['Selling Price']):
                #         temp_dict.update({key: val})
                #     else:temp_dict.update({key: 'none'})
                
                elif(key=='Total Sizes'):
                    val_ind = [i.start() for i in re.finditer(logic, data)]
                    val = []
                    for ind in val_ind: val.append(data[ind:ind+21].split(':')[1].replace(',','').replace('"',''))
                    temp_dict.update({"No of Sizes": len(val)})
                    temp_dict.update({key: [val]})
                elif(key=='Product Details'):
                    val_ind = [i for i in range(len(data)) if data.startswith(logic, i)]
                    val = []
                    for ind in val_ind:
                        ind += len(logic)
                        val.append(data[ind:ind+500].split('"}]}')[0].replace("\\",'').replace('5\'7"',''))
                    try:val.remove('UNI')
                    except: pass
                    temp_dict.update({key: [val]})
                else:
                    val = data[data.find(logic):data.find(logic)+200].split(':')[1].split(',')[0]
                    temp_dict.update({key: val.replace('"','')})
        except: self.Exceception_Id.append(productId)
        pd.DataFrame([{"Exception_ID":self.Exceception_Id}]).to_excel("Ajio_ExceptionID.xlsx")  
        
        try:
            if(temp_dict['MRP']==temp_dict['Selling Price']):
             temp_dict.update({'Discount %': ''})
            else:print("hhhhhhhhhhhh = ",temp_dict)
        except: pass
        if(val1==val2):temp_dict.update({"Selling Price": ''})
        return temp_dict
        
process = CrawlerProcess(settings={'LOG_LEVEL': 'DEBUG',
                                   'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                                   'FEEDS': {"AjioPDP_OutputData.csv": {'format': 'csv', 'overwrite': True}}
                                   })
process.crawl(AjiopdpSpider)
process.start()

df = pd.read_csv('AjioPDP_OutputData.csv')
df.to_excel("AjioPDP_OutputData.xlsx", index=False)