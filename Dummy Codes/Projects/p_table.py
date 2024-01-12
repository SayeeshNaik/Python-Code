from flask import Flask,request
from flask_cors import CORS

app=Flask(__name__)
CORS(app)

@app.route('/p_table')
def a():
    data = {"data":[{"Amount":"20","BusinessCode":"2","Currency":"EUR","Document Item Currency":"*","Market - Country":"FR","Product Division":"01","Product Level 02":"2","Username":"JRathore",
                     "changed":["Product Level 02","Currency","Market - Country"],
                     "flag":"update","id":"1","sequence_id":"1","status":"pending","table_name":"SMB - Base Price - Category Addition","tableid":"911","updated_on":"2022-04-22 13:10:20"},
                    {"Amount":"30","BusinessCode":"5","Currency":"PVR","Document Item Currency":"*","Market - Country":"TT","Product Division":"09","Product Level 02":"2","Username":"JRathore",
                     "changed":["Amount","Product Division"],
                     "flag":"update","id":"1","sequence_id":"1","status":"pending","table_name":"SMB - Base Price - Category Addition","tableid":"911","updated_on":"2022-04-22 13:10:20"}],
            "lis":["BusinessCode","Market - Country","Product Division","Product Level 02","Document Item Currency","Amount","Currency"],
            }

        
    return data

app.run()