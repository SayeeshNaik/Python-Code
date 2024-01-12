from flask import Flask,request
import json
from flask_cors import CORS

app=Flask(__name__)
CORS(app)

@app.route('/forgot_password')
def forgot_password():
    datas = request.args.get('email')
    print(datas)
    return {"status":"success"}

app.run()