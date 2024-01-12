from flask import Flask,request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/lgn',methods=['GET','POST'])
def login():
    query_parameters=json.loads(request.data)
    
    username_auth = query_parameters['username']
    password_auth = query_parameters['password']
    
    username="sayeesh"
    password='naik'
    
    if (username==username_auth and password==password_auth):
        status="Success"
    else:
        status="Failure"
        
    return {"status":status}
        
        
if __name__=='__main__':
    app.run()