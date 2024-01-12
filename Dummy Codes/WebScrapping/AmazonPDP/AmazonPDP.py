from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
import requests

options = ChromeOptions()
options.headless = True

driver = Chrome(options=options)
urls = ["464852642_cream","460453610_white"]
for i in urls:
    driver.get('https://www.ajio.com/p/'+i)
    name = driver.find_element(By.XPATH,'//*[@id="appContainer"]/div[2]/div/div/div[2]/div/div[3]/div/h2')
    print(name.text)