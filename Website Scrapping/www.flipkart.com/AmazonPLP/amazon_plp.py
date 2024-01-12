import scrapy as sp
import pandas as pd
from scrapy.crawler import CrawlerProcess
from datetime import date
import time
import numpy as np


num =  "3800-4000"

class AmazonplpSpider(sp.Spider):
    name = 'amazonplp'
    
    # df = pd.read_excel("D:/Scraping/first_scraping/first_scraping/spiders/Product_list.xlsx")
    # all_products = list(df["Product_list"])
    
    df = pd.read_excel("Batch_"+num+".xlsx")
    all_products = list(df["Product_list"])
    main_xpaths_df = pd.read_excel("xpath_amazon_plp.xlsx")
    xpaths_df = dict(zip(main_xpaths_df['fields'],main_xpaths_df['xpath']))
    main_div_xpath = '('+xpaths_df['Main_Div']+')'
    del xpaths_df['Main_Div']
    Exception_product_name=[]
    output_data = []
    
    def start_requests(self):
        try:
          if(len(self.output_data)>0): self.output_data = []
        except: pass
       
        num_of_page = 5
        for product_name in self.all_products:
            base_url = "https://www.amazon.in/s?k="+product_name+"&page="
            for pagination in range(num_of_page): yield sp.Request(base_url+str(pagination), callback=self.parse)
    
    def parse(self, response):
        len_main_div = len(response.xpath(self.main_div_xpath).getall())
        data_lis = []
        productName= response.url.split('https://www.amazon.in/s?k=')[1].split('&')[0]
        productName = productName.replace("%20",' ')
        for i in range(1,len_main_div+1):
            temp_dict = {}
            for key_name in self.xpaths_df:
                today = date.today()
                temp_dict.update({"Date":str(today.strftime("%d-%m-%Y"))})
                temp_dict.update({"Week":str(today.isocalendar().week)})
                temp_dict.update({"Marketplace":'Amazon'})
                temp_dict.update({"Keyword":productName})
                temp_dict.update({"Platform Sponsored":''})
                temp_dict.update({"Base URL":response.url})
                temp_dict.update({"Available Size":''})
                temp_dict.update({"Total Reviews":0})
                temp_dict.update({"Deal Text":''})
                temp_dict.update({"Total Reviews":''})
                
            
                try:
                    product_xpath = self.main_div_xpath + str([i]) + self.xpaths_df[key_name]
                    
                    if(key_name=='Mrp'):
                        val = response.xpath(product_xpath +  '/text()').getall()
                        
                        if len(val)==2:
                            if val[0]:
                               temp_dict.update({key_name: val[0]})
                            if val[1]:
                                temp_dict.update({'Mrp_1':val[1]})
                        if len(val)==1:
                            temp_dict.update({key_name:val})
                        if len(val)==0:
                            temp_dict.update({key_name:'nan'})
                        
                    if(key_name=='Rating'):
                        try:
                            val = response.xpath(product_xpath + '/text()').get()
                            temp_dict.update({key_name:val})
                        except:
                            temp_dict.update({key_name:'nan'})
                            
                    if(key_name=='Brand'):
                        try:
                            val = response.xpath(product_xpath + '/text()').get()
                            temp_dict.update({key_name:val})
                        except:
                            temp_dict.update({key_name:'nan'})
                            
                    if(key_name=='Title'):
                        try:
                            val = response.xpath(product_xpath + '/text()').get()
                            temp_dict.update({key_name:val})
                        except:
                            temp_dict.update({key_name:'nan'})
                    
                        
                    elif(key_name=="Image URL"):
                        try:
                           val = response.xpath(product_xpath).get()
                           temp_dict.update({key_name: val})
                        except:
                            temp_dict.update({key_name:'nan'})
                    elif(key_name=="Product URL"):
                        try:
                            val = response.xpath(product_xpath).get()
                            val = 'https://www.amazon.in'+val
                            temp_dict.update({key_name:val})
                        except:
                            temp_dict.update({key_name:'nan'})
                    
                    elif(key_name=='Price'):
                        val = response.xpath(product_xpath +  '/text()').getall()
                        
                        if len(val)==2:
                            if val[0]:
                                temp_dict.update({key_name: val[0]})
                            if val[1]:
                                temp_dict.update({'Price_1':val[1]})
                        if len(val)==1:
                            temp_dict.update({key_name:val[0]})
                        if len(val)==0:
                            temp_dict.update({key_name:'nan'})

                    elif(key_name=='Tags'):
                        val = response.xpath(product_xpath + '/text()').get()
                        if(val=='FREE Delivery by Amazon'):
                            temp_dict.update({key_name:val})
                        else:
                            temp_dict.update({key_name:"No Free Delivery by Amazon"})
                            
                    elif(key_name=='Discount'):
                        val = response.xpath(product_xpath +  '/text()').getall()
                        if len(val)==2:
                            if val[0]:
                                temp_dict.update({key_name: val[0]})
                            if val[1]:
                                temp_dict.update({'Discount_1':val[1]})
                        if len(val)==1:
                            temp_dict.update({key_name:val[0]})
                        if(len(val)==0):
                            temp_dict.update({key_name:'nan'})
                        
                    else:
                        val = response.xpath(product_xpath +  '/text()').get()
                        temp_dict.update({key_name: val if val!=None and val!='' else ''})
                except: temp_dict.update({key_name: "***"})
            data_lis.append(temp_dict)
        self.output_data += data_lis
        self.Exception_product_name.append(response.url) if(len(data_lis)==0) else 0
        pd.DataFrame({"Exception_Product_Name":self.Exception_product_name}).to_excel("Amazon_Exception_"+num+".xlsx",index=False)
        pd.DataFrame(self.output_data).to_excel("AmazonPLP_OutputData.xlsx",index=False)
        return data_lis    
     
process = CrawlerProcess(settings={'LOG_LEVEL': 'DEBUG',
                                   'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                                #    'FEEDS':{"AmazonPLP_OutputData_"+num+".csv": {'format': 'csv', 'overwrite':True}}
                                   })
process.crawl(AmazonplpSpider)
process.start()



# Data postprocessing



df = pd.read_excel("AmazonPLP_OutputData_"+num+".xlsx")

df['Rating']=df['Rating'].astype(str)
df['Price']=df['Price'].astype(str)
df['Title']=df['Title'].astype(str)
df['Product URL']=df['Product URL'].astype(str)
df['Brand']=df['Brand'].astype(str)

# df=df[(df['Price'] !='nan') & (df['Title'] !='nan') & (df['Product URL'] !='nan') 
#       & (df['Discount'] !='nan') & (df['Mrp'] !='nan') & (df['Brand'] !='nan')  
#       & (df['Rating'] !='nan') & (df['Rating'] !='None')]
df=df[(df['Price'] !='nan') &(df['Price'] !='0') &(df['Title'] !='nan') & (df['Product URL'] !='nan') ]
df['Is Sponsored']=df['Is Sponsored'].astype(str)
df['Is Sponsored'] = df['Is Sponsored'].str.replace('nan','Not Sponsered')
df['Availability']=df['Availability'].astype(str)
df['Availability'] = df['Availability'].str.replace('nan','Not Showing')
df['Delivery Text']=df['Delivery Text'].astype(str)
df['Delivery Text'] = df['Delivery Text'].str.replace('nan','No Deal Available')
df['Delivery Text'] = df['Delivery Text'].str.replace("Amazon's ",'No Deal Available')


df['Total Reviews']=df['Total Reviews'].astype(str)
df['Total Reviews'] = df['Total Reviews'].str.replace("nan",'0')
df['Rating'] = df['Rating'].str.replace("nan",'0')

df['Price_1']=df['Price_1'].astype(str)
df['Price_1'] = df['Price_1'].str.replace("nan",'0')

df['Discount']=df['Discount'].astype(str)
df['Discount'] = df['Discount'].str.replace("nan",'0')
df['Mrp']=df['Mrp'].astype(str)
df['Mrp'] = df['Mrp'].str.replace("nan",'0')

df['Mrp_1']=df['Mrp_1'].astype(str)
df['Mrp_1'] = df['Mrp_1'].str.replace("nan",'0')

df['Discount_1']=df['Discount_1'].astype(str)
df['Discount_1'] = df['Discount_1'].str.replace("nan",'0')


df['Offers']=df['Offers'].astype(str)
# df['Offers'] = df['Offers'].str.replace("None",'nan')



df['Price'] = df['Price'].str.replace("₹",'')

df['Mrp'] = df['Mrp'].str.replace("₹",'')
df['Mrp'] = df['Mrp'].str.replace("[",'')
df['Mrp'] = df['Mrp'].str.replace("]",'')
df['Mrp'] = df['Mrp'].str.replace("'",'')
df['Mrp_1'] = df['Mrp_1'].str.replace("₹",'')

df['Discount'] = df['Discount'].str.replace('%','').str.replace('off','')
df['Discount'] = df['Discount'].str.replace('(','').str.replace(')','')
df['Discount'] = df['Discount'].str.replace("'",'')


df['Discount_1'] = df['Discount_1'].str.replace('%','').str.replace('off','')
df['Discount_1'] = df['Discount_1'].str.replace('(','').str.replace(')','')
df['Rating'] = df['Rating'].str.replace('(','').str.replace(')','')

df['Rating Count'] = df['Rating Count'].str.replace('out of 5 stars','')

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
filtered_df = df.to_excel("AmazonPLP_OutputData_"+num+".xlsx",index=False)