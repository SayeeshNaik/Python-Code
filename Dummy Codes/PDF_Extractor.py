from flask import Flask,request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/pdf_data',methods=['GET','POST'])
def pdf_data():
    MyPdf = request.files['MyPdf']
    MyPdf.save(MyPdf.filename)
    print(MyPdf.filename)
    
    
    return {"data":"dsf"}

app.run()