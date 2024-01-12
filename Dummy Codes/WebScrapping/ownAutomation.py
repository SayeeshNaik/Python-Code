import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pyperclip
from selenium.webdriver import ActionChains
import pyautogui
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert

df = pd.read_excel('AutomationData.xlsx')
workFlow = df['XPath']

baseUrl = df['baseUrl'][0]
driver = webdriver.Chrome()
driver.get(baseUrl)

def automation(id,className,title,text,xpath):
    try: driver.find_element(By.ID, id).click()
    except:
        try: driver.find_element(By.PARTIAL_LINK_TEXT, text).click()
        except:
            try: driver.find_element(By.CLASS_NAME, className).click()
            except:
                try: driver.find_element(By.LINK_TEXT, title).click()
                except: 
                    try: driver.find_element(By.XPATH, xpath).click()
                    except: pass
   
           
        

for i in range(len(df)):
    time.sleep(1)
    automation(df['id'][i],df['className'][i],df['title'][i],df['textContent'][i],df['XPath'][i],)
# driver.quit()