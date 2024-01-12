from flask import Flask,request
from flask_cors import CORS
import json

app=Flask(__name__)
CORS(app)

@app.route('/post_data',methods=['GET','POST'])
def postdata():
    datas = json.loads(request.data)
    y = json.dumps(datas)
    
    username = datas['name']
    password = datas['password']
    
    user_auth = 'sayeesh'
    pass_auth = 'naik'
    
    if(username == user_auth and password == pass_auth):
        status = 'Success'
    else:
        status = 'Try Again'
    
    print(datas['name'])
    print(datas['password'])
    
    return status

app.run()
