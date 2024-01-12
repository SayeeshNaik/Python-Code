
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime

def MyXML(filePath):
    lst_tag = []
    lst_text = []
    dup_lst = []
    dup_lst_val = []
    xl_val = []
    
    file=open(filePath,"r")
    mytree = ET.parse(file)
    myroot = mytree.getroot()
    element = myroot[0]
    ln = len(element)
    for i in range(ln):
     # print("\n") 
      for j in range(len(element[i])):
          #print(element[i][j].tag,"  ",element[i][j].text)
          if(element[i][j] != "None"):
             # print("modified : ",element[i][j].tag,"    ",element[i][j].text)
              dup_lst.append(element[i][j].tag)
              dup_lst_val.append(element[i][j].text)
              if(element[i][j]=="ZA"):
                  print("Text is Available")
                  
    #print(dup_lst)
    #print(dup_lst_val)
    path = "D:/FlaskProject-1/XML_XL_File.xlsx" 
    df = pd.read_excel(path)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df[df['Name'].notna()]
    js = df.to_dict(orient='records')
    
    #print(df)
    #print(js)
    
    for xl in range(len(df)):
        if(js[xl]['Mandatory'] == 1):
           # print(js[xl]['Name'])
            xl_val.append(js[xl]['Value'])
    
    print("\n")
    for b in range(len(dup_lst)):
        for c in range(len(xl_val)):
          if(dup_lst_val[b]==xl_val[c]):
              print(dup_lst[b],"  ",dup_lst_val[b],"    text exist")
              
    

path = "C:/Users/User/Downloads/111060_Lammering Meppen_EDI.xml"
MyXML(path)