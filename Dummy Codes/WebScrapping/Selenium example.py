from selenium import webdriver
from selenium.webdriver.common.by import By
import getpass
import requests
from bs4 import BeautifulSoup

# url = "https://www.youtube.com/channel/UCHIoz16UQnp5Hcz7NjdGOog"
url = "https://www.youtube.com/shorts/4g-i4f7F4e0"

html = requests.get(url)

# soup = BeautifulSoup(html.content, 'html.parser')
# txt = html.text
# print(txt.endswith('/'))


driver = webdriver.Chrome()
driver.get(url)


