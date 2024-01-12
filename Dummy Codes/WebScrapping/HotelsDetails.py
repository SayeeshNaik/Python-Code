import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import selenium


url = "https://portfolio-sayeesh-naik.web.app"
html = requests.get(url)
driver = webdriver.Chrome()
driver.get(url)

soup = BeautifulSoup(html.content, 'html.parser')
print(html.status_code)