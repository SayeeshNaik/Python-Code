from flask import Flask,request
from flask_cors import CORS
import json
import pandas as pd
import os

app=Flask(__name__)
CORS(app)

@app.route('/all_files',methods=['GET','POST'])
def all_files():
    # Read All xl files
    all_files = []
    for x in os.listdir("C:/Users/User/Myexcel"):
        if x.endswith(".xlsx"):
            all_files.append(x)
    
    all_filename = []
    for y in range(len(all_files)):        
        dic = {'all_files' : all_files[y]};
        all_filename.append(dic)
    
    fl = json.dumps(all_filename)
    js = fl.replace(".xlsx","")
    print(js)
    
    return js   

@app.route('/selected_files',methods=['GET','POST'])
def selected_files():
    datas = json.loads(request.data)
    file_name = datas['file_name']
    
    path = "C:/Users/User/Myexcel/" + file_name + ".xlsx" 
    df = pd.read_excel(path)
    obj = df.to_json(orient='records')
    
    return  obj

app.run()
