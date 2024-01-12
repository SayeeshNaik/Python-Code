from flask import Flask,request
from flask_cors import CORS
import json
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from gspread_dataframe import set_with_dataframe
import gspread

app = Flask(__name__)
CORS(app)

resData = []
clr_storage = False

@app.route('/test',methods=["GET","POST"])
def test():
    res = json.loads(request.data)
    resData.append(res['data'])
    # print(res)
    # print('\n')
    
    return {'status':'success'}

# Spreadsheet id
SPREADSHEET_ID = "1qHUWJr-aZmfuyixisQG6RwjR8Ln6mn0wPzwH7gaowxA"

# Sheet Name and Range to Read
READ_RANGE = "A1:B11"
WRITE_RANGE = "A1:B11"

# The boundary of script
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
credentials = service_account.Credentials.from_service_account_file(
    'C:/Users/User/Downloads/automated-style-322407-aac51e71fea7.json', scopes=SCOPES)
spreadsheet_service = build('sheets', 'v4', credentials=credentials)
drive_service = build('drive', 'v3', credentials=credentials)
gc = gspread.authorize(credentials)
gauth = GoogleAuth()
drive = GoogleDrive(gauth)
gs = gc.open_by_key(SPREADSHEET_ID)

@app.route('/google_sheet',methods=['GET','POST'])
def google_sheet():
    global resData
    df1=pd.DataFrame(resData)
    worksheet = gs.get_worksheet(0)
    df2 = pd.DataFrame(worksheet.get_all_records())
    worksheet.clear()
    final_df= pd.concat([df1,df2],    # Combine vertically
                              ignore_index = True,
                              sort = False)
    header_length=len(final_df.columns)
    worksheet.format("1".format(header_length), {
       
        "horizontalAlignment": "CENTER",
        "textFormat": {
         
          "fontSize": 12,
          "bold": True
        }
    })
    
    worksheet.update([final_df.columns.values.tolist()] + final_df.values.tolist())
    resData = []
    clr_storage = True
    print('success')
    return {'sheet_url':'https://docs.google.com/spreadsheets/d/1qHUWJr-aZmfuyixisQG6RwjR8Ln6mn0wPzwH7gaowxA/edit?usp=sharing'}

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
    print('fdfdf = ',tgstatus)
    return {'toggle_status':tgstatus}

@app.route('/clear_storage')
def clr():
    global clr_storage 
    print('storage ====== ',clr_storage)
    return {'status':clr_storage}

app.run()



df = pd.DataFrame(resData)
df.to_excel('AutomationData.xlsx')

extension_xl_path = "D:/FlaskProject-1/WebScrapping/OwnChromeExtension/MyExcel.xlsx"
df.to_excel(extension_xl_path)
