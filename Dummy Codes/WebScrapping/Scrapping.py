from flask import Flask,request
from flask_cors import CORS
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

app=Flask(__name__)
CORS(app)

@app.route('/webscrapping',methods=['GET','POST'])
def automation():
    xpath_lis = request.args.get('xpaths')
    xpath_lis = xpath_lis.split(',')
    with open('Scrapping.txt','w') as file :
        file.write(str(xpath_lis))
    if(len(xpath_lis)==4):
        url = "file:///D:/FlaskProject-1/WebScrapping/Scrapping.html"
        # all_xpaths = ['//*[@id="btn-login"]','//*[@id="btn-cart"]','//*[@id="btn-order"]','//*[@id="btn-receive"]']
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(2)
        for xpath in xpath_lis:
            driver.find_element(By.XPATH, xpath).click()
            time.sleep(2)
        driver.close()
    return {'data':'success'}

app.run()






