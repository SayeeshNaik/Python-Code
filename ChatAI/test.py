import requests
from bs4 import BeautifulSoup
import difflib
from flask import Flask
from flask import request
from flask_cors import CORS
  
app = Flask(__name__)
CORS(app)
    

main_className = ["FCUp0c rQMQod","BNeawe iBp4i AP7Wnd","BNeawe s3v9rd AP7Wnd"]
except_textlist = ["People also ask",None,"/"]

@app.route('/chatAi',methods=['GET','POST'])
def searchEngine():
    global main_className,except_textlist
    question = request.args.get('question')
    URL = "https://www.google.com/search?q={}"
    URL = URL.format(question)
    page = requests.get(URL).text
    soup = BeautifulSoup(page,  "html.parser")
    
    answer = ""
    for classname in main_className:
       try:
           ans = soup.find(class_=classname).text
           answer += ans
       except: pass
   
    answer = answer.replace("People also ask","")
    answer = answer.replace("/","")
       
    return {"answer":answer}

app.run()
    
