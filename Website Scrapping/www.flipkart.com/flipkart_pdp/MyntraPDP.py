import scrapy as sp
import pandas as pd
import datetime
from requests_html import HTMLSession
import re
import json
from urllib.parse import urlparse
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from selenium.webdriver.common.by import By

main_url = "https://www.myntra.com/"
exception_id = []
exception_url = []
trying_url = []

class MyntrapdpSpider(sp.Spider):
    
    # Global Flow 
    name = 'myntra'
    main_url = "https://www.myntra.com/"
    # productId_df = pd.read_excel("MyntraPDP_ProductID.xlsx")
    productId_df = pd.read_excel("MyntraPDP_ProductID(abhi).xlsx")
    productId_df['Product_ID'] = main_url + productId_df['Product_ID'].astype(str)
    all_urls = productId_df['Product_ID']
  
    logical_df = {
        'Title': '"name":',
        'MRP': '"mrp":',
        'Selling Price': '"discountedPrice":',
        'Discount %': '"discountPercent":',
        'Product Rating': '"averageRating":',
        'Available Sizes': '"available":true',
        'Non-Available Sizes': '"available":false',
        'In Stock': '"outOfStock":',
        'Product Type':'@id" : "https://www.myntra.com/',
        'Product Details':',"title":"Product Details",',
    }
    
    def start_requests(self):
        pass
        for url in self.all_urls[300:400]:
          yield sp.Request(url,callback=self.parse)        
        
    def parse(self, response):
        main_page = str(response.body)
        url = response.url.split("?")[0]
        url = response.url
        productID = response.url.split(self.main_url)[1]
        script_start = [m.start() for m in re.finditer('<script>window.__myx = ', main_page)]
        script_start = script_start[0]+len('<script>window.__myx = ')
        script_end = [m.start() for m in re.finditer('</script>', main_page)]
        page = main_page[script_start:script_end[10]]
        temp_dict = {}
        total_sizes = []
        temp_dict.update({"Date": datetime.date.today().strftime("%d-%m-%Y")})
        temp_dict.update({"Week": datetime.datetime.today().weekday()})
        temp_dict.update({"Marketplace": urlparse(url).netloc.replace('www.','').replace('.com','').title()})
        temp_dict.update({"Product_Id": productID})
        temp_dict.update({"Product URL": url})
        for key in self.logical_df:
            logic = self.logical_df[key]
            try:  ind = page.index(logic)
            except: 
                temp_dict.update({key:"***"})
            try:  
                if(key=='Title'):
                    val = page[ind:ind+500].split(':')[1].split(',')[0].replace('"','').split()
                    temp_dict.update({'Brand': val[0]})
                    temp_dict.update({key: ''.join(val[1:])})
                elif(key=='Available Sizes'):
                    available_sizes = [m.start() for m in re.finditer(logic, page)]
                    val = []
                    for available_size in available_sizes:
                        ind=available_size
                        val.append(page[ind-20:ind-1].split(':')[1].replace('"',''))
                    temp_dict.update({"No of Available Sizes": len(val)})
                    temp_dict.update({key: [val]})
                    total_sizes += val
                elif(key=='Non-Available Sizes'):
                    non_available_sizes = [m.start() for m in re.finditer(logic, page)]
                    val = []
                    for non_available_size in non_available_sizes:
                        ind=non_available_size
                        val.append(page[ind-20:ind-1].split(':')[1].replace('"',''))
                    temp_dict.update({"No of Non-Available Sizes": len(val)})
                    temp_dict.update({key: [val]})
                    total_sizes+=val
                    temp_dict.update({"No of Total Sizes": len(total_sizes)})
                    temp_dict.update({"Total Sizes": [total_sizes]}) 
                elif(key=='Product Type'):
                    val =  [m.start() for m in re.finditer(logic, main_page)]
                    val = main_page[val[1]:val[1]+100].split(main_url)[1].split('"')[0]
                    val = val.split('-')
                    temp_dict.update({"Product Type": val[1].title()})   
                    temp_dict.update({"Division":val[0].title() })      
                else:
                    try:
                        val = page[ind:ind+500].split(':')[1].split(',')[0].replace('"','')
                    except: val = ""
                    temp_dict.update({key: val})
            except: 
                temp_dict.update({key: "***"})
                if(len(response.url.split("?"))>1):
                    trying_url.append(response.url)
        try: 
            if(int(temp_dict['Product Rating'])>5):
                temp_dict['Product Rating']=''
            if(temp_dict['MRP']==temp_dict['Selling Price']):
                temp_dict['Discount %']=''
            if(temp_dict['In Stock']!='true'):
                temp_dict['In Stock']='In Stock'
            else: 
                temp_dict['In Stock']='Out Of Stock'
                temp_dict['No of Available Sizes'] = '0'
                temp_dict['Available Sizes'] = [[]]
                temp_dict['No of Non-Available Sizes'] = '0'
                temp_dict['Non-Available Sizes'] = [[]]
                temp_dict['No of Total Sizes'] = '0'
                temp_dict['Total Sizes'] = [[]]
        except: pass
        try:
            if(temp_dict['In Stock']=='true'): 
                temp_dict['In Stock']='Out Of Stock'
                temp_dict['No of Available Sizes'] = '0'
                temp_dict['Available Sizes'] = [[]]
                temp_dict['No of Non-Available Sizes'] = '0'
                temp_dict['Non-Available Sizes'] = [[]]
                temp_dict['No of Total Sizes'] = '0'
                temp_dict['Total Sizes'] = [[]]
            if(temp_dict['In Stock']=='false'):temp_dict['In Stock'] = 'In Stock'
            if(temp_dict['Brand']=='tags.fewLeft'):
                exception_url.append(response.url)

            else:  return temp_dict
        except: pass
       
process = CrawlerProcess(settings={'LOG_LEVEL': 'DEBUG',
                                   'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                                   'FEEDS': {"MyntraPDP_OutputData.csv": {'format': 'csv', 'overwrite': True}}
                                   })
process.crawl(MyntrapdpSpider)
process.start()
try:
    df = pd.read_csv('MyntraPDP_OutputData.csv')
    df.to_excel("MyntraPDP_OutputData.xlsx", index=False)
except: pass

# For Product Details
# details_urls = pd.read_excel("MyntraPDP_OutputData.xlsx")
# details_urls = list(details_urls['Product URL'])
# for d_url in details_urls:
#     page = str(HTMLSession().get(d_url).content)
#     login_df = {"Product Details":'"articleAttributes":'}
#     try:
#         st_ind = page.find(login_df['Product Details'])+len(login_df['Product Details'])
#         data = page[st_ind:].split("}")[0]+'}'
#         data = json.loads(data)
#         specification = ['Fabric','Length','Multipack Set','Number of Pockets','Pattern','Sleeve Length',
#         'Surface Stying','Fit','Main Trend','Neck','Occasion','Print or Pattern Type','Sleeve Styling',
#         'Wash Care']
#         details_dict = {}
#         for key in specification:
#             try:
#                 details_dict.update({key: data[key]})
#             except: pass
#     except:details_dict = {}
#     print("ddddddddd = ",d_url,details_dict)

pd.DataFrame({"Exception_URL":exception_url}).to_excel("Myntra_Exception_ProductID.xlsx",index=False)
pd.DataFrame({"Trying_URL":trying_url}).to_excel("Myntra_Trying_ProductID.xlsx",index=False)

print(exception_url,'\n',len(exception_url))
print(trying_url,'\n',len(trying_url))


  
xpath_df = pd.read_excel("xpath_myntra_pdp.xlsx")
xpath_dict = dict(zip(xpath_df['field'],xpath_df['xpath']))
selenium_urls = pd.read_excel("Myntra_Trying_ProductID.xlsx")
selenium_urls = list(selenium_urls['Trying_URL'])
driver = webdriver.Chrome()
again_trying = []
def selenium_scrapper(url):
    productID = url.split("?")[0].split(main_url)[1]
    driver.get(url)
    temp_dict = {}
    for key in xpath_dict:
        xpath = xpath_dict[key]
        temp_dict.update({"Date": datetime.date.today().strftime("%d-%m-%Y")})
        temp_dict.update({"Week": datetime.datetime.today().weekday()})
        temp_dict.update({"Marketplace": urlparse(url).netloc.replace('www.','').replace('.com','').title()})
        temp_dict.update({"Product_Id": productID})
        temp_dict.update({"Product URL": url})
        try:
            if(key=='Available Sizes' or key=='Non-Available Sizes' or key=='Total Sizes'):
               val = driver.find_elements(By.XPATH,xpath)
               if(len(val)>0): val = [val.text for val in val]
               temp_dict.update({'No of '+key: len(val)})
            elif(key=='In Stock'):
                try:
                    val = driver.find_element(By.XPATH,xpath).text
                    val = "Out Of Stock"
                except: val = "In Stock"
            
            else: val = driver.find_element(By.XPATH,xpath).text
            if(key=='Product Type'):
                temp_dict.update({key: val.split()[1].title()})
                temp_dict.update({'Division': val.split()[0].title()})
            else:
                temp_dict.update({key: val})
        except: 
            temp_dict.update({key: ''})
        try: again_trying.append(url) if(temp_dict['Title']=='') else 0
        except: pass
    return temp_dict
  
selenium_outputData = []
for url in selenium_urls:
  df = selenium_scrapper(url)
  print("ddddddddddddd = ",df)
  selenium_outputData.append(df)

driver.close()
main_output_df = pd.read_excel('MyntraPDP_OutputData.xlsx')

# Filtration
selenium_outputDF = pd.DataFrame(selenium_outputData)
selenium_outputDF['MRP']=selenium_outputDF['MRP'].str.replace('MRP','').str.replace('₹','')
selenium_outputDF['Selling Price']=selenium_outputDF['Selling Price'].str.replace('₹','')
selenium_outputDF['Discount %']=selenium_outputDF['Discount %'].str.replace('(','',regex=True).str.replace('%','',regex=True).str.replace('OFF','',regex=True).str.replace(')','',regex=True)

pd.concat([main_output_df,selenium_outputDF]).to_excel("MyntraPDP_Filtered_OutputData.xlsx",index=False)

print(again_trying,len(again_trying))