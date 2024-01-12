from flask import Flask,request
from flask_cors import CORS
import json
import pandas as pd

app=Flask(__name__)
CORS(app)

@app.route('/user_management',methods=['GET','POST'])
def user_management():
    data = json.loads(request.data)
    j = json.dump(data)
    
    ans = j['username']
    print(ans)
    return ans
    
app.run()
