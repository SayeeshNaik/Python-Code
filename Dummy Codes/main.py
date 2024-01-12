from flask import Flask,request,jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Get api
@app.route('/get_api',methods=['GET','POST'])
def ex():
    path = 'C:/Users/User/OneDrive/Documents/' ;
    file = pd.read_excel(path+'MyExcell.xlsx') ;
    
    # To convert DataFrame to Object
    DJ = file.to_json(orient = 'records')

    return DJ

