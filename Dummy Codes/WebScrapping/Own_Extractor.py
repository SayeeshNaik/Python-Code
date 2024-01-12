import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import gspread as gg

Data_Sheet = pd.read_excel("AutomationData.xlsx")
baseUrl = Data_Sheet['baseUrl'][0]
parentXpath = Data_Sheet['parentXpath']
xpath = Data_Sheet['XPath']
data_len = len(Data_Sheet)
data = {}

name_lis = []
price_lis = []
discount_lis = []
discount_price_lis = []

lis = []

product_len = 0
glob_url = ''
driver = webdriver.Chrome()
def get_page(url):
    global glob_url
    if(glob_url!=url):
      driver.get(url)
      glob_url = url

def extractor(url, parentXpath,xpath):
    global lis,product_len,baseUrl,data
    lis = []
    get_page(url)
    if(product_len==0):
      elmt_len = len(driver.find_elements(By.XPATH,parentXpath))
      product_len = elmt_len
    
    for i in range(1,product_len+1):
        myXpath = "({})[{}]{}".format(parentXpath,i,xpath)
        try:
          txt = driver.find_element(By.XPATH,myXpath).text
          if(txt==''): txt = "***"
          
        except: 
          txt = "***"
    
        lis.append(txt)
    return lis  
    if(url!=baseUrl): driver.close()
    
for i in range(data_len):
    url         = Data_Sheet['baseUrl'][i]
    parentXpath = Data_Sheet['parentXpath'][i]
    xpath       = Data_Sheet['XPath'][i]
    
    time.sleep(1)
    ans = extractor(url, parentXpath, xpath)
    print(ans)
    if(i==0): 
        name_lis = ans
        data.update({i :name_lis})
    if(i==1): 
        price_lis = ans
        data.update({i :price_lis})
    if(i==2): 
        discount_lis = ans
        data.update({i :discount_lis})
    if(i==3): 
        discount_price_lis = ans
        data.update({i :discount_price_lis})
 
    
# data = data

# df = pd.DataFrame(data)
# for i in range(data_len):
#   col_name = input("Enter Column Name "+ str(i+1) +" : ")
#   df = df.rename({i:col_name}, axis=1)

# df.to_excel('ExtractedData.xlsx')

    
gg = gg.service_account(filename='C:/Users/User/Downloads/automated-style-322407-aac51e71fea7.json')
sh = gg.open_by_url('https://docs.google.com/spreadsheets/d/1qHUWJr-aZmfuyixisQG6RwjR8Ln6mn0wPzwH7gaowxA/edit#gid=25307983')
ws = sh.worksheet('A worksheet15-Dec-22-17-03-51')
df = pd.DataFrame(ws.get_all_records())
print(df['NextButtonStatus'])
if(df['NextButtonStatus'][0]=='FALSE'):
    print('ss')




        