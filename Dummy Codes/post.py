from flask import Flask,request
from flask_cors import CORS
import json

app=Flask(__name__)
CORS(app)

@app.route('/post',methods=['GET','POST'])
def post():
    datas = json.loads(request.data)
    js = json.dumps(datas)
    print((datas['name']))
    
    return datas['name']


app.run()