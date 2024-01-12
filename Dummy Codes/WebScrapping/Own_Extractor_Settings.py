from flask import Flask,request
from flask_cors import CORS
import json
import pandas as pd

app = Flask(__name__)
CORS(app)


tgstatus = False
next_button_status = False
next_button_xpath = "//div[next_button_Xpath]"

@app.route('/toggle',methods=["GET","POST"])
def toggle():
    global tgstatus
    status = request.args.get('toggle_status')
    if(status==True):
        status == True
    else:
        status == False
    tgstatus = status
    return {'toggle_status':status}

@app.route('/toggle_getting',methods=["GET","POST"])
def d():
    print('toggle_Status = ',tgstatus)
    return {'toggle_status':tgstatus}

@app.route('/clear_storage')
def clr():
    global clr_storage 
    print('storage ====== ',clr_storage)
    return {'status':clr_storage}


@app.route('/next_button_sending',methods=['GET','POST'])
def next_button_sending():
    global next_button_status, next_button_xpath
    if(next_button_status == False):
        next_button_status = True
    else:
        next_button_status = False
    print('next_button_status = ',next_button_status)
    return {'next_button_status': next_button_status,'next_button_xpath': next_button_xpath}

@app.route('/next_button_xpath')
def next_button_xpaht_func():
    global next_button_xpath
    return {'next_button_xpath': next_button_xpath}
    
@app.route('/test',methods=["GET","POST"])
def test():
    global next_button_enable
    res = json.loads(request.data)['data']
    
    try:
        next_button_input = request.args.get('next_button_input');
        print("hello button == ",next_button_input)
    except: pass

    if(next_button_enable):
        res['NextButtonStatus'] = True
    else:
        res['NextButtonStatus'] = False
          
    return {'data':next_button_enable}

@app.route('/next_button_input')
def next_button_xpath_func():
    next_button_getting = request.args.get('next_button_xpath')
    print("nxt xpath = ",next_button_xpath)
    return {'data':next_button_xpath}

app.run()
