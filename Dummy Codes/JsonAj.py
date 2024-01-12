
from flask import  Flask
from flask_cors import CORS
import json

app=Flask(__name__)
CORS(app)



@app.route('/data',methods=['GET','POST'])
def hello():
    x = [{
      "name": "John",
      "age": 30,
      "city": "New York"
    },
    {
      "name": "Subbu",
      "age": 20,
      "city": "Kumta"
    },
    {
      "name": "Yathish",
      "age": 26,
      "city": "Shivmogga"
    }]
    
    y = json.dumps(x)
    
    return y
app.run()
# the result is a JSON string:
