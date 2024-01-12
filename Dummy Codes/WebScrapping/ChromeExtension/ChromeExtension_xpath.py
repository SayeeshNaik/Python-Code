from flask import Flask,request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

Event_Details = []
@app.route('/test',methods=["GET","POST"])
def test():
    global Event_Details
    res = json.loads(request.data)['data']
    Event_Details.append(res)
    print(Event_Details)
    return {'Status':'Success', "StatusCode": 200}

app.run()