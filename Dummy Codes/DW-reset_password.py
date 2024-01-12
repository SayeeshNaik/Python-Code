from flask import Flask,request
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/forgot_password',methods=['GET','POST'])
def send_email() :
    url = 'http://127.0.0.1:5000/'
    params = {'user_id' : '333sayeesh1234'}
    requests.post(url,params)
    email = request.args.get('email')
    print(email)
    return {'stasu':'good'}
@app.route('/reset_password',methods=['GET','POST'])
def reset_password() :
    new_pass = request.args.get('new_password')
    print('new_pass',new_pass)
    return {'status':'Password set Successfully'},200
app.run()