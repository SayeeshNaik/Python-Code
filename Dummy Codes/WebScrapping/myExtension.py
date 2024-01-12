from flask import Flask,request
from flask_cors import CORS
import json
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from gspread_dataframe import set_with_dataframe
from datetime import datetime
import gspread

app = Flask(__name__)
CORS(app)

resData = []
clr_storage = False
next_button_enable = False

@app.route('/next_button',methods=["GET","POST"])
def next_button():
    global next_button_enable
    default_status = request.args.get('default')
    if(next_button_enable==False):
        next_button_enable = True
    else:
        next_button_enable = False
    if(default_status=='false'):
        next_button_enable = False
    print('next_button = ',next_button_enable)
    return {'next_button_status': next_button_enable}

@app.route('/xpath_data',methods=["GET","POST"])
def test():
    global next_button_enable,resData
    
    res = json.loads(request.data)['data']
    
    if(next_button_enable):
        try:
            resData=[ item for item in resData if item['NextButtonStatus']!=True ]
        except: pass
        res['NextButtonStatus'] = True
        
    else:
        res['NextButtonStatus'] = False
        
    if (res["className"] != "btnId txt"): 
        resData.append(res) 
    
    print(resData)
    
    return {'status':'success'}

@app.route('/sheet_data',methods=['GET','POST'])
def getxpath():
    final_data = pd.DataFrame(resData)
    print("fffffffffffffffffffffffffffffffffffffffffff")
    print(final_data)
    return {"final_data": final_data[0]}

# Spreadsheet id
# SPREADSHEET_ID = "1qHUWJr-aZmfuyixisQG6RwjR8Ln6mn0wPzwH7gaowxA"

# # Sheet Name and Range to Read
# READ_RANGE = "A1:B11"
# WRITE_RANGE = "A1:B11"

# # The boundary of script
# SCOPES = [
#     'https://www.googleapis.com/auth/spreadsheets',
#     'https://www.googleapis.com/auth/drive'
# ]
# credentials = service_account.Credentials.from_service_account_file(
#     'C:/Users/User/Downloads/automated-style-322407-aac51e71fea7.json', scopes=SCOPES)
# spreadsheet_service = build('sheets', 'v4', credentials=credentials)
# drive_service = build('drive', 'v3', credentials=credentials)
# gc = gspread.authorize(credentials)
# gauth = GoogleAuth()
# drive = GoogleDrive(gauth)
# gs = gc.open_by_key(SPREADSHEET_ID)

# @app.route('/google_sheet',methods=['GET','POST'])
# def google_sheet():
#     global resData,clr_storage,next_button_enable
#     df1=pd.DataFrame(resData)
#     worksheet = gs.add_worksheet(title="A worksheet"+datetime.now().strftime("%d-%h-%y-%H-%M-%S"), rows=100, cols=20)
    
#     header_length=len(df1.columns)
#     worksheet.format("1".format(header_length), {
#         "horizontalAlignment": "CENTER",
#         "textFormat": {
#           "fontSize": 12,
#           "bold": True
#         }
#     })
    
#     worksheet.update([df1.columns.values.tolist()] + df1.values.tolist())
#     local_df = pd.DataFrame(resData)
#     local_df.to_excel('AutomationData.xlsx')

#     resData = []
#     clr_storage = True
#     next_button_enable = False
#     print('Stored Google Sheet')
#     return {'sheet_url':'https://docs.google.com/spreadsheets/d/1qHUWJr-aZmfuyixisQG6RwjR8Ln6mn0wPzwH7gaowxA/edit#gid='+str(worksheet.id)}

tgstatus = False
@app.route('/toggle',methods=["GET","POST"])
def toggle():
    global tgstatus
    status = request.args.get('toggle_status')
    if(status==True):
        status == True
    else:
        status == False
    tgstatus = status
    return {'toggle_status':status}

@app.route('/toggle_getting',methods=["GET","POST"])
def d():
    print('togle_status = ',tgstatus)
    return {'toggle_status':tgstatus}

@app.route('/clear_storage')
def clr():
    global clr_storage 
    print('storage ====== ',clr_storage)
    return {'status':clr_storage}

app.run()





