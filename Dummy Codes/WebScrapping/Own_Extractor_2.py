import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import gspread as gg


resData = []
# gg = gg.service_account(filename='C:/Users/User/Downloads/automated-style-322407-aac51e71fea7.json')
# sh = gg.open_by_url('https://docs.google.com/spreadsheets/d/1qHUWJr-aZmfuyixisQG6RwjR8Ln6mn0wPzwH7gaowxA/edit#gid=25307983')
# ws = sh.worksheet('A worksheet16-Dec-22-13-10-29')
# df = pd.DataFrame(ws.get_all_records())
df = pd.read_excel('AutomationData.xlsx')
all_baseurl = df['baseUrl']
all_parentXpath = df['parentXpath']
all_xpath = df['XPath']
all_nxt_btn_status = df['NextButtonStatus']

product_len = 0
glob_url = ''
driver = webdriver.Chrome()

# driver.get('https://www.flipkart.com/search?q=laptop&sid=6bo%2Cb5g&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_3_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_3_na_na_na&as-pos=1&as-type=RECENT&suggestionId=laptop%7CLaptops&requestId=2d1c7961-570e-46d2-89d6-2ff97b45176b&as-backfill=on&sort=price_desc&page=2')


name_lis = []
data = {} 

def get_page(url):
    global glob_url
    if(glob_url!=url):
      driver.get(url)
      glob_url = url

def extractor(url,parentXpath,xpath,nxt_btn):
    global resData
    lis = []
    get_page(url)
    elmt_len = len(driver.find_elements(By.XPATH,parentXpath))
    product_len = elmt_len
    for i in range(1,product_len+1):
        myXpath = "({})[{}]{}".format(parentXpath,i,xpath)
        if(nxt_btn == 'TRUE'):
            # len_of_nxt = len(driver.find_elements(By.XPATH,xpath))
            # print(len_of_nxt)
            # if(len_of_nxt>1):
            #     myXpath = "({})[{}]".format(xpath,2)
            # else:
            #     myXpath = "{}".format(xpath)
            
            myXpath = "(//A[(@class='_1LKTO3')])[2]"
            ln = len(driver.find_elements(By.XPATH,myXpath))
            driver.find_element(By.XPATH,myXpath).click()
            out_loop()
            print('mypath = ',myXpath)
        else:
            try:
              txt = driver.find_element(By.XPATH,myXpath).text
              if(txt==''): txt = "***"
              
            except: 
              txt = "***"
            lis.append(txt)
    
    # print("== ",lis)
    resData.append(lis)
    return lis  
    
    

def out_loop():
    for i in range(len(df)):
        time.sleep(1)
        ans = extractor(all_baseurl[i],all_parentXpath[i],all_xpath[i],all_nxt_btn_status[i])
        if(i==0): 
            name_lis = ans
            data.update({i :name_lis})
    
# out_loop()

extractor("https://www.goa.gov.in/government/who-is-who/", "", "//a[(@title='Go to next page')]", '')

myData = {}
print(len(resData))
for i in range(len(resData)):
    col_name = input('Enter colum name '+str(i+1)+' : ')
    myData[col_name] = resData[i]
xl_data = pd.DataFrame(myData)
xl_data.to_excel('Output.xlsx')
