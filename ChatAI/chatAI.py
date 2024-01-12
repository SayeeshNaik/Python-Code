import requests
from bs4 import BeautifulSoup
import difflib
from flask import Flask
from flask import request
from flask_cors import CORS
import random
  
app = Flask(__name__)
CORS(app)
    

main_className = ["FCUp0c rQMQod","BNeawe iBp4i AP7Wnd","BNeawe s3v9rd AP7Wnd"]
except_textlist = ["People also ask",None,"/"]

common_question = [
     ["Hii","hi","hlo","hiii","Hello","Hl","Hlw","hay","hey"],
     ["What is your name","Your name","Ur name","your nice name","can i get your name","ur nice name","ur nyc name"], 
     ["How are you","Hw r u","Hw are you","Hw r you"],  
     ["who developed you","your developer name","chatai developer name","who is your father"],  
     ["fine","Im fine","I'm fine","good","I'm good"],  
     ["not good","not fine","i'm not good","i'm not fine"],  
     ["I love you","I lv u","ilu","I lv you","I lv you","143"],  
     ["Do you have boyfriend","do you have girl friend","Do you have bf","Do you have gf","your boyfriend name","ur bf name","your bf name","your girlfriend name","ur gf name","your gf name"],
     ["when you born","your birthday","when were you born","when u born"],
     ["who is sayeesh","sayeesh"]
     ]
common_answer = [
    ["Hey !!, Nice to meet you...","Hello !!,I'm Very Glad to see you...","Hey whatsUp dude ?","Hey Meri Jaan...","Hay My Sweet Heart"],
    ["I'm a ChatAI, developed by Sayeesh Naik...","Here ChatAI..Thank's for asking dude...","I'm a ChatAI... Nice to meet you dude"],
    ["I'm fine...What about you ?...","Hey, I'm good !!... Thaks for asking, What about you ?"],
    ["I've developed by - Sayeesh Manjunath Naik  at 2023"],
    ["Wow!!.. Nice to hear this...","I'm very glad to hear this..."],
    ["Ohh dude why?.. What happened?..","Ohh!!!.. I'm very sad to heard this one","Oh!! dear...What happened?..."],
    ["I love you too my Sweet Heart", "Hay dear, I love You Too","Ohh my babe, I Love You Too...","Ayyy..I Love You Too Darling"],
    ["Yess dear... I'm engaged with Sayeesh Naik","Hann babe, My boy is Sayeesh Naik","My heart already sold out to Sayeesh Naik"],
    ["I was born in 2023...Haha.. Thank's for asking..."],
    ["Sayeesh is a great person for me...I can't survive without he...","He is my Sweet Heart...","He is a good and king hearted person...","Hay... He is my Life..."]
    ]

def searchEngine(question):
    global main_className,except_textlist
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
    return answer

def flirtingChat(question):
    question = question
    question = question.replace("?","").replace(".","")
    ans_ind = 0
    for question_lis in common_question:
        question_lis_lower = list(map(lambda x: x.lower(),question_lis))
        if question.lower() in question_lis_lower:
            ans_ind = common_question.index(question_lis)
            break
        else: ans_ind = None
    answer = random.choice(common_answer[ans_ind]) if ans_ind!=None else None
    return answer

def mathAnswer(question):
    try:
      answer = eval(question) if str(question) !="143" else None
      answer = "Your Answer is : " + str(answer)
    except: answer = None
    return answer
    
@app.route('/chatAi',methods=['GET','POST'])
def answerGenarator():
    global main_className,except_textlist
    question = request.args.get('question')
    
    if(flirtingChat(question)):
        answer = flirtingChat(question)
    elif(mathAnswer(question)):
        answer = mathAnswer(question)
    else:
        answer = searchEngine(question)
        
    print(answer)
    return {"answer": answer}


app.run()
    
