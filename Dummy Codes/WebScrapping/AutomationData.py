import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import requests
from flask import Flask,request
from flask_cors import CORS

url = "file:///D:/FlaskProject-1/WebScrapping/Scrapping.html"
driver = webdriver.Chrome()
driver.get(url)
soup = BeautifulSoup(driver.page_source, 'html.parser')

app=Flask(__name__)
CORS(app)

df = []
@app.route('/test',methods=['GET','POST'])
def automation():
    className = request.args.get('className')
    idName = request.args.get('idName')
    ans = soup.find(class_= className)
    element = ans
    try:idName = ans.attrs['id']
    except:idName = 'None'
    try:tagName = ans.name
    except:tagName = 'None'
    try:btnName = ans.text
    except:btnName = 'None'
    try:link = ans.find('a')
    except:link = 'None'
    try:
        if(link!=None):link = link.get('href')
        else: link = 'None'
    except:link = 'None'
    
    df.append({'TagName':tagName,'ButtonName':btnName,'IdName':idName,'ClassName':className,'Link':link,'Element':str(element)})
    print(df)
    return {'data':'success'}

app.run()

# Updating XL-Sheet
df = pd.DataFrame(df)
df.to_excel('AutomationData.xlsx')


