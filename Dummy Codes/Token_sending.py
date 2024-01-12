from flask import Flask,request
from flask_cors import CORS
import json
import secrets

app=Flask(__name__)
CORS(app)

@app.route('/tok',methods=['GET','POST'])
def test() :
    
    user_id = 56
    token = secrets.token_hex(32)
    print(token)
    return {'user_id':user_id,'token':token}

@app.route('/pm',methods=['GET','POST'])
def pm() :
    header_value = request.headers.get('AAA_Token')
    datas = json.loads(request.data)
    user_id = datas['user_id']
    print('User_Id = ',user_id)
    print('Token = ',header_value)
    return {'Token ':header_value,'Use_Id ':user_id}

app.run()