from flask import Flask,request
from flask_cors import CORS
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from googleapiclient.discovery import build
from google.oauth2 import service_account
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from gspread_dataframe import set_with_dataframe
from datetime import datetime
import gspread
import time


# Spreadsheet id
SPREADSHEET_ID = "1qHUWJr-aZmfuyixisQG6RwjR8Ln6mn0wPzwH7gaowxA"

SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_file(
    'C:/Users/User/Downloads/automated-style-322407-aac51e71fea7.json', scopes=SCOPES)

spreadsheet_service = build('sheets', 'v4', credentials=credentials)

drive_service = build('drive', 'v3', credentials=credentials)
gc = gspread.authorize(credentials)
gs = gc.open_by_key(SPREADSHEET_ID)


work_sheet_list=worksheet_list = gs.worksheets() 
df_list=[]

for sheet in work_sheet_list:
    df_list.append(pd.DataFrame(sheet.get_all_records()))
    
data=[]
glob_url = df_list[-2]['baseUrl'][0]
print(df_list[-2])

def scraper(df):
   global glob_url
   next_button=json.loads(df.loc[df['NextButtonStatus'] == 'TRUE'].to_json(orient='records'))[0]
   xpaths=json.loads(df.loc[df['NextButtonStatus'] != 'TRUE'].to_json(orient='records'))
   
   driver = webdriver.Chrome()
   for xp in xpaths:
       
       driver.get(glob_url)
       elem_lis=driver.find_elements(By.XPATH,xp['XPath'])
       for val in elem_lis:
           data.append(val.text)
   
   button_list=driver.find_elements(By.XPATH,next_button['XPath'])
   if(len(button_list)>1):
      driver.find_element(By.XPATH,next_button['XPath']+'[2]').click()
      scraper(df_list[-2])
   else:
      driver.find_element(By.XPATH,next_button['XPath']).click()
      scraper(df_list[-2])
     
   time.sleep(2)
   glob_url = driver.current_url
   driver.close()
      
scraper(df_list[-2])

print(data)
     
   

       
   
   
