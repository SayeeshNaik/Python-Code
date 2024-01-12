import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

tag_lis = []
id_lis = []
class_lis = []
text_content_lis = []
src_lis = []

name_lis = []
price_lis = []
discount_lis = []
discount_price_lis = []

Data_Sheet = pd.read_excel("AutomationData.xlsx")
url = Data_Sheet['baseUrl']
xpath = Data_Sheet['XPath']


    
def extractor(url,Xpath):
    link = url
    driver = webdriver.Chrome()
    driver.get(link)
    xpath = Xpath
    
    elmt = driver.find_elements(By.XPATH,xpath)
    count_of_xpath = len(elmt)
    for unique in range(count_of_xpath):
        
        if(unique == 0):
            tag_lis.append(elmt[unique].tag_name)
        else: tag_lis.append('''" "''')
        
        if(elmt[unique].get_attribute("id")!=''):
            id_lis.append(elmt[unique].get_attribute("id"))
        else: id_lis.append("***")
        
        if(elmt[unique].get_attribute("class")!=''):
            class_lis.append(elmt[unique].get_attribute("class"))
        else: class_lis.append("***")
        
        if(elmt[unique].text != ''):
            text_content_lis.append(elmt[unique].text)
        # else: text_content_lis.append("***")
        
        if(elmt[unique].get_attribute("src")!='' and elmt[unique].get_attribute("src")!=None):
            src_lis.append(elmt[unique].get_attribute("src"))
        # else: src_lis.append("***")
        
        if(unique == count_of_xpath-1):
            tag_lis.append(" ")
            id_lis.append(" ")
            class_lis.append(" ")
            text_content_lis.append(" ")
            src_lis.append(" ")
   

def test(url,xpath):
    link = url
    driver = webdriver.Chrome()
    driver.get(link)
    xpath = Xpath
    
    elmt = driver.find_elements(By.XPATH,xpath)
    count_of_xpath = len(elmt)
    print(count_of_xpath)
        

# for i in range(2):
#     url = Data_Sheet['baseUrl']
#     Xpath = Data_Sheet['XPath']
#     link = url[i]
#     driver = webdriver.Chrome()
#     driver.get(link)
#     xpath = Xpath[i]
#     l = len(driver.find_elements(By.XPATH,xpath))
#     for j in range(l):
#         a = driver.find_elements(By.XPATH,xpath)
#         val = a[j].text
#         try:
#             if(i==0):
#                 if(val!=''): name_lis.append(val)
#                 else: name_lis.append("***")
#             if(i==1):
#                 if(val!=''): price_lis.append(val)
#                 else: price_lis.append("***")
#             if(i==2):
#                 if(val!=''): discount_lis.append(val)
#                 else: discount_lis.append("***")
#             if(i==3):
#                 if(val!=''): discount_price_lis.append(val)
#                 else: discount_price_lis.append("***")
#         except: pass
            
#         print(a[j].text)
#     driver.close()
        

print(url[0],xpath[0])
driver = webdriver.Chrome()
driver.get(url[0])
a=driver.find_elements(By.XPATH,"(//DIV[(@class='_4rR01T')])").text
driver.close()
print(a)

        


# data = {"ProductName":name_lis,"Price":price_lis,"Discount":discount_lis,'GrandTotal':discount_price_lis}
# print(data)

# df = pd.DataFrame(data)
# df.to_excel('ExtractedData.xlsx')
        
        
        
# data = {"TagName":tag_lis, "Id":id_lis, "ClassName":class_lis, "TextContent":text_content_lis, "Src-Link":src_lis}
# df['Id'].style.set_properties(**{'background-color': 'gray'})
        
        
        
        
        
        
        
        
        
        
    