from selenium import webdriver
from selenium.webdriver.common.by import By
import getpass
import requests
from bs4 import BeautifulSoup
import time

url = "https://mail.google.com/mail/u/0/#inbox"
email    = "saish.naik@dhiomics.com"
password = "9845283954"
driver = webdriver.Chrome()
driver.get(url)

driver.find_element(By.ID,'identifierId').send_keys(email)
driver.find_element(By.XPATH,'//*[@id="identifierNext"]/div/button').click() 
time.sleep(5)
driver.find_element(By.XPATH,'//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
driver.find_element(By.XPATH,'//*[@id="passwordNext"]/div/button').click()
time.sleep(5)
driver.find_element(By.XPATH,'/html/body/div[7]/div[3]/div/div[2]/div[2]/div[1]/div[1]/div/div').click()
time.sleep(10)
driver.find_element(By.CLASS_NAME,'agP aFw').send_keys('yathish.s@dhiomics.com')
time.sleep(10)
# driver.find_element(By.CLASS_NAME,'aoT').send_keys('Selenium Testing')
# driver.find_element(By.CLASS_NAME,'//*[@id=":161"]').send_keys('Henge Naavu')
# time.sleep(5)
# driver.find_element(By.XPATH,'//*[@id=":14m"]').click()
# driver.find_element(By.XPATH,'/html/body/div[7]/div[3]/div/div[2]/div[1]/div[2]').click()
# time.sleep(3)
# driver.find_element(By.CLASS_NAME,'bA4').click()

