from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import requests
import pandas as pd

# driver = webdriver.Chrome()
 
url = "https://odisha.gov.in/about-us/whos-who/department?title=&field_domain_access_target_id=All&page=65"
glob_url = ''
main_df = pd.DataFrame()

def table_with_next_button():  
    global driver,url,glob_url
    
    xpath = "(//DIV[(@class='container')]//A[(@title='Go to next page')])"

    try:
        # print(url)
        driver.get(url)
        driver.implicitly_wait(2)
        len_xpath = len(driver.find_elements(By.XPATH,xpath))

        if(len_xpath>1):
            xpath = xpath+'[{}]'.format(len_xpath)
        
        next_button = driver.find_element(By.XPATH,xpath)
        
        if(glob_url!=url):
            simple(url)
            glob_url = url
        
        driver.implicitly_wait(3)
        next_button.click()
        url = driver.current_url
        
        table_with_next_button()
            
    except NoSuchElementException:
        simple(url)
        main_df.to_excel('NewOne.xlsx')
        print("Data Stored Successfully !!")
        driver.close()
        pass
    
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
        
    # print(main_df)

xl_num = 0

table_with_next_button()






