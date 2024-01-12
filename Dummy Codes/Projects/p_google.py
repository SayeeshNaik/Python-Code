from flask import Flask,request
from flask_cors import CORS
from selenium import webdriver
import time

app=Flask(__name__)
CORS(app)
@app.route('/p_google',methods=['GET','POST'])
def google():
    text = request.args.get('text')
    print(text)
    driver = webdriver.Chrome()
    driver.get('https://www.google.com/search?q=' + text)
    time.sleep(10)
    return {'status':'success'},200
    
app.run()
