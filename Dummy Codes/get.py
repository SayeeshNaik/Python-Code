from flask import Flask,request
from flask_cors import CORS 
import json

app = Flask(__name__)
CORS(app)

@app.route('/get')
def get():
    return {'name':'Sayeesh'}

app.run()