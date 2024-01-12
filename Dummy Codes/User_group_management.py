from flask import Flask,request
from flask_cors import CORS
import json
import pandas as pd

app=Flask(__name__)
CORS(app)

@app.route('/management',methods=['GET','POST'])
def mm() :
   datas=json.loads(request.data)
   js = json.dumps(datas)
   
   return js


app.run()