import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import io

base_url_lis = ["https://assam.gov.in/list-of-secretaries",
"https://www.ap.gov.in/#/government/councilofministers",
"https://state.bihar.gov.in/main/CitizenHome.html",
"http://agriportal.cg.nic.in/PortEn/ContactListForWhoisWho_En.html",
"https://www.goa.gov.in/government/who-is-who/",
"https://gad.gujarat.gov.in/personnel/secretaries-government-gujarat.htm",
"https://himachal.nic.in/en-IN/council-of-ministers.html",
"https://www.jkgad.nic.in/leftmenu/officers_gad.aspx",
"https://www.jharkhand.gov.in/Home/WebDirectory",
"https://karnataka.gov.in/gokdirectory/en",
"https://gad.kerala.gov.in/who-who",
"https://finance.mp.gov.in/whos-who",
"https://gad.maharashtra.gov.in/en/whos-who",
"http://www.ditmanipur.gov.in/who-is-who/",
"https://meghalaya.gov.in/key-contacts/council-of-ministers",
"https://mizoram.nic.in/gov/minister.htm",
"https://odisha.gov.in/about-us/whos-who/department",
"https://ludhiana.nic.in/about-district/whos-who/",
"https://minority.rajasthan.gov.in/Directorate/Who_isWho.aspx",
"https://sikkim.gov.in/mygovernment/whos-who/council-of-ministers",
"https://www.tn.gov.in/contact_directory",
"https://westtripura.nic.in/whos-who/",
"https://governoruk.gov.in/whos-who/",
"http://upcmo.up.nic.in/cabinet_minister.htm",
"https://wbpower.gov.in/whos-who/",
"https://nicobars.andaman.nic.in/about-district/whos-who/",
"https://www.meity.gov.in/about-meity/who-is-who"]


main_df = pd.DataFrame()
exception_lis = []
empty_df = []

def simple(url):
    global main_df
    link = url
    html = requests.get(link)
    soup = BeautifulSoup(html.content, 'html.parser')
    table_div = soup.find_all('table')
    
    num = 0
    for table in table_div:
        num += 1
        table = table.prettify( formatter="html" ) 
        df = pd.read_html(table)
        main_df =pd.concat([main_df, df[0]])
        if(len(df[0])>0):
          xl_genetator(url,num)
          
    if(len(main_df)==0):
        empty_df.append(url)

def difficult(url):
    global main_df
    link = url
    driver = webdriver.Chrome()
    driver.get(link)
    time.sleep(2)
    html = driver.page_source
    
    html_file = open("Output.html","w",encoding="utf8")
    html_file.write(html)		
    html_file.close()
    
    try:
        file = 'Output.html'
        page = open(file)
        soup = BeautifulSoup(page, 'html.parser')
        table_div = soup.find_all('table')
        
        num = 0
        for table in table_div:
            num += 1
            table = table.prettify( formatter="html" ) 
            df = pd.read_html(table)
            main_df =pd.concat([main_df, df[0]])
    
            if(len(df[0])>0):
              xl_genetator(url,num)
          
    except: 
        pass
    
    
    driver.close()
    
def xl_genetator(url,num):
    global main_df
    if not os.path.exists('Govt-Xl-Sheets'):
        os.makedirs('Govt-Xl-Sheets')
    parsed = urlparse(url)
    base_name = parsed.netloc
    if not os.path.exists('Govt-Xl-Sheets/'+base_name):
        os.makedirs('Govt-Xl-Sheets/'+base_name)
    sheet_name = 'Govt-Xl-Sheets/' + base_name + '/'+ base_name + str(num) + '.xlsx'
    main_df.to_excel(sheet_name)
    main_df = pd.DataFrame()
  
    
for base_url in base_url_lis:
    try:
        simple(base_url)
    except:
        difficult(base_url)


print("Exception Url = ",len(exception_lis),"\n",exception_lis)
print("Exception Url = ",len(empty_df),"\n",empty_df)











