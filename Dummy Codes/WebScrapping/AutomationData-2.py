import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.keys import Keys
import pyperclip
from selenium.webdriver import ActionChains
import pyautogui
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert

op = Options()

op.add_extension('D:\FlaskProject-1\WebScrapping\extension_1_2_0_0.crx')

url = "https://www.amazon.in/s?k=laptop"
driver = webdriver.Chrome(options=op)
driver.get(url)
# action = ActionChains(driver)
# soup = BeautifulSoup(driver.page_source, 'html.parser')

xpath_lis = []
class_lis = []

time.sleep(5)
x_path = driver.find_element(By.XPATH,'//*[@id="selectorgadget_main"]/input[4]').click()
time.sleep(1)
pyautogui.hotkey("ctrl", "c")
time.sleep(2)
Alert(driver).accept()
copied_path = pyperclip.paste()
lis = copied_path.split('//')
time.sleep(2)
[xpath_lis.append('//' + i)  for i in lis if(i!='')]
# print(xpath_lis)
# for j in list(xpath_lis):
#     time.sleep(3)
#     print('x : ',j)
#     myElement=driver.find_element(By.XPATH,j)
#     time.sleep(3)
#     tagName= myElement.tag_name
#     time.sleep(3)
#     className = str(myElement.get_attribute('class').split())
#     time.sleep(3)
#     idName = str(myElement.get_attribute('id').split())
#     print(tagName)
#     print(className)
#     print(idName)

for j in xpath_lis:
    try:
        time.sleep(2)
        print((driver.find_element(By.XPATH,j)).get_attribute('class'))
    except:print('Noooo : ',j)

# time.sleep(2)
# Alert(driver).accept()
# time.sleep(2)
# driver.find_element(By.XPATH,'//*[@id="selectorgadget_main"]/input[6]').click()
# time.sleep(5)
# print(copied_path)
# driver.find_element(By.XPATH,copied_path).click()
# func()



# df = pd.DataFrame({'X-Paths':xpath_lis})
# df.to_excel('AutomationData.xlsx')



