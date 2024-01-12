import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import io

main_df = pd.DataFrame()

def simple(url):
    global main_df
    link = url
    html = requests.get(link)
    soup = BeautifulSoup(html.content, 'html.parser')
    table_div = soup.find_all('table')
    
    
    
    # num = 0
    # for table in table_div:
    #     num += 1
    #     table = table.prettify( formatter="html" ) 
    #     df = pd.read_html(table)
    #     main_df =pd.concat([main_df, df[0]])
   
url = "https://www.ajio.com/hardsoda-checked-shirt-with-patch-pocket/p/469100769_white"       
simple(url)