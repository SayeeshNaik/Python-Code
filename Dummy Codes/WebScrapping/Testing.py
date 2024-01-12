import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pyperclip
from selenium.webdriver import ActionChains
import pyautogui
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert

op = Options()

op.add_extension('D:\FlaskProject-1\WebScrapping\extension_1_2_0_0.crx')

url = "https://www.amazon.in/s?k=laptop"
driver = webdriver.Chrome(options=op)
driver.get(url)
action = ActionChains(driver)

url_lis,tag_lis,xpath_lis,id_lis,class_lis,text_lis   = [],[],[],[],[],[]
  
def extracted(xpath):
    try:
        myElement=driver.find_element(By.XPATH,xpath)
        try: tagName= myElement.tag_name
        except: tagName = '--'
        tag_lis.append(tagName)
        try: className = str(myElement.get_attribute('class').split())
        except: className = '--'
        class_lis.append(className)
        try: 
            idName = str(myElement.get_attribute('id'))
            if(idName==''):idName = '--'
        except: idName = '--'
        id_lis.append(idName)
        try: text = myElement.text
        except: text = '--'
        text_lis.append(text)
    except: pass

def func():
    try:
        time.sleep(5)
        driver.find_element(By.XPATH,'//*[@id="selectorgadget_main"]/input[4]').click()
        pyautogui.hotkey("ctrl", "c")
        Alert(driver).accept()
        try: copied_path = pyperclip.paste()
        except: copied_path = 'None'
        xpath_lis.append(copied_path)
        try: currentUrl = driver.current_url
        except: currentUrl = 'None'
        url_lis.append(currentUrl)
        extracted(copied_path)
        driver.find_element(By.XPATH,'//*[@id="selectorgadget_main"]/input[6]').click()
        driver.find_element(By.XPATH,copied_path).click()
        time.sleep(2)
        func()
    except:
        print('URL\n',url_lis)
        print('Tags\n',tag_lis)
        print('X-Paths\n',xpath_lis)
        print('ClassName\n',class_lis)
        print('IdName\n',id_lis)

func()

data = {'UrlName':url_lis,'TagName':tag_lis,'XPath':xpath_lis,'ClassName':class_lis,'IdName':id_lis,'Text':text_lis}
df = pd.DataFrame(data)
df.to_excel('AutomationData.xlsx')




# [xpath_lis.append('//' + i)  for i in lis if(i!='')]
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

# for j in xpath_lis:
#     try:
#         time.sleep(2)
#         print((driver.find_element(By.XPATH,j)).get_attribute('class'))
#     except:print('Noooo : ',j)

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



