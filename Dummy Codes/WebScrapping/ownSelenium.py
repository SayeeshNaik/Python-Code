import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# baseUrl = "https://en.wikipedia.org/wiki/Samantha_Ruth_Prabhu"
baseUrl = "https://www.amazon.in/Mobile-Phone-Lightweight-Camera-Type-C/dp/B0BM93NHD2/ref=sr_1_omk_4?keywords=mobile&qid=1669009451&qu=eyJxc2MiOiI4LjMyIiwicXNhIjoiNy45NCIsInFzcCI6IjYuOTIifQ%3D%3D&sr=8-4&th=1"
driver = webdriver.Chrome()
driver.get(baseUrl)

try:driver.find_element(By.PARTIAL_LINK_TEXT,'SUPCASE Unicorn Beetle Pro Series Rugged Protective Case with Strap Bands for Galax...').click()
except:pass