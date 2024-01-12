from selenium import webdriver
from selenium.webdriver.common.by import By
import getpass
import requests
from bs4 import BeautifulSoup
import time
import html
import pandas as pd

# link = "https://www.amazon.in/"
# product_name = input('Enter Product Name : ')
# link = "https://www.amazon.in/s?k="+product_name
link = "https://www.amazon.in/s?k=realme 6 pro"
driver = webdriver.Chrome()
driver.get(link)
html = requests.get(link)
soup = BeautifulSoup(driver.page_source,'html.parser')
all_div = soup.find_all('div',{'data-component-type':"s-search-result"})

product_names = []
ratings = []
prices = []
def data_func(div):
    try:
        name = div.h2.a.text
        product_names.append(name)
        rating = div.i.find('span').text
        ratings.append(rating)
        price = div.find('span',{'class':'a-price-whole'}).text
        prices.append(price)
    except:
        try:
            del product_names[product_names.index(name)]
            del ratings[ratings.index(rating)]
            del prices[prices.index(price)]
        except:pass
    
for j in all_div:
    data_func(j)


data = {'Product Name':product_names,'Rating':ratings,'Price':prices}
df = pd.DataFrame(data)
df.to_excel('AmazonData.xlsx')
print(len(product_names),len(ratings),len(prices))
    
    
# driver.find_element(By.ID,"twotabsearchtextbox").send_keys('i phone')
# driver.find_element(By.ID,"nav-search-submit-button").click()
# driver.find_element(By.CLASS_NAME,'s-image').click()