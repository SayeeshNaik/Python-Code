import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pyperclip
from selenium.webdriver import ActionChains
import pyautogui
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert

baseUrl = "https://www.amazon.in/s?k=laptop"
driver = webdriver.Chrome()
driver.get(baseUrl)

def automation(xpath):
    try:driver.find_element(By.XPATH,xpath).click()
    except:pass

df = pd.read_excel('AutomationData.xlsx')
workFlow = df['XPath']

for xpath in workFlow:
    time.sleep(1)
    automation(xpath)
driver.close()